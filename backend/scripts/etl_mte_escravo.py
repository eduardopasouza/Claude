"""
ETL — Cadastro de Empregadores MTE (Lista Suja de Trabalho Escravo)
Estratégia: extract_text() página a página + parser linha-por-linha por regex.
O parser extract_tables() do pdfplumber falha em tabelas multi-página deste PDF.
"""
import os
import re
import httpx
import pdfplumber
import logging
from datetime import datetime, timezone

from app.models.database import get_session, EnvironmentalAlert

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MTE_PDF_URL = (
    "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho"
    "/areas-de-atuacao/cadastro_de_empregadores.pdf"
)
DATA_DIR = "/app/data"
PDF_PATH = os.path.join(DATA_DIR, "mte_trabalho_escravo.pdf")

# ──────────────────────────────────────────────────────────────────────────────
# Padrões de documento
# CPF:  000.000.000-00  ou  00000000000
# CNPJ: 00.000.000/0000-00  ou  00000000000000
# ──────────────────────────────────────────────────────────────────────────────
_CPF_RE  = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
_CNPJ_RE = re.compile(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b')

# Linha de dado tem estrutura:
#   <ID> <ANO?> <UF?> <NOME_EMPREGADOR> <CPF_ou_CNPJ> <ESTABELECIMENTO> ...
# O ID numérico no início é o marcador mais confiável.
_ROW_START = re.compile(r'^\s*(\d{1,5})\s+')

# UF brasileiras
_UF_RE = re.compile(
    r'\b(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b'
)


def fetch_pdf() -> bool:
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(PDF_PATH):
        size = os.path.getsize(PDF_PATH)
        logger.info("PDF já existe localmente (%.1f KB) — pulando download.", size / 1024)
        return True

    logger.info("Baixando Cadastro de Empregadores MTE…")
    try:
        with httpx.stream(
            "GET", MTE_PDF_URL, timeout=60.0, follow_redirects=True, verify=False
        ) as r:
            r.raise_for_status()
            with open(PDF_PATH, "wb") as f:
                for chunk in r.iter_bytes(chunk_size=65536):
                    f.write(chunk)
        logger.info("PDF baixado: %.1f KB", os.path.getsize(PDF_PATH) / 1024)
        return True
    except Exception as exc:
        logger.error("Falha no download: %s", exc)
        return False


def _extract_doc(text: str) -> str | None:
    """Extrai o primeiro CPF ou CNPJ encontrado num trecho de texto."""
    m = _CNPJ_RE.search(text) or _CPF_RE.search(text)
    return m.group() if m else None


def _clean_doc(raw: str) -> str:
    return re.sub(r'[\.\-/]', '', raw).strip()


def _extract_uf(text: str) -> str:
    m = _UF_RE.search(text)
    return m.group() if m else ""


def _extract_workers(text: str) -> str:
    """Extrai qty de trabalhadores (número isolado após o doc, antes do CNAE)."""
    m = re.search(r'\b(\d{1,4})\s+\d{4}-\d{1}/\d{2}', text)  # N° antes do CNAE
    return m.group(1) if m else "N/A"


def _extract_year(text: str) -> str:
    m = re.search(r'\b(20\d{2})\b', text)
    return m.group() if m else ""


def parse_pdf() -> list[dict]:
    """
    Percorre o PDF página a página usando texto bruto.
    Cada registro começa com um ID numérico na primeira coluna.
    Linhas de continuação (sem ID) são agregadas ao registro anterior.
    """
    records: list[dict] = []
    current: dict | None = None
    seen_ids: set[str] = set()

    with pdfplumber.open(PDF_PATH) as pdf:
        logger.info("PDF aberto — %d páginas.", len(pdf.pages))

        for page_num, page in enumerate(pdf.pages, start=1):
            raw = page.extract_text(layout=False) or ""
            lines = raw.splitlines()

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Detecta início de nova linha de dado pelo ID numérico
                m_start = _ROW_START.match(line)
                if m_start:
                    row_id = m_start.group(1)

                    # Salva o registro anterior se tiver documento
                    if current and current.get("doc"):
                        if current["id"] not in seen_ids:
                            records.append(current)
                            seen_ids.add(current["id"])

                    current = {"id": row_id, "text": line, "page": page_num}
                    doc = _extract_doc(line)
                    if doc:
                        current["doc"] = doc
                else:
                    # Linha de continuação: agrega ao registro atual
                    if current:
                        current["text"] = current["text"] + " " + line
                        if not current.get("doc"):
                            doc = _extract_doc(line)
                            if doc:
                                current["doc"] = doc

            logger.info("  Página %d/%d — %d registros acumulados", page_num, len(pdf.pages), len(records))

    # Salva o último registro
    if current and current.get("doc") and current["id"] not in seen_ids:
        records.append(current)

    return records


def build_alert(rec: dict) -> EnvironmentalAlert | None:
    raw_doc  = rec.get("doc", "")
    if not raw_doc:
        return None

    doc_clean = _clean_doc(raw_doc)
    text      = rec.get("text", "")
    uf        = _extract_uf(text)
    workers   = _extract_workers(text)
    year      = _extract_year(text)

    # Empregador: tudo entre o ID e o documento, sem o UF e o ano
    before_doc = text[: text.find(raw_doc)].strip()
    empregador_raw = re.sub(r'^\d+\s+', '', before_doc)     # remove ID
    empregador_raw = re.sub(r'\b20\d{2}\b', '', empregador_raw)  # remove ano
    empregador_raw = _UF_RE.sub('', empregador_raw).strip()

    # Estabelecimento: tudo após o documento (até o CNAE ou fim)
    after_doc  = text[text.find(raw_doc) + len(raw_doc):].strip()
    # Corta no padrão CNAE (4 dígitos - 1 dígito / 2 dígitos)
    cnae_match = re.search(r'\d{4}-\d/\d{2}', after_doc)
    estabelecimento = after_doc[: cnae_match.start()].strip() if cnae_match else after_doc[:120].strip()

    desc = (
        f"Trabalho Análogo à Escravidão — {empregador_raw} | "
        f"Trabalhadores: {workers} | {uf} | Ano: {year}"
    )

    return EnvironmentalAlert(
        property_car_code="N/A",
        cpf_cnpj=doc_clean,
        alert_type="trabalho_escravo",
        source="MTE",
        description=desc,
        raw_data={
            "id": rec["id"],
            "empregador": empregador_raw,
            "estabelecimento": estabelecimento,
            "cpf_cnpj_original": raw_doc,
            "trabalhadores": workers,
            "uf": uf,
            "ano": year,
            "pagina_pdf": rec.get("page"),
        },
        created_at=datetime.now(timezone.utc),
    )


def run_etl():
    if not fetch_pdf():
        logger.error("PDF não disponível — abortando ETL.")
        return

    logger.info("Iniciando parsing do PDF…")
    records = parse_pdf()
    logger.info("Parsing concluído: %d registros brutos encontrados.", len(records))

    db = get_session()
    try:
        # Apaga registros antigos do MTE
        deleted = db.query(EnvironmentalAlert).filter(
            EnvironmentalAlert.source == "MTE"
        ).delete()
        logger.info("%d registros antigos MTE removidos.", deleted)

        inserted = 0
        skipped  = 0
        for rec in records:
            alert = build_alert(rec)
            if alert:
                db.add(alert)
                inserted += 1
            else:
                skipped += 1

        db.commit()
        logger.info(
            "✅ ETL MTE concluído — %d inseridos, %d ignorados (sem doc).",
            inserted, skipped
        )
    except Exception as exc:
        db.rollback()
        logger.error("Erro ao inserir no banco: %s", exc)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_etl()
