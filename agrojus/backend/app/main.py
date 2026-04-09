from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import search, report, map_data, market, news, auth, monitoring, smart_search, geo, lawsuits


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Startup: ensure data directories exist
    from pathlib import Path
    Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.cache_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.shapefile_dir).mkdir(parents=True, exist_ok=True)
    yield
    # Shutdown: dispose DB engine
    from app.models.database import _engine
    if _engine:
        _engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Plataforma de Inteligência Fundiária, Jurídica e de Mercado para o Agronegócio",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["monitoring"])


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
        },
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
