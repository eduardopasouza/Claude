"""
Coletor de dados do SIGEF/INCRA (Sistema de Gestão Fundiária).

Fontes:
- Acervo Fundiário: https://acervofundiario.incra.gov.br/
- WFS: dados geoespaciais de parcelas certificadas
- API SIGEF: https://sigef.incra.gov.br/api/v1/
"""

from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import SIGEFData
from app.config import settings


class SIGEFCollector(BaseCollector):
    """Coleta dados de parcelas certificadas do SIGEF/INCRA."""

    def __init__(self):
        super().__init__("sigef")
        self.wfs_url = settings.sigef_wfs_url
        self.api_url = settings.sigef_api_url

    async def get_parcel_by_code(self, parcel_code: str) -> Optional[SIGEFData]:
        """Busca uma parcela pelo código SIGEF."""
        cached = self._get_cached(f"parcel:{parcel_code}")
        if cached:
            return SIGEFData(**cached)

        try:
            data = await self._fetch_parcel_api(parcel_code)
            if data:
                self._set_cached(f"parcel:{parcel_code}", data.model_dump())
            return data
        except Exception as e:
            print(f"[SIGEF] Error fetching parcel {parcel_code}: {e}")
            return None

    async def _fetch_parcel_api(self, parcel_code: str) -> Optional[SIGEFData]:
        """Consulta API pública do SIGEF para detalhes da parcela."""
        url = f"{self.api_url}/parcela/{parcel_code}"

        try:
            response = await self._http_get(url, timeout=30.0)
            if response.status_code == 200:
                result = response.json()
                return SIGEFData(
                    parcel_code=result.get("codigo", parcel_code),
                    certified=result.get("certificada", False),
                    area_ha=result.get("area", 0),
                    certification_date=result.get("data_certificacao"),
                    responsible_professional=result.get("responsavel_tecnico"),
                )
        except Exception:
            pass

        return None

    async def search_parcels_by_location(
        self, lat: float, lon: float, radius_km: float = 5.0
    ) -> list[SIGEFData]:
        """Busca parcelas SIGEF próximas a uma coordenada via WFS."""
        cached = self._get_cached(f"location:{lat}:{lon}:{radius_km}")
        if cached:
            return [SIGEFData(**item) for item in cached]

        try:
            # Convert radius to degrees (approximate)
            radius_deg = radius_km / 111.0

            bbox = f"{lon - radius_deg},{lat - radius_deg},{lon + radius_deg},{lat + radius_deg}"

            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "GetFeature",
                "typeName": "acervo:sigef_parcelas_certificadas",
                "outputFormat": "application/json",
                "bbox": bbox,
                "srsName": "EPSG:4326",
                "maxFeatures": "50",
            }

            response = await self._http_get(self.wfs_url, params=params, timeout=60.0)
            geojson = response.json()

            results = []
            for feature in geojson.get("features", []):
                props = feature.get("properties", {})
                geometry = feature.get("geometry")

                parcel = SIGEFData(
                    parcel_code=props.get("parcela_co", ""),
                    certified=True,
                    area_ha=props.get("area_hecta", 0),
                    certification_date=props.get("data_certi"),
                    responsible_professional=props.get("rt_nome"),
                    geometry_wkt=str(geometry) if geometry else None,
                )
                results.append(parcel)

            if results:
                self._set_cached(
                    f"location:{lat}:{lon}:{radius_km}",
                    [r.model_dump() for r in results],
                )
            return results
        except Exception as e:
            print(f"[SIGEF] Error searching by location ({lat}, {lon}): {e}")
            return []

    async def get_geometry_wfs(self, parcel_code: str) -> Optional[str]:
        """Busca geometria da parcela via WFS."""
        try:
            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "GetFeature",
                "typeName": "acervo:sigef_parcelas_certificadas",
                "outputFormat": "application/json",
                "CQL_FILTER": f"parcela_co='{parcel_code}'",
            }

            response = await self._http_get(self.wfs_url, params=params, timeout=60.0)
            geojson = response.json()

            if geojson.get("features") and len(geojson["features"]) > 0:
                geometry = geojson["features"][0].get("geometry")
                if geometry:
                    import json
                    return json.dumps(geometry)
        except Exception as e:
            print(f"[SIGEF WFS] Error fetching geometry for {parcel_code}: {e}")

        return None
