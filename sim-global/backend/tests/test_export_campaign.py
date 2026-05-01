"""Cobertura do script export_campaign."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from simengine.schemas import (
    ConsolidatedSummary,
    Event,
)
from simengine.scripts import export_campaign


def _setup_save(tmp_path: Path, base_state) -> Path:
    save = tmp_path / "vargas-tenentista"
    save.mkdir()
    (save / "current_state.json").write_text(
        base_state.model_dump_json(), encoding="utf-8"
    )
    (save / "pending_actions.json").write_text("[]", encoding="utf-8")
    return save


def test_export_writes_default_output(tmp_path, base_state):
    save = _setup_save(tmp_path, base_state)
    code = export_campaign.main([str(save)])
    assert code == 0
    out = (save / "CAMPAIGN.md").read_text(encoding="utf-8")
    assert "Campanha `vargas-tenentista`" in out
    assert state_marker(base_state) in out


def state_marker(state) -> str:
    return f"**Polity do jogador:** {state.player_polity}"


def test_export_includes_summaries_and_events(tmp_path, base_state):
    save = _setup_save(tmp_path, base_state)
    summary = ConsolidatedSummary(
        period_start=date(1930, 11, 3),
        period_end=date(1932, 6, 30),
        key_events=["Posse de Vargas"],
        state_changes_summary="Centralização administrativa avança.",
        emerging_tensions=["Oposição paulista"],
        generated_at=date(1932, 7, 1),
    )
    (save / "consolidated_summaries.json").write_text(
        json.dumps([summary.model_dump(mode="json")]), encoding="utf-8"
    )
    raw_event = Event(
        date=date(1932, 7, 9),
        category="military",
        description="Eclode revolução em SP",
        affected_polities=["Brasil"],
        affected_regions=["São Paulo cafeeiro"],
        caused_by="scheduled",
    )
    (save / "event_log.jsonl").write_text(
        raw_event.model_dump_json() + "\n", encoding="utf-8"
    )

    export_campaign.main([str(save)])
    out = (save / "CAMPAIGN.md").read_text(encoding="utf-8")
    assert "Centralização administrativa" in out
    assert "Eclode revolução em SP" in out
    assert "Eventos recentes" in out


def test_export_filters_events_before_last_summary(tmp_path, base_state):
    save = _setup_save(tmp_path, base_state)
    summary = ConsolidatedSummary(
        period_start=date(1930, 11, 3),
        period_end=date(1932, 6, 30),
        key_events=[],
        state_changes_summary="x",
        emerging_tensions=[],
        generated_at=date(1932, 7, 1),
    )
    (save / "consolidated_summaries.json").write_text(
        json.dumps([summary.model_dump(mode="json")]), encoding="utf-8"
    )
    older = Event(
        date=date(1931, 1, 1), category="internal",
        description="velho", caused_by="emergent",
    )
    newer = Event(
        date=date(1933, 1, 1), category="internal",
        description="novo", caused_by="emergent",
    )
    (save / "event_log.jsonl").write_text(
        older.model_dump_json() + "\n" + newer.model_dump_json() + "\n",
        encoding="utf-8",
    )

    export_campaign.main([str(save)])
    out = (save / "CAMPAIGN.md").read_text(encoding="utf-8")
    assert "novo" in out
    assert "velho" not in out


def test_export_includes_diplomatic_log(tmp_path, base_state):
    save = _setup_save(tmp_path, base_state)
    log_dir = save / "diplomatic_log"
    log_dir.mkdir()
    (log_dir / "Argentina.json").write_text(
        json.dumps([
            {
                "date": "1933-04-15",
                "from": "Brasil",
                "to": "Argentina",
                "message_in": "Mensagem do Brasil",
                "message_out": "Resposta da Argentina",
            }
        ]),
        encoding="utf-8",
    )

    export_campaign.main([str(save)])
    out = (save / "CAMPAIGN.md").read_text(encoding="utf-8")
    assert "Apêndice: histórico diplomático" in out
    assert "Argentina" in out
    assert "Mensagem do Brasil" in out
    assert "Resposta da Argentina" in out


def test_export_custom_output_path(tmp_path, base_state):
    save = _setup_save(tmp_path, base_state)
    output = tmp_path / "custom.md"
    code = export_campaign.main([str(save), str(output)])
    assert code == 0
    assert output.exists()
    assert not (save / "CAMPAIGN.md").exists()


def test_export_invalid_save_dir(tmp_path, capsys):
    code = export_campaign.main([str(tmp_path / "missing")])
    assert code == 1
    assert "save-dir" in capsys.readouterr().err
