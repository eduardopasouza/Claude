"""
etl_prodes.py — Ingestao do desmatamento anual consolidado PRODES (INPE)
via WFS do TerraBrasilis. Complementa o DETER (alertas recentes).
PRODES = desmatamento CONFIRMADO anual. Essencial para MCR 2.9 (corte 31/07/2019).
Cria tabela: geo_prodes
"""
import io
import logging
import os
import sys

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
TABLE_NAME = "geo_prodes"

# PRODES Amazonia — incrementos anuais de desmatamento
PRODES_URLS = [
    {
        "name": "PRODES Amazonia Legal (desmatamento acumulado)",
        "url": (
            "https://terrabrasilis.dpi.inpe.br/geoserver/prodes-legal-amz/ows"
            "?service=WFS&version=1.0.0&request=GetFeature"
            "&typeName=prodes-legal-amz:accumulated_deforestation_2007"
            "&outputFormat=application/json"
            "&maxFeatures=50000"
        ),
    },
]


def discover_layers(workspace: str) -> list[str]:
    """Descobre camadas disponvels no WFS."""
    import re
    caps_url = (
        f"https://terrabrasilis.dpi.inpe.br/geoserver/{workspace}/ows"
        "?service=WFS&version=2.0.0&request=GetCapabilities"
    )
    try:
        r = httpx.get(caps_url, timeout=30, verify=False)
        names = re.findall(rf"<Name>({workspace}:[^<]+)</Name>", r.text)
        return names
    except Exception as exc:
        logger.warning("GetCapabilities falhou para %s: %s", workspace, exc)
        return []


def fetch_prodes() -> gpd.GeoDataFrame | None:
    """Tenta baixar PRODES de multiplas URLs."""
    for src in PRODES_URLS:
        logger.info("Tentando: %s", src["name"])
        logger.info("  URL: %s", src["url"][:120])
        try:
            r = httpx.get(src["url"], timeout=180, follow_redirects=True, verify=False)
            logger.info("  HTTP %d — %d bytes", r.status_code, len(r.content))
            if r.status_code == 200 and len(r.content) > 1000:
                gdf = gpd.read_file(io.BytesIO(r.content))
                if len(gdf) > 0:
                    logger.info("  GeoDataFrame: %d poligonos | CRS: %s", len(gdf), gdf.crs)
                    logger.info("  Colunas: %s", list(gdf.columns))
                    return gdf
                logger.warning("  GeoDataFrame vazio")
        except Exception as exc:
            logger.warning("  Falha: %s", exc)
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
    logger.info("OK %d poligonos PRODES -> tabela '%s'", len(gdf), TABLE_NAME)


if __name__ == "__main__":
    logger.info("=== ETL PRODES (desmatamento anual consolidado) ===")

    # Descobrir camadas disponiveis
    for ws in ["prodes-amz", "prodes-cerrado"]:
        layers = discover_layers(ws)
        logger.info("Camadas %s: %s", ws, layers)

    gdf = fetch_prodes()
    if gdf is not None and len(gdf) > 0:
        load_to_postgis(gdf)
    else:
        logger.error("Nenhuma fonte PRODES retornou dados.")
        logger.info("Alternativa: baixar shapefiles em terrabrasilis.dpi.inpe.br/downloads/")
