"""
Endpoints para triagem e consulta das camadas do Sprint 4.

Rotas:
  GET  /api/v1/dados-gov/loaders          — lista loaders disponíveis
  GET  /api/v1/dados-gov/status            — últimas execuções (log)
  POST /api/v1/dados-gov/run?loader=X      — dispara loader síncrono (admin)
  GET  /api/v1/dados-gov/stats             — contagens por tabela

As consultas de geometria vão pelo router geo_layers existente; aqui ficam
apenas a administração do ETL e métricas.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import text

from app.collectors.dados_gov_loaders import LOADERS
from app.models.database import DadosGovIngestLog, get_engine, get_session

logger = logging.getLogger("agrojus.dados_gov_api")
router = APIRouter()


LAYER_TABLES = [
    ("sigmine_processos", "SIGMINE/ANM - processos minerários"),
    ("ana_outorgas_full", "ANA - outorgas de recursos hídricos"),
    ("ana_bho", "ANA - base hidrográfica ottocodificada"),
    ("incra_assentamentos", "INCRA - assentamentos"),
    ("incra_quilombolas", "INCRA/Palmares - áreas quilombolas"),
    ("aneel_usinas", "ANEEL - usinas de geração"),
    ("aneel_linhas_transmissao", "ANEEL - linhas de transmissão"),
    ("garantia_safra", "Garantia-Safra - beneficiários"),
    ("ceis_registros", "CGU - CEIS (inidôneos)"),
    ("cnep_registros", "CGU - CNEP (punidos)"),
    ("ibama_embargos", "IBAMA - termos de embargo"),
    ("ibama_autos_infracao", "IBAMA - autos de infração (SIFISC)"),
    ("ibama_ctf", "IBAMA - CTF (atividades poluidoras)"),
]


@router.get("/loaders")
def list_loaders():
    """Lista loaders disponíveis para acionamento."""
    return {"loaders": list(LOADERS.keys()), "total": len(LOADERS)}


@router.get("/status")
def get_status(limit: int = 30):
    """Últimas execuções dos loaders."""
    session = get_session()
    try:
        rows = (
            session.query(DadosGovIngestLog)
            .order_by(DadosGovIngestLog.started_at.desc())
            .limit(limit)
            .all()
        )
        return {
            "total": len(rows),
            "executions": [
                {
                    "id": r.id,
                    "loader": r.loader,
                    "dataset_id": r.dataset_id,
                    "status": r.status,
                    "started_at": r.started_at.isoformat() if r.started_at else None,
                    "finished_at": r.finished_at.isoformat() if r.finished_at else None,
                    "rows_fetched": r.rows_fetched,
                    "rows_persisted": r.rows_persisted,
                    "duration_sec": (
                        (r.finished_at - r.started_at).total_seconds()
                        if r.started_at and r.finished_at else None
                    ),
                    "error": (r.error or "")[:400] if r.error else None,
                }
                for r in rows
            ],
        }
    finally:
        session.close()


@router.post("/run")
async def run_loader(loader: str):
    """Dispara um loader específico (síncrono)."""
    if loader not in LOADERS:
        raise HTTPException(status_code=400, detail=f"Loader desconhecido. Disponíveis: {list(LOADERS.keys())}")

    # Roda em threadpool para não bloquear loop (é síncrono e potencialmente longo)
    result = await run_in_threadpool(LOADERS[loader])
    return result


@router.get("/stats")
def get_layer_stats():
    """Contagens por tabela — útil para frontend saber quais camadas têm dados."""
    engine = get_engine()
    stats = []
    with engine.connect() as conn:
        for table, label in LAYER_TABLES:
            try:
                n = int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0)
            except Exception:
                n = 0
            stats.append({"table": table, "label": label, "rows": n, "active": n > 0})
    return {
        "total_tables": len(stats),
        "active": sum(1 for s in stats if s["active"]),
        "stats": stats,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
