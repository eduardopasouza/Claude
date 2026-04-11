"""Parser for IBAMA embargos CSV with coordinates."""
import csv
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("agrojus.collectors.ibama_csv")

IBAMA_CSV_URL = "https://dadosabertos.ibama.gov.br/dados/SICAFI/relatorio_auto_infracao_ibama_coords.csv"


def parse_ibama_csv_row(row: dict) -> dict:
    """Parse a single row from IBAMA CSV into normalized dict."""
    def safe_float(val):
        try:
            return float(val) if val else None
        except (ValueError, TypeError):
            return None

    return {
        "id": row.get("SEQ_AUTO_INFRACAO", ""),
        "auto_number": row.get("NUM_AUTO_INFRACAO", ""),
        "date": row.get("DAT_AUTO_INFRACAO", ""),
        "name": row.get("NOM_RAZAO_SOCIAL", ""),
        "cpf_cnpj": row.get("CPF_CNPJ", "").replace(".", "").replace("/", "").replace("-", ""),
        "description": row.get("DES_AUTO_INFRACAO", ""),
        "value": safe_float(row.get("VAL_AUTO_INFRACAO")),
        "municipality": row.get("DES_MUNICIPIO", ""),
        "state": row.get("SIG_UF", ""),
        "lat": safe_float(row.get("NUM_LATITUDE")),
        "lon": safe_float(row.get("NUM_LONGITUDE")),
    }


def load_ibama_csv(filepath: Path) -> list[dict]:
    """Load and parse entire IBAMA CSV file."""
    records = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            parsed = parse_ibama_csv_row(row)
            if parsed["lat"] and parsed["lon"]:
                records.append(parsed)
    logger.info("Loaded %d IBAMA records with coordinates", len(records))
    return records


def search_ibama_by_cpf_cnpj(records: list[dict], cpf_cnpj: str) -> list[dict]:
    """Search loaded records by CPF/CNPJ."""
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    return [r for r in records if r["cpf_cnpj"] == clean]


def search_ibama_by_municipality(records: list[dict], municipality: str, uf: str = "") -> list[dict]:
    """Search loaded records by municipality name."""
    name = municipality.lower()
    results = [r for r in records if name in r["municipality"].lower()]
    if uf:
        results = [r for r in results if r["state"].upper() == uf.upper()]
    return results
