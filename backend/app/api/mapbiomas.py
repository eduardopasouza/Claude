"""
Endpoints REST para MapBiomas Alerta (GraphQL wrapper).

Prefix: /api/v1/mapbiomas/*

Diferença para as tabelas já carregadas no Postgres:
  - geo_mapbiomas_alertas  (515k registros) → alertas validados HISTÓRICOS
  - Este módulo            → alertas em TEMPO REAL via API oficial

Auth: JWT gerado via POST /auth/login com credenciais no .env.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.collectors.mapbiomas_alerta import MapBiomasAlertaCollector

router = APIRouter()


@router.get("/status")
async def mapbiomas_status():
    """Versão da API + intervalo disponível. API é pública (sem auth)."""
    c = MapBiomasAlertaCollector()
    version = await c.version()
    dates = await c.date_range()
    return {
        "status": "ok",
        "endpoint": "https://plataforma.alerta.mapbiomas.org/api/v2/graphql",
        "auth": "public",
        "version": version,
        "date_range": dates,
    }


@router.get("/territories")
async def mapbiomas_territories():
    """Todos os territórios disponíveis (~30k entries)."""
    c = MapBiomasAlertaCollector()
    return await c.territory_options()


@router.get("/alerts")
async def mapbiomas_alerts(
    start: Optional[str] = Query(None, description="YYYY-MM-DD (default: 30d atrás)"),
    end: Optional[str] = Query(None, description="YYYY-MM-DD (default: hoje)"),
    territory_ids: Optional[str] = Query(None, description="CSV de ids de território"),
    sources: Optional[str] = Query(None, description="CSV de ids de fonte"),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Busca alertas publicados.
    Sem parâmetros de data → últimos 30 dias.
    """
    today = date.today()
    start_d = start or (today - timedelta(days=30)).isoformat()
    end_d = end or today.isoformat()

    t_ids = [int(x) for x in territory_ids.split(",") if x.strip().isdigit()] if territory_ids else None
    s_ids = [int(x) for x in sources.split(",") if x.strip().isdigit()] if sources else None

    c = MapBiomasAlertaCollector()
    return await c.alerts(start_d, end_d, t_ids, s_ids, page, limit)


@router.get("/alert/{alert_code}")
async def mapbiomas_alert_detail(alert_code: int):
    """Detalhe de um alerta pelo código numérico."""
    c = MapBiomasAlertaCollector()
    return await c.alert_detail(alert_code)


@router.get("/property/{car_code}")
async def mapbiomas_property_alerts(car_code: str):
    """Alertas que intersectam um imóvel CAR (código de 43 chars)."""
    c = MapBiomasAlertaCollector()
    return await c.alerts_by_property(car_code)
