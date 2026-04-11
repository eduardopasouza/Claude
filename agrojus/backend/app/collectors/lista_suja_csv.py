"""Parser for Lista Suja (slave labour) CSV from Portal da Transparencia."""
import csv
import logging
from pathlib import Path

logger = logging.getLogger("agrojus.collectors.lista_suja_csv")

LISTA_SUJA_URL = "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo"


def parse_lista_suja_row(row: dict) -> dict:
    """Parse a single row from Lista Suja CSV."""
    def safe_int(val):
        try:
            return int(val) if val else 0
        except (ValueError, TypeError):
            return 0

    cpf_cnpj = row.get("CNPJ/CPF", "")
    cpf_cnpj_clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

    return {
        "year": safe_int(row.get("Ano da acao fiscal")),
        "state": row.get("UF", ""),
        "employer": row.get("Empregador", ""),
        "cpf_cnpj": cpf_cnpj_clean,
        "establishment": row.get("Estabelecimento", ""),
        "workers": safe_int(row.get("Trabalhadores envolvidos")),
        "cnae": row.get("CNAE", ""),
        "decision": row.get("Decisao administrativa", ""),
    }


def load_lista_suja_csv(filepath: Path) -> list[dict]:
    """Load and parse Lista Suja CSV."""
    records = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            records.append(parse_lista_suja_row(row))
    logger.info("Loaded %d Lista Suja records", len(records))
    return records


def search_by_cpf_cnpj(records: list[dict], cpf_cnpj: str) -> list[dict]:
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    return [r for r in records if r["cpf_cnpj"] == clean]


def search_by_state(records: list[dict], uf: str) -> list[dict]:
    return [r for r in records if r["state"].upper() == uf.upper()]
