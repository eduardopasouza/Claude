"""Testes do wrapper do Claude Agent SDK e dos prompts dos subagentes."""
from __future__ import annotations

import asyncio
import importlib
import json
import os
from pathlib import Path
from unittest import mock

import pytest

PROMPTS_DIR = (
    Path(__file__).resolve().parent.parent / "src" / "simglobal" / "prompts"
)
EXPECTED_PROMPTS = [
    "advisor.md",
    "game_master.md",
    "diplomat.md",
    "consolidator.md",
    "scenario_builder.md",
]


# --------------------------------------------------------------------- #
# Prompts: existência e estrutura mínima
# --------------------------------------------------------------------- #


@pytest.mark.parametrize("name", EXPECTED_PROMPTS)
def test_prompt_file_exists_and_is_nonempty(name: str) -> None:
    path = PROMPTS_DIR / name
    assert path.exists(), f"Prompt ausente: {path}"
    text = path.read_text(encoding="utf-8")
    assert text.strip(), f"Prompt vazio: {path}"


@pytest.mark.parametrize("name", EXPECTED_PROMPTS)
def test_prompt_has_identity_and_input_sections(name: str) -> None:
    """Markdown bem-formado: cabeçalho de nível 1 + seções principais."""
    text = (PROMPTS_DIR / name).read_text(encoding="utf-8")
    # Cabeçalho top-level.
    assert text.lstrip().startswith("# "), (
        f"{name}: deve iniciar com cabeçalho de nível 1"
    )
    # Seções obrigatórias do contrato.
    assert "## Identidade" in text, f"{name}: falta seção '## Identidade'"
    assert "## Input" in text, f"{name}: falta seção '## Input'"
    assert "## Output" in text, f"{name}: falta seção '## Output'"
    assert "## Princípios não-negociáveis" in text, (
        f"{name}: falta seção '## Princípios não-negociáveis'"
    )


def test_game_master_prompt_lists_all_delta_types() -> None:
    """game_master precisa enumerar todos os tipos de delta válidos."""
    text = (PROMPTS_DIR / "game_master.md").read_text(encoding="utf-8")
    expected_types = [
        "region_owner_change",
        "diplomatic_status_change",
        "diplomatic_opinion_change",
        "polity_leader_change",
        "polity_doctrine_add",
        "polity_doctrine_remove",
        "polity_tension_add",
        "polity_tension_remove",
        "battalion_create",
        "battalion_destroy",
        "battalion_move",
    ]
    for t in expected_types:
        assert t in text, f"game_master.md deve mencionar delta '{t}'"


def test_diplomat_and_consolidator_specify_strict_json() -> None:
    diplomat = (PROMPTS_DIR / "diplomat.md").read_text(encoding="utf-8")
    consolidator = (PROMPTS_DIR / "consolidator.md").read_text(encoding="utf-8")
    assert "JSON estrito" in diplomat
    assert "JSON estrito" in consolidator


# --------------------------------------------------------------------- #
# AgentRunner: imports e configuração
# --------------------------------------------------------------------- #


def _sdk_available() -> bool:
    try:
        importlib.import_module("claude_agent_sdk")
        return True
    except ModuleNotFoundError:
        return False


def test_agent_runner_raises_useful_error_on_missing_token_or_sdk() -> None:
    """Sem SDK: ImportError com instrução clara.

    Com SDK mas sem token: AgentRunnerError mencionando a env var.
    Cobre os dois caminhos de falha do `__init__`.
    """
    from simglobal.agent.client import AgentRunner, AgentRunnerError

    if not _sdk_available():
        with pytest.raises(ImportError) as exc:
            AgentRunner()
        assert "claude_agent_sdk" in str(exc.value)
        assert "pip install" in str(exc.value)
        return

    # SDK disponível: força ausência da env var.
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
        with pytest.raises(AgentRunnerError) as exc:
            AgentRunner()
        assert "CLAUDE_CODE_OAUTH_TOKEN" in str(exc.value)


# --------------------------------------------------------------------- #
# AgentRunner.run_subagent: payload e prompt loading (mock test)
# --------------------------------------------------------------------- #


@pytest.mark.skipif(not _sdk_available(), reason="claude_agent_sdk não instalado")
def test_run_subagent_loads_prompt_and_formats_payload() -> None:
    """Verifica que o prompt é carregado do arquivo e o payload é
    serializado como JSON dentro de <payload> na mensagem de usuário.
    """
    from simglobal.agent import client as client_mod
    from simglobal.agent.client import AgentRunner

    # Cria um AssistantMessage fake com TextBlock contendo JSON válido.
    fake_text = '{"ok": true, "echo": "advisor"}'

    class _FakeBlock:
        def __init__(self, text: str) -> None:
            self.text = text

    class _FakeMsg:
        def __init__(self, blocks: list) -> None:
            self.content = blocks
            self.usage = {"input_tokens": 10, "output_tokens": 5}

    captured: dict = {}

    async def fake_query(prompt, options):  # noqa: ANN001
        captured["prompt"] = prompt
        captured["system_prompt"] = options.system_prompt
        captured["model"] = options.model
        # Garante que o tipo retornado é reconhecido como AssistantMessage
        # via isinstance: monkey-patch no módulo do client.
        yield _FakeMsg([_FakeBlock(fake_text)])

    with mock.patch.dict(
        os.environ, {"CLAUDE_CODE_OAUTH_TOKEN": "fake-token"}, clear=False
    ), mock.patch.object(client_mod, "query", fake_query), mock.patch.object(
        client_mod, "AssistantMessage", _FakeMsg
    ), mock.patch.object(client_mod, "TextBlock", _FakeBlock):
        runner = AgentRunner(model="claude-opus-4-7")
        result = asyncio.run(
            runner.run_subagent(
                prompt_path=PROMPTS_DIR / "advisor.md",
                payload={"question": "qual a opção mais segura?", "n": 3},
                json_output=True,
            )
        )

    assert result == {"ok": True, "echo": "advisor"}
    # System prompt = conteúdo do arquivo advisor.md.
    assert "Advisor" in captured["system_prompt"]
    assert "## Identidade" in captured["system_prompt"]
    # Prompt do usuário inclui contrato e payload serializado.
    assert "<payload>" in captured["prompt"]
    assert "<contrato_de_saida>" in captured["prompt"]
    assert "qual a opção mais segura" in captured["prompt"]
    # Modelo propagado.
    assert captured["model"] == "claude-opus-4-7"


@pytest.mark.skipif(not _sdk_available(), reason="claude_agent_sdk não instalado")
def test_run_subagent_retries_on_invalid_json_then_fails() -> None:
    """Saída não-JSON dispara retry; após max_retries levanta erro."""
    from simglobal.agent import client as client_mod
    from simglobal.agent.client import AgentRunner, AgentRunnerError

    class _FakeBlock:
        def __init__(self, text: str) -> None:
            self.text = text

    class _FakeMsg:
        def __init__(self, blocks: list) -> None:
            self.content = blocks
            self.usage = {}

    call_count = {"n": 0}

    async def fake_query(prompt, options):  # noqa: ANN001
        call_count["n"] += 1
        yield _FakeMsg([_FakeBlock("isto não é JSON")])

    with mock.patch.dict(
        os.environ, {"CLAUDE_CODE_OAUTH_TOKEN": "fake-token"}, clear=False
    ), mock.patch.object(client_mod, "query", fake_query), mock.patch.object(
        client_mod, "AssistantMessage", _FakeMsg
    ), mock.patch.object(client_mod, "TextBlock", _FakeBlock):
        runner = AgentRunner()
        with pytest.raises(AgentRunnerError) as exc:
            asyncio.run(
                runner.run_subagent(
                    prompt_path=PROMPTS_DIR / "game_master.md",
                    payload={"x": 1},
                    json_output=True,
                    max_retries=2,
                )
            )

    assert call_count["n"] == 2
    assert "JSON" in str(exc.value)


# --------------------------------------------------------------------- #
# Sanidade do JSON serializado (datas convertem)
# --------------------------------------------------------------------- #


def test_format_user_message_serializes_dates() -> None:
    """Garante que payload com `date` não quebra json.dumps."""
    from datetime import date

    if not _sdk_available():
        pytest.skip("AgentRunner exige SDK")

    from simglobal.agent.client import AgentRunner

    msg = AgentRunner._format_user_message(
        {"current_date": date(1930, 11, 3), "n": 1}, json_output=True
    )
    # Confirma que a data virou string ISO.
    assert "1930-11-03" in msg
    assert "<payload>" in msg
    assert "JSON" in msg
