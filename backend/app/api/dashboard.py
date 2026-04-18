"""
dashboard.py — Endpoint de metricas agregadas do AgroJus Dashboard.
GET /api/v1/dashboard/metrics retorna KPIs via materialized view (~5ms).
POST /api/v1/dashboard/refresh para atualizar a MV.
"""
import time
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    KPIs reais do banco via materialized view (instantaneo).
    Se a MV nao existir, faz fallback para queries diretas.
    """
    t0 = time.perf_counter()

    try:
        row = db.execute(text("SELECT * FROM mv_dashboard_kpis LIMIT 1")).mappings().first()
        if row:
            t1 = time.perf_counter()
            return _build_response_from_mv(dict(row), round((t1 - t0) * 1000, 1))
    except Exception:
        logger.info("MV nao disponivel, usando queries diretas")

    # Fallback: queries diretas
    return _build_response_direct(db, t0)


@router.post("/refresh")
def refresh_dashboard(db: Session = Depends(get_db)):
    """Atualiza materialized view do dashboard."""
    try:
        db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_dashboard_kpis"))
        db.commit()
        return {"status": "ok", "refreshed_at": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _build_response_from_mv(r: dict, latency_ms: float) -> dict:
    """Monta resposta a partir da materialized view."""
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_refreshed_at": r["refreshed_at"].isoformat() if r.get("refreshed_at") else None,
        "db_latency_ms": latency_ms,
        "kpis": {
            "cars_imoveis": {"total": r["cars_total"], "ufs": r["cars_ufs"], "label": "Imoveis Rurais (CAR)"},
            "desmatamento": {
                "deter_amazonia": r["deter_amazonia"],
                "deter_cerrado": r["deter_cerrado"],
                "prodes": r["prodes_total"],
                "mapbiomas_alertas": r["mapbiomas_alertas"],
                "total": r["deter_amazonia"] + r["deter_cerrado"] + r["prodes_total"] + r["mapbiomas_alertas"],
                "label": "Alertas de Desmatamento",
            },
            "areas_protegidas": {
                "terras_indigenas": r["terras_indigenas"],
                "unidades_conservacao": r["ucs_total"],
                "total": r["terras_indigenas"] + r["ucs_total"],
                "label": "Areas Protegidas",
            },
            "icmbio": {
                "embargos": r["embargos_icmbio"],
                "autos": r["autos_icmbio"],
                "total": r["embargos_icmbio"] + r["autos_icmbio"],
                "label": "Fiscalizacao ICMBio",
            },
            "ibama_embargos": {"total": r["ibama_total"], "label": "Embargos IBAMA"},
            "mte_lista_suja": {"total": r["mte_total"], "label": "Lista Suja MTE"},
            "credito_rural": {"total": r["credito_rural"], "label": "Parcelas Credito Rural"},
            "infraestrutura": {
                "armazens": r["armazens"],
                "frigorificos": r["frigorificos"],
                "rodovias": r["rodovias"],
                "portos": r["portos"],
                "label": "Infraestrutura Logistica",
            },
            "market_quotes": {
                "total": r["market_total"],
                "products": r["market_products"],
                "last_date": str(r["market_last_date"]) if r.get("market_last_date") else None,
                "label": "Cotacoes de Mercado",
            },
            "users": {"total": r["users_total"], "label": "Usuarios Cadastrados"},
        },
        "geo_summary": {
            "total_cars": r["cars_total"],
            "total_environmental_alerts": r["ibama_total"] + r["mte_total"] + r["embargos_icmbio"] + r["autos_icmbio"],
            "total_deforestation_alerts": r["deter_amazonia"] + r["deter_cerrado"] + r["prodes_total"] + r["mapbiomas_alertas"],
            "total_protected_areas": r["terras_indigenas"] + r["ucs_total"],
            "total_credito_rural_parcelas": r["credito_rural"],
        },
    }


def _build_response_direct(db: Session, t0: float) -> dict:
    """Fallback com queries diretas (lento, ~1.7s)."""
    def count(table, where=""):
        sql = f"SELECT COUNT(*) FROM {table}"
        if where:
            sql += f" WHERE {where}"
        return db.execute(text(sql)).scalar() or 0

    r = {
        "cars_total": count("geo_car"),
        "cars_ufs": db.execute(text("SELECT COUNT(DISTINCT uf) FROM geo_car")).scalar() or 0,
        "ibama_total": count("environmental_alerts", "source = 'IBAMA'"),
        "mte_total": count("environmental_alerts", "source = 'MTE'"),
        "deter_amazonia": count("geo_deter_amazonia"),
        "deter_cerrado": count("geo_deter_cerrado"),
        "prodes_total": count("geo_prodes"),
        "mapbiomas_alertas": count("geo_mapbiomas_alertas"),
        "embargos_icmbio": count("geo_embargos_icmbio"),
        "autos_icmbio": count("geo_autos_icmbio"),
        "terras_indigenas": count("geo_terras_indigenas"),
        "ucs_total": count("geo_unidades_conservacao"),
        "credito_rural": count("mapbiomas_credito_rural"),
        "armazens": count("geo_armazens_silos"),
        "frigorificos": count("geo_frigorificos"),
        "rodovias": count("geo_rodovias_federais"),
        "portos": count("geo_portos"),
        "market_total": count("market_quotes"),
        "market_products": db.execute(text("SELECT COUNT(DISTINCT product) FROM market_quotes")).scalar() or 0,
        "market_last_date": db.execute(text("SELECT MAX(date) FROM market_quotes")).scalar(),
        "users_total": count("users"),
        "refreshed_at": datetime.now(timezone.utc),
    }
    t1 = time.perf_counter()
    return _build_response_from_mv(r, round((t1 - t0) * 1000, 1))
