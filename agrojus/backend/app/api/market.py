"""Rotas de dados de mercado agrícola."""

from fastapi import APIRouter

from app.collectors.market_data import MarketDataCollector

router = APIRouter()


@router.get("/quotes")
async def get_latest_quotes():
    """Retorna cotações mais recentes de commodities agrícolas."""
    collector = MarketDataCollector()
    quotes = await collector.get_latest_quotes()
    return {"quotes": quotes}


@router.get("/production/{municipality_code}")
async def get_production_data(municipality_code: str):
    """Retorna dados de produção agrícola por município (IBGE/SIDRA)."""
    collector = MarketDataCollector()
    data = await collector.get_production_by_municipality(municipality_code)
    return {"source": "IBGE/SIDRA", "data": data}


@router.get("/harvest/{crop}")
async def get_harvest_data(crop: str = "soja"):
    """Retorna dados de safra da CONAB."""
    collector = MarketDataCollector()
    data = await collector.get_conab_harvest_data(crop)
    return {"source": "CONAB", "data": data}
