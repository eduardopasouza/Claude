"""
ETL para baixar shapefiles geoespaciais de fontes públicas brasileiras
e carregar no PostGIS via GeoPandas.

Fontes suportadas:
  - FUNAI: Terras Indígenas
  - ICMBio: Unidades de Conservação
  - INPE DETER: Alertas de desmatamento
"""

import io
import logging
import os
import sys
import tempfile
import zipfile
from pathlib import Path

import httpx

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Importar GeoPandas e SQLAlchemy
try:
    import geopandas as gpd
    from sqlalchemy import create_engine
except ImportError:
    logger.error("Instale geopandas e sqlalchemy: pip install geopandas sqlalchemy psycopg2-binary")
    sys.exit(1)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://agrojus:agrojus_secure_2024@db:5432/agrojus"  
)

# ── Fontes ──────────────────────────────────────────────────

SOURCES = {
    "funai_ti": {
        "name": "Terras Indígenas (FUNAI)",
        "url": "https://geoserver.funai.gov.br/geoserver/Funai/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Funai:tis_poligonais&outputFormat=SHAPE-ZIP&maxFeatures=10000",
        "table": "geo_terras_indigenas",
        "description": "Polígonos de Terras Indígenas do Brasil",
    },
    "icmbio_uc": {
        "name": "Unidades de Conservação (ICMBio)",
        "url": "https://geoserver.icmbio.gov.br/geoserver/cecav/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=cecav:view_uc_federal&outputFormat=SHAPE-ZIP&maxFeatures=5000",
        "table": "geo_unidades_conservacao",
        "description": "Polígonos de UCs Federais do Brasil",
    },
    "deter_amazonia": {
        "name": "DETER Amazônia (INPE)",
        "url": "https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=deter-amz:deter_amz&outputFormat=SHAPE-ZIP&maxFeatures=50000",
        "table": "geo_deter_amazonia",
        "description": "Alertas de desmatamento DETER na Amazônia",
    },
    # ── MapBiomas Infraestrutura ──
    "mb_armazens_silos": {
        "name": "Armazéns e Silos (MapBiomas)",
        "url": "https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/armazens-silos.zip",
        "table": "geo_armazens_silos",
        "description": "Localização de armazéns e silos agrícolas — logística",
    },
    "mb_frigorificos": {
        "name": "Frigoríficos (MapBiomas)",
        "url": "https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/frigorificos.zip",
        "table": "geo_frigorificos",
        "description": "Localização de frigoríficos — rastreabilidade pecuária",
    },
    "mb_rodovias_federais": {
        "name": "Rodovias Federais (MapBiomas)",
        "url": "https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/rodovia-federal.zip",
        "table": "geo_rodovias_federais",
        "description": "Malha rodoviária federal — acesso logístico",
    },
    "mb_ferrovias": {
        "name": "Ferrovias (MapBiomas)",
        "url": "https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/ferrovia.zip",
        "table": "geo_ferrovias",
        "description": "Malha ferroviária — escoamento de grãos",
    },
    "mb_portos": {
        "name": "Portos Organizados (MapBiomas)",
        "url": "https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Porto-organizado.zip",
        "table": "geo_portos",
        "description": "Portos organizados — exportação de commodities",
    },
}


def download_shapefile(url: str, name: str) -> gpd.GeoDataFrame:
    """Baixa um shapefile (ZIP) e retorna como GeoDataFrame."""
    logger.info(f"Baixando {name}...")
    logger.info(f"  URL: {url[:120]}...")

    response = httpx.get(url, timeout=120.0, follow_redirects=True)
    
    if response.status_code != 200:
        logger.error(f"  HTTP {response.status_code} — falha no download")
        return None
    
    logger.info(f"  Download: {len(response.content):,} bytes")
    
    # Salvar ZIP temporário e extrair
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "data.zip"
        zip_path.write_bytes(response.content)
        
        try:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(tmpdir)
                logger.info(f"  Arquivos: {zf.namelist()}")
        except zipfile.BadZipFile:
            logger.error(f"  Resposta não é um ZIP válido. Primeiros bytes: {response.content[:200]}")
            return None
        
        # Encontrar .shp
        shp_files = list(Path(tmpdir).rglob("*.shp"))
        if not shp_files:
            logger.error(f"  Nenhum .shp encontrado no ZIP")
            return None
        
        shp_path = shp_files[0]
        logger.info(f"  Lendo: {shp_path.name}")
        gdf = gpd.read_file(shp_path)
        logger.info(f"  Geometrias: {len(gdf):,} | CRS: {gdf.crs}")
        
        return gdf


def load_to_postgis(gdf: gpd.GeoDataFrame, table: str, description: str):
    """Carrega GeoDataFrame no PostGIS."""
    if gdf is None or len(gdf) == 0:
        logger.warning(f"  GeoDataFrame vazio — pulando {table}")
        return
    
    # Reprojetar para WGS84 (EPSG:4326) se necessário
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        logger.info(f"  Reprojetando de {gdf.crs} para EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)
    
    engine = create_engine(DATABASE_URL)
    logger.info(f"  Carregando {len(gdf):,} geometrias na tabela '{table}'...")
    
    gdf.to_postgis(table, engine, if_exists="replace", index=True)
    
    logger.info(f"  ✔ {len(gdf):,} registros em '{table}' — {description}")


def run(source_key: str = None):
    """Executa ingestão para uma fonte específica ou todas."""
    targets = {source_key: SOURCES[source_key]} if source_key else SOURCES
    
    for key, src in targets.items():
        logger.info(f"\n{'='*60}")
        logger.info(f"FONTE: {src['name']}")
        logger.info(f"{'='*60}")
        
        gdf = download_shapefile(src["url"], src["name"])
        if gdf is not None:
            load_to_postgis(gdf, src["table"], src["description"])
        else:
            logger.warning(f"  ⚠ Falha ao baixar {src['name']}")
    
    logger.info("\n=== Ingestão Concluída ===")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=list(SOURCES.keys()), default=None,
                        help="Fonte específica para baixar (default: todas)")
    args = parser.parse_args()
    run(args.source)
