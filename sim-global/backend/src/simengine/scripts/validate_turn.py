"""Valida turn_buffer.json contra current_state.json.

Uso:
    python -m simengine.scripts.validate_turn <state.json> <turn_buffer.json>

Exit 0 se válido, 1 se inválido (schema ou invariante de turno),
2 se uso incorreto.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

from simengine.engine import check_turn_invariants
from simengine.schemas import GameState, TurnBuffer


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "uso: python -m simengine.scripts.validate_turn "
            "<state.json> <turn_buffer.json>",
            file=sys.stderr,
        )
        return 2

    state_path = Path(argv[0])
    buffer_path = Path(argv[1])

    try:
        state = GameState.model_validate_json(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"arquivo de estado não encontrado: {state_path}", file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(f"schema de estado inválido em {state_path}:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    try:
        buffer = TurnBuffer.model_validate_json(
            buffer_path.read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        print(f"turn_buffer não encontrado: {buffer_path}", file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(f"schema de turn_buffer inválido em {buffer_path}:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    violations = check_turn_invariants(state, buffer)
    if violations:
        print(f"invariantes de turno violados em {buffer_path}:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(
        f"OK: turno válido — {len(buffer.events)} eventos, "
        f"{len(buffer.deltas)} deltas, "
        f"{buffer.turn_start_date} → {buffer.turn_end_date}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
