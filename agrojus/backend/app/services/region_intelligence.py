"""
Serviço de Inteligência Regional.

Gera relatório sobre um município ou região, cruzando:
- Estatísticas de imóveis (CAR)
- Embargos ambientais (IBAMA)
- Produção agrícola (IBGE/SIDRA)
- Crédito rural (SICOR/BCB)
- Preços de terra
- Notícias locais
"""

import uuid
from datetime import datetime, timezone

from app.collectors.sicar import SICARCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.market_data import MarketDataCollector
from app.collectors.financial import FinancialDataCollector
from app.collectors.news_aggregator import NewsAggregator
from app.models.schemas import RegionSearchRequest, RegionReport


class RegionIntelligenceService:
    """Gera relatórios de inteligência sobre uma região."""

    def __init__(self):
        self.sicar = SICARCollector()
        self.ibama = IBAMACollector()
        self.market = MarketDataCollector()
        self.financial = FinancialDataCollector()
        self.news = NewsAggregator()

    async def generate_report(self, request: RegionSearchRequest) -> RegionReport:
        """Gera relatório completo de uma região."""
        report = RegionReport(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            municipality=request.municipality,
            state=request.state,
        )

        # 1. Imóveis na região
        if request.municipality and request.state:
            properties = await self.sicar.search_by_municipality(
                request.municipality, request.state
            )
            report.total_properties = len(properties)
            report.total_area_ha = sum(p.area_total_ha or 0 for p in properties)

        # 2. Embargos na região
        if request.municipality and request.state:
            report.ibama_embargos = await self.ibama.search_embargos_by_municipality(
                request.municipality, request.state
            )

        # 3. Cotações de mercado
        quotes = await self.market.get_latest_quotes()
        report.quotes = quotes

        # 4. Produção agrícola
        if request.municipality_code:
            production = await self.market.get_production_by_municipality(
                request.municipality_code
            )
            report.main_crops = production.get("crops", [])

        # 5. Dados financeiros
        if request.municipality_code:
            report.financial_summary = await self.financial.get_financial_summary_by_municipality(
                request.municipality_code
            )

        # 6. Notícias da região
        all_news = await self.news.fetch_all_news(limit=100)
        if request.municipality:
            report.news = [
                n for n in all_news
                if request.municipality.lower() in (n.title + " " + (n.summary or "")).lower()
            ][:10]

        return report
