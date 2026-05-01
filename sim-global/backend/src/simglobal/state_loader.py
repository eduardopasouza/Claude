"""Carrega estados de jogo de fixtures (cenário-piloto Brasil/1930)."""
from __future__ import annotations

from pathlib import Path

from simengine.schemas import GameState

from .config import project_root


def load_example(name: str = "brasil-vargas-1930") -> GameState:
    """Carrega um GameState de examples/<name>/initial_state.json."""
    path = project_root() / "examples" / name / "initial_state.json"
    return GameState.model_validate_json(path.read_text(encoding="utf-8"))


def list_examples() -> list[str]:
    base = project_root() / "examples"
    if not base.exists():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())
