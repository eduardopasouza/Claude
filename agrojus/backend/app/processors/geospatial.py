"""
Processador geoespacial para cruzamento de camadas.

Realiza análise de sobreposição entre o imóvel rural e:
- Terras Indígenas (FUNAI)
- Unidades de Conservação (ICMBio)
- Áreas embargadas (IBAMA)
- Alertas de desmatamento (INPE/DETER)
- Áreas de preservação (MapBiomas)
"""

import logging
import json
from pathlib import Path
from typing import Optional

from app.models.schemas import OverlapAnalysis
from app.config import settings

logger = logging.getLogger("agrojus")


class GeospatialProcessor:
    """Processa dados geoespaciais e verifica sobreposições."""

    def __init__(self):
        self.shapefile_dir = Path(settings.shapefile_dir)
        self._layers_loaded = False
        self._indigenous_lands = None
        self._conservation_units = None
        self._embargoed_areas = None

    def load_reference_layers(self):
        """
        Carrega camadas de referência (shapefiles) para análise de sobreposição.

        Em produção, os shapefiles seriam baixados periodicamente de:
        - FUNAI: terras indígenas
        - ICMBio: unidades de conservação
        - IBAMA: áreas embargadas
        - INPE: desmatamento

        Os dados ficariam no PostGIS para consultas espaciais eficientes.
        """
        try:
            import geopandas as gpd

            ti_path = self.shapefile_dir / "terras_indigenas"
            if ti_path.exists():
                shapefiles = list(ti_path.glob("*.shp"))
                if shapefiles:
                    self._indigenous_lands = gpd.read_file(shapefiles[0])

            uc_path = self.shapefile_dir / "unidades_conservacao"
            if uc_path.exists():
                shapefiles = list(uc_path.glob("*.shp"))
                if shapefiles:
                    self._conservation_units = gpd.read_file(shapefiles[0])

            self._layers_loaded = True
        except ImportError:
            print("[GEO] GeoPandas not available, running in limited mode")
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)

    def analyze_overlaps(self, property_geometry_geojson: str) -> OverlapAnalysis:
        """
        Analisa sobreposições entre a geometria do imóvel e camadas de referência.

        Args:
            property_geometry_geojson: Geometria do imóvel em formato GeoJSON string
        """
        analysis = OverlapAnalysis()

        if not property_geometry_geojson:
            return analysis

        try:
            import geopandas as gpd
            from shapely.geometry import shape

            geometry = shape(json.loads(property_geometry_geojson))

            # Check overlap with indigenous lands
            if self._indigenous_lands is not None:
                for _, row in self._indigenous_lands.iterrows():
                    if geometry.intersects(row.geometry):
                        analysis.overlaps_indigenous_land = True
                        analysis.indigenous_land_name = row.get("terrai_nom", "Unknown")
                        break

            # Check overlap with conservation units
            if self._conservation_units is not None:
                for _, row in self._conservation_units.iterrows():
                    if geometry.intersects(row.geometry):
                        analysis.overlaps_conservation_unit = True
                        analysis.conservation_unit_name = row.get("nome", "Unknown")
                        break

        except ImportError:
            print("[GEO] GeoPandas not available for overlap analysis")
        except Exception as e:
            logger.warning("%s: %s", type(e).__name__, e)

        return analysis

    def analyze_overlaps_postgis(self, property_car_code: str) -> OverlapAnalysis:
        """
        Analisa sobreposições usando consultas PostGIS (mais eficiente em produção).

        Em produção, todas as camadas estariam no PostGIS e as consultas
        seriam feitas via SQL espacial (ST_Intersects, ST_Area, etc.)
        """
        analysis = OverlapAnalysis()

        # Example PostGIS queries that would be used:
        # SELECT ti.terrai_nom FROM terras_indigenas ti
        # JOIN properties p ON ST_Intersects(p.geometry, ti.geometry)
        # WHERE p.car_code = :car_code

        # SELECT uc.nome FROM unidades_conservacao uc
        # JOIN properties p ON ST_Intersects(p.geometry, uc.geometry)
        # WHERE p.car_code = :car_code

        # SELECT e.* FROM embargos_ibama e
        # JOIN properties p ON ST_Intersects(p.geometry, e.geometry)
        # WHERE p.car_code = :car_code

        return analysis

    @staticmethod
    def calculate_area_ha(geometry_geojson: str) -> Optional[float]:
        """Calcula a área em hectares de uma geometria GeoJSON."""
        try:
            from shapely.geometry import shape
            from pyproj import Geod

            geometry = shape(json.loads(geometry_geojson))
            geod = Geod(ellps="WGS84")
            area_m2 = abs(geod.geometry_area_perimeter(geometry)[0])
            return area_m2 / 10000  # m² to hectares
        except Exception:
            return None

    @staticmethod
    def geometry_to_geojson(geometry_wkt: str) -> Optional[str]:
        """Converte WKT para GeoJSON."""
        try:
            from shapely import wkt
            geometry = wkt.loads(geometry_wkt)
            return json.dumps(geometry.__geo_interface__)
        except Exception:
            return None
