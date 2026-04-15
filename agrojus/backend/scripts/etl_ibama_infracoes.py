"""
ETL para Autos de Infração do IBAMA.
Baixa o ZIP oficial com multas ambientais e insere no PostGIS.
URL: https://dadosabertos.ibama.gov.br/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip
"""

import csv
import io
import logging
import sys
import zipfile
from datetime import datetime, timezone

import httpx

csv.field_size_limit(sys.maxsize)

from app.models.database import get_session, EnvironmentalAlert

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

IBAMA_AI_URL = "https://dadosabertos.ibama.gov.br/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip"


def run():
    logger.info("=== ETL IBAMA Autos de Infração — Início ===")

    logger.info(f"Baixando {IBAMA_AI_URL}...")
    response = httpx.get(IBAMA_AI_URL, timeout=120.0, follow_redirects=True)
    response.raise_for_status()
    logger.info(f"Download concluído: {len(response.content)} bytes")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        csv_names = [n for n in zf.namelist() if n.endswith('.csv')]
        logger.info(f"Arquivos no ZIP: {zf.namelist()}")
        csv_name = csv_names[0]
        csv_raw = zf.read(csv_name).decode('latin-1')

    first_line = csv_raw.split('\n')[0]
    delimiter = ';' if ';' in first_line else ','
    logger.info(f"Cabeçalho: {first_line[:300]}")

    reader = csv.DictReader(io.StringIO(csv_raw), delimiter=delimiter)
    db = get_session()

    deleted = db.query(EnvironmentalAlert).filter(
        EnvironmentalAlert.source == "IBAMA_INFR"
    ).delete()
    logger.info(f"{deleted} infrações antigas deletadas.")

    count = 0
    batch = []
    BATCH_SIZE = 500

    for row in reader:
        cpf_cnpj = row.get("CPF_CNPJ_INFRATOR", "")
        if not cpf_cnpj:
            # Tentar NUM_PESSOA_INFRATOR como fallback
            cpf_cnpj = row.get("NUM_PESSOA_INFRATOR", "")
        cpf_cnpj = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "").strip() if cpf_cnpj else ""
        if not cpf_cnpj:
            continue

        municipio = row.get("MUNICIPIO", "")
        uf = row.get("UF", "")
        valor = row.get("VAL_AUTO_INFRACAO", "")
        nome = row.get("NOME_INFRATOR", "")
        num_ai = row.get("NUM_AUTO_INFRACAO", row.get("SEQ_AUTO_INFRACAO", ""))
        descricao = row.get("DES_AUTO_INFRACAO", "Infração Ambiental")

        raw = {
            "NUM_AI": num_ai,
            "NOME": nome,
            "CPF_CNPJ": cpf_cnpj,
            "MUNICIPIO": municipio,
            "UF": uf,
            "VALOR": valor,
            "DATA": row.get("DAT_AUTO_INFRACAO", row.get("DATA", "")),
        }

        record = EnvironmentalAlert(
            property_car_code=str(num_ai)[:100],
            cpf_cnpj=cpf_cnpj[:20],
            alert_type="infraction",
            source="IBAMA_INFR",
            description=f"Auto de Infração R${valor} ({nome}): {str(descricao)[:200]} — {municipio}/{uf}",
            raw_data=raw,
            created_at=datetime.now(timezone.utc),
        )
        batch.append(record)
        count += 1

        if len(batch) >= BATCH_SIZE:
            db.bulk_save_objects(batch)
            db.flush()
            batch = []
            if count % 5000 == 0:
                logger.info(f"  ... {count} registros processados")

    if batch:
        db.bulk_save_objects(batch)

    db.commit()
    db.close()
    logger.info(f"✔ Sucesso! {count} Autos de Infração do IBAMA indexados no PostGIS.")
    logger.info("=== ETL IBAMA Autos de Infração — Fim ===")


if __name__ == '__main__':
    run()
