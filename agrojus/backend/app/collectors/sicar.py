"""
Coletor de dados do SICAR/CAR (Cadastro Ambiental Rural).

Fontes:
- Consulta pública: https://consultapublica.car.gov.br/publico/imoveis/index
- GeoServer WFS: dados geoespaciais dos imóveis
- Download de shapefiles por município
"""

import logging
import httpx
from typing import Optional

from app.collectors.base import BaseCollector
from app.models.schemas import CARData
from app.config import settings

logger = logging.getLogger("agrojus")


class SICARCollector(BaseCollector):
    """Coleta dados de imóveis rurais do SICAR/CAR."""

    def __init__(self):
        super().__init__("sicar")
        self.public_url = settings.sicar_public_url
        self.wfs_url = settings.sicar_wfs_url

    async def get_property_by_car(self, car_code: str) -> Optional[CARData]:
        """Busca um imóvel pelo código CAR."""
        cached = self._get_cached(f"car:{car_code}")
        if cached:
            return CARData(**cached)

        try:
            data = await self._fetch_car_data(car_code)
            if data:
                self._set_cached(f"car:{car_code}", data.model_dump())
            return data
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return None

    async def _fetch_car_data(self, car_code: str) -> Optional[CARData]:
        """Consulta dados do imóvel no SICAR via API pública."""
        # Extract state code from CAR code (first 2 chars are state IBGE code)
        state_code = car_code[:2]

        url = f"{self.public_url}/publico/imoveis/index"
        params = {
            "codigo": car_code,
        }

        try:
            response = await self._http_get(url, params=params, timeout=60.0)
            # Parse the response based on SICAR's public API format
            if response.status_code == 200:
                return self._parse_car_response(car_code, response.text)
        except httpx.HTTPStatusError:
            pass

        return None

    def _parse_car_response(self, car_code: str, html: str) -> Optional[CARData]:
        """Parse SICAR public consultation response."""
        # The SICAR public API returns HTML - we parse key fields
        # This is a simplified parser; production would use BeautifulSoup
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        data = CARData(car_code=car_code)

        # Try to extract basic property data from the response
        # Field extraction depends on the exact HTML structure
        area_fields = soup.find_all("td")
        for i, td in enumerate(area_fields):
            text = td.get_text(strip=True).lower()
            if "área total" in text and i + 1 < len(area_fields):
                try:
                    data.area_total_ha = float(
                        area_fields[i + 1].get_text(strip=True).replace(",", ".")
                    )
                except (ValueError, IndexError):
                    pass
            elif "município" in text and i + 1 < len(area_fields):
                data.municipality = area_fields[i + 1].get_text(strip=True)
            elif "estado" in text or "uf" in text:
                if i + 1 < len(area_fields):
                    data.state = area_fields[i + 1].get_text(strip=True)

        return data

    async def get_geometry_wfs(self, car_code: str) -> Optional[str]:
        """Busca geometria do imóvel via WFS do SICAR."""
        try:
            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "GetFeature",
                "typeName": "publico:imoveis",
                "outputFormat": "application/json",
                "CQL_FILTER": f"cod_imovel='{car_code}'",
            }

            response = await self._http_get(self.wfs_url, params=params, timeout=60.0)
            geojson = response.json()

            if geojson.get("features") and len(geojson["features"]) > 0:
                geometry = geojson["features"][0].get("geometry")
                if geometry:
                    import json
                    return json.dumps(geometry)
        except Exception as e:
            logger.info("%s: %s", type(e).__name__, e)

        return None

    async def search_by_municipality(self, municipality: str, state: str) -> list[CARData]:
        """Busca imóveis por município via WFS."""
        cached = self._get_cached(f"municipality:{state}:{municipality}")
        if cached:
            return [CARData(**item) for item in cached]

        try:
            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "GetFeature",
                "typeName": "publico:imoveis",
                "outputFormat": "application/json",
                "CQL_FILTER": f"nom_municipio='{municipality}' AND sig_uf='{state}'",
                "maxFeatures": "100",
            }

            response = await self._http_get(self.wfs_url, params=params, timeout=120.0)
            geojson = response.json()

            results = []
            for feature in geojson.get("features", []):
                props = feature.get("properties", {})
                car = CARData(
                    car_code=props.get("cod_imovel", ""),
                    area_total_ha=props.get("num_area", 0),
                    municipality=props.get("nom_municipio", municipality),
                    state=state,
                    status=props.get("des_condic", ""),
                )
                results.append(car)

            if results:
                self._set_cached(
                    f"municipality:{state}:{municipality}",
                    [r.model_dump() for r in results],
                )
            return results
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []
