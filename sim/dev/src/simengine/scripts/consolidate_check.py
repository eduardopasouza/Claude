"""Verifica se o event_log atingiu o threshold de consolidação.

Compara o número de eventos em event_log.jsonl posteriores ao último
ConsolidatedSummary (consolidated_summaries.json) com o threshold
configurado em config.yaml (chave consolidator.threshold).

Imprime em stdout um JSON:
    {
      "events_since_last_summary": int,
      "threshold": int,
      "should_consolidate": bool,
      "last_summary_period_end": str | null
    }

Exit 0 se a leitura foi bem-sucedida (independente do veredito).
Exit 1 em erro de I/O ou config.

Uso:
    python -m simengine.scripts.consolidate_check \\
        <event_log.jsonl> <consolidated_summaries.json> <config.yaml>
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import yaml
from pydantic import ValidationError

from simengine.schemas import ConsolidatedSummary, Event


def _last_summary_period_end(summaries_path: Path) -> date | None:
    if not summaries_path.exists():
        return None
    raw = summaries_path.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    data = json.loads(raw)
    if not data:
        return None
    summaries = [ConsolidatedSummary.model_validate(item) for item in data]
    return max(s.period_end for s in summaries)


def _count_events_after(event_log_path: Path, cutoff: date | None) -> int:
    if not event_log_path.exists():
        return 0
    count = 0
    with event_log_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            event = Event.model_validate_json(line)
            if cutoff is None or event.date > cutoff:
                count += 1
    return count


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "uso: python -m simengine.scripts.consolidate_check "
            "<event_log.jsonl> <consolidated_summaries.json> <config.yaml>",
            file=sys.stderr,
        )
        return 1

    event_log_path = Path(argv[0])
    summaries_path = Path(argv[1])
    config_path = Path(argv[2])

    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        print(f"config não encontrado: {config_path}", file=sys.stderr)
        return 1

    threshold = config.get("consolidator", {}).get("threshold")
    if not isinstance(threshold, int) or threshold <= 0:
        print(
            f"config.yaml: consolidator.threshold ausente ou inválido "
            f"(recebido: {threshold!r})",
            file=sys.stderr,
        )
        return 1

    try:
        cutoff = _last_summary_period_end(summaries_path)
        events_after = _count_events_after(event_log_path, cutoff)
    except (json.JSONDecodeError, ValidationError) as exc:
        print(f"falha lendo histórico: {exc}", file=sys.stderr)
        return 1

    payload = {
        "events_since_last_summary": events_after,
        "threshold": threshold,
        "should_consolidate": events_after >= threshold,
        "last_summary_period_end": cutoff.isoformat() if cutoff else None,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
