
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


class Webhook(Base):
    """
    Webhook de notificação para alertas de monitoramento.

    Usuário cadastra uma URL que receberá POST com payload JSON quando
    eventos pertinentes forem disparados (novo alerta MapBiomas/DETER,
    nova publicação DJEN, mudança cadastral do CAR, novo embargo IBAMA).
    Filtros opcionais por car_code e cpf_cnpj.
    """
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)  # FK lógica para users (nullable em dev sem auth)

    name = Column(String(200), nullable=False)
    url = Column(String(1000), nullable=False)
    secret = Column(String(200))  # opcional: usado para HMAC-SHA256 header X-AgroJus-Signature

    # Filtros
    event_types = Column(JSON, nullable=False)  # lista: ["mapbiomas_alert","deter_alert","djen_publicacao","car_status_change","ibama_embargo"]
    car_filter = Column(String(100), index=True)  # se setado, só dispara para este CAR
    cpf_cnpj_filter = Column(String(20), index=True)  # se setado, só dispara para este CPF/CNPJ

    active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_delivery_at = Column(DateTime)
    last_delivery_status = Column(String(20))  # success, failed, pending

    __table_args__ = (
        Index("idx_webhooks_user_active", "user_id", "active"),
    )


class WebhookDelivery(Base):
    """Log de cada tentativa de entrega de webhook."""
    __tablename__ = "webhook_deliveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    webhook_id = Column(Integer, index=True, nullable=False)
    event_type = Column(String(50), index=True, nullable=False)
    payload = Column(JSON)
    status_code = Column(Integer)
    response_body = Column(Text)  # truncado em 2000 chars
    success = Column(Boolean, default=False, index=True)
    attempt = Column(Integer, default=1)
    error = Column(Text)
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    duration_ms = Column(Integer)

    __table_args__ = (
        Index("idx_deliveries_webhook_time", "webhook_id", "attempted_at"),
    )


# ==========================================================================
# Sprint 4 — 10 coletores dados.gov.br + Portal Transparência
# Novas camadas PostGIS que substituem stubs do layers-catalog.
# ==========================================================================


class SigmineProcesso(Base):
    """Processo minerário ANM (shapefile SIGMINE)."""
    __tablename__ = "sigmine_processos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    processo = Column(String(30), index=True)
    ano = Column(Integer, index=True)
    fase = Column(String(100), index=True)  # "Requerimento de Pesquisa", "Concessão de Lavra"...
    ult_evento = Column(String(200))
    nome = Column(String(300))
    subs = Column(String(200), index=True)  # Substância
    uf = Column(String(2), index=True)
    area_ha = Column(Float)
    uso = Column(String(50))
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AnaOutorga(Base):
    """Outorga de direito de uso de recursos hídricos (ANA)."""
    __tablename__ = "ana_outorgas_full"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_ato = Column(String(100), index=True)
    uf = Column(String(2), index=True)
    municipio = Column(String(200))
    cpf_cnpj = Column(String(20), index=True)
    nome_usuario = Column(String(500))
    finalidade = Column(String(200), index=True)  # irrigação, consumo humano, etc.
    tipo_corpo_hidrico = Column(String(100))
    nome_corpo_hidrico = Column(String(300))
    vazao_l_s = Column(Float)
    area_irrigada_ha = Column(Float)
    data_emissao = Column(Date)
    data_validade = Column(Date)
    situacao = Column(String(50))
    geometry = Column(Geometry("POINT", srid=4326))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AnaBho(Base):
    """Base Hidrográfica Ottocodificada — trechos de drenagem."""
    __tablename__ = "ana_bho"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cocursodag = Column(String(100), index=True)
    cotrecho = Column(String(100))
    nome_curso = Column(String(300))
    nu_ordem = Column(Integer)
    nu_comptrec = Column(Float)  # comprimento em km
    nu_areacont = Column(Float)  # area de contribuição
    geometry = Column(Geometry("MULTILINESTRING", srid=4326))


class IncraAssentamento(Base):
    """Projeto de Assentamento INCRA."""
    __tablename__ = "incra_assentamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_proje = Column(String(300), index=True)
    cd_sipra = Column(String(30), index=True)
    municipio = Column(String(200))
    uf = Column(String(2), index=True)
    area_ha = Column(Float)
    capacidade = Column(Integer)  # famílias assentadas
    num_famili = Column(Integer)
    data_criac = Column(Date)
    fase = Column(String(100))
    forma_obte = Column(String(100))
    esfera = Column(String(20))  # federal/estadual
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    raw_data = Column(JSON)


class IncraQuilombola(Base):
    """Área quilombola INCRA/Palmares."""
    __tablename__ = "incra_quilombolas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(300), index=True)
    municipio = Column(String(200))
    uf = Column(String(2), index=True)
    area_ha = Column(Float)
    num_famili = Column(Integer)
    fase = Column(String(100))  # titulada, em processo, etc.
    esfera = Column(String(20))
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    raw_data = Column(JSON)


class AneelUsina(Base):
    """Empreendimento de geração elétrica (BIG/ANEEL)."""
    __tablename__ = "aneel_usinas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ceg = Column(String(50), index=True)  # Código Único de Empreendimento
    nome = Column(String(300))
    tipo = Column(String(50), index=True)  # UHE/PCH/CGH/UTE/UFV/EOL
    combustivel = Column(String(100))
    potencia_mw = Column(Float)
    fase = Column(String(50))  # Operação/Construção/Projeto
    uf = Column(String(2), index=True)
    municipio = Column(String(200))
    proprietario = Column(String(300))
    geometry = Column(Geometry("POINT", srid=4326))
    raw_data = Column(JSON)


class AneelLinhaTransmissao(Base):
    """Linha de transmissão elétrica (ONS/ANEEL)."""
    __tablename__ = "aneel_linhas_transmissao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(300), index=True)
    tensao_kv = Column(Float)
    operador = Column(String(300))
    situacao = Column(String(50))
    comprimento_km = Column(Float)
    geometry = Column(Geometry("MULTILINESTRING", srid=4326))


class GarantiaSafraBeneficiario(Base):
    """Beneficiário do programa Garantia-Safra (semiárido)."""
    __tablename__ = "garantia_safra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nis = Column(String(20), index=True)  # Número de Identificação Social
    nome = Column(String(300))
    cpf_cnpj = Column(String(20), index=True)
    municipio = Column(String(200))
    uf = Column(String(2), index=True)
    ano_safra = Column(Integer, index=True)
    valor_beneficio = Column(Float)
    data_pagamento = Column(Date)
    raw_data = Column(JSON)

    __table_args__ = (
        Index("idx_gs_uf_ano", "uf", "ano_safra"),
        Index("idx_gs_mun_ano", "municipio", "ano_safra"),
    )


class CeisRegistro(Base):
    """Cadastro de Empresas Inidôneas e Suspensas (CGU)."""
    __tablename__ = "ceis_registros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True, nullable=False)
    nome = Column(String(500))
    razao_social = Column(String(500))
    tipo_pessoa = Column(String(2))  # PF/PJ
    tipo_sancao = Column(String(200))
    data_inicio_sancao = Column(Date)
    data_fim_sancao = Column(Date)
    orgao_sancionador = Column(String(300))
    uf_orgao = Column(String(2))
    fundamentacao = Column(Text)
    processo = Column(String(100))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CnepRegistro(Base):
    """Cadastro Nacional de Empresas Punidas (CGU)."""
    __tablename__ = "cnep_registros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True, nullable=False)
    nome = Column(String(500))
    razao_social = Column(String(500))
    tipo_pessoa = Column(String(2))
    tipo_sancao = Column(String(200))
    data_inicio_sancao = Column(Date)
    data_fim_sancao = Column(Date)
    valor_multa = Column(Float)
    orgao_sancionador = Column(String(300))
    fundamentacao = Column(Text)
    processo = Column(String(100))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class IbamaEmbargo(Base):
    """Termo de embargo IBAMA (com geometria quando disponível)."""
    __tablename__ = "ibama_embargos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_termo = Column(String(50), index=True)
    cpf_cnpj = Column(String(20), index=True)
    nome_pessoa = Column(String(500))
    uf = Column(String(2), index=True)
    municipio = Column(String(200))
    area_embargada_ha = Column(Float)
    data_embargo = Column(Date)
    tipo_infracao = Column(String(300))
    artigo = Column(String(100))
    valor_multa = Column(Float)
    situacao = Column(String(50))
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    raw_data = Column(JSON)


class IbamaCtf(Base):
    """Cadastro Técnico Federal de atividades potencialmente poluidoras."""
    __tablename__ = "ibama_ctf"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True)
    nome = Column(String(500))
    categoria = Column(String(200))
    atividade = Column(String(300))
    situacao = Column(String(50))
    uf = Column(String(2), index=True)
    municipio = Column(String(200))
    data_cadastro = Column(Date)
    raw_data = Column(JSON)


class IbamaAutoInfracao(Base):
    """
    Auto de infração IBAMA — base completa SIFISC (CSV).

    Complementa geo_autos_ibama (apenas pontos georreferenciados, ~16k) com
    registros tabulares completos (geralmente 600k+ autos históricos).
    Usado para cruzamento por CPF/CNPJ nos critérios do MCR 2.9.
    """
    __tablename__ = "ibama_autos_infracao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_auto = Column(String(50), index=True)  # não-único: mesmo número em séries diferentes
    serie_auto = Column(String(20))
    tipo_auto = Column(String(50))
    cpf_cnpj_infrator = Column(String(20), index=True)
    nome_infrator = Column(String(500))
    data_auto = Column(Date)
    data_lavratura = Column(Date)
    uf = Column(String(2), index=True)
    municipio = Column(String(200), index=True)
    valor_auto = Column(Float)
    status_debito = Column(String(50))
    desc_infracao = Column(Text)
    enq_legal = Column(String(200))
    lat = Column(Float)
    lon = Column(Float)
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_autos_cpf_uf", "cpf_cnpj_infrator", "uf"),
        Index("idx_autos_num_serie", "numero_auto", "serie_auto"),
    )


class DadosGovIngestLog(Base):
    """Log de ingestões executadas pelo ETL dados_gov."""
    __tablename__ = "dados_gov_ingest_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loader = Column(String(100), index=True, nullable=False)
    dataset_id = Column(String(200))
    resource_url = Column(Text)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime)
    status = Column(String(20))  # success, partial, failed
    rows_fetched = Column(Integer)
    rows_persisted = Column(Integer)
    error = Column(Text)


# ==========================================================================
# Jurídico-Agro — contratos, teses, legislação, monitoramento
# (Sprint Jurídico-Agro — AgroJus não é focado em advogado;
#  é um hub de informação jurídica para todo o agronegócio)
# ==========================================================================


class ContratoAgroTemplate(Base):
    """
    Template de contrato do agronegócio (arrendamento, parceria, CPR, CDA-WA,
    compra e venda rural, meação, comodato, integração, fomento, etc).

    Cada template tem:
      - categoria e subcategoria (taxonomia do agro)
      - texto_markdown: minuta completa em markdown, com placeholders {{ NOME }}
      - campos[]: lista estruturada de campos que o usuário preenche
      - legislacao_referencia[]: base legal citada
      - cautelas[]: pontos de atenção editoriais
      - aplicacao: "PJ", "PF", "Ambos"
      - publico_alvo: tags (comprador, produtor, trading, banco...)
    """
    __tablename__ = "contratos_agro_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    titulo = Column(String(300), nullable=False)
    categoria = Column(String(80), index=True)  # exploracao_rural, garantia, compra_venda, trabalhista, etc
    subcategoria = Column(String(100))
    sinopse = Column(Text)
    aplicacao = Column(String(20))  # "PF" | "PJ" | "Ambos"
    publico_alvo = Column(JSON)  # ["comprador", "produtor", "trading"...]
    texto_markdown = Column(Text, nullable=False)
    campos = Column(JSON)  # [{nome, tipo, obrigatorio, descricao}]
    legislacao_referencia = Column(JSON)  # ["Lei 4.504/64 art. 92", "CC art. 1.196"...]
    cautelas = Column(JSON)  # lista de alertas
    versao = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class TeseDefesaAgro(Base):
    """
    Tese de defesa/argumentativa para questões do agronegócio (auto IBAMA,
    execução fiscal ambiental, usucapião rural, dissídio do trabalhador
    rural, previdência agro, lista suja MTE, litígios fundiários...).

    Cada tese traz:
      - sumula_propria (síntese em 1 parágrafo)
      - argumentos_principais[]: cada um com enunciado + fundamentacao
      - precedentes_sugeridos[]: jurisprudência útil (STJ/STF/TRF/TJ)
      - legislacao_aplicavel[]
      - aplicabilidade: quando usar
      - contra_argumentos_esperados[]: o que o adversário provavelmente dirá
      - proxima_acao_recomendada
    """
    __tablename__ = "teses_defesa_agro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    titulo = Column(String(400), nullable=False)
    area = Column(String(80), index=True)  # ambiental, fundiario, trabalhista, tributario, previdenciario, penal_agro
    situacao = Column(Text)  # descrição completa do contexto
    sumula_propria = Column(Text)
    argumentos_principais = Column(JSON)  # [{enunciado, fundamentacao, peso}]
    precedentes_sugeridos = Column(JSON)  # [{tribunal, numero, ementa_resumida, url}]
    legislacao_aplicavel = Column(JSON)
    aplicabilidade = Column(Text)
    contra_argumentos = Column(JSON)
    proxima_acao = Column(Text)
    publico_alvo = Column(JSON)  # ["produtor_autuado", "advogado", "consultor_ambiental"...]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class LegislacaoAgro(Base):
    """
    Legislação relevante ao agronegócio, com escopo territorial
    (federal, estadual, municipal) e tema.

    Campos mínimos que permitem filtrar por "o que se aplica na UF X
    para tema Y" (ex: RL no Cerrado goiano → Lei 12.651/12 +
    Lei estadual Z + normativas ambientais municipais).
    """
    __tablename__ = "legislacao_agro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    titulo = Column(String(500), nullable=False)
    esfera = Column(String(20), index=True, nullable=False)  # federal | estadual | municipal
    uf = Column(String(2), index=True)
    municipio = Column(String(200))
    municipio_ibge = Column(String(10), index=True)
    tipo = Column(String(60))  # lei, decreto, resolucao, portaria, instrucao_normativa
    numero = Column(String(50))
    ano = Column(Integer, index=True)
    orgao = Column(String(200))
    ementa = Column(Text)
    temas = Column(JSON)  # ["reserva_legal", "apa", "irrigacao", "itr", "credito_rural", "zee", "licenciamento"...]
    publicacao = Column(Date)
    situacao = Column(String(30))  # vigente, revogada, suspensa
    url_oficial = Column(Text)
    url_lexml = Column(Text)
    texto_integral_url = Column(Text)
    resumo = Column(Text)  # resumo pratico do que significa para o agricultor
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_leg_esfera_uf_tema", "esfera", "uf"),
    )


class MonitoramentoParte(Base):
    """
    Cadastro de CPF/CNPJ para monitoramento processual contínuo.

    O produto permite que o agricultor/trading/consultor monitore partes
    (proprietários vizinhos, prestadores de serviço, vendedores potenciais)
    sem ser o advogado deles. Triagem automática de processos novos,
    embargos, autos IBAMA, inclusão em lista suja.

    Diferente do webhook de imóvel (que é sobre uma area), este é sobre uma
    PARTE (CPF ou CNPJ) — util para due diligence comercial.
    """
    __tablename__ = "monitoramento_partes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)  # quem cadastrou
    cpf_cnpj = Column(String(20), index=True, nullable=False)
    nome_sugerido = Column(String(500))  # rotulo livre ("Vizinho sul", "Fornecedor de gado")
    contexto = Column(Text)  # por que está monitorando
    tags = Column(JSON)  # ["fornecedor", "vizinho", "vendedor", "comprador"]
    eventos_monitorados = Column(JSON)  # ["datajud_novo_processo","ibama_auto","ceis","cnep","lista_suja","djen"]
    frequencia = Column(String(20), default="diaria")  # diaria | semanal | mensal
    webhook_url = Column(Text)  # opcional — dispara quando algo novo for detectado
    active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_checked_at = Column(DateTime)

    __table_args__ = (
        Index("idx_monit_user_cpf", "user_id", "cpf_cnpj", unique=True),
    )


class MonitoramentoParteEvento(Base):
    """Eventos detectados no monitoramento (trilha de auditoria)."""
    __tablename__ = "monitoramento_partes_eventos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    monitoramento_id = Column(Integer, index=True, nullable=False)
    cpf_cnpj = Column(String(20), index=True, nullable=False)
    tipo_evento = Column(String(50), index=True)  # novo_auto_ibama, nova_sancao_ceis, novo_processo, etc
    resumo = Column(Text)
    valor_rs = Column(Float)
    data_evento = Column(Date)
    fonte = Column(String(50))
    raw_data = Column(JSON)
    notificado = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


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
