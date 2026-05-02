"""Cobertura dos scripts CLI: validate_state, validate_turn, apply_delta, consolidate_check."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from simengine.schemas import (
    Event,
    GameState,
    PolityLeaderChange,
    TurnBuffer,
)
from simengine.scripts import (
    apply_delta as apply_delta_script,
    consolidate_check,
    validate_state,
    validate_turn,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------- validate_state ----------

def test_validate_state_ok(tmp_path, base_state, capsys):
    p = tmp_path / "state.json"
    _write(p, base_state.model_dump_json())
    code = validate_state.main([str(p)])
    assert code == 0
    assert "OK" in capsys.readouterr().out


def test_validate_state_schema_error(tmp_path, capsys):
    p = tmp_path / "state.json"
    _write(p, '{"current_date": "not-a-date"}')
    code = validate_state.main([str(p)])
    assert code == 1
    assert "schema inválido" in capsys.readouterr().err


def test_validate_state_invariant_violation(tmp_path, base_state, capsys):
    base_state.player_polity = "Inexistente"
    p = tmp_path / "state.json"
    _write(p, base_state.model_dump_json())
    code = validate_state.main([str(p)])
    assert code == 1
    assert "invariantes violados" in capsys.readouterr().err


def test_validate_state_wrong_argc(capsys):
    assert validate_state.main([]) == 2
    assert validate_state.main(["a", "b"]) == 2


# ---------- validate_turn ----------

def test_validate_turn_ok(tmp_path, base_state):
    state_path = tmp_path / "state.json"
    buffer_path = tmp_path / "turn_buffer.json"
    _write(state_path, base_state.model_dump_json())
    buf = TurnBuffer(
        turn_start_date=base_state.current_date,
        turn_end_date=date(1931, 5, 3),
        deltas=[PolityLeaderChange(polity="Brasil", new_leader="X")],
        narrative="...",
    )
    _write(buffer_path, buf.model_dump_json())
    assert validate_turn.main([str(state_path), str(buffer_path)]) == 0


def test_validate_turn_rejects_invalid_delta_target(tmp_path, base_state, capsys):
    state_path = tmp_path / "state.json"
    buffer_path = tmp_path / "turn_buffer.json"
    _write(state_path, base_state.model_dump_json())
    buf = TurnBuffer(
        turn_start_date=base_state.current_date,
        turn_end_date=date(1931, 5, 3),
        deltas=[PolityLeaderChange(polity="Atlântida", new_leader="X")],
        narrative="...",
    )
    _write(buffer_path, buf.model_dump_json())
    code = validate_turn.main([str(state_path), str(buffer_path)])
    assert code == 1
    assert "Atlântida" in capsys.readouterr().err


# ---------- apply_delta ----------

def test_apply_delta_writes_state_event_log_and_clears_pending(tmp_path, base_state):
    state_path = tmp_path / "state.json"
    buffer_path = tmp_path / "turn_buffer.json"
    log_path = tmp_path / "event_log.jsonl"
    pending_path = tmp_path / "pending_actions.json"

    _write(state_path, base_state.model_dump_json())
    _write(pending_path, "[{\"description\": \"x\", \"submitted_on\": \"1930-12-01\"}]")

    event = Event(
        date=date(1931, 1, 10),
        category="internal",
        description="Centralização administrativa avança",
        affected_polities=["Brasil"],
        affected_regions=[],
        caused_by="emergent",
    )
    buf = TurnBuffer(
        turn_start_date=base_state.current_date,
        turn_end_date=date(1931, 5, 3),
        deltas=[PolityLeaderChange(polity="Brasil", new_leader="Aranha")],
        events=[event],
        narrative="...",
    )
    _write(buffer_path, buf.model_dump_json())

    code = apply_delta_script.main(
        [str(state_path), str(buffer_path), str(log_path), str(pending_path)]
    )
    assert code == 0

    state_after = GameState.model_validate_json(state_path.read_text())
    assert state_after.current_date == date(1931, 5, 3)
    assert state_after.polities["Brasil"].leader == "Aranha"

    log_lines = log_path.read_text().strip().splitlines()
    assert len(log_lines) == 1
    assert "Centralização" in log_lines[0]

    assert json.loads(pending_path.read_text()) == []


def test_apply_delta_appends_to_existing_event_log(tmp_path, base_state):
    state_path = tmp_path / "state.json"
    buffer_path = tmp_path / "turn_buffer.json"
    log_path = tmp_path / "event_log.jsonl"
    pending_path = tmp_path / "pending_actions.json"

    _write(state_path, base_state.model_dump_json())
    _write(pending_path, "[]")
    _write(log_path, '{"date": "1929-01-01", "category": "internal", "description": "antigo", "affected_polities": [], "affected_regions": [], "caused_by": "emergent"}\n')

    event = Event(
        date=date(1931, 1, 10),
        category="internal",
        description="novo",
        affected_polities=[],
        affected_regions=[],
        caused_by="emergent",
    )
    buf = TurnBuffer(
        turn_start_date=base_state.current_date,
        turn_end_date=date(1931, 5, 3),
        events=[event],
        narrative="...",
    )
    _write(buffer_path, buf.model_dump_json())

    apply_delta_script.main(
        [str(state_path), str(buffer_path), str(log_path), str(pending_path)]
    )

    log_lines = log_path.read_text().strip().splitlines()
    assert len(log_lines) == 2
    assert "antigo" in log_lines[0]
    assert "novo" in log_lines[1]


def test_apply_delta_aborts_on_invalid_buffer(tmp_path, base_state):
    state_path = tmp_path / "state.json"
    buffer_path = tmp_path / "turn_buffer.json"
    log_path = tmp_path / "event_log.jsonl"
    pending_path = tmp_path / "pending_actions.json"

    original_state_text = base_state.model_dump_json()
    _write(state_path, original_state_text)
    _write(pending_path, "[]")

    buf = TurnBuffer(
        turn_start_date=base_state.current_date,
        turn_end_date=date(1931, 5, 3),
        deltas=[PolityLeaderChange(polity="Inexistente", new_leader="X")],
        narrative="...",
    )
    _write(buffer_path, buf.model_dump_json())

    code = apply_delta_script.main(
        [str(state_path), str(buffer_path), str(log_path), str(pending_path)]
    )
    assert code == 1
    assert state_path.read_text() == original_state_text
    assert not log_path.exists()


# ---------- consolidate_check ----------

def _write_config(path: Path, threshold: int) -> None:
    _write(path, f"consolidator:\n  threshold: {threshold}\n")


def test_consolidate_check_below_threshold(tmp_path, capsys):
    log = tmp_path / "event_log.jsonl"
    summaries = tmp_path / "consolidated_summaries.json"
    config = tmp_path / "config.yaml"
    _write_config(config, 20)
    _write(summaries, "[]")
    for d in [date(1931, 1, 1), date(1931, 2, 1), date(1931, 3, 1)]:
        with log.open("a") as f:
            f.write(
                Event(
                    date=d, category="internal", description="x",
                    caused_by="emergent",
                ).model_dump_json() + "\n"
            )

    code = consolidate_check.main([str(log), str(summaries), str(config)])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["events_since_last_summary"] == 3
    assert payload["threshold"] == 20
    assert payload["should_consolidate"] is False
    assert payload["last_summary_period_end"] is None


def test_consolidate_check_above_threshold(tmp_path, capsys):
    log = tmp_path / "event_log.jsonl"
    summaries = tmp_path / "consolidated_summaries.json"
    config = tmp_path / "config.yaml"
    _write_config(config, 2)
    _write(summaries, "[]")
    for i in range(5):
        with log.open("a") as f:
            f.write(
                Event(
                    date=date(1931, 1, 1 + i),
                    category="internal",
                    description=f"e{i}",
                    caused_by="emergent",
                ).model_dump_json() + "\n"
            )

    code = consolidate_check.main([str(log), str(summaries), str(config)])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["events_since_last_summary"] == 5
    assert payload["should_consolidate"] is True


def test_consolidate_check_uses_cutoff_from_last_summary(tmp_path, capsys):
    log = tmp_path / "event_log.jsonl"
    summaries = tmp_path / "consolidated_summaries.json"
    config = tmp_path / "config.yaml"
    _write_config(config, 10)

    summaries_data = [
        {
            "period_start": "1930-11-03",
            "period_end": "1932-06-30",
            "key_events": [],
            "state_changes_summary": "x",
            "emerging_tensions": [],
            "generated_at": "1932-07-01",
        }
    ]
    _write(summaries, json.dumps(summaries_data))

    for d in [date(1932, 1, 1), date(1932, 6, 30), date(1932, 7, 1), date(1933, 1, 1)]:
        with log.open("a") as f:
            f.write(
                Event(
                    date=d, category="internal", description=str(d),
                    caused_by="emergent",
                ).model_dump_json() + "\n"
            )

    code = consolidate_check.main([str(log), str(summaries), str(config)])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    # Apenas datas estritamente posteriores a 1932-06-30: 1932-07-01 e 1933-01-01.
    assert payload["events_since_last_summary"] == 2
    assert payload["last_summary_period_end"] == "1932-06-30"


def test_consolidate_check_invalid_threshold(tmp_path, capsys):
    log = tmp_path / "event_log.jsonl"
    summaries = tmp_path / "consolidated_summaries.json"
    config = tmp_path / "config.yaml"
    _write(config, "consolidator:\n  threshold: -1\n")
    _write(log, "")
    _write(summaries, "[]")
    code = consolidate_check.main([str(log), str(summaries), str(config)])
    assert code == 1
    assert "threshold" in capsys.readouterr().err
