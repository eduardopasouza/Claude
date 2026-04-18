"""
Script master do Sprint 4 — orquestra os 10 loaders do dados.gov.br.

Uso:
    python -m scripts.run_dados_gov_etl --only sigmine ceis cnep
    python -m scripts.run_dados_gov_etl --all
    python -m scripts.run_dados_gov_etl --status   # lê dados_gov_ingest_log

Em produção, agendar via cron (ex: diário às 03:00):
    docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --all
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from app.collectors.dados_gov_loaders import LOADERS, run_all
from app.logging_config import setup_logging
from app.models.database import DadosGovIngestLog, get_session


def cmd_status() -> None:
    session = get_session()
    try:
        rows = (
            session.query(DadosGovIngestLog)
            .order_by(DadosGovIngestLog.started_at.desc())
            .limit(30)
            .all()
        )
        for r in rows:
            dur = ""
            if r.started_at and r.finished_at:
                dur = f" ({(r.finished_at - r.started_at).total_seconds():.0f}s)"
            print(
                f"[{r.started_at:%Y-%m-%d %H:%M}] {r.loader:20s} "
                f"{r.status:8s} fetched={r.rows_fetched or 0} persisted={r.rows_persisted or 0}{dur}"
            )
            if r.error:
                print(f"    ERRO: {r.error[:200]}")
    finally:
        session.close()


def cmd_run(selected: list[str] | None) -> None:
    results: list[dict] = []
    if selected:
        for name in selected:
            if name not in LOADERS:
                print(f"loader desconhecido: {name}")
                continue
            print(f"=== {name} ===")
            res = LOADERS[name]()
            results.append(res)
            print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        results = run_all()
        for r in results:
            print(json.dumps(r, indent=2, ensure_ascii=False))

    success = sum(1 for r in results if r["status"] == "success")
    print(f"\nConcluído: {success}/{len(results)} loaders com sucesso")


def main() -> None:
    setup_logging("INFO")
    logging.getLogger("httpx").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Roda todos os 10 loaders")
    parser.add_argument("--only", nargs="+", help="Roda loaders específicos")
    parser.add_argument("--status", action="store_true", help="Mostra últimas execuções")
    parser.add_argument("--list", action="store_true", help="Lista loaders disponíveis")
    args = parser.parse_args()

    if args.list:
        for name in LOADERS:
            print(f"  {name}")
        return

    if args.status:
        cmd_status()
        return

    if args.only:
        cmd_run(args.only)
        return

    if args.all:
        cmd_run(None)
        return

    parser.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
