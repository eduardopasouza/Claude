"""Valida current_state.json: schema Pydantic + invariantes globais.

Uso:
    python -m simengine.scripts.validate_state <caminho/current_state.json>

Exit 0 se válido, 1 se inválido (schema ou invariante), 2 se uso incorreto.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

from simengine.engine import check_state_invariants
from simengine.schemas import GameState


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(
            "uso: python -m simengine.scripts.validate_state <caminho/current_state.json>",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[0])
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"arquivo não encontrado: {path}", file=sys.stderr)
        return 1

    try:
        state = GameState.model_validate_json(raw)
    except ValidationError as exc:
        print(f"schema inválido em {path}:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    violations = check_state_invariants(state)
    if violations:
        print(f"invariantes violados em {path}:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(
        f"OK: {path} válido "
        f"({len(state.polities)} polities, {len(state.regions)} regions, "
        f"{len(state.diplomatic_relations)} relações diplomáticas)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
