"""
Download + ETL do CSV oficial de Autos de Infração IBAMA (dados abertos).

Fonte:
  https://dadosabertos.ibama.gov.br/dados/SICAFI/relatorio_auto_infracao_ibama_coords.csv

Esse é um CSV gigante (~200MB, ~1.2M autos de infração) com coordenadas.
Carrega em duas tabelas:
  - geo_autos_ibama     (pontos, para camada de mapa)
  - environmental_alerts (relacional, para busca por CPF/CNPJ)

Uso:
  docker compose exec backend python scripts/download_ibama_autos.py

Performance: primeira execução ~2-3 min (download + COPY). Re-execução é idempotente.

Schema geo_autos_ibama:
  id             serial primary key
  seq_auto       varchar(20)
  num_auto       varchar(30) unique
  data           date
  nome           text
  cpf_cnpj       varchar(20)
  descricao      text
  valor          numeric
  municipio      varchar(200)
  uf             varchar(2)
  latitude       double precision
  longitude      double precision
  geometry       geometry(Point, 4326)
"""
from __future__ import annotations

import argparse
import csv
import io
import logging
import sys
from pathlib import Path

import httpx
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ibama_csv")

IBAMA_CSV_URL = (
    "https://dadosabertos.ibama.gov.br/dados/SIFISC/"
    "auto_infracao/auto_infracao/auto_infracao_csv.zip"
)
# Nota: em abr/2026 IBAMA migrou SICAFI → SIFISC e o CSV virou ZIP.
# O script precisa extrair o zip antes de parsear.


DDL = """
CREATE TABLE IF NOT EXISTS geo_autos_ibama (
    id SERIAL PRIMARY KEY,
    seq_auto VARCHAR(20),
    num_auto VARCHAR(30) UNIQUE,
    data_auto DATE,
    nome TEXT,
    cpf_cnpj VARCHAR(20),
    descricao TEXT,
    valor NUMERIC,
    municipio VARCHAR(200),
    uf VARCHAR(2),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geometry geometry(Point, 4326)
);

CREATE INDEX IF NOT EXISTS idx_autos_ibama_cpf
    ON geo_autos_ibama (cpf_cnpj);
CREATE INDEX IF NOT EXISTS idx_autos_ibama_uf_municipio
    ON geo_autos_ibama (uf, municipio);
CREATE INDEX IF NOT EXISTS idx_autos_ibama_geom
    ON geo_autos_ibama USING GIST (geometry);
"""


def parse_row(row: dict) -> dict | None:
    """Parse uma linha do CSV IBAMA. Retorna None se inválida."""

    def sf(v):
        try:
            return float(str(v).replace(",", ".")) if v else None
        except (ValueError, TypeError):
            return None

    lat = sf(row.get("NUM_LATITUDE_AUTO"))
    lon = sf(row.get("NUM_LONGITUDE_AUTO"))
    if lat is None or lon is None or not (-90 <= lat <= 90 and -180 <= lon <= 0):
        return None

    num_auto = (row.get("NUM_AUTO_INFRACAO") or "").strip()
    if not num_auto:
        return None

    return {
        "seq_auto": (row.get("SEQ_AUTO_INFRACAO") or "").strip()[:20],
        "num_auto": num_auto[:30],
        "data_auto": (row.get("DAT_AUTO_INFRACAO") or "").strip()[:10] or None,
        "nome": (row.get("NOME_INFRATOR") or "").strip()[:500],
        "cpf_cnpj": (row.get("CPF_CNPJ_INFRATOR") or "")
        .replace(".", "")
        .replace("/", "")
        .replace("-", "")
        .strip()[:20],
        "descricao": (row.get("DES_AUTO_INFRACAO") or "")[:2000],
        "valor": sf(row.get("VAL_AUTO_INFRACAO")),
        "municipio": (row.get("MUNICIPIO") or "").strip()[:200],
        "uf": (row.get("UF") or "").strip()[:2].upper(),
        "latitude": lat,
        "longitude": lon,
    }


def download_csv(target: Path) -> Path:
    """Baixa o ZIP do IBAMA, extrai o CSV principal."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        logger.info("CSV já existe em %s (%.1f MB) — reutilizando", target, target.stat().st_size / 1e6)
        return target

    zip_path = target.with_suffix(".zip")
    logger.info("Baixando %s → %s", IBAMA_CSV_URL, zip_path)
    with httpx.stream("GET", IBAMA_CSV_URL, timeout=600.0, follow_redirects=True) as r:
        r.raise_for_status()
        total = 0
        with zip_path.open("wb") as f:
            for chunk in r.iter_bytes(chunk_size=1024 * 1024):
                f.write(chunk)
                total += len(chunk)
                if total % (25 * 1024 * 1024) < 1024 * 1024:
                    logger.info("  %.0f MB baixados...", total / 1e6)
    logger.info("Download completo: %.1f MB", zip_path.stat().st_size / 1e6)

    # Extrair CSV do ZIP
    import zipfile
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_files = [n for n in zf.namelist() if n.endswith(".csv")]
        if not csv_files:
            raise RuntimeError(f"ZIP {zip_path} não contém CSV")
        main_csv = max(csv_files, key=lambda n: zf.getinfo(n).file_size)
        logger.info("Extraindo %s do ZIP (%.1f MB)", main_csv, zf.getinfo(main_csv).file_size / 1e6)
        with zf.open(main_csv) as src, target.open("wb") as dst:
            import shutil
            shutil.copyfileobj(src, dst, length=1024 * 1024)
    logger.info("Extraído: %s (%.1f MB)", target, target.stat().st_size / 1e6)
    zip_path.unlink()  # economiza espaço
    return target


def load_csv(db_url: str, csv_path: Path, batch_size: int = 5000) -> int:
    """Carrega CSV em geo_autos_ibama com UPSERT + ST_SetSRID."""
    engine = create_engine(db_url)

    with engine.begin() as conn:
        for stmt in DDL.split(";"):
            s = stmt.strip()
            if s:
                conn.execute(text(s + ";"))
        logger.info("DDL aplicado")

    insert_sql = text(
        """
        INSERT INTO geo_autos_ibama (
            seq_auto, num_auto, data_auto, nome, cpf_cnpj,
            descricao, valor, municipio, uf,
            latitude, longitude, geometry
        ) VALUES (
            :seq_auto, :num_auto,
            NULLIF(:data_auto, '')::date, :nome, :cpf_cnpj,
            :descricao, :valor, :municipio, :uf,
            :latitude, :longitude,
            ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)
        )
        ON CONFLICT (num_auto) DO NOTHING
        """
    )

    total_inserted = 0
    batch: list[dict] = []

    # Tentar vários encodings comuns do IBAMA
    for encoding in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        try:
            f = csv_path.open("r", encoding=encoding)
            # Testar leitura das primeiras linhas
            reader = csv.DictReader(f, delimiter=";")
            _ = reader.fieldnames
            break
        except (UnicodeDecodeError, UnicodeError):
            f.close()
            continue
    else:
        raise RuntimeError("Não conseguiu detectar encoding do CSV")

    logger.info("Encoding detectado: %s, cabeçalhos: %s", encoding, reader.fieldnames)

    with engine.begin() as conn:
        row_count = 0
        for row in reader:
            row_count += 1
            parsed = parse_row(row)
            if parsed:
                batch.append(parsed)
            if len(batch) >= batch_size:
                conn.execute(insert_sql, batch)
                total_inserted += len(batch)
                if total_inserted % 50000 == 0:
                    logger.info(
                        "  %d inseridos (de %d lidos)", total_inserted, row_count
                    )
                batch.clear()
        if batch:
            conn.execute(insert_sql, batch)
            total_inserted += len(batch)

    f.close()
    logger.info("Total inseridos: %d de %d lidos", total_inserted, row_count)
    return total_inserted


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skip-download", action="store_true")
    p.add_argument("--db-url", default=None, help="DATABASE_URL override")
    p.add_argument("--data-dir", default="/app/data")
    args = p.parse_args()

    db_url = args.db_url
    if not db_url:
        import os

        db_url = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")

    csv_path = Path(args.data_dir) / "ibama_autos_infracao.csv"
    if not args.skip_download:
        download_csv(csv_path)

    if not csv_path.exists():
        logger.error("CSV não encontrado: %s", csv_path)
        sys.exit(1)

    inserted = load_csv(db_url, csv_path)
    logger.info("✅ Concluído. %d autos de infração IBAMA carregados.", inserted)


if __name__ == "__main__":
    main()
