"""
etl_mte_lista_suja_csv.py — Ingestao da Lista Suja de Trabalho Escravo (MTE)
via download direto de XLSX/CSV do Portal da Transparencia / dados.gov.br.
Substitui o parser de PDF (etl_mte_escravo.py) que era fragil.

Fontes tentadas em ordem:
1. dados.gov.br dataset trabalho-analogo-ao-de-escravo (CSV/XLSX)
2. Portal MTE download direto
3. Fallback: PDF parser existente
"""
import io
import logging
import os
import re
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
except ImportError:
    logger.error("Instale: pip install pandas sqlalchemy psycopg2-binary openpyxl")
    sys.exit(1)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")

# URLs em ordem de preferencia
SOURCES = [
    {
        "name": "Portal Transparencia - Download de Dados",
        "url": "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo",
        "type": "page",
    },
    {
        "name": "MTE Cadastro de Empregadores (PDF)",
        "url": "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/cadastro_de_empregadores.pdf",
        "type": "pdf",
    },
]

# Tentar buscar CSV/XLSX de trabalho escravo via search
SEARCH_URLS = [
    "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo/2024",
    "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo/2025",
    "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo/2026",
]


def try_portal_transparencia() -> pd.DataFrame | None:
    """Tenta baixar CSV do Portal da Transparencia."""
    for url in SEARCH_URLS:
        logger.info("Tentando Portal Transparencia: %s", url)
        try:
            r = httpx.get(url, timeout=60, follow_redirects=True, verify=False)
            logger.info("  HTTP %d — %d bytes — Content-Type: %s",
                       r.status_code, len(r.content), r.headers.get("content-type", "?"))
            if r.status_code == 200 and len(r.content) > 1000:
                ct = r.headers.get("content-type", "")
                if "zip" in ct or "octet" in ct or r.content[:2] == b"PK":
                    import zipfile
                    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                        for name in zf.namelist():
                            if name.endswith(".csv"):
                                with zf.open(name) as f:
                                    df = pd.read_csv(f, sep=";", encoding="latin-1")
                                    logger.info("  CSV: %d linhas, colunas: %s", len(df), list(df.columns))
                                    return df
                            elif name.endswith(".xlsx"):
                                with zf.open(name) as f:
                                    df = pd.read_excel(io.BytesIO(f.read()))
                                    logger.info("  XLSX: %d linhas, colunas: %s", len(df), list(df.columns))
                                    return df
                elif "csv" in ct or "text" in ct:
                    df = pd.read_csv(io.BytesIO(r.content), sep=";", encoding="latin-1")
                    logger.info("  CSV direto: %d linhas", len(df))
                    return df
        except Exception as exc:
            logger.warning("  Falha: %s", exc)
    return None


def try_ceis_api() -> pd.DataFrame | None:
    """Tenta API CEIS do Portal da Transparencia (empresas inidoneas — complementar)."""
    logger.info("Tentando API CEIS (Cadastro de Empresas Inidoneas)...")
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/ceis"
    params = {"pagina": 1, "tamanhoPagina": 500}
    # API requer chave — pular se nao tiver
    logger.info("  API CEIS requer chave de acesso — pulando")
    return None


def try_dados_gov_br() -> pd.DataFrame | None:
    """Tenta dados.gov.br dataset de trabalho escravo."""
    logger.info("Tentando dados.gov.br...")
    # Buscar no CKAN
    search_url = "https://dados.gov.br/api/3/action/package_search?q=trabalho+escravo"
    try:
        r = httpx.get(search_url, timeout=30, verify=False)
        if r.status_code == 200:
            data = r.json()
            results = data.get("result", {}).get("results", [])
            for ds in results:
                for res in ds.get("resources", []):
                    res_url = res.get("url", "")
                    if res_url and (res_url.endswith(".csv") or res_url.endswith(".xlsx")):
                        logger.info("  Recurso encontrado: %s", res_url)
                        r2 = httpx.get(res_url, timeout=60, follow_redirects=True, verify=False)
                        if r2.status_code == 200 and len(r2.content) > 500:
                            if res_url.endswith(".csv"):
                                return pd.read_csv(io.BytesIO(r2.content), sep=";", encoding="latin-1")
                            else:
                                return pd.read_excel(io.BytesIO(r2.content))
        else:
            logger.info("  dados.gov.br API retornou %d", r.status_code)
    except Exception as exc:
        logger.warning("  dados.gov.br falhou: %s", exc)
    return None


def parse_existing_pdf_data() -> pd.DataFrame | None:
    """Reaproveita dados ja carregados na tabela environmental_alerts (MTE)."""
    logger.info("Verificando dados existentes no PostGIS (do parser PDF anterior)...")
    engine = create_engine(DATABASE_URL)
    try:
        df = pd.read_sql(
            "SELECT cpf_cnpj, description, raw_data, created_at FROM environmental_alerts WHERE source = 'MTE'",
            engine,
        )
        if len(df) > 0:
            logger.info("  %d registros MTE ja existentes no banco", len(df))
            return df
    except Exception as exc:
        logger.warning("  Falha ao ler banco: %s", exc)
    return None


def load_to_db(df: pd.DataFrame, source_name: str):
    """Salva dados MTE na tabela dedicada."""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS mte_lista_suja CASCADE"))
        conn.commit()

    df.to_sql("mte_lista_suja", engine, if_exists="replace", index=True)
    logger.info("OK %d registros -> mte_lista_suja (fonte: %s)", len(df), source_name)


if __name__ == "__main__":
    logger.info("=== ETL MTE Lista Suja (CSV/XLSX) ===")

    df = try_portal_transparencia()
    if df is not None and len(df) > 0:
        load_to_db(df, "portal_transparencia")
        sys.exit(0)

    df = try_dados_gov_br()
    if df is not None and len(df) > 0:
        load_to_db(df, "dados_gov_br")
        sys.exit(0)

    # Fallback: usar dados ja existentes do parser PDF
    df = parse_existing_pdf_data()
    if df is not None and len(df) > 0:
        logger.info("Mantendo %d registros existentes do parser PDF", len(df))
    else:
        logger.error("Nenhuma fonte retornou dados. Lista Suja nao atualizada.")
