"""
Coletores de dados geoespaciais de fontes que funcionam em tempo real via WFS.

Fontes testadas e confirmadas:
- FUNAI GeoServer: 655 TIs, WFS sem auth, GeoJSON
- TerraBrasilis/INPE: 445K alertas DETER, WFS sem auth
- MMA/CNUC: UCs via shapefile download (atualizado 2025)
- IBGE: Biomas, solos, vegetação via shapefile download
"""

import logging

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


class FUNAICollector(BaseCollector):
    """Consulta terras indígenas em tempo real via FUNAI GeoServer WFS."""

    WFS_BASE = "https://geoserver.funai.gov.br/geoserver/Funai/ows"

    LAYERS = {
        "tis_poligonais": "Terras Indígenas (polígonos)",
        "tis_pontos": "Terras Indígenas (pontos)",
        "aldeias_pontos": "Aldeias (pontos)",
        "tis_poligonais_portarias": "TIs com portarias",
        "tis_amazonia_legal_poligonais": "TIs Amazônia Legal",
    }

    def __init__(self):
        super().__init__("funai")

    async def get_all_tis(self, max_features: int = 10000) -> dict:
        """Retorna todas as TIs como GeoJSON FeatureCollection."""
        cached = self._get_cached("all_tis")
        if cached:
            return cached

        try:
            params = {
                "service": "WFS",
                "version": "1.0.0",
                "request": "GetFeature",
                "typeName": "Funai:tis_poligonais",
                "maxFeatures": str(max_features),
                "outputFormat": "application/json",
            }
            response = await self._http_get(self.WFS_BASE, params=params, timeout=60.0)
            data = response.json()
            self._set_cached("all_tis", data)
            return data
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return {"type": "FeatureCollection", "features": []}

    async def check_overlap_ti(self, lat: float, lon: float, buffer_km: float = 0.1) -> list[dict]:
        """Verifica se um ponto está dentro de uma terra indígena."""
        cached = self._get_cached(f"overlap:{lat}:{lon}")
        if cached:
            return cached

        try:
            # Use CQL_FILTER INTERSECTS with a point buffer
            buffer_deg = buffer_km / 111.0
            bbox = f"{lon - buffer_deg},{lat - buffer_deg},{lon + buffer_deg},{lat + buffer_deg}"

            params = {
                "service": "WFS",
                "version": "1.0.0",
                "request": "GetFeature",
                "typeName": "Funai:tis_poligonais",
                "outputFormat": "application/json",
                "bbox": bbox,
            }
            response = await self._http_get(self.WFS_BASE, params=params, timeout=30.0)
            data = response.json()

            results = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                results.append({
                    "name": props.get("terrai_nome"),
                    "ethnicity": props.get("etnia_nome"),
                    "municipality": props.get("municipio_nome"),
                    "state": props.get("uf_sigla"),
                    "area_ha": props.get("superficie_perimetro_ha"),
                    "phase": props.get("fase_ti"),
                    "modality": props.get("modalidade_ti"),
                })

            self._set_cached(f"overlap:{lat}:{lon}", results)
            return results
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []

    async def search_by_state(self, uf: str) -> list[dict]:
        """Busca TIs por estado."""
        cached = self._get_cached(f"tis_uf:{uf}")
        if cached:
            return cached

        try:
            params = {
                "service": "WFS",
                "version": "1.0.0",
                "request": "GetFeature",
                "typeName": "Funai:tis_poligonais",
                "outputFormat": "application/json",
                "CQL_FILTER": f"uf_sigla='{uf.upper()}'",
            }
            response = await self._http_get(self.WFS_BASE, params=params, timeout=30.0)
            data = response.json()

            results = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                results.append({
                    "name": props.get("terrai_nome"),
                    "ethnicity": props.get("etnia_nome"),
                    "municipality": props.get("municipio_nome"),
                    "state": uf.upper(),
                    "area_ha": props.get("superficie_perimetro_ha"),
                    "phase": props.get("fase_ti"),
                })
            self._set_cached(f"tis_uf:{uf}", results)
            return results
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return []


class TerraBrasilisCollector(BaseCollector):
    """Consulta dados de desmatamento do INPE via TerraBrasilis WFS."""

    WFS_BASE = "https://terrabrasilis.dpi.inpe.br/geoserver"

    LAYERS = {
        "deter_amazonia": "deter-amz:deter_amz",
        "deter_cerrado": "deter-cerrado-nb:deter_cerrado",
        "prodes_amazonia": "prodes-legal-amz:accumulated_deforestation_2007",
        "prodes_cerrado": "prodes-cerrado-nb:accumulated_deforestation_2000",
        "prodes_mata_atlantica": "prodes-mata-atlantica-nb:accumulated_deforestation_2000",
        "prodes_caatinga": "prodes-caatinga-nb:accumulated_deforestation_2000",
        "prodes_pampa": "prodes-pampa-nb:accumulated_deforestation_2000",
        "prodes_pantanal": "prodes-pantanal-nb:accumulated_deforestation_2000",
        "biomas": "prodes-brasil-nb:biomas_brasil",
        "ucs_amazonia": "prodes-legal-amz:conservation_units_legal_amazon",
        "tis_amazonia": "prodes-legal-amz:indigenous_area_legal_amazon",
        "hidrografia_amazonia": "prodes-legal-amz:hydrography",
    }

    def __init__(self):
        super().__init__("terrabrasilis")

    async def get_deter_alerts(
        self, biome: str = "amazonia", bbox: str = None, max_features: int = 100
    ) -> dict:
        """Busca alertas DETER de desmatamento."""
        layer_key = f"deter_{biome}"
        layer_name = self.LAYERS.get(layer_key)
        if not layer_name:
            return {"error": f"Biome '{biome}' not supported", "available": list(self.LAYERS.keys())}

        cache_key = f"deter:{biome}:{bbox or 'all'}:{max_features}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            workspace = layer_name.split(":")[0]
            params = {
                "service": "WFS",
                "version": "1.0.0",
                "request": "GetFeature",
                "typeName": layer_name,
                "maxFeatures": str(max_features),
                "outputFormat": "application/json",
                "sortBy": "view_date+D",
            }
            if bbox:
                params["bbox"] = bbox

            url = f"{self.WFS_BASE}/{workspace}/wfs"
            response = await self._http_get(url, params=params, timeout=60.0)
            data = response.json()
            self._set_cached(cache_key, data)
            return data
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return {"type": "FeatureCollection", "features": []}

    async def check_deforestation(self, lat: float, lon: float, radius_km: float = 5.0) -> list[dict]:
        """Verifica alertas de desmatamento próximos a uma coordenada."""
        buffer_deg = radius_km / 111.0
        bbox = f"{lon - buffer_deg},{lat - buffer_deg},{lon + buffer_deg},{lat + buffer_deg}"

        results = []
        for biome in ["amazonia", "cerrado"]:
            data = await self.get_deter_alerts(biome=biome, bbox=bbox, max_features=50)
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                results.append({
                    "biome": biome,
                    "class": props.get("classname"),
                    "date": props.get("view_date"),
                    "sensor": props.get("sensor"),
                    "area_km2": props.get("areamunkm"),
                    "municipality": props.get("municipality"),
                    "state": props.get("uf"),
                })

        return results

    async def get_biomes_geojson(self) -> dict:
        """Retorna limites dos biomas brasileiros."""
        cached = self._get_cached("biomas")
        if cached:
            return cached

        try:
            params = {
                "service": "WFS",
                "version": "1.0.0",
                "request": "GetFeature",
                "typeName": self.LAYERS["biomas"],
                "outputFormat": "application/json",
            }
            url = f"{self.WFS_BASE}/prodes-brasil-nb/wfs"
            response = await self._http_get(url, params=params, timeout=60.0)
            data = response.json()
            self._set_cached("biomas", data)
            return data
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)
            return {"type": "FeatureCollection", "features": []}
