import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_config import setup_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.api import search, report, map_data, market, news, auth, monitoring, smart_search, geo, lawsuits, consulta, compliance, jurisdicao, dashboard, property, publicacoes, geo_layers, embrapa, ibge_choropleth, mapbiomas, webhooks, property_actions, dados_gov, dossie

setup_logging("DEBUG" if settings.debug else "INFO")
logger = logging.getLogger("agrojus")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    from pathlib import Path
    Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.cache_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.shapefile_dir).mkdir(parents=True, exist_ok=True)

    # Auto-cria tabelas novas (idempotente — só cria as que não existem).
    # Tabelas pré-existentes NÃO são alteradas.
    try:
        from app.models.database import create_tables
        create_tables()
        logger.info("AgroJus schema sincronizado (create_all idempotente)")
    except Exception as e:
        logger.warning("Falha ao sincronizar schema: %s", e)

    logger.info("AgroJus API v%s started", settings.app_version)
    yield
    from app.models.database import _engine
    if _engine:
        _engine.dispose()
    logger.info("AgroJus API shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Plataforma de Inteligência Fundiária, Jurídica e de Mercado para o Agronegócio",
    lifespan=lifespan,
)

# IMPORTANTE: ordem inversa no Starlette - o ULTIMO adicionado roda PRIMEIRO.
# CORS deve ser o mais externo para que TODAS as respostas tenham headers CORS,
# inclusive 429 do rate limiter.
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Remaining-Searches", "X-RateLimit-Remaining-Reports"],
)

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(smart_search.router, prefix="/api/v1/search", tags=["smart-search"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(report.router, prefix="/api/v1/report", tags=["report"])
app.include_router(map_data.router, prefix="/api/v1/map", tags=["map"])
app.include_router(geo.router, prefix="/api/v1/geo", tags=["geo"])
app.include_router(market.router, prefix="/api/v1/market", tags=["market"])
app.include_router(news.router, prefix="/api/v1/news", tags=["news"])
app.include_router(lawsuits.router, prefix="/api/v1/lawsuits", tags=["lawsuits"])
app.include_router(consulta.router, prefix="/api/v1/consulta", tags=["consulta-unificada"])
app.include_router(compliance.router, prefix="/api/v1/compliance", tags=["compliance"])
app.include_router(jurisdicao.router, prefix="/api/v1/jurisdicao", tags=["jurisdicao"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["monitoring"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(property.router, prefix="/api/v1/property", tags=["property"])
app.include_router(publicacoes.router, prefix="/api/v1/publicacoes", tags=["publicacoes-djen"])
app.include_router(geo_layers.router, prefix="/api/v1/geo/postgis", tags=["geo-layers"])
app.include_router(ibge_choropleth.router, prefix="/api/v1/geo/ibge/choropleth", tags=["ibge-choropleth"])
app.include_router(embrapa.router, prefix="/api/v1/embrapa", tags=["embrapa-agroapi"])
app.include_router(mapbiomas.router, prefix="/api/v1/mapbiomas", tags=["mapbiomas-alerta"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(property_actions.router, prefix="/api/v1/property", tags=["property-actions"])
app.include_router(dados_gov.router, prefix="/api/v1/dados-gov", tags=["dados-gov-etl"])
app.include_router(dossie.router, prefix="/api/v1/dossie", tags=["dossie-agrofundiario"])


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/v1/auth",
            "search": "/api/v1/search",
            "report": "/api/v1/report",
            "map": "/api/v1/map",
            "geo": "/api/v1/geo",
            "market": "/api/v1/market",
            "news": "/api/v1/news",
            "lawsuits": "/api/v1/lawsuits",
            "monitoring": "/api/v1/monitoring",
            "dashboard": "/api/v1/dashboard",
            "property": "/api/v1/property",
        },
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
