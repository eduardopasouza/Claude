"""
etl_sigef_download.py — Baixa parcelas SIGEF e SNCI do INCRA para PostGIS.

Download direto dos shapefiles por estado via certificacao.incra.gov.br.
Nao requer autenticacao para os ZIPs.

Uso:
    # Baixar SIGEF do MA
    python scripts/etl_sigef_download.py MA

    # Baixar SIGEF + SNCI de multiplos estados
    python scripts/etl_sigef_download.py MA MT PA GO TO MS --snci

    # Baixar todos os estados (demora ~1h)
    python scripts/etl_sigef_download.py ALL

URLs:
    SIGEF: https://certificacao.incra.gov.br/csv_shp/zip/Sigef%20Brasil_XX.zip
    SNCI:  https://certificacao.incra.gov.br/csv_shp/zip/Im%C3%B3vel%20certificado%20SNCI%20Brasil_XX.zip
"""

import sys
import os
import time
import tempfile
import logging
import zipfile

import httpx
import geopandas as gpd
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
SIGEF_URL = "https://certificacao.incra.gov.br/csv_shp/zip/Sigef%20Brasil_{uf}.zip"
SNCI_URL = "https://certificacao.incra.gov.br/csv_shp/zip/Im%C3%B3vel%20certificado%20SNCI%20Brasil_{uf}.zip"

ALL_UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
    "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
    "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]


def download_and_load(url_template: str, table_name: str, uf: str, engine) -> int:
    """Baixa ZIP, extrai shapefile, carrega no PostGIS."""
    url = url_template.format(uf=uf)
    logger.info("Baixando %s ...", url)

    try:
        with httpx.Client(timeout=120, follow_redirects=True) as client:
            r = client.get(url)
            if r.status_code != 200:
                logger.warning("  HTTP %d para %s", r.status_code, uf)
                return 0
            content = r.content
            if len(content) < 1000 or b"<!DOCTYPE" in content[:200]:
                logger.warning("  Resposta HTML (login?), pulando %s", uf)
                return 0
    except Exception as e:
        logger.warning("  Download falhou %s: %s", uf, e)
        return 0

    # Salvar e extrair
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, f"{uf}.zip")
        with open(zip_path, "wb") as f:
            f.write(content)

        try:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(tmpdir)
        except zipfile.BadZipFile:
            logger.warning("  ZIP invalido para %s", uf)
            return 0

        # Encontrar .shp
        shp_files = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]
        if not shp_files:
            logger.warning("  Nenhum .shp encontrado para %s", uf)
            return 0

        shp_path = os.path.join(tmpdir, shp_files[0])
        logger.info("  Lendo %s (%d bytes)...", shp_files[0], os.path.getsize(shp_path))

        gdf = gpd.read_file(shp_path)
        if gdf.empty:
            logger.warning("  Shapefile vazio para %s", uf)
            return 0

        # Converter para 4326 se necessario
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)

        # Carregar no PostGIS (append)
        gdf.to_postgis(table_name, engine, if_exists="append", index=False)
        logger.info("  %s: %d parcelas carregadas", uf, len(gdf))
        return len(gdf)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    include_snci = "--snci" in sys.argv
    ufs = [a for a in sys.argv[1:] if a != "--snci"]
    if "ALL" in ufs:
        ufs = ALL_UFS

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    # SIGEF
    logger.info("=== SIGEF - Parcelas Certificadas ===")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS sigef_parcelas"))
        conn.commit()

    total_sigef = 0
    for uf in ufs:
        uf = uf.upper()
        n = download_and_load(SIGEF_URL, "sigef_parcelas", uf, engine)
        total_sigef += n

    # Indices SIGEF
    with engine.connect() as conn:
        for sql in [
            "CREATE INDEX IF NOT EXISTS idx_sigef_geom ON sigef_parcelas USING GIST (geometry)",
            "CREATE INDEX IF NOT EXISTS idx_sigef_parcela ON sigef_parcelas (parcela_co)",
            "CREATE INDEX IF NOT EXISTS idx_sigef_codigo ON sigef_parcelas (codigo_imo)",
        ]:
            try:
                conn.execute(text(sql))
            except Exception:
                pass
        conn.commit()

    logger.info("SIGEF total: %s parcelas", f"{total_sigef:,}")

    # SNCI (opcional)
    if include_snci:
        logger.info("\n=== SNCI - Imoveis Certificados (pre-2013) ===")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS snci_imoveis"))
            conn.commit()

        total_snci = 0
        for uf in ufs:
            uf = uf.upper()
            n = download_and_load(SNCI_URL, "snci_imoveis", uf, engine)
            total_snci += n

        with engine.connect() as conn:
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_snci_geom ON snci_imoveis USING GIST (geometry)"))
                conn.commit()
            except Exception:
                pass

        logger.info("SNCI total: %s imoveis", f"{total_snci:,}")


if __name__ == "__main__":
    main()
