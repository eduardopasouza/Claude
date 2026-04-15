"""
dashboard.py — Endpoint de métricas agregadas do AgroJus Dashboard.
GET /api/v1/dashboard/metrics retorna contagens reais do PostgreSQL + latência.
"""
import time
import logging
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Retorna KPIs reais do banco de dados para os cards do dashboard.
    Todas as contagens vêm diretamente do PostgreSQL — sem mock.
    """
    t0 = time.perf_counter()

    # ── Embargos IBAMA ────────────────────────────────────────────────────────
    ibama_total = db.execute(
        text("SELECT COUNT(*) FROM environmental_alerts WHERE source = 'IBAMA'")
    ).scalar() or 0

    ibama_last_30d = db.execute(
        text("""
            SELECT COUNT(*) FROM environmental_alerts
            WHERE source = 'IBAMA'
              AND created_at >= NOW() - INTERVAL '30 days'
        """)
    ).scalar() or 0

    # ── Lista Suja MTE ────────────────────────────────────────────────────────
    mte_total = db.execute(
        text("SELECT COUNT(*) FROM environmental_alerts WHERE source = 'MTE'")
    ).scalar() or 0

    # ── Cotações de Mercado ───────────────────────────────────────────────────
    market_total = db.execute(
        text("SELECT COUNT(*) FROM market_quotes")
    ).scalar() or 0

    market_last_date = db.execute(
        text("SELECT MAX(date) FROM market_quotes")
    ).scalar()

    market_products = db.execute(
        text("SELECT COUNT(DISTINCT product) FROM market_quotes")
    ).scalar() or 0

    # ── Crédito Rural MapBiomas ───────────────────────────────────────────────
    credito_rural_total = db.execute(
        text("SELECT COUNT(*) FROM mapbiomas_credito_rural")
    ).scalar() or 0

    # ── Usuários (se tabela existir) ──────────────────────────────────────────
    try:
        users_total = db.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar() or 0
    except Exception:
        users_total = 0

    # ── Geo Layers — Alertas DETER ───────────────────────────────────────────
    deter_amazonia = db.execute(
        text("SELECT COUNT(*) FROM geo_deter_amazonia")
    ).scalar() or 0

    deter_cerrado = db.execute(
        text("SELECT COUNT(*) FROM geo_deter_cerrado")
    ).scalar() or 0

    # ── Geo Layers — Terras Indígenas ─────────────────────────────────────────
    terras_indigenas = db.execute(
        text("SELECT COUNT(*) FROM geo_terras_indigenas")
    ).scalar() or 0

    # ── Infraestrutura Logística ──────────────────────────────────────────────
    armazens = db.execute(
        text("SELECT COUNT(*) FROM geo_armazens_silos")
    ).scalar() or 0

    frigorificos = db.execute(
        text("SELECT COUNT(*) FROM geo_frigorificos")
    ).scalar() or 0

    # ── MapBiomas Stats ───────────────────────────────────────────────────────
    try:
        area_irrigada_ha = db.execute(
            text("SELECT SUM(\"2023\") FROM mapbiomas_irrigation_stats")
        ).scalar() or 0
    except Exception:
        area_irrigada_ha = 0


    # ── Latência do banco ─────────────────────────────────────────────────────
    t1 = time.perf_counter()
    db_latency_ms = round((t1 - t0) * 1000, 1)

    # ── Cotações recentes (últimas 10 para cards) ────────────────────────────
    recent_quotes_raw = db.execute(
        text("""
            SELECT product, price_brl, date
            FROM market_quotes
            ORDER BY date DESC, id DESC
            LIMIT 10
        """)
    ).fetchall()

    recent_quotes = [
        {"product": row[0], "price_brl": row[1], "date": str(row[2])}
        for row in recent_quotes_raw
    ]


    # ── Últimos embargos IBAMA ────────────────────────────────────────────────
    recent_embargos_raw = db.execute(
        text("""
            SELECT cpf_cnpj, description, created_at
            FROM environmental_alerts
            WHERE source = 'IBAMA'
            ORDER BY created_at DESC
            LIMIT 5
        """)
    ).fetchall()

    recent_embargos = [
        {
            "cpf_cnpj": row[0],
            "description": (row[1] or "")[:100],
            "created_at": row[2].isoformat() if row[2] else None,
        }
        for row in recent_embargos_raw
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "db_latency_ms": db_latency_ms,
        "kpis": {
            "ibama_embargos": {
                "total": ibama_total,
                "last_30d": ibama_last_30d,
                "label": "Embargos IBAMA",
                "icon": "🔴",
            },
            "mte_lista_suja": {
                "total": mte_total,
                "label": "Empregadores Lista Suja MTE",
                "icon": "⚠️",
            },
            "market_quotes": {
                "total": market_total,
                "products": market_products,
                "last_date": str(market_last_date) if market_last_date else None,
                "label": "Cotações de Mercado",
                "icon": "📈",
            },
            "credito_rural": {
                "total": credito_rural_total,
                "label": "Parcelas MapBiomas",
                "icon": "🌿",
            },
            "deter_alertas": {
                "amazonia": deter_amazonia,
                "cerrado": deter_cerrado,
                "total": deter_amazonia + deter_cerrado,
                "label": "Alertas Desmatamento (DETER)",
                "icon": "🌳",
            },
            "terras_indigenas": {
                "total": terras_indigenas,
                "label": "Terras Indígenas (FUNAI)",
                "icon": "🏛",
            },
            "infraestrutura": {
                "armazens": armazens,
                "frigorificos": frigorificos,
                "label": "Infraestrutura Logística",
                "icon": "🏭",
            },
            "users": {
                "total": users_total,
                "label": "Usuários Cadastrados",
                "icon": "👤",
            },
        },
        "geo_summary": {
            "total_environmental_alerts": ibama_total + mte_total,
            "total_deter_alerts": deter_amazonia + deter_cerrado,
            "total_terras_indigenas": terras_indigenas,
            "total_credito_rural_parcelas": credito_rural_total,
            "area_irrigada_ha": round(float(area_irrigada_ha), 0) if area_irrigada_ha else 0,
        },
        "recent_quotes": recent_quotes,
        "recent_embargos": recent_embargos,
    }
