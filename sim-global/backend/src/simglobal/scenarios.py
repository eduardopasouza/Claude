"""Helpers para carregar e filtrar eventos pré-programados de cenários.

Cenários originam de YAML versionado em `examples/<name>/scheduled_events.yaml`
ou (no futuro) gerados pelo scenario_builder e persistidos junto com a
campanha. Este módulo concentra leitura + filtragem por janela
temporal.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml

from .config import project_root


def _scheduled_events_path(campaign_name: str) -> Path | None:
    candidate = (
        project_root() / "examples" / campaign_name / "scheduled_events.yaml"
    )
    return candidate if candidate.exists() else None


def load_scheduled_events_raw(campaign_name: str) -> list[dict[str, Any]]:
    """Carrega lista de eventos scriptados do YAML do cenário.

    Devolve lista vazia se não há YAML correspondente. Não valida
    schema — devolve dicts crus para o subagente interpretar.
    """
    path = _scheduled_events_path(campaign_name)
    if path is None:
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    events = raw.get("events", [])
    if not isinstance(events, list):
        return []
    return events


def filter_in_window(
    events: list[dict[str, Any]], start: date, end: date
) -> list[dict[str, Any]]:
    """Mantém apenas eventos cuja janela [date - window, date + window]
    cruza [start, end]. Útil para o game_master receber apenas o que
    pode disparar no turno.
    """
    out: list[dict[str, Any]] = []
    for ev in events:
        ev_date = ev.get("date")
        if isinstance(ev_date, str):
            try:
                ev_date = date.fromisoformat(ev_date)
            except ValueError:
                continue
        elif not isinstance(ev_date, date):
            continue
        window_days = int(ev.get("trigger_window_days", 30))
        ev_start = ev_date - timedelta(days=window_days)
        ev_end = ev_date + timedelta(days=window_days)
        if ev_end < start or ev_start > end:
            continue
        out.append(ev)
    return out
