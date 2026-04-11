"""
Rotas de dados geoespaciais em tempo real.

Fontes REAIS que funcionam sem autenticacao:
- FUNAI GeoServer WFS: Terras Indigenas (655 TIs)
- INPE/TerraBrasilis WFS: Alertas DETER desmatamento
- IBGE API: Malhas municipais/estaduais

O endpoint principal /analyze-point faz consulta paralela
em todas as fontes para um ponto clicado no mapa.
"""

import asyncio
import logging
from fastapi import APIRouter
from typing import Optional

import httpx

from app.collectors.geolayers import FUNAICollector, TerraBrasilisCollector
from app.collectors.ibge import IBGECollector

logger = logging.getLogger("agrojus.geo")
router = APIRouter()


# --- Analise de ponto (right-click no mapa) ---

@router.get("/analyze-point")
async def analyze_point(lat: float, lon: float, radius_km: float = 5.0):
    """
    Analise completa de um ponto no mapa.

    Consulta TODAS as fontes geoespaciais em paralelo:
    - Terras Indigenas (FUNAI)
    - Alertas de desmatamento (INPE/DETER)
    - Municipio (IBGE)

    Ideal para right-click no mapa → "Analisar esta regiao".
    """
    funai = FUNAICollector()
    tb = TerraBrasilisCollector()

    # Consultar todas as fontes em paralelo
    ti_task = funai.check_overlap_ti(lat, lon, buffer_km=radius_km)
    deter_task = tb.check_deforestation(lat, lon, radius_km=radius_km)
    municipio_task = _get_municipio_ibge(lat, lon)

    tis, deter_alerts, municipio_info = await asyncio.gather(
        ti_task, deter_task, municipio_task,
        return_exceptions=True,
    )

    # Tratar resultados (exceptions viram listas vazias)
    if isinstance(tis, Exception):
        logger.warning("FUNAI query failed: %s", tis)
        tis = []
    if isinstance(deter_alerts, Exception):
        logger.warning("DETER query failed: %s", deter_alerts)
        deter_alerts = []
    if isinstance(municipio_info, Exception):
        logger.warning("IBGE query failed: %s", municipio_info)
        municipio_info = None

    # Montar analise de sobreposicao
    overlaps = []
    risk_flags = []

    if tis:
        for ti in tis:
            overlaps.append({
                "type": "terra_indigena",
                "name": ti.get("name"),
                "ethnicity": ti.get("ethnicity"),
                "phase": ti.get("phase"),
                "area_ha": ti.get("area_ha"),
                "severity": "critical",
            })
        risk_flags.append(f"Sobreposicao com {len(tis)} Terra(s) Indigena(s)")

    if deter_alerts:
        for alert in deter_alerts[:10]:
            overlaps.append({
                "type": "desmatamento",
                "class": alert.get("class"),
                "date": alert.get("date"),
                "sensor": alert.get("sensor"),
                "area_km2": alert.get("area_km2"),
                "severity": "high",
            })
        risk_flags.append(f"{len(deter_alerts)} alerta(s) de desmatamento na regiao")

    # Determinar risco geral do ponto
    if any(o["severity"] == "critical" for o in overlaps):
        overall_risk = "critical"
    elif any(o["severity"] == "high" for o in overlaps):
        overall_risk = "high"
    elif overlaps:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    return {
        "coordinates": {"lat": lat, "lon": lon, "radius_km": radius_km},
        "municipio": municipio_info,
        "overall_risk": overall_risk,
        "risk_flags": risk_flags if risk_flags else ["Nenhuma sobreposicao detectada"],
        "overlaps": overlaps,
        "summary": {
            "terras_indigenas": len(tis) if isinstance(tis, list) else 0,
            "alertas_desmatamento": len(deter_alerts) if isinstance(deter_alerts, list) else 0,
        },
        "sources": ["FUNAI GeoServer", "INPE/TerraBrasilis", "IBGE"],
    }


async def _get_municipio_ibge(lat: float, lon: float) -> dict | None:
    """Consulta API do IBGE para descobrir municipio a partir de coordenadas."""
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            # IBGE API de localidades por coordenadas
            r = await client.get(
                f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios",
            )
            # A API do IBGE nao tem busca por coordenada direta,
            # usar reversegeocode alternativo
            r2 = await client.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={
                    "lat": lat, "lon": lon,
                    "format": "json", "zoom": 10,
                    "accept-language": "pt-BR",
                },
                headers={"User-Agent": "AgroJus/1.0"},
            )
            if r2.status_code == 200:
                data = r2.json()
                addr = data.get("address", {})
                return {
                    "municipio": addr.get("city") or addr.get("town") or addr.get("municipality"),
                    "estado": addr.get("state"),
                    "pais": addr.get("country"),
                    "display_name": data.get("display_name"),
                }
    except Exception as e:
        logger.warning("Reverse geocode failed: %s", e)
    return None


# --- Camadas GeoJSON para o mapa (dados reais via WFS) ---

@router.get("/layers/{layer_id}/geojson")
async def get_layer_geojson(
    layer_id: str,
    bbox: Optional[str] = None,
    max_features: int = 200,
    uf: Optional[str] = None,
):
    """
    Retorna GeoJSON real de uma camada para renderizar no Leaflet.

    Camadas disponiveis:
    - `terras_indigenas`: Terras Indigenas (FUNAI WFS)
    - `desmatamento`: Alertas DETER Amazonia (INPE WFS)
    - `desmatamento_cerrado`: Alertas DETER Cerrado (INPE WFS)

    Parametros:
    - bbox: bounding box (west,south,east,north)
    - max_features: limite de features (default 200)
    - uf: filtro por estado (apenas terras_indigenas)
    """
    if layer_id == "terras_indigenas":
        funai = FUNAICollector()
        if uf:
            # Buscar por estado e retornar como FeatureCollection
            tis = await funai.search_by_state(uf)
            # Converter para GeoJSON FeatureCollection simplificado
            return {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": ti,
                        "geometry": None,  # Pontos, nao poligonos neste modo
                    }
                    for ti in tis
                ],
                "source": "FUNAI GeoServer",
                "total": len(tis),
            }
        else:
            # Buscar GeoJSON completo com geometrias
            params = {
                "service": "WFS",
                "version": "1.0.0",
                "request": "GetFeature",
                "typeName": "Funai:tis_poligonais",
                "maxFeatures": str(max_features),
                "outputFormat": "application/json",
            }
            if bbox:
                params["bbox"] = bbox

            try:
                async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
                    r = await client.get(FUNAICollector.WFS_BASE, params=params)
                    if r.status_code == 200:
                        data = r.json()
                        data["source"] = "FUNAI GeoServer"
                        data["total"] = len(data.get("features", []))
                        return data
            except Exception as e:
                logger.warning("FUNAI WFS error: %s", e)
                return {"type": "FeatureCollection", "features": [], "error": str(e)}

    elif layer_id in ("desmatamento", "desmatamento_cerrado"):
        biome = "cerrado" if "cerrado" in layer_id else "amazonia"
        tb = TerraBrasilisCollector()
        data = await tb.get_deter_alerts(biome=biome, bbox=bbox, max_features=max_features)
        data["source"] = "INPE/TerraBrasilis"
        data["total"] = len(data.get("features", []))
        return data

    elif layer_id == "municipios":
        if not uf:
            return {"error": "Parametro 'uf' obrigatorio para camada municipios"}
        ibge = IBGECollector()
        data = await ibge.get_malha_estado(uf)
        data["source"] = "IBGE"
        data["total"] = len(data.get("features", []))
        return data

    else:
        return {
            "error": f"Camada '{layer_id}' nao encontrada",
            "available": ["terras_indigenas", "desmatamento", "desmatamento_cerrado", "municipios"],
        }


# --- Terras Indígenas (FUNAI) ---

@router.get("/terras-indigenas")
async def list_terras_indigenas(uf: Optional[str] = None):
    """Lista terras indigenas. Filtra por UF se informado."""
    funai = FUNAICollector()
    if uf:
        tis = await funai.search_by_state(uf)
        return {"source": "FUNAI GeoServer", "state": uf, "total": len(tis), "data": tis}

    data = await funai.get_all_tis()
    count = len(data.get("features", []))
    return {"source": "FUNAI GeoServer", "total": count, "data": data}


@router.get("/terras-indigenas/check")
async def check_overlap_ti(lat: float, lon: float, buffer_km: float = 0.1):
    """Verifica se uma coordenada esta dentro de uma terra indigena."""
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
    """Alertas DETER de desmatamento. Biomas: amazonia, cerrado."""
    tb = TerraBrasilisCollector()
    data = await tb.get_deter_alerts(biome=biome, bbox=bbox, max_features=max_features)
    count = len(data.get("features", []))
    return {"source": "INPE/TerraBrasilis", "biome": biome, "total": count, "data": data}


@router.get("/desmatamento/check")
async def check_deforestation(lat: float, lon: float, radius_km: float = 5.0):
    """Verifica alertas de desmatamento proximos a uma coordenada."""
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


# --- IBGE (Municipios, malhas, producao) ---

@router.get("/municipios/busca")
async def buscar_municipio(nome: str):
    """Busca municipios por nome. Retorna codigo IBGE, nome, UF."""
    ibge = IBGECollector()
    results = await ibge.buscar_municipio_por_nome(nome)
    return {"source": "IBGE", "total": len(results), "municipios": results}


@router.get("/municipios/{codigo}")
async def get_municipio(codigo: str):
    """Retorna dados de um municipio pelo codigo IBGE."""
    ibge = IBGECollector()
    data = await ibge.get_municipio_by_code(codigo)
    if data:
        return {"source": "IBGE", "data": data}
    return {"error": "Municipio nao encontrado"}


@router.get("/municipios/{codigo}/malha")
async def get_malha_municipio(codigo: str):
    """Retorna GeoJSON com contorno do municipio (para Leaflet)."""
    ibge = IBGECollector()
    data = await ibge.get_malha_municipio(codigo)
    return data


@router.get("/municipios/{codigo}/producao")
async def get_producao_agricola(codigo: str):
    """
    Dados reais de producao agricola do municipio (IBGE/SIDRA/PAM).

    Retorna area colhida, area plantada e quantidade produzida
    para soja, milho, cafe, cana e algodao.
    """
    ibge = IBGECollector()
    data = await ibge.get_producao_agricola(codigo)
    return {"source": "IBGE/SIDRA (PAM)", "data": data}


@router.get("/estados/{uf}/municipios")
async def get_municipios_estado(uf: str):
    """Retorna GeoJSON com malha de todos os municipios de um estado."""
    ibge = IBGECollector()
    data = await ibge.get_malha_estado(uf)
    total = len(data.get("features", []))
    return {"source": "IBGE", "uf": uf.upper(), "total": total, "data": data}
