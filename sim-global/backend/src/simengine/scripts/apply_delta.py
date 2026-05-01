"""Aplica turn_buffer.json ao current_state.json.

Re-valida ambos antes de aplicar; se algo falhar, NADA é escrito em
disco. Em caso de sucesso:

- current_state.json é sobrescrito com o estado pós-turno.
- event_log.jsonl recebe append-only com cada Event do buffer (uma
  linha JSON por evento).
- pending_actions.json é zerado para [].
- turn_buffer.json NÃO é alterado nem removido aqui (deixe a remoção
  para o auto-commit do mestre, ou inclua no .gitignore).

Uso:
    python -m simengine.scripts.apply_delta \\
        <state.json> <turn_buffer.json> <event_log.jsonl> <pending_actions.json>

Exit 0 se aplicado, 1 se rejeitado, 2 se uso incorreto.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

from simengine.engine import apply_turn_buffer, check_turn_invariants
from simengine.schemas import GameState, TurnBuffer


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "uso: python -m simengine.scripts.apply_delta "
            "<state.json> <turn_buffer.json> <event_log.jsonl> "
            "<pending_actions.json>",
            file=sys.stderr,
        )
        return 2

    state_path = Path(argv[0])
    buffer_path = Path(argv[1])
    event_log_path = Path(argv[2])
    pending_path = Path(argv[3])

    try:
        state = GameState.model_validate_json(
            state_path.read_text(encoding="utf-8")
        )
        buffer = TurnBuffer.model_validate_json(
            buffer_path.read_text(encoding="utf-8")
        )
    except FileNotFoundError as exc:
        print(f"arquivo não encontrado: {exc.filename}", file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(f"schema inválido: {exc}", file=sys.stderr)
        return 1

    violations = check_turn_invariants(state, buffer)
    if violations:
        print("invariantes de turno violados, nada aplicado:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    apply_turn_buffer(state, buffer)

    state_path.write_text(
        state.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )

    event_log_path.parent.mkdir(parents=True, exist_ok=True)
    with event_log_path.open("a", encoding="utf-8") as f:
        for event in buffer.events:
            f.write(event.model_dump_json() + "\n")

    pending_path.write_text("[]\n", encoding="utf-8")

    print(
        f"OK: aplicados {len(buffer.deltas)} deltas e "
        f"{len(buffer.events)} eventos. "
        f"current_date agora é {state.current_date}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
