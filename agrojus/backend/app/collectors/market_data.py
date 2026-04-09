"""
Coletor de dados de mercado agrícola (cotações, safras).

Fontes:
- CEPEA/ESALQ: indicadores de preços
- CONAB: dados de safra
- IBGE/SIDRA: produção agrícola municipal
"""

from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import MarketQuote


# CEPEA indicator URLs (public data)
CEPEA_INDICATORS = {
    "soja": {"name": "Soja", "unit": "R$/saca 60kg"},
    "milho": {"name": "Milho", "unit": "R$/saca 60kg"},
    "boi_gordo": {"name": "Boi Gordo", "unit": "R$/@"},
    "cafe_arabica": {"name": "Cafe Arabica", "unit": "R$/saca 60kg"},
    "algodao": {"name": "Algodao", "unit": "c/lp"},
    "arroz": {"name": "Arroz", "unit": "R$/saca 50kg"},
    "trigo": {"name": "Trigo", "unit": "R$/t"},
    "acucar": {"name": "Acucar Cristal", "unit": "R$/saca 50kg"},
    "etanol": {"name": "Etanol Hidratado", "unit": "R$/litro"},
    "leite": {"name": "Leite", "unit": "R$/litro"},
}

# IBGE SIDRA API for agricultural production data
SIDRA_BASE_URL = "https://apisidra.ibge.gov.br/values"


class MarketDataCollector(BaseCollector):
    """Coleta cotações e dados de mercado agrícola."""

    def __init__(self):
        super().__init__("market")

    async def get_latest_quotes(self) -> list[MarketQuote]:
        """Busca cotações mais recentes de todas as commodities."""
        cached = self._get_cached("latest_quotes")
        if cached:
            return [MarketQuote(**item) for item in cached]

        quotes = []
        for key, info in CEPEA_INDICATORS.items():
            try:
                quote = await self._fetch_cepea_indicator(key, info)
                if quote:
                    quotes.append(quote)
            except Exception as e:
                print(f"[MARKET] Error fetching {key}: {e}")

        if quotes:
            self._set_cached("latest_quotes", [q.model_dump() for q in quotes])

        return quotes

    async def _fetch_cepea_indicator(self, key: str, info: dict) -> Optional[MarketQuote]:
        """
        Busca indicador CEPEA.

        Note: CEPEA não tem API pública oficial. Em produção, os dados seriam
        obtidos via scraping do site do CEPEA ou de fontes que republicam
        (como Notícias Agrícolas ou Agrolink).
        """
        # Placeholder - in production this would scrape CEPEA or use
        # an aggregator that provides this data
        return MarketQuote(
            commodity=info["name"],
            price=0.0,
            unit=info["unit"],
            date="",
            source="CEPEA/ESALQ",
            variation_pct=None,
            location="Brasil",
        )

    async def get_production_by_municipality(
        self, municipality_code: str
    ) -> dict:
        """
        Busca dados de produção agrícola por município via IBGE/SIDRA.

        A API SIDRA fornece dados do PAM (Produção Agrícola Municipal).
        """
        cached = self._get_cached(f"production:{municipality_code}")
        if cached:
            return cached

        try:
            # PAM - Table 5457 (production, area, yield by municipality)
            # Main crops: soja (39), milho (33), cafe (9), cana (31)
            # v/214=area colhida, v/215=area plantada, v/216=quantidade produzida
            # c782: 39=soja, 33=milho, 9=cafe, 31=cana
            url = (
                f"{SIDRA_BASE_URL}/t/5457/n6/{municipality_code}"
                f"/v/214,215,216/p/last%201/c782/39,33,9,31"
                f"/f/n"
            )

            response = await self._http_get(url, timeout=30.0)
            data = response.json()

            result = self._parse_sidra_response(data)
            if result:
                self._set_cached(f"production:{municipality_code}", result)
            return result
        except Exception as e:
            print(f"[MARKET] Error fetching SIDRA data for {municipality_code}: {e}")
            return {}

    def _parse_sidra_response(self, data: list) -> dict:
        """Parse resposta da API SIDRA do IBGE."""
        result = {"crops": []}

        if not data or len(data) <= 1:
            return result

        # First row is header
        for row in data[1:]:
            try:
                crop = {
                    "name": row.get("D4N", ""),
                    "variable": row.get("D2N", ""),
                    "value": row.get("V", "0"),
                    "unit": row.get("MN", ""),
                    "year": row.get("D3N", ""),
                    "municipality": row.get("D1N", ""),
                }
                result["crops"].append(crop)
            except Exception:
                continue

        return result

    async def get_conab_harvest_data(self, crop: str = "soja") -> dict:
        """
        Busca dados de safra da CONAB.

        Note: CONAB disponibiliza relatórios e tabelas via portal.
        Em produção, os dados seriam baixados periodicamente.
        """
        cached = self._get_cached(f"conab:{crop}")
        if cached:
            return cached

        # Placeholder - CONAB data would be periodically downloaded
        # from portaldeinformacoes.conab.gov.br
        return {
            "crop": crop,
            "source": "CONAB",
            "note": "Dados a serem importados do Portal de Informacoes CONAB",
        }
