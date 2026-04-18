"""
ETL agendado de preços de commodities por UF (mercado físico).

Executa o coletor Agrolink para todas as 13 commodities cobertas,
persiste o histórico mensal em `market_prices_uf` (UPSERT), e
registra execução em `scraping_job_logs` para monitoramento.

Agendamento recomendado:
  - 2x/dia (08h + 18h BRT) via Windows Task Scheduler ou cron host
  - OU 1x/dia (06h BRT)
  - Dados Agrolink são mensais, não precisa mais frequente

Uso:
  docker compose exec backend python scripts/scrape_market_prices.py
  docker compose exec backend python scripts/scrape_market_prices.py --commodity soja

Ambientes:
  - Dev: rodar manualmente ou 1x/dia
  - Prod: cron diário + alerta Sentry se status != success

Persistência: ON CONFLICT DO UPDATE (idempotente — pode rodar 100x/dia).
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from datetime import datetime, timezone

from sqlalchemy import text

from app.collectors.agrolink import AgrolinkCollector, AGROLINK_PATHS
from app.models.database import get_engine, create_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("scrape_market_prices")


UPSERT_SQL = text("""
    INSERT INTO market_prices_uf
      (commodity, uf, mes_ano, preco_estadual, preco_nacional, unit, label, collected_at)
    VALUES
      (:commodity, :uf, :mes_ano, :preco_estadual, :preco_nacional, :unit, :label, :collected_at)
    ON CONFLICT (commodity, uf, mes_ano) DO UPDATE SET
      preco_estadual = EXCLUDED.preco_estadual,
      preco_nacional = EXCLUDED.preco_nacional,
      collected_at = EXCLUDED.collected_at
""")

LOG_INSERT_SQL = text("""
    INSERT INTO scraping_job_logs
      (job_name, started_at, finished_at, status, items_fetched, items_persisted, error)
    VALUES
      (:job_name, :started_at, :finished_at, :status, :items_fetched, :items_persisted, :error)
""")


async def scrape_one(commodity: str) -> tuple[int, int]:
    """Busca + persiste uma commodity. Retorna (fetched, persisted)."""
    collector = AgrolinkCollector()
    meta = AGROLINK_PATHS[commodity]
    label = meta["label"]
    unit = meta["unit"]

    logger.info("→ %s (%s)", commodity, label)
    data = await collector.fetch_commodity(commodity)
    if "error" in data:
        logger.warning("  skipped: %s", data.get("error"))
        return 0, 0

    ufs_data = data.get("ufs", [])
    total_fetched = 0
    total_persisted = 0

    engine = get_engine()
    with engine.begin() as conn:
        for uf_entry in ufs_data:
            uf = uf_entry["uf"]
            historico = uf_entry.get("historico", [])
            for h in historico:
                total_fetched += 1
                if h.get("estadual") is None and h.get("nacional") is None:
                    continue
                try:
                    conn.execute(
                        UPSERT_SQL,
                        {
                            "commodity": commodity,
                            "uf": uf,
                            "mes_ano": h["mes"],
                            "preco_estadual": h.get("estadual"),
                            "preco_nacional": h.get("nacional"),
                            "unit": unit,
                            "label": label,
                            "collected_at": datetime.now(timezone.utc),
                        },
                    )
                    total_persisted += 1
                except Exception as e:
                    logger.warning(
                        "  upsert %s %s %s falhou: %s", commodity, uf, h["mes"], e
                    )

    logger.info(
        "  ✓ %d registros persistidos (de %d fetched) em %d UFs",
        total_persisted, total_fetched, len(ufs_data),
    )
    return total_fetched, total_persisted


async def main(commodities: list[str]):
    # Garante que tabelas existem (primeira execução)
    create_tables()

    started = datetime.now(timezone.utc)
    total_fetched = 0
    total_persisted = 0
    failures: list[str] = []

    for commodity in commodities:
        if commodity not in AGROLINK_PATHS:
            logger.warning("skip desconhecida: %s", commodity)
            continue
        try:
            f, p = await scrape_one(commodity)
            total_fetched += f
            total_persisted += p
        except Exception as e:
            logger.exception("erro em %s: %s", commodity, e)
            failures.append(f"{commodity}: {e}")

    finished = datetime.now(timezone.utc)
    status = "success" if not failures else ("partial" if total_persisted > 0 else "failed")

    # Log da execução
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            LOG_INSERT_SQL,
            {
                "job_name": "agrolink_prices",
                "started_at": started,
                "finished_at": finished,
                "status": status,
                "items_fetched": total_fetched,
                "items_persisted": total_persisted,
                "error": "\n".join(failures) if failures else None,
            },
        )

    logger.info(
        "=" * 60 +
        f"\n📊 Job 'agrolink_prices' [{status}]\n"
        f"   Duração: {(finished - started).total_seconds():.1f}s\n"
        f"   Fetched: {total_fetched} registros\n"
        f"   Persistidos: {total_persisted}\n"
        f"   Falhas: {len(failures)}\n" +
        "=" * 60
    )

    return 0 if status != "failed" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--commodity",
        action="append",
        help="Executar só uma (repetível). Default: todas.",
    )
    args = parser.parse_args()

    commodities = args.commodity or list(AGROLINK_PATHS.keys())
    exit_code = asyncio.run(main(commodities))
    sys.exit(exit_code)
