"""
etl_sicor_bcb.py — Ingestão de operações de Crédito Rural (SICOR/BCB)
Fonte: OData API pública do Banco Central
Endpoint: https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata

Tabela destino: rural_credits
Campos: id, ano_referencia, uf, municipio_ibge, nivelidade, programa,
        modalidade, produto, area_ha, valor_contratado, valor_parcela, data_emissao
"""
import logging
import os
from datetime import datetime, timezone

import httpx
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Date, BigInteger, text
)
from sqlalchemy.orm import declarative_base, sessionmaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
Base = declarative_base()

# ─── OData endpoint do BCB/SICOR ─────────────────────────────────────────────
SICOR_ODATA = "https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata"
PAGE_SIZE = 1000
MAX_PAGES = 100   # máx 100k registros por execução

# Recursos disponíveis no SICOR OData
ENDPOINTS = {
    "contratos": "MCR_EMPR",           # Empreendimentos de Crédito Rural
    "operacoes":  "MCR_OPER_COMP",     # Operações completas
    "municipios": "MCR_MUN_EMPR",      # Por município
}


class RuralCredit(Base):
    __tablename__ = "rural_credits"
    id               = Column(Integer, primary_key=True, autoincrement=True)
    ref_bacen        = Column(BigInteger)      # referência BCB
    ano_ref          = Column(Integer)
    uf               = Column(String(2))
    cod_municipio    = Column(String(7))
    municipio        = Column(String(100))
    programa         = Column(String(80))     # PRONAF, PRONAMP, Invest...
    modalidade       = Column(String(80))
    produto          = Column(String(80))     # Soja, Milho, Bovinos...
    atividade        = Column(String(40))     # custeio, investimento, comercialização
    area_ha          = Column(Float)
    qt_animais       = Column(Integer)
    valor_contrato   = Column(Float)
    taxa_juros       = Column(Float)
    data_emissao     = Column(Date)
    data_vencimento  = Column(Date)
    fonte_recurso    = Column(String(80))


def setup_db():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def fetch_sicor_page(client: httpx.Client, endpoint: str, skip: int) -> list[dict]:
    """Busca uma página de dados do OData SICOR."""
    url = f"{SICOR_ODATA}/{endpoint}"
    params = {
        "$top": PAGE_SIZE,
        "$skip": skip,
        "$format": "json",
    }
    try:
        r = client.get(url, params=params, timeout=30)
        if r.status_code != 200:
            logger.warning("HTTP %d no endpoint %s skip=%d", r.status_code, endpoint, skip)
            return []
        data = r.json()
        return data.get("value", [])
    except Exception as e:
        logger.warning("Erro SICOR [%s skip=%d]: %s", endpoint, skip, e)
        return []


def parse_contrato(row: dict) -> dict:
    def safe_float(v):
        try: return float(str(v).replace(",", "."))
        except: return None

    def safe_date(v):
        if not v: return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"):
            try: return datetime.strptime(str(v)[:19], fmt).date()
            except: continue
        return None

    return {
        "ref_bacen":       row.get("RefBacen"),
        "ano_ref":         row.get("AnoReferencia"),
        "uf":              str(row.get("Uf") or row.get("SiglaUF") or "")[:2],
        "cod_municipio":   str(row.get("CodMunicipio") or "")[:7],
        "municipio":       str(row.get("NomeMunicipio") or "")[:100],
        "programa":        str(row.get("NomePrograma") or "")[:80],
        "modalidade":      str(row.get("NomeModalidade") or "")[:80],
        "produto":         str(row.get("NomeProduto") or row.get("Produto") or "")[:80],
        "atividade":       str(row.get("NomeAtividade") or row.get("Atividade") or "")[:40],
        "area_ha":         safe_float(row.get("AreaFinanciadaHa") or row.get("Area")),
        "qt_animais":      row.get("QtdeAnimais"),
        "valor_contrato":  safe_float(row.get("ValorContrato") or row.get("Valor")),
        "taxa_juros":      safe_float(row.get("TaxaJuros") or row.get("Taxa")),
        "data_emissao":    safe_date(row.get("DataEmissao") or row.get("DtEmissao")),
        "data_vencimento": safe_date(row.get("DataVencimento") or row.get("DtVencimento")),
        "fonte_recurso":   str(row.get("NomeFonteRecurso") or row.get("FonteRecurso") or "")[:80],
    }


def list_sicor_resources(client: httpx.Client) -> list[str]:
    """Descobre recursos disponíveis no OData SICOR."""
    try:
        r = client.get(f"{SICOR_ODATA}?$format=json", timeout=15)
        if r.status_code == 200:
            data = r.json()
            resources = [v["name"] for v in data.get("value", [])]
            logger.info("Recursos SICOR disponíveis: %s", resources)
            return resources
    except Exception as e:
        logger.warning("Não foi possível listar recursos: %s", e)
    return []


def main():
    logger.info("=== ETL SICOR / BCB — Crédito Rural ===")
    session = setup_db()

    with httpx.Client(verify=False, follow_redirects=True,
                      headers={"User-Agent": "AgroJus/1.0"}) as client:

        # Descobre endpoints disponíveis
        resources = list_sicor_resources(client)
        if not resources:
            logger.warning("SICOR OData não listou recursos. Tentando endpoint padrão...")
            resources = ["MCR_EMPR"]

        total_saved = 0
        for resource in resources[:2]:  # máx 2 recursos por execução
            logger.info("Ingerindo recurso: %s", resource)
            skip = 0
            pages = 0

            while pages < MAX_PAGES:
                rows = fetch_sicor_page(client, resource, skip)
                if not rows:
                    logger.info("  Fim do recurso %s em skip=%d", resource, skip)
                    break

                batch = []
                for row in rows:
                    parsed = parse_contrato(row)
                    if parsed.get("ref_bacen") or parsed.get("valor_contrato"):
                        batch.append(RuralCredit(**{
                            k: v for k, v in parsed.items() if v is not None
                        }))

                if batch:
                    session.bulk_save_objects(batch)
                    session.flush()
                    total_saved += len(batch)

                logger.info("  Recurso %s: skip=%d, %d registros nesta página, total=%d",
                            resource, skip, len(rows), total_saved)
                skip += PAGE_SIZE
                pages += 1

                if len(rows) < PAGE_SIZE:
                    break  # última página

    session.commit()
    session.close()
    logger.info("✅ %d contratos SICOR/BCB carregados na tabela rural_credits", total_saved)


if __name__ == "__main__":
    main()
