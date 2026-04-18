"""
etl_icmbio_ucs.py — Ingestao de Unidades de Conservacao federais (ICMBio)
via WFS do INDE GeoServer ou download direto de shapefile.
Cria tabela: geo_unidades_conservacao
"""
import io
import logging
import os
import sys
import tempfile
import zipfile
from pathlib import Path

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

try:
    import geopandas as gpd
    from sqlalchemy import create_engine, text
except ImportError:
    logger.error("Instale: pip install geopandas sqlalchemy psycopg2-binary")
    sys.exit(1)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
TABLE_NAME = "geo_unidades_conservacao"

# Fontes em ordem de preferencia
SOURCES = [
    {
        "name": "INDE GeoServer WFS (GeoJSON)",
        "url": (
            "https://geoservicos.inde.gov.br/geoserver/ICMBio/ows"
            "?service=WFS&version=2.0.0&request=GetFeature"
            "&typeName=ICMBio:limiteucsfederais_a"
            "&outputFormat=application/json"
            "&count=1000"
        ),
        "format": "geojson",
    },
    {
        "name": "ICMBio GeoServer WFS (Shapefile)",
        "url": (
            "https://geoserver.icmbio.gov.br/geoserver/cecav/ows"
            "?service=WFS&version=1.0.0&request=GetFeature"
            "&typeName=cecav:view_uc_federal"
            "&outputFormat=SHAPE-ZIP&maxFeatures=5000"
        ),
        "format": "shapefile",
    },
    {
        "name": "dados.gov.br download direto",
        "url": "https://dados.gov.br/dados/conjuntos-dados/limites-oficiais-de-unidades-de-conservacao-federais",
        "format": "page",
    },
]


def fetch_geojson(url: str) -> gpd.GeoDataFrame | None:
    """Baixa GeoJSON via WFS."""
    try:
        r = httpx.get(url, timeout=120, follow_redirects=True, verify=False)
        logger.info("HTTP %d — %d bytes", r.status_code, len(r.content))
        if r.status_code == 200 and len(r.content) > 1000:
            gdf = gpd.read_file(io.BytesIO(r.content))
            if len(gdf) > 0:
                logger.info("GeoDataFrame: %d UCs | CRS: %s", len(gdf), gdf.crs)
                return gdf
    except Exception as exc:
        logger.warning("Falha: %s", exc)
    return None


def fetch_shapefile(url: str) -> gpd.GeoDataFrame | None:
    """Baixa Shapefile ZIP via WFS."""
    try:
        r = httpx.get(url, timeout=120, follow_redirects=True, verify=False)
        logger.info("HTTP %d — %d bytes", r.status_code, len(r.content))
        if r.status_code == 200 and len(r.content) > 1000:
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = Path(tmpdir) / "ucs.zip"
                zip_path.write_bytes(r.content)
                try:
                    with zipfile.ZipFile(zip_path) as zf:
                        zf.extractall(tmpdir)
                except zipfile.BadZipFile:
                    logger.warning("Resposta nao e ZIP valido")
                    return None
                shp_files = list(Path(tmpdir).rglob("*.shp"))
                if shp_files:
                    gdf = gpd.read_file(shp_files[0])
                    logger.info("GeoDataFrame: %d UCs | CRS: %s", len(gdf), gdf.crs)
                    return gdf
    except Exception as exc:
        logger.warning("Falha: %s", exc)
    return None


def fetch_ucs() -> gpd.GeoDataFrame | None:
    """Tenta baixar UCs de multiplas fontes."""
    for src in SOURCES:
        if src["format"] == "page":
            continue
        logger.info("Tentando: %s", src["name"])
        logger.info("  URL: %s", src["url"][:120])
        if src["format"] == "geojson":
            gdf = fetch_geojson(src["url"])
        else:
            gdf = fetch_shapefile(src["url"])
        if gdf is not None and len(gdf) > 0:
            return gdf
        logger.warning("  Sem dados nessa fonte")
    return None


def load_to_postgis(gdf: gpd.GeoDataFrame):
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        logger.info("Reprojetando %s -> EPSG:4326", gdf.crs)
        gdf = gdf.to_crs(epsg=4326)

    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS "{TABLE_NAME}" CASCADE'))
        conn.commit()

    gdf.to_postgis(TABLE_NAME, engine, if_exists="replace", index=True)
    logger.info("OK %d UCs -> tabela '%s'", len(gdf), TABLE_NAME)


if __name__ == "__main__":
    logger.info("=== ETL ICMBio Unidades de Conservacao ===")
    gdf = fetch_ucs()
    if gdf is not None and len(gdf) > 0:
        load_to_postgis(gdf)
    else:
        logger.error("Nenhuma fonte retornou dados. Verificar URLs manualmente.")
