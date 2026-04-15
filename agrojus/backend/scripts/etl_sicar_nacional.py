"""
etl_sicar_nacional.py — Ingestao do CAR (Cadastro Ambiental Rural) nacional
via WFS do GeoServer SICAR. Carrega imoveis de todos os 27 estados.
Cria tabela: geo_car (consolidada nacional)

ATENCAO: SSL do SICAR requer cipher level rebaixado (SECLEVEL=1).
Cada estado pode ter dezenas de milhares de imoveis. maxFeatures limita o download.
"""
import io
import logging
import os
import ssl
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

try:
    import geopandas as gpd
    import pandas as pd
    from sqlalchemy import create_engine, text
except ImportError:
    logger.error("Instale: pip install geopandas sqlalchemy psycopg2-binary")
    sys.exit(1)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
TABLE_NAME = "geo_car"

ESTADOS = [
    "ac", "al", "am", "ap", "ba", "ce", "df", "es", "go",
    "ma", "mg", "ms", "mt", "pa", "pb", "pe", "pi", "pr",
    "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to",
]

MAX_FEATURES_PER_STATE = 5000


def get_ssl_client() -> httpx.Client:
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT@SECLEVEL=1")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return httpx.Client(verify=ctx, timeout=300)


def fetch_state(client: httpx.Client, uf: str) -> gpd.GeoDataFrame | None:
    url = (
        f"https://geoserver.car.gov.br/geoserver/sicar/wfs"
        f"?service=WFS&version=1.0.0&request=GetFeature"
        f"&typeName=sicar:sicar_imoveis_{uf}"
        f"&outputFormat=application/json"
        f"&maxFeatures={MAX_FEATURES_PER_STATE}"
    )
    try:
        r = client.get(url)
        if r.status_code == 200 and len(r.content) > 1000:
            gdf = gpd.read_file(io.BytesIO(r.content))
            if len(gdf) > 0:
                return gdf
    except Exception as exc:
        logger.warning("  %s falhou: %s", uf.upper(), exc)
    return None


def run():
    engine = create_engine(DATABASE_URL)
    client = get_ssl_client()

    with engine.connect() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS "{TABLE_NAME}" CASCADE'))
        conn.commit()

    total = 0
    first = True

    for uf in ESTADOS:
        logger.info("Baixando CAR %s...", uf.upper())
        gdf = fetch_state(client, uf)

        if gdf is None or len(gdf) == 0:
            logger.warning("  %s: sem dados ou erro", uf.upper())
            continue

        logger.info("  %s: %d imoveis | CRS: %s", uf.upper(), len(gdf), gdf.crs)

        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)

        mode = "replace" if first else "append"
        gdf.to_postgis(TABLE_NAME, engine, if_exists=mode, index=True)
        total += len(gdf)
        first = False
        logger.info("  %s: OK (acumulado: %d)", uf.upper(), total)

    logger.info("=== TOTAL: %d imoveis CAR em %s ===", total, TABLE_NAME)


if __name__ == "__main__":
    logger.info("=== ETL SICAR Nacional (27 estados) ===")
    run()
