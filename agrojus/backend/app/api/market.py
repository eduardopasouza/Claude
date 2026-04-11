"""
Rotas de dados de mercado e financeiros do agronegócio.

Cotações de commodities, crédito rural, preços de terra,
produção agrícola, safras.

Quando as fontes reais (CEPEA scraping) nao estiverem disponiveis,
retorna dados de referencia realistas para que o frontend possa
desenvolver com dados estruturados.
"""

from fastapi import APIRouter
from typing import Optional
from datetime import datetime

from app.collectors.market_data import MarketDataCollector
from app.collectors.financial import FinancialDataCollector
from app.collectors.cepea import CEPEACollector
from app.models.schemas import MarketQuote

router = APIRouter()


# Dados de referencia (precos realistas do mercado brasileiro, abril 2026)
_REFERENCE_QUOTES = [
    MarketQuote(commodity="Soja", price=139.50, unit="R$/saca 60kg", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=1.15, location="Paranagua/PR"),
    MarketQuote(commodity="Milho", price=73.20, unit="R$/saca 60kg", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=-0.42, location="Campinas/SP"),
    MarketQuote(commodity="Boi Gordo", price=312.85, unit="R$/@", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=0.78, location="Sao Paulo/SP"),
    MarketQuote(commodity="Cafe Arabica", price=1425.00, unit="R$/saca 60kg", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=2.30, location="Mogiana/SP"),
    MarketQuote(commodity="Algodao", price=118.45, unit="c/lp", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=-0.15, location="Esalq"),
    MarketQuote(commodity="Arroz", price=94.80, unit="R$/saca 50kg", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=0.55, location="Esalq"),
    MarketQuote(commodity="Trigo", price=1580.00, unit="R$/t", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=-0.90, location="Parana"),
    MarketQuote(commodity="Acucar Cristal", price=148.30, unit="R$/saca 50kg", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=0.33, location="Sao Paulo/SP"),
    MarketQuote(commodity="Etanol Hidratado", price=2.78, unit="R$/litro", date="09/04/2026", source="CEPEA/ESALQ", variation_pct=-1.05, location="Sao Paulo/SP"),
]


# === Cotações ===

@router.get("/quotes")
async def get_latest_quotes():
    """
    Retorna cotações mais recentes de commodities agrícolas.

    Tenta buscar dados reais do CEPEA/ESALQ via scraping.
    Se falhar, retorna dados de referência com flag `is_reference: true`.
    """
    cepea = CEPEACollector()
    quotes = await cepea.get_all_quotes()

    if quotes:
        return {"quotes": quotes, "source": "CEPEA/ESALQ", "total": len(quotes), "is_reference": False}

    # Fallback: dados de referencia realistas
    return {
        "quotes": _REFERENCE_QUOTES,
        "source": "CEPEA/ESALQ (referencia)",
        "total": len(_REFERENCE_QUOTES),
        "is_reference": True,
    }


@router.get("/quotes/{commodity}")
async def get_commodity_quote(commodity: str):
    """Retorna cotação de uma commodity específica."""
    cepea = CEPEACollector()
    quote = await cepea.get_quote(commodity)
    if quote:
        return {"quote": quote, "source": "CEPEA/ESALQ", "is_reference": False}

    # Fallback: buscar nos dados de referencia
    commodity_lower = commodity.lower().replace("_", " ")
    for ref in _REFERENCE_QUOTES:
        if commodity_lower in ref.commodity.lower():
            return {"quote": ref, "source": "CEPEA/ESALQ (referencia)", "is_reference": True}

    return {"error": f"Commodity '{commodity}' nao encontrada", "available": [
        "soja", "milho", "boi_gordo", "cafe_arabica", "algodao", "arroz", "trigo", "acucar", "etanol_hidratado"
    ]}


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


# === Indicadores Economicos (BCB - dados reais) ===

@router.get("/indicators")
async def get_economic_indicators():
    """
    Indicadores economicos em TEMPO REAL do Banco Central.

    Retorna: SELIC, dolar, IPCA, IGP-M, CDI — dados atualizados diariamente.
    """
    from app.collectors.bcb import BCBCollector
    bcb = BCBCollector()
    indicators = await bcb.get_indicators_summary()
    return {"source": "Banco Central do Brasil", "indicators": indicators}


@router.get("/indicators/{serie}")
async def get_indicator_serie(serie: str, ultimos: int = 30):
    """
    Serie temporal de um indicador do BCB.

    Series: selic, dolar, ipca, igpm, cdi, poupanca, tr.
    """
    from app.collectors.bcb import BCBCollector
    bcb = BCBCollector()
    data = await bcb.get_serie(serie, ultimos=ultimos)
    return data
