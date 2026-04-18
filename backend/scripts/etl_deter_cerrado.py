"""
etl_deter_cerrado.py — Ingestão dos alertas de desmatamento DETER Cerrado (INPE)
via WFS do TerraClass/TerraBrasilis. Complementa o geo_deter_amazonia já existente.
Cria tabela: geo_deter_cerrado
"""
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

try:
    import geopandas as gpd
    from sqlalchemy import create_engine, text
    import io
except ImportError:
    logger.error("Instale: pip install geopandas sqlalchemy psycopg2-binary")
    sys.exit(1)

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")

# WFS DETER Cerrado — INPE TerraBrasilis (mesma infraestrutura do DETER Amazônia)
DETER_CERRADO_WFS = (
    "https://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/ows"
    "?service=WFS&version=1.0.0&request=GetFeature"
    "&typeName=deter-cerrado:deter_cerrado_aggregated_by_state"
    "&outputFormat=application/json"
    "&maxFeatures=50000"
)

DETER_CERRADO_WFS_ALT = (
    "https://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/ows"
    "?service=WFS&version=2.0.0&request=GetFeature"
    "&typeNames=deter-cerrado:deter_cerrado"
    "&outputFormat=application/json"
    "&count=50000"
)

TABLE_NAME = "geo_deter_cerrado"


def fetch_deter_cerrado() -> gpd.GeoDataFrame | None:
    """Tenta baixar os alertas DETER Cerrado via WFS."""
    for url in [DETER_CERRADO_WFS, DETER_CERRADO_WFS_ALT]:
        logger.info("Tentando: %s", url[:100])
        try:
            r = httpx.get(url, timeout=120, follow_redirects=True, verify=False)
            logger.info("HTTP %d — %d bytes", r.status_code, len(r.content))

            if r.status_code == 200 and r.content:
                gdf = gpd.read_file(io.BytesIO(r.content))
                if len(gdf) > 0:
                    logger.info("GeoDataFrame: %d alertas | CRS: %s", len(gdf), gdf.crs)
                    return gdf
                logger.warning("GeoDataFrame vazio nessa URL")
        except Exception as exc:
            logger.warning("Falha: %s", exc)

    return None


def load_to_postgis(gdf: gpd.GeoDataFrame):
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        logger.info("Reprojetando %s → EPSG:4326", gdf.crs)
        gdf = gdf.to_crs(epsg=4326)

    engine = create_engine(DATABASE_URL)

    # Remove tabela anterior se existir
    with engine.connect() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS "{TABLE_NAME}" CASCADE'))
        conn.commit()

    gdf.to_postgis(TABLE_NAME, engine, if_exists="replace", index=True)
    logger.info("✅ %d alertas DETER Cerrado → tabela '%s'", len(gdf), TABLE_NAME)


def list_deter_cerrado_layers():
    """Lista as camadas disponíveis no WFS DETER Cerrado para debug."""
    caps_url = (
        "https://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/ows"
        "?service=WFS&version=2.0.0&request=GetCapabilities"
    )
    r = httpx.get(caps_url, timeout=20, verify=False)
    # Extrai FeatureType names do XML
    import re
    names = re.findall(r"<Name>(deter-cerrado:[^<]+)</Name>", r.text)
    return names


if __name__ == "__main__":
    logger.info("=== ETL DETER Cerrado ===")

    # Descobre camadas disponíveis
    layers = list_deter_cerrado_layers()
    logger.info("Camadas WFS disponíveis: %s", layers)

    gdf = fetch_deter_cerrado()

    if gdf is not None and len(gdf) > 0:
        load_to_postgis(gdf)
    else:
        logger.error("Nenhum dado obtido do DETER Cerrado. Verifique as camadas acima.")
        logger.info("Use a camada correta: python etl_deter_cerrado.py")
