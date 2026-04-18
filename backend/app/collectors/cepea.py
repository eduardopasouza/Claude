"""
Coletor de cotações reais do CEPEA/ESALQ.

Scraping ético do site do CEPEA para obter indicadores de preços
agropecuários atualizados (soja, milho, boi gordo, café, etc).
"""

import logging
from typing import Optional
from datetime import datetime

from app.collectors.base import BaseCollector
from app.models.schemas import MarketQuote

logger = logging.getLogger("agrojus")


CEPEA_INDICATORS = {
    "soja": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/soja.aspx",
        "name": "Soja",
        "unit": "R$/saca 60kg",
    },
    "milho": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/milho.aspx",
        "name": "Milho",
        "unit": "R$/saca 60kg",
    },
    "boi_gordo": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/boi-gordo.aspx",
        "name": "Boi Gordo",
        "unit": "R$/@",
    },
    "cafe_arabica": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/cafe.aspx",
        "name": "Cafe Arabica",
        "unit": "R$/saca 60kg",
    },
    "algodao": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/algodao.aspx",
        "name": "Algodao",
        "unit": "c/lp",
    },
    "arroz": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/arroz.aspx",
        "name": "Arroz",
        "unit": "R$/saca 50kg",
    },
    "trigo": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/trigo.aspx",
        "name": "Trigo",
        "unit": "R$/t",
    },
    "acucar": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/acucar.aspx",
        "name": "Acucar Cristal",
        "unit": "R$/saca 50kg",
    },
    "etanol_hidratado": {
        "url": "https://www.cepea.esalq.usp.br/br/indicador/etanol.aspx",
        "name": "Etanol Hidratado",
        "unit": "R$/litro",
    },
}


class CEPEACollector(BaseCollector):
    """Coleta cotações do CEPEA/ESALQ via scraping ético."""

    def __init__(self):
        super().__init__("cepea")

    async def get_all_quotes(self) -> list[MarketQuote]:
        """Busca cotações mais recentes de todas as commodities CEPEA."""
        cached = self._get_cached("all_quotes")
        if cached:
            return [MarketQuote(**item) for item in cached]

        quotes = []
        for key, info in CEPEA_INDICATORS.items():
            try:
                quote = await self._scrape_indicator(key, info)
                if quote:
                    quotes.append(quote)
            except Exception as e:
                logger.warning("%s: %s", type(e).__name__, e)

        if quotes:
            self._set_cached("all_quotes", [q.model_dump() for q in quotes])

        return quotes

    async def get_quote(self, commodity: str) -> Optional[MarketQuote]:
        """Busca cotação de uma commodity específica."""
        if commodity not in CEPEA_INDICATORS:
            return None

        cached = self._get_cached(f"quote:{commodity}")
        if cached:
            return MarketQuote(**cached)

        info = CEPEA_INDICATORS[commodity]
        quote = await self._scrape_indicator(commodity, info)
        if quote:
            self._set_cached(f"quote:{commodity}", quote.model_dump())
        return quote

    async def _scrape_indicator(self, key: str, info: dict) -> Optional[MarketQuote]:
        """Scraping de uma página de indicador CEPEA."""
        try:
            response = await self._http_get(
                info["url"],
                headers={
                    "User-Agent": "AgroJus/1.0 (research; agrojus@example.com)",
                    "Accept": "text/html",
                },
                timeout=15.0,
            )

            return self._parse_cepea_page(key, info, response.text)
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return None

    def _parse_cepea_page(self, key: str, info: dict, html: str) -> Optional[MarketQuote]:
        """Parse HTML da página de indicador CEPEA."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        price = None
        variation = None
        date_str = None

        # CEPEA layout: table with class "imagenet-content" or
        # div with id "imagenet-indicador1"
        # The indicator value is typically in a specific table structure
        indicator_table = soup.find("table", {"id": "imagenet-indicador1"})
        if not indicator_table:
            # Alternative: look for the value in common patterns
            indicator_table = soup.find("table", class_="responsive")

        if indicator_table:
            rows = indicator_table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4:
                    try:
                        date_str = cells[0].get_text(strip=True)
                        price_text = cells[1].get_text(strip=True)
                        var_text = cells[3].get_text(strip=True)

                        price = self._parse_brl(price_text)
                        variation = self._parse_pct(var_text)

                        if price and price > 0:
                            break
                    except (ValueError, IndexError):
                        continue

        # Fallback: look for specific span/div patterns
        if not price:
            valor_span = soup.find("span", class_="valor")
            if valor_span:
                price = self._parse_brl(valor_span.get_text(strip=True))

            var_span = soup.find("span", class_="variacao")
            if var_span:
                variation = self._parse_pct(var_span.get_text(strip=True))

        if price and price > 0:
            return MarketQuote(
                commodity=info["name"],
                price=price,
                unit=info["unit"],
                date=date_str or datetime.now().strftime("%d/%m/%Y"),
                source="CEPEA/ESALQ",
                variation_pct=variation,
                location="Brasil",
            )

        return None

    @staticmethod
    def _parse_brl(text: str) -> Optional[float]:
        """Parse valor monetário brasileiro (1.234,56 → 1234.56)."""
        try:
            cleaned = text.replace("R$", "").replace(" ", "").strip()
            cleaned = cleaned.replace(".", "").replace(",", ".")
            return float(cleaned)
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _parse_pct(text: str) -> Optional[float]:
        """Parse percentual brasileiro (1,23% → 1.23)."""
        try:
            cleaned = text.replace("%", "").replace(" ", "").strip()
            cleaned = cleaned.replace(",", ".")
            return float(cleaned)
        except (ValueError, AttributeError):
            return None
