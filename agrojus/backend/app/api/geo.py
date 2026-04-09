"""
Rotas de dados geoespaciais em tempo real (FUNAI, INPE/TerraBrasilis).

Integra os coletores de geolayers que consultam WFS públicos
sem autenticação para terras indígenas e alertas de desmatamento.
"""

from fastapi import APIRouter
from typing import Optional

from app.collectors.geolayers import FUNAICollector, TerraBrasilisCollector

router = APIRouter()


# --- Terras Indígenas (FUNAI) ---

@router.get("/terras-indigenas")
async def list_terras_indigenas(uf: Optional[str] = None):
    """
    Lista terras indígenas. Filtra por UF se informado.

    Fonte: FUNAI GeoServer WFS (tempo real, sem auth).
    """
    funai = FUNAICollector()
    if uf:
        tis = await funai.search_by_state(uf)
        return {"source": "FUNAI GeoServer", "state": uf, "total": len(tis), "data": tis}

    data = await funai.get_all_tis()
    count = len(data.get("features", []))
    return {"source": "FUNAI GeoServer", "total": count, "type": "FeatureCollection"}


@router.get("/terras-indigenas/check")
async def check_overlap_ti(lat: float, lon: float, buffer_km: float = 0.1):
    """
    Verifica se uma coordenada está dentro ou próxima de uma terra indígena.

    Útil para análise de sobreposição em due diligence.
    """
    funai = FUNAICollector()
    results = await funai.check_overlap_ti(lat, lon, buffer_km)
    return {
        "source": "FUNAI GeoServer",
        "overlaps": len(results) > 0,
        "terras_indigenas": results,
        "coordinates": {"lat": lat, "lon": lon},
    }


# --- Desmatamento (INPE/TerraBrasilis) ---

@router.get("/desmatamento/alertas")
async def get_deforestation_alerts(
    biome: str = "amazonia",
    bbox: Optional[str] = None,
    max_features: int = 100,
):
    """
    Retorna alertas DETER de desmatamento por bioma.

    Biomas: amazonia, cerrado.
    Fonte: INPE/TerraBrasilis WFS (tempo real, sem auth).
    """
    tb = TerraBrasilisCollector()
    data = await tb.get_deter_alerts(biome=biome, bbox=bbox, max_features=max_features)
    count = len(data.get("features", []))
    return {"source": "INPE/TerraBrasilis", "biome": biome, "total": count, "data": data}


@router.get("/desmatamento/check")
async def check_deforestation(lat: float, lon: float, radius_km: float = 5.0):
    """
    Verifica alertas de desmatamento próximos a uma coordenada.

    Útil para análise de risco ambiental em due diligence.
    """
    tb = TerraBrasilisCollector()
    results = await tb.check_deforestation(lat, lon, radius_km)
    return {
        "source": "INPE/TerraBrasilis",
        "alerts_found": len(results),
        "alerts": results,
        "coordinates": {"lat": lat, "lon": lon, "radius_km": radius_km},
    }


@router.get("/biomas")
async def get_biomes():
    """Retorna limites dos biomas brasileiros (GeoJSON)."""
    tb = TerraBrasilisCollector()
    data = await tb.get_biomes_geojson()
    return {"source": "INPE/TerraBrasilis", "data": data}
