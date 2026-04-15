"""
etl_ana_outorgas.py — Ingestão de Outorgas de Uso de Recursos Hídricos (ANA)
Fonte: SNIRH / ANA via API pública (sem autenticação)

Tabela destino: ana_outorgas
Campos: id, bacia, sub_bacia, uf, municipio, tipo_uso, tipo_ato, vazao_m3s,
        data_emissao, data_vencimento, situacao, lat, lon, geometry
"""
import logging
import os
import csv
import io
import zipfile
from datetime import datetime, timezone

import httpx
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
Base = declarative_base()


# ─── Download direto do CSV de outorgas (SNIRH dados abertos) ───────────────

# O SNIRH disponibiliza CSV completo de outorgas via download direto
OUTORGA_URLS = [
    # CSV via SNIRH Consulta Pública
    "https://www.snirh.gov.br/snirh/download/outorgas/outorgas_completo.zip",
    # Alternativa: dados abertos ANA
    "https://metadados.snirh.gov.br/files/outorgas/outorgas_emitidas.zip",
    # OGC WFS direto (limitado a 10k registros por request)
    "https://metadados.snirh.gov.br/geoserver/wms/ows?service=WFS&version=1.0.0"
    "&request=GetFeature&typeName=snirh:DadosOutorgaConsultaPublica"
    "&outputFormat=csv&maxFeatures=50000",
]

# CSV de referência — disponível sem zip no SNIRH
SICAJ_CSV = "https://dadosabertos.ana.gov.br/api/3/action/datastore_search?resource_id=outorgas&limit=100"


class AnaOutorga(Base):
    __tablename__ = "ana_outorgas"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    cod_outorga     = Column(String(50))
    bacia           = Column(String(100))
    sub_bacia       = Column(String(100))
    uf              = Column(String(2))
    municipio       = Column(String(100))
    tipo_uso        = Column(String(80))     # irrigação, abastecimento, indústria...
    tipo_ato        = Column(String(60))     # portaria, resolução, declaração...
    vazao_m3s       = Column(Float)
    data_emissao    = Column(Date)
    data_vencimento = Column(Date)
    situacao        = Column(String(40))     # vigente, cancelada, vencida...
    lat             = Column(Float)
    lon             = Column(Float)


def setup_db():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def try_wfs_csv(client: httpx.Client) -> list[dict]:
    """Tenta obter outorgas via WFS em formato CSV."""
    url = (
        "https://metadados.snirh.gov.br/geoserver/wms/ows"
        "?service=WFS&version=1.0.0&request=GetFeature"
        "&typeName=snirh:DadosOutorgaConsultaPublica"
        "&outputFormat=csv&maxFeatures=50000"
    )
    try:
        logger.info("Tentando WFS CSV: %s", url[:100])
        r = client.get(url, timeout=60)
        logger.info("HTTP %d — %d bytes", r.status_code, len(r.content))
        if r.status_code == 200 and b"," in r.content[:100]:
            reader = csv.DictReader(io.StringIO(r.text))
            return list(reader)
    except Exception as e:
        logger.warning("WFS CSV falhou: %s", e)
    return []


def try_zip_csv(client: httpx.Client) -> list[dict]:
    """Tenta obter outorgas via ZIP+CSV."""
    for url in [
        "https://www.snirh.gov.br/snirh/download/outorgas/outorgas_completo.zip",
        "https://metadados.snirh.gov.br/files/outorgas/outorgas_emitidas.zip",
    ]:
        try:
            logger.info("Tentando ZIP: %s", url)
            r = client.get(url, timeout=120)
            logger.info("HTTP %d — %d bytes", r.status_code, len(r.content))
            if r.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                    csv_files = [n for n in zf.namelist() if n.lower().endswith(".csv")]
                    if csv_files:
                        raw = zf.read(csv_files[0]).decode("latin-1")
                        reader = csv.DictReader(io.StringIO(raw), delimiter=";")
                        return list(reader)
        except Exception as e:
            logger.warning("ZIP falhou [%s]: %s", url, e)
    return []


def parse_row(row: dict) -> dict | None:
    """Normaliza uma linha de outorga para o schema do banco."""
    def safe_float(v):
        try:
            return float(str(v).replace(",", ".").strip())
        except Exception:
            return None

    def safe_date(v):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(str(v).strip(), fmt).date()
            except Exception:
                continue
        return None

    lat = safe_float(row.get("LATITUDE") or row.get("lat") or row.get("COORD_Y"))
    lon = safe_float(row.get("LONGITUDE") or row.get("lon") or row.get("COORD_X"))

    return {
        "cod_outorga":     str(row.get("COD_OUTORGA") or row.get("NUMERO_ATO") or "")[:50],
        "bacia":           str(row.get("BACIA") or row.get("NOM_BACIA") or "")[:100],
        "sub_bacia":       str(row.get("SUB_BACIA") or row.get("NOM_SUB_BACIA") or "")[:100],
        "uf":              str(row.get("UF") or row.get("EST_SIGLA") or "")[:2].upper(),
        "municipio":       str(row.get("MUNICIPIO") or row.get("NOM_MUNICIPIO") or "")[:100],
        "tipo_uso":        str(row.get("TIPO_USO") or row.get("FINALIDADE") or "")[:80],
        "tipo_ato":        str(row.get("TIPO_ATO") or row.get("TIPO_OUTORGA") or "")[:60],
        "vazao_m3s":       safe_float(row.get("VAZAO_M3S") or row.get("Q_OUTORGADA")),
        "data_emissao":    safe_date(row.get("DATA_EMISSAO") or row.get("DT_EMISSAO")),
        "data_vencimento": safe_date(row.get("VENCIMENTO") or row.get("DT_VENCIMENTO")),
        "situacao":        str(row.get("SITUACAO") or row.get("SIT_OUTORGA") or "vigente")[:40],
        "lat":             lat,
        "lon":             lon,
    }


def main():
    logger.info("=== ETL ANA Outorgas de Água ===")
    session = setup_db()

    rows = []
    with httpx.Client(verify=False, timeout=120, follow_redirects=True,
                      headers={"User-Agent": "AgroJus/1.0 (agrojus@github.com)"}) as client:
        rows = try_wfs_csv(client)
        if not rows:
            rows = try_zip_csv(client)

    if not rows:
        logger.error("Nenhum dado obtido da ANA. Verifique os endpoints.")
        logger.info("Alternativa: baixar manualmente de https://metadados.snirh.gov.br/")
        return

    logger.info("%d outorgas a processar", len(rows))

    # Limpa registros antigos
    deleted = session.execute(text("DELETE FROM ana_outorgas")).rowcount
    logger.info("%d registros antigos deletados", deleted)

    saved = 0
    batch = []
    for row in rows:
        parsed = parse_row(row)
        if parsed:
            batch.append(AnaOutorga(**{k: v for k, v in parsed.items() if v is not None}))
            saved += 1

        if len(batch) >= 500:
            session.bulk_save_objects(batch)
            session.flush()
            batch = []
            logger.info("  ... %d outorgas processadas", saved)

    if batch:
        session.bulk_save_objects(batch)

    session.commit()
    session.close()
    logger.info("✅ %d outorgas da ANA carregadas", saved)


if __name__ == "__main__":
    main()
