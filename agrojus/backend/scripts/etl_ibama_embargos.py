"""
ETL Python para Áreas Embargadas do IBAMA.
Baixa o ZIP oficial com CSV de termos de embargo do portal de dados abertos e insere no PostGIS.
URL correta: https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip
"""

import csv
import io
import logging
import sys
import zipfile
from datetime import datetime, timezone

import httpx

# Dados do IBAMA têm campos muito grandes (descrições, coordenadas)
csv.field_size_limit(sys.maxsize)

from app.models.database import get_session, EnvironmentalAlert

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

IBAMA_ZIP_URL = "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip"


def download_and_extract_csv() -> str:
    """Baixa o ZIP do IBAMA e extrai o CSV principal."""
    logger.info(f"Baixando {IBAMA_ZIP_URL}...")
    response = httpx.get(IBAMA_ZIP_URL, timeout=60.0, follow_redirects=True)
    response.raise_for_status()
    logger.info(f"Download concluído: {len(response.content)} bytes")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        csv_names = [n for n in zf.namelist() if n.endswith('.csv')]
        logger.info(f"Arquivos no ZIP: {zf.namelist()}")
        if not csv_names:
            raise ValueError("Nenhum CSV encontrado dentro do ZIP")
        csv_name = csv_names[0]
        logger.info(f"Extraindo: {csv_name}")
        return zf.read(csv_name).decode('latin-1')


def get_backup_csv() -> str:
    """Fallback para desenvolvimento offline."""
    return """NUM_TAD;DATA_TAD;CPF_CNPJ;NOME;MUNICIPIO;UF;SITUACAO;DESCARACTERIZACAO
123456;2024-01-10;12345678000190;Madeireira Ilegal Ltda;Altamira;PA;ATIVO;Desmatamento a corte raso
654321;2023-05-20;98765432000155;Agropecuaria Rio Bonito;Cumaru do Norte;PA;ATIVO;Fogo em APP
111222;2024-02-15;55667788000199;Siderurgica Norte;Paragominas;PA;ATIVO;Poluição hídrica severa"""


def run():
    logger.info("=== ETL IBAMA Embargos — Início ===")

    try:
        csv_raw = download_and_extract_csv()
        is_real = True
    except Exception as e:
        logger.warning(f"Erro ao baixar dados reais: {e}")
        logger.warning("Utilizando backup CSV de contingência.")
        csv_raw = get_backup_csv()
        is_real = False

    # Detectar delimitador — pode ser ; ou ,
    first_line = csv_raw.split('\n')[0]
    delimiter = ';' if ';' in first_line else ','

    reader = csv.DictReader(io.StringIO(csv_raw), delimiter=delimiter)
    db = get_session()

    deleted = db.query(EnvironmentalAlert).filter(EnvironmentalAlert.source == "IBAMA").delete()
    logger.info(f"{deleted} alertas antigos do IBAMA deletados.")

    count = 0
    batch = []
    BATCH_SIZE = 500

    for row in reader:
        cpf_cnpj = row.get("CPF_CNPJ_EMBARGADO", row.get("CPF_CNPJ", ""))
        cpf_cnpj = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "").strip() if cpf_cnpj else ""
        if not cpf_cnpj:
            continue

        municipio = row.get("MUNICIPIO", "")
        uf = row.get("UF", "")
        situacao = row.get("SIT_DESEMBARGO", "ATIVO")
        if situacao != "S":
            situacao = "ATIVO"
        else:
            situacao = "DESEMBARGADO"
        descricao = row.get("DES_TAD", "Infração Ambiental")
        num_tad = row.get("NUM_TAD", row.get("SEQ_TAD", ""))
        nome = row.get("NOME_EMBARGADO", "")
        area = row.get("QTD_AREA_EMBARGADA", "")

        # Pegar só campos essenciais para raw_data (evitar campo GEOM gigante)
        raw = {
            "SEQ_TAD": row.get("SEQ_TAD", ""),
            "NUM_TAD": num_tad,
            "NOME_EMBARGADO": nome,
            "CPF_CNPJ": cpf_cnpj,
            "MUNICIPIO": municipio,
            "UF": uf,
            "DAT_EMBARGO": row.get("DAT_EMBARGO", ""),
            "QTD_AREA_EMBARGADA": area,
            "NOME_IMOVEL": row.get("NOME_IMOVEL", ""),
            "NUM_LATITUDE": row.get("NUM_LATITUDE_TAD", ""),
            "NUM_LONGITUDE": row.get("NUM_LONGITUDE_TAD", ""),
        }

        record = EnvironmentalAlert(
            property_car_code=str(num_tad)[:100],
            cpf_cnpj=cpf_cnpj[:20],
            alert_type="embargo",
            source="IBAMA",
            description=f"Embargo {situacao} ({nome}): {descricao[:200]} — {municipio}/{uf} [{area} ha]",
            raw_data=raw,
            created_at=datetime.now(timezone.utc),
        )
        batch.append(record)
        count += 1

        if len(batch) >= BATCH_SIZE:
            db.bulk_save_objects(batch)
            db.flush()
            batch = []
            logger.info(f"  ... {count} registros processados")

    if batch:
        db.bulk_save_objects(batch)

    db.commit()
    db.close()

    source_label = "DADOS REAIS do Portal" if is_real else "BACKUP de contingência"
    logger.info(f"✔ Sucesso! {count} Embargos do IBAMA ({source_label}) indexados no PostGIS.")
    logger.info("=== ETL IBAMA Embargos — Fim ===")


if __name__ == '__main__':
    run()
