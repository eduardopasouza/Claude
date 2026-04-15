"""
etl_sicar_bigquery.py — Baixa CARs do BigQuery BasedosDados para PostGIS local.

Fonte: basedosdados.br_sfb_sicar.area_imovel (79.3M registros, set/2025)
Destino: tabela sicar_completo no PostGIS

Uso:
    # Baixar MA
    docker exec agrojus-backend-1 python scripts/etl_sicar_bigquery.py MA

    # Baixar multiplas UFs
    docker exec agrojus-backend-1 python scripts/etl_sicar_bigquery.py MA MT PA GO TO MS

    # Baixar TODAS as UFs (79.3M, ~2-4h)
    docker exec agrojus-backend-1 python scripts/etl_sicar_bigquery.py ALL
"""

import sys
import time
import logging

from google.cloud import bigquery
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://agrojus:agrojus@db:5432/agrojus"
BQ_TABLE = "`basedosdados.br_sfb_sicar.area_imovel`"
PAGE_SIZE = 50000

ALL_UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
    "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
    "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]


def ensure_table(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sicar_completo (
                cod_imovel TEXT PRIMARY KEY,
                status_imovel TEXT,
                data_atualizacao TEXT,
                area DOUBLE PRECISION,
                condicao TEXT,
                uf TEXT,
                cod_municipio_ibge TEXT,
                m_fiscal DOUBLE PRECISION,
                tipo_imovel TEXT,
                geometry GEOMETRY(GEOMETRY, 4326)
            )
        """))
        conn.commit()


def ensure_indices(engine):
    with engine.connect() as conn:
        for sql in [
            "CREATE INDEX IF NOT EXISTS idx_sicar_geom ON sicar_completo USING GIST (geometry)",
            "CREATE INDEX IF NOT EXISTS idx_sicar_uf ON sicar_completo (uf)",
            "CREATE INDEX IF NOT EXISTS idx_sicar_cod ON sicar_completo (cod_imovel)",
            "CREATE INDEX IF NOT EXISTS idx_sicar_mun ON sicar_completo (cod_municipio_ibge)",
            "CREATE INDEX IF NOT EXISTS idx_sicar_status ON sicar_completo (status_imovel)",
        ]:
            conn.execute(text(sql))
        conn.commit()


def download_uf(client, engine, uf: str):
    """Baixa todos os CARs de uma UF por paginas."""
    t0 = time.time()
    offset = 0
    total = 0

    logger.info("Baixando %s...", uf)

    while True:
        query = f"""
        SELECT id_imovel, status, CAST(data_atualizacao_car AS STRING) as data_at,
               area, condicao, sigla_uf, id_municipio,
               SAFE_CAST(modulos_fiscais AS FLOAT64) as mf, tipo,
               ST_ASTEXT(geometria) as wkt
        FROM {BQ_TABLE}
        WHERE sigla_uf = '{uf}'
        ORDER BY id_imovel
        LIMIT {PAGE_SIZE} OFFSET {offset}
        """
        rows = list(client.query(query).result())
        if not rows:
            break

        batch = [
            {
                "cod": r.id_imovel, "status": r.status, "data_at": r.data_at,
                "area": r.area, "cond": r.condicao, "uf": r.sigla_uf,
                "mun": r.id_municipio, "mf": r.mf, "tipo": r.tipo, "wkt": r.wkt,
            }
            for r in rows if r.wkt
        ]

        if batch:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO sicar_completo
                    (cod_imovel, status_imovel, data_atualizacao, area, condicao,
                     uf, cod_municipio_ibge, m_fiscal, tipo_imovel, geometry)
                    VALUES (:cod, :status, :data_at, :area, :cond,
                            :uf, :mun, :mf, :tipo, ST_GeomFromText(:wkt, 4326))
                    ON CONFLICT (cod_imovel) DO NOTHING
                """), batch)
                conn.commit()

        total += len(batch)
        offset += PAGE_SIZE
        elapsed = time.time() - t0
        rate = total / elapsed if elapsed > 0 else 0
        logger.info("  %s: %s CARs (%s lidos) | %.0f/s | %.0fs",
                     uf, f"{total:,}", f"{offset:,}", rate, elapsed)

        if len(rows) < PAGE_SIZE:
            break

    elapsed = time.time() - t0
    logger.info("  %s COMPLETO: %s CARs em %.0fs", uf, f"{total:,}", elapsed)
    return total


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    ufs = sys.argv[1:]
    if "ALL" in ufs:
        ufs = ALL_UFS

    client = bigquery.Client(project="agrojus")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    ensure_table(engine)

    grand_total = 0
    t0 = time.time()

    for uf in ufs:
        uf = uf.upper()
        if uf not in ALL_UFS:
            logger.warning("UF invalida: %s", uf)
            continue

        # Verificar se ja tem dados desta UF
        with engine.connect() as conn:
            existing = conn.execute(
                text("SELECT COUNT(*) FROM sicar_completo WHERE uf = :uf"),
                {"uf": uf},
            ).scalar()
            if existing and existing > 0:
                logger.info("  %s: ja tem %s CARs, pulando", uf, f"{existing:,}")
                grand_total += existing
                continue

        n = download_uf(client, engine, uf)
        grand_total += n

    ensure_indices(engine)

    elapsed = time.time() - t0
    logger.info("=== TOTAL: %s CARs de %d UFs em %.0fs ===", f"{grand_total:,}", len(ufs), elapsed)

    # Stats
    with engine.connect() as conn:
        by_uf = conn.execute(text(
            "SELECT uf, COUNT(*) as n FROM sicar_completo GROUP BY uf ORDER BY n DESC"
        )).fetchall()
        for uf, n in by_uf:
            logger.info("  %s: %s", uf, f"{n:,}")


if __name__ == "__main__":
    main()
