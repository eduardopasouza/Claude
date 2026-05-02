"""Wrapper do Claude Agent SDK autenticado via OAuth.

Este módulo encapsula a chamada aos cinco subagentes do `sim-global`
(advisor, game_master, diplomat, consolidator, scenario_builder).

Princípios:

- Cada chamada é one-shot e isolada. Usamos `query()` do SDK passando
  um `system_prompt` carregado de arquivo `.md` em
  `simglobal/prompts/`. O SDK abre uma conversa nova por chamada, o
  que dá efeito equivalente ao `context: fork` do design original.
- Saída JSON estrita é reforçada por contrato no prompt (cada arquivo
  define seu schema). O wrapper valida com `json.loads` e refaz a
  chamada com erro injetado, no máximo `max_retries` vezes. A
  validação Pydantic do schema final é responsabilidade do chamador
  (BRIEFING §9: Pydantic é o último guardião).
- Autenticação por OAuth via env var `CLAUDE_CODE_OAUTH_TOKEN`,
  herdada pelo subprocesso do CLI Claude Code. Nunca logada.
- Se `claude_agent_sdk` não estiver instalado, `AgentRunner` levanta
  `ImportError` no `__init__` com instrução para instalar via
  `pip install -e .[agent]`.
"""
from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Import opcional do SDK. Mantemos uma flag para os testes determinísticos
# (que rodam sem o SDK instalado) detectarem ausência sem importar nada.
try:  # pragma: no cover - cobertura depende do ambiente de instalação
    from claude_agent_sdk import (  # type: ignore[import-not-found]
        AssistantMessage,
        ClaudeAgentOptions,
        TextBlock,
        query,
    )

    _SDK_AVAILABLE = True
    _SDK_IMPORT_ERROR: ModuleNotFoundError | None = None
except ModuleNotFoundError as exc:  # pragma: no cover
    _SDK_AVAILABLE = False
    _SDK_IMPORT_ERROR = exc
    AssistantMessage = None  # type: ignore[assignment,misc]
    ClaudeAgentOptions = None  # type: ignore[assignment,misc]
    TextBlock = None  # type: ignore[assignment,misc]
    query = None  # type: ignore[assignment]


_INSTALL_HINT = (
    "claude_agent_sdk não está instalado. Instale o extra opcional com "
    "`pip install -e .[agent]` (a partir de backend/) ou diretamente "
    "`pip install claude-agent-sdk>=0.1`."
)


class AgentRunnerError(RuntimeError):
    """Falha de configuração ou de invocação do AgentRunner."""


class AgentRunner:
    """Wrapper estável sobre o Claude Agent SDK para os subagentes do sim-global.

    Uso típico::

        runner = AgentRunner()
        text = await runner.run_subagent(
            prompt_path=Path("prompts/advisor.md"),
            payload={"state": ..., "question": "..."},
        )
        buffer = await runner.run_subagent(
            prompt_path=Path("prompts/game_master.md"),
            payload={...},
            json_output=True,
        )
    """

    def __init__(
        self,
        model: str = "claude-opus-4-7",
        token_env: str = "CLAUDE_CODE_OAUTH_TOKEN",
        *,
        max_turns: int = 1,
    ) -> None:
        if not _SDK_AVAILABLE:
            raise ImportError(_INSTALL_HINT) from _SDK_IMPORT_ERROR
        self.model = model
        self.token_env = token_env
        self.max_turns = max_turns
        self._assert_token()

    # ------------------------------------------------------------------ #
    # Configuração / pré-condições
    # ------------------------------------------------------------------ #

    def _assert_token(self) -> None:
        """Garante que a env var do OAuth está presente. Não loga o valor."""
        token = os.environ.get(self.token_env)
        if not token:
            raise AgentRunnerError(
                f"Variável de ambiente {self.token_env} ausente. "
                "Gere o token uma vez com `claude setup-token` e exporte-o "
                "antes de subir o backend. Sem token, o Agent SDK não "
                "autentica via OAuth Pro/Max."
            )

    @staticmethod
    def _read_prompt(prompt_path: Path) -> str:
        if not prompt_path.exists():
            raise AgentRunnerError(f"Prompt de subagente não encontrado: {prompt_path}")
        text = prompt_path.read_text(encoding="utf-8")
        if not text.strip():
            raise AgentRunnerError(f"Prompt de subagente vazio: {prompt_path}")
        return text

    @staticmethod
    def _format_user_message(payload: dict[str, Any], *, json_output: bool) -> str:
        """Serializa o payload e amarra contrato de saída.

        O prompt do subagente já descreve o schema esperado. Aqui só
        repetimos a regra de JSON estrito quando aplicável, e
        encapsulamos o payload em uma seção delimitada para reduzir
        confusão de parsing.
        """
        # default=str cobre date/datetime sem perder fidelidade.
        payload_json = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
        contract = (
            "Responda EXCLUSIVAMENTE com um objeto JSON válido. "
            "Sem markdown, sem cercas de código, sem comentários, sem "
            "texto antes ou depois do JSON."
            if json_output
            else "Responda em prosa direta, sem cercas de código."
        )
        return (
            f"<contrato_de_saida>\n{contract}\n</contrato_de_saida>\n\n"
            f"<payload>\n{payload_json}\n</payload>"
        )

    # ------------------------------------------------------------------ #
    # Invocação
    # ------------------------------------------------------------------ #

    async def run_subagent(
        self,
        prompt_path: Path,
        payload: dict[str, Any],
        *,
        json_output: bool = False,
        max_retries: int = 3,
    ) -> str | dict[str, Any]:
        """Executa um subagente one-shot e devolve a resposta.

        Se `json_output=True`, valida que a saída é JSON parseável. Em
        caso de falha, refaz a chamada com a mensagem de erro injetada
        no payload (chave especial `__previous_attempt_error`), até
        `max_retries` tentativas. Retorna `dict` (parseado). Validação
        de schema Pydantic é responsabilidade do chamador.
        """
        system_prompt = self._read_prompt(prompt_path)
        attempt_payload: dict[str, Any] = dict(payload)
        last_error: str | None = None

        for attempt in range(1, max_retries + 1):
            user_message = self._format_user_message(
                attempt_payload, json_output=json_output
            )
            t0 = time.monotonic()
            text, usage = await self._invoke_once(system_prompt, user_message)
            dt_ms = int((time.monotonic() - t0) * 1000)
            logger.info(
                "agent.call prompt=%s model=%s attempt=%d duration_ms=%d "
                "tokens_in=%s tokens_out=%s",
                prompt_path.name,
                self.model,
                attempt,
                dt_ms,
                usage.get("input_tokens"),
                usage.get("output_tokens"),
            )

            if not json_output:
                return text

            try:
                parsed = json.loads(text)
            except json.JSONDecodeError as exc:
                last_error = (
                    f"Tentativa {attempt}/{max_retries}: saída não é JSON "
                    f"válido ({exc}). Refazendo. Trecho recebido: "
                    f"{text[:200]!r}"
                )
                logger.warning("agent.json_parse_failed %s", last_error)
                attempt_payload = dict(payload)
                attempt_payload["__previous_attempt_error"] = last_error
                continue

            if not isinstance(parsed, dict):
                last_error = (
                    f"Tentativa {attempt}/{max_retries}: saída JSON não é "
                    f"objeto (got {type(parsed).__name__}). Refazendo."
                )
                logger.warning("agent.json_shape_failed %s", last_error)
                attempt_payload = dict(payload)
                attempt_payload["__previous_attempt_error"] = last_error
                continue

            return parsed

        raise AgentRunnerError(
            f"Subagente {prompt_path.name} falhou em devolver JSON válido "
            f"após {max_retries} tentativas. Último erro: {last_error}"
        )

    async def stream_subagent(
        self,
        prompt_path: Path,
        payload: dict[str, Any],
    ) -> AsyncIterator[str]:
        """Streaming token-a-token (na granularidade que o SDK entrega).

        Útil para o painel do advisor renderizar incrementalmente.
        Não suporta `json_output` — streaming de JSON estrito requer
        validação ao final, que é o caso de `run_subagent`.
        """
        system_prompt = self._read_prompt(prompt_path)
        user_message = self._format_user_message(payload, json_output=False)
        options = self._build_options(system_prompt)
        async for message in query(prompt=user_message, options=options):  # type: ignore[misc]
            if isinstance(message, AssistantMessage):  # type: ignore[arg-type]
                for block in message.content:
                    if isinstance(block, TextBlock):  # type: ignore[arg-type]
                        yield block.text

    # ------------------------------------------------------------------ #
    # Internos
    # ------------------------------------------------------------------ #

    def _build_options(self, system_prompt: str) -> Any:
        """Constrói o `ClaudeAgentOptions` para uma chamada one-shot.

        - `max_turns=1`: garante que o subagente responde direto, sem
          ciclos de tool use. Os subagentes do sim-global são puros
          processadores de texto/JSON; nenhum precisa de ferramentas
          locais (Read/Write/Bash) — a exceção é o `scenario_builder`,
          que pesquisa via WebFetch/WebSearch e por isso recebe esses
          tools no caller (ver `routes/campaigns.py`, fora deste PR).
        - `system_prompt`: prompt do subagente carregado do `.md`.
        - `model`: fixo no construtor.
        - Sem `agents=`: cada chamada já é um contexto isolado por ser
          uma `query()` independente. O recurso `agents=` do SDK é para
          delegação intra-conversa, que não usamos.
        """
        return ClaudeAgentOptions(  # type: ignore[misc]
            system_prompt=system_prompt,
            model=self.model,
            max_turns=self.max_turns,
        )

    async def _invoke_once(
        self, system_prompt: str, user_message: str
    ) -> tuple[str, dict[str, Any]]:
        """Roda `query()` uma vez e concatena os TextBlocks da resposta."""
        options = self._build_options(system_prompt)
        chunks: list[str] = []
        usage: dict[str, Any] = {}
        async for message in query(prompt=user_message, options=options):  # type: ignore[misc]
            if isinstance(message, AssistantMessage):  # type: ignore[arg-type]
                for block in message.content:
                    if isinstance(block, TextBlock):  # type: ignore[arg-type]
                        chunks.append(block.text)
                if getattr(message, "usage", None):
                    # SDK expõe usage como dict bruto da API.
                    usage = dict(message.usage)  # type: ignore[arg-type]
        return "".join(chunks).strip(), usage


__all__ = ["AgentRunner", "AgentRunnerError"]
