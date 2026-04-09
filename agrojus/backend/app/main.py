from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import search, report, map_data, market, news

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Plataforma de Inteligência Fundiária, Jurídica e de Mercado para o Agronegócio",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(report.router, prefix="/api/v1/report", tags=["report"])
app.include_router(map_data.router, prefix="/api/v1/map", tags=["map"])
app.include_router(market.router, prefix="/api/v1/market", tags=["market"])
app.include_router(news.router, prefix="/api/v1/news", tags=["news"])


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
