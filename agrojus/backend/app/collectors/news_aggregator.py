"""
Agregador de notícias do agronegócio via RSS feeds.

Fontes:
- Agrolink
- Canal Rural
- Notícias Agrícolas
- Agrofy News
- AgFeed
- Embrapa
"""

from typing import Optional
from datetime import datetime

try:
    import feedparser
except ImportError:
    feedparser = None

from app.collectors.base import BaseCollector
from app.models.schemas import NewsArticle


# RSS feed URLs dos principais portais agro
AGRO_RSS_FEEDS = {
    "Agrolink": "https://www.agrolink.com.br/rss/noticias.xml",
    "Canal Rural": "https://www.canalrural.com.br/feed/",
    "Noticias Agricolas": "https://www.noticiasagricolas.com.br/rss/noticias.xml",
    "Embrapa": "https://www.embrapa.br/rss/ultimas-noticias.xml",
    "Portal do Agronegocio": "https://www.portaldoagronegocio.com.br/feed",
}

# Categories for news classification
LEGAL_KEYWORDS = [
    "legislação", "lei", "decreto", "regulament", "jurídic", "juríd",
    "tribunal", "processo", "embargo", "multa", "autuação", "fiscal",
    "ambiental", "desmatamento", "reserva legal", "app ", "fundiár",
    "registro", "matrícula", "escritura", "contrato", "arrendamento",
    "trabalho escravo", "trabalhista", "compliance", "lgpd",
    "código florestal", "crime ambiental", "ibama", "icmbio",
]

MARKET_KEYWORDS = [
    "cotação", "preço", "soja", "milho", "café", "boi", "arroz",
    "commodit", "mercado", "exportação", "importação", "safra",
    "produção", "colheita", "plantio", "b3", "bolsa", "dólar",
]


class NewsAggregator(BaseCollector):
    """Agrega e categoriza notícias do agronegócio de múltiplas fontes RSS."""

    def __init__(self):
        super().__init__("news")
        self.feeds = AGRO_RSS_FEEDS

    async def fetch_all_news(self, limit: int = 50) -> list[NewsArticle]:
        """Busca notícias de todas as fontes RSS configuradas."""
        cached = self._get_cached("all_news")
        if cached:
            return [NewsArticle(**item) for item in cached[:limit]]

        all_articles = []
        for source_name, feed_url in self.feeds.items():
            try:
                articles = await self._fetch_feed(source_name, feed_url)
                all_articles.extend(articles)
            except Exception as e:
                print(f"[NEWS] Error fetching {source_name}: {e}")

        # Sort by date (most recent first)
        all_articles.sort(
            key=lambda a: a.published_at or "",
            reverse=True,
        )

        # Cache results
        if all_articles:
            self._set_cached(
                "all_news",
                [a.model_dump() for a in all_articles[:200]],
            )

        return all_articles[:limit]

    async def fetch_legal_news(self, limit: int = 20) -> list[NewsArticle]:
        """Busca notícias relacionadas a temas jurídicos/regulatórios."""
        all_news = await self.fetch_all_news(limit=200)
        legal_news = [
            article for article in all_news
            if self._is_legal_related(article)
        ]
        return legal_news[:limit]

    async def fetch_market_news(self, limit: int = 20) -> list[NewsArticle]:
        """Busca notícias relacionadas a mercado/cotações."""
        all_news = await self.fetch_all_news(limit=200)
        market_news = [
            article for article in all_news
            if self._is_market_related(article)
        ]
        return market_news[:limit]

    async def _fetch_feed(self, source_name: str, feed_url: str) -> list[NewsArticle]:
        """Busca e parseia um feed RSS individual."""
        if feedparser is None:
            print(f"[NEWS] feedparser not installed, skipping {source_name}")
            return []

        try:
            response = await self._http_get(feed_url, timeout=15.0)
            feed = feedparser.parse(response.text)

            articles = []
            for entry in feed.entries[:30]:
                # Parse publication date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6]).isoformat()
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6]).isoformat()

                # Get summary
                summary = None
                if hasattr(entry, "summary"):
                    summary = self._clean_html(entry.summary)[:300]

                # Get image
                image_url = None
                if hasattr(entry, "media_content") and entry.media_content:
                    image_url = entry.media_content[0].get("url")
                elif hasattr(entry, "enclosures") and entry.enclosures:
                    image_url = entry.enclosures[0].get("href")

                # Classify category
                category = self._classify_article(entry.title, summary or "")

                article = NewsArticle(
                    title=entry.title,
                    url=entry.link,
                    source=source_name,
                    published_at=published,
                    summary=summary,
                    category=category,
                    image_url=image_url,
                )
                articles.append(article)

            return articles
        except Exception as e:
            print(f"[NEWS] Error parsing feed {source_name}: {e}")
            return []

    def _classify_article(self, title: str, summary: str) -> str:
        """Classifica artigo em categorias baseado em keywords."""
        text = (title + " " + summary).lower()

        if any(kw in text for kw in LEGAL_KEYWORDS):
            return "juridico"
        elif any(kw in text for kw in MARKET_KEYWORDS):
            return "mercado"
        else:
            return "geral"

    def _is_legal_related(self, article: NewsArticle) -> bool:
        text = (article.title + " " + (article.summary or "")).lower()
        return any(kw in text for kw in LEGAL_KEYWORDS)

    def _is_market_related(self, article: NewsArticle) -> bool:
        text = (article.title + " " + (article.summary or "")).lower()
        return any(kw in text for kw in MARKET_KEYWORDS)

    @staticmethod
    def _clean_html(html: str) -> str:
        """Remove HTML tags de um texto."""
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, "html.parser").get_text(strip=True)
