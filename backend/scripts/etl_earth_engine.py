"""
etl_earth_engine.py — Extracao de dados MapBiomas via Google Earth Engine
Extrai estatisticas por municipio/estado dos rasters MapBiomas.
Requer: pip install earthengine-api + autenticacao Google Cloud

Assets acessiveis (verificado 2026-04-15):
- LULC Collection 10: 52 assets (cobertura, agricultura, degradacao, mineracao, pastagem, solo, vegetacao, urbano)
- Agua Collection 4: 4 assets (superficie hidrica 1985-2024)
- Fogo Collection 4: 12 assets (area queimada 1985-2023)
- Solo Collection 2: 10 assets (carbono, argila, areia, silte)
- Degradacao: dentro do LULC Collection 10 (edge_size, isolation, patch_size)
"""
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

try:
    import ee
    import pandas as pd
    from sqlalchemy import create_engine, text
except ImportError:
    logger.error("Instale: pip install earthengine-api pandas sqlalchemy")
    sys.exit(1)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
GCP_PROJECT = os.environ.get("GCP_PROJECT_ID", "agrojus")

# MapBiomas Earth Engine Assets
ASSETS = {
    # LULC Collection 10
    "lulc_integration": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_integration_v2",
    "lulc_agriculture_cycles": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_agriculture_number_cycles_v2",
    "lulc_agriculture_second_crop": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_agriculture_second_crop_v1",
    "lulc_agriculture_irrigation": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_agriculture_irrigation_systems_v3",
    "lulc_pasture": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_v1",
    "lulc_pasture_age": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_age_v2",
    "lulc_pasture_vigor": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_vigor_v3",
    "lulc_pasture_biomass": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_biomass_v2",
    "lulc_mining": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_mining_annual_v1",
    "lulc_deforestation_secondary": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_deforestation_secondary_vegetation_v2",
    "lulc_degradation_edge": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_degradation_edge_size_v1",
    "lulc_degradation_isolation": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_degradation_isolation_v1",
    "lulc_degradation_patch": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_degradation_patch_size_v1",
    "lulc_pedology": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pedology_ibge_v2",
    "lulc_vegetation": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_vegetation_ibge_v4",
    "lulc_coverage": "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_coverage_v2",
    # Agua
    "water": "projects/mapbiomas-public/assets/brazil/water/collection4/mapbiomas_brazil_collection4_water_v3",
    # Fogo
    "fire_annual": "projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_annual_burned_v1",
    "fire_accumulated": "projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_accumulated_burned_v1",
    "fire_coverage": "projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_annual_burned_coverage_v1",
    # Solo
    "soil_soc": "projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_soc_kg_m2_000_030cm",
    "soil_clay": "projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_granulometry_clay_percentage",
    "soil_sand": "projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_granulometry_sand_percentage",
    "soil_silt": "projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_granulometry_silt_percentage",
}

# Classes de uso do solo MapBiomas LULC
LULC_CLASSES = {
    3: "Formacao Florestal", 4: "Formacao Savanica", 5: "Mangue",
    6: "Floresta Alagavel", 9: "Silvicultura", 11: "Campo Alagado",
    12: "Formacao Campestre", 13: "Outras Formacoes nao Florestais",
    15: "Pastagem", 18: "Agricultura", 19: "Lavoura Temporaria",
    20: "Cana", 21: "Mosaico Agricultura Pastagem",
    24: "Area Urbanizada", 25: "Outra Area nao Vegetada",
    26: "Corpo Dagua", 29: "Afloramento Rochoso", 30: "Mineracao",
    31: "Aquicultura", 33: "Rio Lago Oceano",
    35: "Lavoura Perene", 39: "Soja", 40: "Arroz",
    41: "Outras Lavouras Temporarias", 46: "Cafe", 47: "Citrus",
    48: "Outras Lavouras Perenes", 62: "Algodao",
}


def extract_lulc_for_property(geometry_geojson: dict, year: int = 2023) -> dict:
    """
    Extrai uso do solo para uma propriedade especifica.
    Entrada: GeoJSON do poligono da propriedade
    Saida: dicionario com area (ha) por classe de uso

    USO NO MOTOR DE RELATORIO:
    Dado um imovel (CAR), buscar geometria no PostGIS,
    converter pra GeoJSON, chamar esta funcao.
    """
    ee.Initialize(project=GCP_PROJECT)

    geom = ee.Geometry(geometry_geojson)
    lulc = ee.Image(ASSETS["lulc_integration"]).select(f"classification_{year}")
    area_img = ee.Image.pixelArea().divide(1e4)  # hectares

    results = {}
    for class_id, class_name in LULC_CLASSES.items():
        mask = lulc.eq(class_id)
        area = area_img.updateMask(mask).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=geom,
            scale=30,
            maxPixels=1e9,
        ).getInfo()
        area_ha = area.get("area", 0)
        if area_ha and area_ha > 0.01:
            results[class_name] = round(area_ha, 2)

    return results


def extract_fire_for_property(geometry_geojson: dict, start_year: int = 2019, end_year: int = 2023) -> list:
    """Extrai historico de queimadas para uma propriedade."""
    ee.Initialize(project=GCP_PROJECT)

    geom = ee.Geometry(geometry_geojson)
    fire = ee.Image(ASSETS["fire_annual"])
    area_img = ee.Image.pixelArea().divide(1e4)

    results = []
    for year in range(start_year, end_year + 1):
        try:
            band = f"burned_area_{year}"
            fire_y = fire.select(band)
            area = area_img.updateMask(fire_y.eq(1)).reduceRegion(
                reducer=ee.Reducer.sum(), geometry=geom, scale=30, maxPixels=1e9
            ).getInfo()
            area_ha = area.get("area", 0)
            results.append({"ano": year, "area_queimada_ha": round(area_ha, 2) if area_ha else 0})
        except:
            results.append({"ano": year, "area_queimada_ha": 0})

    return results


def extract_soil_for_property(geometry_geojson: dict) -> dict:
    """Extrai dados de solo (carbono, textura) para uma propriedade."""
    ee.Initialize(project=GCP_PROJECT)

    geom = ee.Geometry(geometry_geojson)
    results = {}

    for name, asset_id in [
        ("carbono_organico_kg_m2", ASSETS["soil_soc"]),
        ("argila_pct", ASSETS["soil_clay"]),
        ("areia_pct", ASSETS["soil_sand"]),
        ("silte_pct", ASSETS["soil_silt"]),
    ]:
        try:
            img = ee.Image(asset_id)
            last_band = img.bandNames().getInfo()[-1]
            stats = img.select(last_band).reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geom, scale=250, maxPixels=1e8
            ).getInfo()
            val = list(stats.values())[0] if stats else None
            results[name] = round(val, 2) if val else None
        except:
            results[name] = None

    return results


def extract_water_for_property(geometry_geojson: dict, year: int = 2023) -> dict:
    """Extrai superficie hidrica para uma propriedade."""
    ee.Initialize(project=GCP_PROJECT)

    geom = ee.Geometry(geometry_geojson)
    water = ee.Image(ASSETS["water"]).select(f"classification_{year}")
    area_img = ee.Image.pixelArea().divide(1e4)

    # Classe 1 = agua
    area = area_img.updateMask(water.eq(1)).reduceRegion(
        reducer=ee.Reducer.sum(), geometry=geom, scale=30, maxPixels=1e9
    ).getInfo()

    return {"area_agua_ha": round(area.get("area", 0), 2) if area.get("area") else 0}


if __name__ == "__main__":
    logger.info("=== ETL Earth Engine — Verificacao de assets ===")
    ee.Initialize(project=GCP_PROJECT)

    for name, asset_id in ASSETS.items():
        try:
            img = ee.Image(asset_id)
            bands = img.getInfo()["bands"]
            logger.info("  %s: %d bandas OK", name, len(bands))
        except Exception as e:
            logger.warning("  %s: ERRO — %s", name, str(e)[:80])
