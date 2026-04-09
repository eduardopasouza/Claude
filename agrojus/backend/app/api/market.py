"""
Rotas de dados de mercado e financeiros do agronegócio.

Cotações de commodities, crédito rural, preços de terra,
produção agrícola, safras.
"""

from fastapi import APIRouter
from typing import Optional

from app.collectors.market_data import MarketDataCollector
from app.collectors.financial import FinancialDataCollector
from app.collectors.cepea import CEPEACollector

router = APIRouter()


# === Cotações ===

@router.get("/quotes")
async def get_latest_quotes():
    """Retorna cotações mais recentes de commodities agrícolas (CEPEA/ESALQ)."""
    cepea = CEPEACollector()
    quotes = await cepea.get_all_quotes()
    return {"quotes": quotes, "source": "CEPEA/ESALQ", "total": len(quotes)}


@router.get("/quotes/{commodity}")
async def get_commodity_quote(commodity: str):
    """Retorna cotação de uma commodity específica."""
    cepea = CEPEACollector()
    quote = await cepea.get_quote(commodity)
    if quote:
        return {"quote": quote, "source": "CEPEA/ESALQ"}
    return {"error": f"Commodity '{commodity}' nao encontrada", "available": list(
        ["soja", "milho", "boi_gordo", "cafe_arabica", "algodao", "arroz", "trigo", "acucar", "etanol_hidratado"]
    )}


# === Produção Agrícola ===

@router.get("/production/{municipality_code}")
async def get_production_data(municipality_code: str):
    """Retorna dados de produção agrícola por município (IBGE/SIDRA/PAM)."""
    collector = MarketDataCollector()
    data = await collector.get_production_by_municipality(municipality_code)
    return {"source": "IBGE/SIDRA", "data": data}


@router.get("/harvest/{crop}")
async def get_harvest_data(crop: str = "soja"):
    """Retorna dados de safra da CONAB."""
    collector = MarketDataCollector()
    data = await collector.get_conab_harvest_data(crop)
    return {"source": "CONAB", "data": data}


# === Crédito Rural ===

@router.get("/credit/municipality/{municipality_code}")
async def get_rural_credit_by_municipality(municipality_code: str, year: int = 2025):
    """
    Retorna dados de crédito rural por município (SICOR/BCB).

    Inclui: PRONAF, PRONAMP, crédito empresarial. Dados agregados
    por banco, linha de crédito, finalidade e cultura.
    """
    collector = FinancialDataCollector()
    credits = await collector.get_rural_credits_by_municipality(municipality_code, year)
    total = sum(c.amount or 0 for c in credits)
    return {
        "source": "BCB/SICOR",
        "municipality_code": municipality_code,
        "year": year,
        "total_credit": total,
        "records": credits,
    }


# === Preços de Terra ===

@router.get("/land-prices/{state}")
async def get_land_prices(state: str, municipality: Optional[str] = None):
    """
    Retorna preços de terras por estado/município.

    Dados de referência para avaliação de imóveis rurais.
    """
    collector = FinancialDataCollector()
    prices = await collector.get_land_prices(state, municipality)
    return {
        "source": "Dados de Mercado",
        "state": state,
        "municipality": municipality,
        "prices": prices,
    }


# === FIAGRO ===

@router.get("/fiagro")
async def get_fiagro_funds():
    """
    Retorna informações sobre fundos FIAGRO (CVM).

    Útil para investidores em ativos rurais.
    """
    collector = FinancialDataCollector()
    funds = await collector.get_fiagro_funds()
    return {"source": "CVM", "funds": funds}
