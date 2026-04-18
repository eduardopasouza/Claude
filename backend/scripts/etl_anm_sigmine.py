"""
etl_anm_sigmine.py — Ingestao de processos minerarios (ANM/SIGMINE)
via ArcGIS REST FeatureServer. Sem autenticacao.
Cria tabela: geo_processos_minerarios
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
TABLE_NAME = "geo_processos_minerarios"

# ArcGIS REST FeatureServer — processos minerarios ativos
BASE_URL = "https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/FeatureServer/0/query"

# Estados prioritarios para agronegocio
ESTADOS_PRIORITARIOS = ["MA", "MT", "PA", "TO", "GO", "MS", "BA", "PI", "MG", "SP", "PR", "RS", "SC", "RO", "AC", "AM", "RR", "AP"]


def fetch_by_state(uf: str, offset: int = 0, page_size: int = 5000) -> gpd.GeoDataFrame | None:
    """Busca processos minerarios de um estado via ArcGIS REST."""
    params = {
        "where": f"UF='{uf}'",
        "outFields": "PROCESSO,NOME,SUBS,USO,ULT_EVENTO,FASE,AREA_HA,UF,NUM",
        "outSR": "4674",
        "f": "geojson",
        "resultOffset": offset,
        "resultRecordCount": page_size,
    }
    try:
        r = httpx.get(BASE_URL, params=params, timeout=60, verify=False)
        if r.status_code == 200 and len(r.content) > 100:
            gdf = gpd.read_file(io.BytesIO(r.content))
            if len(gdf) > 0:
                return gdf
    except Exception as exc:
        logger.warning("  %s falhou: %s", uf, exc)
    return None


def fetch_all_states() -> gpd.GeoDataFrame | None:
    """Busca processos de todos os estados prioritarios."""
    all_gdfs = []
    for uf in ESTADOS_PRIORITARIOS:
        logger.info("  Buscando %s...", uf)
        gdf = fetch_by_state(uf)
        if gdf is not None and len(gdf) > 0:
            logger.info("    %s: %d processos", uf, len(gdf))
            all_gdfs.append(gdf)
        else:
            logger.info("    %s: 0 processos ou falha", uf)

    if all_gdfs:
        import pandas as pd
        combined = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True))
        combined.set_crs(epsg=4674, inplace=True, allow_override=True)
        logger.info("Total: %d processos minerarios de %d estados", len(combined), len(all_gdfs))
        return combined
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
    logger.info("OK %d processos minerarios -> tabela '%s'", len(gdf), TABLE_NAME)


if __name__ == "__main__":
    logger.info("=== ETL ANM/SIGMINE (processos minerarios) ===")
    gdf = fetch_all_states()
    if gdf is not None and len(gdf) > 0:
        load_to_postgis(gdf)
    else:
        logger.error("Nenhum dado obtido do ANM/SIGMINE.")
