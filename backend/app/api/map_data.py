"""Rotas de dados geoespaciais para o mapa interativo."""

from fastapi import APIRouter, HTTPException

from app.collectors.sicar import SICARCollector
from app.collectors.sigef import SIGEFCollector

router = APIRouter()


@router.get("/layers")
async def list_layers():
    """Lista as camadas disponíveis no mapa."""
    return {
        "layers": [
            {
                "id": "car",
                "name": "Cadastro Ambiental Rural (CAR)",
                "source": "SICAR",
                "type": "polygon",
                "description": "Perimetros de imoveis rurais cadastrados no CAR",
            },
            {
                "id": "sigef",
                "name": "Parcelas Certificadas (SIGEF)",
                "source": "INCRA/SIGEF",
                "type": "polygon",
                "description": "Parcelas com georreferenciamento certificado",
            },
            {
                "id": "embargos",
                "name": "Areas Embargadas (IBAMA)",
                "source": "IBAMA",
                "type": "polygon",
                "description": "Areas com embargo ambiental ativo",
            },
            {
                "id": "terras_indigenas",
                "name": "Terras Indigenas",
                "source": "FUNAI",
                "type": "polygon",
                "description": "Terras indigenas demarcadas",
            },
            {
                "id": "unidades_conservacao",
                "name": "Unidades de Conservacao",
                "source": "ICMBio",
                "type": "polygon",
                "description": "Unidades de conservacao federais e estaduais",
            },
            {
                "id": "desmatamento",
                "name": "Alertas de Desmatamento",
                "source": "INPE/DETER",
                "type": "polygon",
                "description": "Alertas recentes de desmatamento",
            },
        ]
    }


@router.get("/geojson/car/{car_code}")
async def get_car_geojson(car_code: str):
    """Retorna geometria GeoJSON de um imóvel pelo código CAR."""
    sicar = SICARCollector()
    geometry = await sicar.get_geometry_wfs(car_code)
    if geometry:
        return {"type": "Feature", "geometry": geometry, "properties": {"car_code": car_code}}
    raise HTTPException(status_code=404, detail="Geometria nao encontrada")


@router.get("/geojson/sigef/{parcel_code}")
async def get_sigef_geojson(parcel_code: str):
    """Retorna geometria GeoJSON de uma parcela SIGEF."""
    sigef = SIGEFCollector()
    geometry = await sigef.get_geometry_wfs(parcel_code)
    if geometry:
        return {"type": "Feature", "geometry": geometry, "properties": {"parcel_code": parcel_code}}
    raise HTTPException(status_code=404, detail="Geometria nao encontrada")


@router.get("/search/bbox")
async def search_by_bbox(
    west: float, south: float, east: float, north: float,
    layer: str = "sigef",
):
    """Busca features dentro de um bounding box (para o mapa interativo)."""
    if layer == "sigef":
        sigef = SIGEFCollector()
        center_lat = (south + north) / 2
        center_lon = (west + east) / 2
        radius_km = max(abs(north - south), abs(east - west)) * 111 / 2

        parcels = await sigef.search_parcels_by_location(
            center_lat, center_lon, radius_km
        )
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": p.model_dump(exclude={"geometry_wkt"}),
                    "geometry": p.geometry_wkt,
                }
                for p in parcels
            ],
        }

    raise HTTPException(status_code=400, detail=f"Camada '{layer}' nao suportada para busca por bbox")
