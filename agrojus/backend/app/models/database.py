
from sqlalchemy import (
    Column, String, Float, Integer, BigInteger, Boolean, Date, DateTime, Text, JSON,
    create_engine, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timezone

try:
    from geoalchemy2 import Geometry
except ImportError:
    # Fallback: use Text column when GeoAlchemy2 is not available
    from sqlalchemy import Text as Geometry  # noqa: N812

from app.config import settings

Base = declarative_base()


class Property(Base):
    """Imóvel rural com todos os identificadores possíveis."""
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Identificadores do imóvel (cada um indexado para busca rápida)
    car_code = Column(String(100), unique=True, index=True)
    matricula = Column(String(100), index=True)
    sncr_code = Column(String(100), index=True)
    nirf = Column(String(50), index=True)
    ccir = Column(String(50), index=True)
    sigef_code = Column(String(100), index=True)
    itr_number = Column(String(50), index=True)

    # Dados cadastrais
    property_name = Column(String(500))
    area_total_ha = Column(Float)
    area_app_ha = Column(Float)
    area_reserva_legal_ha = Column(Float)
    area_uso_consolidado_ha = Column(Float)
    area_remanescente_ha = Column(Float)
    municipality = Column(String(200))
    municipality_code = Column(String(10))
    state = Column(String(2))
    comarca = Column(String(200))
    cartorio = Column(String(500))
    classification = Column(String(100))  # Pequena/média/grande propriedade
    modules_fiscais = Column(Float)

    # Proprietário
    owner_name = Column(String(500))
    owner_cpf_cnpj = Column(String(20), index=True)

    # Status
    car_status = Column(String(50))
    sigef_certified = Column(Boolean, default=False)
    ccir_valid = Column(Boolean)
    has_onus = Column(Boolean)  # Gravames na matrícula
    onus_description = Column(Text)

    # Geoespacial
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))

    # ITR
    itr_vti = Column(Float)  # Valor da Terra Nua
    itr_status = Column(String(50))

    # Metadados
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    raw_data = Column(JSON)

    __table_args__ = (
        Index("idx_properties_municipality_state", "municipality", "state"),
        Index("idx_properties_owner", "owner_cpf_cnpj"),
    )


class Person(Base):
    """Pessoa física ou jurídica monitorada."""
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), unique=True, index=True)
    person_type = Column(String(2))  # PF ou PJ
    name = Column(String(500), index=True)
    trade_name = Column(String(500))  # Nome fantasia (PJ)
    registration_status = Column(String(50))
    cnae_principal = Column(String(200))
    address = Column(Text)
    municipality = Column(String(200))
    state = Column(String(2))
    capital_social = Column(Float)
    partners = Column(JSON)  # Lista de sócios

    # Monitoramento
    monitored = Column(Boolean, default=False)
    last_checked_at = Column(DateTime)
    alert_on_change = Column(Boolean, default=False)

    # Contadores (cache para consulta rápida)
    properties_count = Column(Integer, default=0)
    embargos_count = Column(Integer, default=0)
    lawsuits_count = Column(Integer, default=0)
    slave_labour_records = Column(Integer, default=0)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    raw_data = Column(JSON)


class EnvironmentalAlert(Base):
    __tablename__ = "environmental_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_car_code = Column(String(100), index=True)
    cpf_cnpj = Column(String(20), index=True)
    alert_type = Column(String(50))  # embargo, deforestation, overlap_uc, overlap_ti
    source = Column(String(50))  # ibama, inpe, icmbio, funai
    description = Column(Text)
    area_ha = Column(Float)
    date_detected = Column(DateTime)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class LegalRecord(Base):
    __tablename__ = "legal_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True)
    record_type = Column(String(50))  # lawsuit, debt, protest, slave_labour, certificate
    source = Column(String(100))  # tribunal name, ibama, mte, receita
    case_number = Column(String(100))
    description = Column(Text)
    amount = Column(Float)
    status = Column(String(50))
    date_filed = Column(DateTime)
    municipality = Column(String(200))
    state = Column(String(2))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class RuralCredit(Base):
    """Crédito rural (dados do SICOR/BCB)."""
    __tablename__ = "rural_credits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True)
    contract_number = Column(String(100))
    bank = Column(String(200))
    credit_line = Column(String(100))  # PRONAF, PRONAMP, etc.
    purpose = Column(String(100))  # Custeio, investimento, comercialização
    amount = Column(Float)
    municipality = Column(String(200))
    state = Column(String(2))
    year = Column(Integer)
    crop = Column(String(100))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_rural_credits_cpf_year", "cpf_cnpj", "year"),
    )


class LandPrice(Base):
    """Preços de terra por região."""
    __tablename__ = "land_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    municipality = Column(String(200))
    municipality_code = Column(String(10))
    state = Column(String(2))
    land_type = Column(String(100))  # Lavoura, pastagem, cerrado, mata
    price_per_ha = Column(Float)
    source = Column(String(100))
    reference_date = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_land_prices_location", "municipality", "state"),
    )


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    commodity = Column(String(50), index=True)
    price = Column(Float)
    unit = Column(String(20))
    date = Column(DateTime, index=True)
    source = Column(String(50))
    variation_pct = Column(Float)
    location = Column(String(200))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_market_commodity_date", "commodity", "date"),
    )


class MonitoringAlert(Base):
    """Alertas de monitoramento (mudanças detectadas)."""
    __tablename__ = "monitoring_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True)
    property_car_code = Column(String(100), index=True)
    alert_type = Column(String(100))  # new_lawsuit, new_embargo, car_change, price_change
    title = Column(String(500))
    description = Column(Text)
    severity = Column(String(20))  # info, warning, critical
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Publicacao(Base):
    """
    Publicação/intimação judicial coletada do DJEN (Comunica.PJe / CNJ).

    Cada item é uma intimação não-pessoal publicada no Diário de Justiça
    Eletrônico Nacional. Relacionada a um advogado (OAB) e/ou processo.
    """
    __tablename__ = "publicacoes_djen"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Identificador DJEN (único no sistema CNJ)
    djen_id = Column(BigInteger, unique=True, index=True, nullable=False)
    djen_hash = Column(String(100), index=True)

    # Metadados da publicação
    data_disponibilizacao = Column(Date, index=True, nullable=False)
    tribunal = Column(String(20), index=True)  # TRF1, TJMA, STJ, etc.
    orgao = Column(String(500))  # Vara, câmara etc.
    id_orgao = Column(Integer)
    tipo_comunicacao = Column(String(100))  # Intimação, Citação, Decisão
    tipo_documento = Column(String(200))
    classe = Column(String(300))  # Classe processual (com código TPU CNJ)
    codigo_classe = Column(String(20))
    meio = Column(String(10))  # D = DJEN, F = físico
    numero_comunicacao = Column(Integer)

    # Processo vinculado
    numero_processo = Column(String(30), index=True)
    numero_processo_mascarado = Column(String(40))  # 0000000-00.0000.0.00.0000

    # Conteúdo
    texto = Column(Text)  # HTML/texto completo da publicação
    link = Column(String(1000))  # URL para peça no tribunal

    # Advogado que motivou a busca (quando fizemos query por OAB)
    oab_numero = Column(String(20), index=True)
    oab_uf = Column(String(2))

    # Status de leitura / prazo (controle interno)
    lida = Column(Boolean, default=False, index=True)
    urgencia = Column(String(20))  # critico, alto, medio, baixo
    prazo_prescricao = Column(Date)  # quando definido manualmente

    # Raw + timestamps
    raw_data = Column(JSON)  # JSON original da API (destinatários, advogados etc.)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_publicacoes_oab_data", "oab_uf", "oab_numero", "data_disponibilizacao"),
        Index("idx_publicacoes_processo_data", "numero_processo", "data_disponibilizacao"),
    )


class MarketPriceUF(Base):
    """
    Snapshot mensal de preços de commodities por UF (mercado físico).

    Populado por job agendado (backend/scripts/scrape_market_prices.py)
    que consulta diariamente o collector Agrolink e persiste histórico.
    Frontend lê deste banco em vez de scrape live — mais rápido,
    menos impacto no site-fonte, dados preservados.
    """
    __tablename__ = "market_prices_uf"

    id = Column(Integer, primary_key=True, autoincrement=True)
    commodity = Column(String(30), index=True, nullable=False)  # soja, milho, etc.
    uf = Column(String(2), index=True, nullable=False)
    mes_ano = Column(String(7), index=True, nullable=False)  # "4/2026"
    preco_estadual = Column(Float)
    preco_nacional = Column(Float)
    unit = Column(String(30))
    label = Column(String(200))
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_market_prices_commodity_uf_mes", "commodity", "uf", "mes_ano", unique=True),
        Index("idx_market_prices_commodity_mes", "commodity", "mes_ano"),
    )


class ScrapingJobLog(Base):
    """Log de execução dos jobs de scraping (para monitoramento)."""
    __tablename__ = "scraping_job_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_name = Column(String(100), index=True, nullable=False)  # ex: "agrolink_prices"
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime)
    status = Column(String(20))  # success, partial, failed
    items_fetched = Column(Integer)
    items_persisted = Column(Integer)
    error = Column(Text)


class User(Base):
    """Usuário da plataforma."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(500), nullable=False)
    cpf_cnpj = Column(String(20), index=True)
    plan = Column(String(20), default="free")  # free, basic, pro, enterprise
    reports_used_this_month = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class CachedQuery(Base):
    __tablename__ = "cached_queries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_type = Column(String(50), index=True)
    query_key = Column(String(500), index=True)
    response_data = Column(JSON)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_cache_type_key", "query_type", "query_key"),
    )


# --- Engine & Session ---

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False)
    return _SessionLocal


def get_db() -> Session:
    """FastAPI dependency: yields a DB session per request."""
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    """Get a standalone DB session (for scripts/CLI)."""
    SessionLocal = get_session_factory()
    return SessionLocal()


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)
