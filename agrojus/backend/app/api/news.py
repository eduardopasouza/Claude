"""Rotas do portal de notícias do agronegócio."""

from fastapi import APIRouter

from app.collectors.news_aggregator import NewsAggregator

router = APIRouter()


@router.get("/")
async def get_latest_news(limit: int = 30):
    """Retorna as últimas notícias do agronegócio (curadoria de múltiplas fontes)."""
    aggregator = NewsAggregator()
    articles = await aggregator.fetch_all_news(limit=limit)
    return {"articles": articles, "total": len(articles)}


@router.get("/legal")
async def get_legal_news(limit: int = 20):
    """Retorna notícias com relevância jurídica (legislação, regulamentação, etc)."""
    aggregator = NewsAggregator()
    articles = await aggregator.fetch_legal_news(limit=limit)
    return {"articles": articles, "total": len(articles), "category": "juridico"}


@router.get("/market")
async def get_market_news(limit: int = 20):
    """Retorna notícias de mercado (cotações, safras, commodities)."""
    aggregator = NewsAggregator()
    articles = await aggregator.fetch_market_news(limit=limit)
    return {"articles": articles, "total": len(articles), "category": "mercado"}
