from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# --- Enums ---

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PersonaType(str, Enum):
    BUYER = "buyer"           # Comprador de imóvel
    LAWYER = "lawyer"         # Advogado fazendo diligência
    FARMER = "farmer"         # Agropecuarista
    INVESTOR = "investor"     # Investidor / banco / cooperativa


# --- Search Requests ---

class PropertySearchRequest(BaseModel):
    """
    Busca universal de imóvel rural.
    O usuário pode informar qualquer identificador que possua.
    O sistema tenta resolver a partir de qualquer um deles.
    """
    # Identificadores do imóvel (qualquer um serve como ponto de entrada)
    car_code: Optional[str] = Field(None, description="Codigo do Cadastro Ambiental Rural (CAR)")
    matricula: Optional[str] = Field(None, description="Numero da matricula no Cartorio de Registro de Imoveis")
    sncr_code: Optional[str] = Field(None, description="Codigo SNCR (Sistema Nacional de Cadastro Rural / INCRA)")
    nirf: Optional[str] = Field(None, description="NIRF - Numero do Imovel na Receita Federal")
    ccir: Optional[str] = Field(None, description="CCIR - Certificado de Cadastro de Imovel Rural")
    itr_number: Optional[str] = Field(None, description="Numero da declaracao do ITR")
    sigef_code: Optional[str] = Field(None, description="Codigo da parcela no SIGEF")

    # Localização geográfica
    latitude: Optional[float] = Field(None, description="Latitude (decimal)")
    longitude: Optional[float] = Field(None, description="Longitude (decimal)")

    # Busca por localidade
    municipality: Optional[str] = Field(None, description="Nome do municipio")
    state: Optional[str] = Field(None, description="Sigla do estado (UF)")

    # Busca pelo proprietário
    cpf_cnpj: Optional[str] = Field(None, description="CPF ou CNPJ do proprietario")
    owner_name: Optional[str] = Field(None, description="Nome do proprietario")

    # Tipo de relatório desejado
    persona: Optional[PersonaType] = Field(None, description="Perfil do solicitante (ajusta nivel de detalhe do relatorio)")

    # Enriquecimentos opcionais (lentos, ~10-30s)
    include_satellite: bool = Field(False, description="Incluir dados Earth Engine (LULC, fogo, solo, agua) — adiciona ~20s")
    include_realtime_alerts: bool = Field(False, description="Incluir alertas MapBiomas em tempo real via GraphQL — adiciona ~3s")


class PersonSearchRequest(BaseModel):
    """
    Busca de informações sobre uma pessoa (CPF/CNPJ).
    Retorna dossiê completo: imóveis, processos, embargos, notícias.
    """
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ a consultar")
    include_properties: bool = Field(True, description="Buscar imoveis vinculados")
    include_legal: bool = Field(True, description="Buscar processos judiciais")
    include_environmental: bool = Field(True, description="Buscar embargos/infracoes ambientais")
    include_labour: bool = Field(True, description="Buscar na Lista Suja")
    include_news: bool = Field(True, description="Buscar noticias publicas")
    include_financial: bool = Field(True, description="Buscar dados financeiros (credito rural, etc)")


class RegionSearchRequest(BaseModel):
    """Busca de informações sobre uma região (município, estado, bacia)."""
    municipality: Optional[str] = Field(None, description="Nome do municipio")
    state: Optional[str] = Field(None, description="Sigla do estado (UF)")
    municipality_code: Optional[str] = Field(None, description="Codigo IBGE do municipio")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = Field(None, description="Raio de busca em km")


# --- Data Models ---

class LawsuitRecord(BaseModel):
    """Registro de processo judicial (DataJud/CNJ)."""
    case_number: Optional[str] = None
    tribunal: Optional[str] = None
    court: Optional[str] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    subjects: list[str] = []
    class_name: Optional[str] = None
    filing_date: Optional[str] = None
    last_update: Optional[str] = None
    status: Optional[str] = None
    degree: Optional[str] = None
    system: Optional[str] = None


class CARData(BaseModel):
    car_code: str
    status: Optional[str] = None
    area_total_ha: Optional[float] = None
    area_app_ha: Optional[float] = None
    area_reserva_legal_ha: Optional[float] = None
    area_uso_consolidado_ha: Optional[float] = None
    area_remanescente_ha: Optional[float] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    geometry_wkt: Optional[str] = None


class SIGEFData(BaseModel):
    parcel_code: Optional[str] = None
    certified: bool = False
    area_ha: Optional[float] = None
    certification_date: Optional[str] = None
    responsible_professional: Optional[str] = None
    geometry_wkt: Optional[str] = None


class MatriculaData(BaseModel):
    """Dados da matrícula no Cartório de Registro de Imóveis."""
    matricula_number: Optional[str] = None
    cartorio: Optional[str] = None
    comarca: Optional[str] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    area_ha: Optional[float] = None
    owner_name: Optional[str] = None
    owner_cpf_cnpj: Optional[str] = None
    registration_date: Optional[str] = None
    has_onus: Optional[bool] = None  # Ônus/gravames
    onus_description: Optional[str] = None


class SNCRData(BaseModel):
    """Dados do SNCR (Sistema Nacional de Cadastro Rural / INCRA)."""
    sncr_code: Optional[str] = None
    nirf: Optional[str] = None
    property_name: Optional[str] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    area_ha: Optional[float] = None
    classification: Optional[str] = None  # Pequena/média/grande propriedade
    modules_fiscais: Optional[float] = None
    owner_name: Optional[str] = None
    owner_cpf_cnpj: Optional[str] = None


class CCIRData(BaseModel):
    """Dados do CCIR (Certificado de Cadastro de Imóvel Rural)."""
    ccir_number: Optional[str] = None
    valid: Optional[bool] = None
    expiration_date: Optional[str] = None
    property_name: Optional[str] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    area_ha: Optional[float] = None


class ITRData(BaseModel):
    """Dados do ITR (Imposto Territorial Rural)."""
    nirf: Optional[str] = None
    year: Optional[int] = None
    vti: Optional[float] = None  # Valor da Terra Nua (VTN)
    area_total_ha: Optional[float] = None
    area_tributavel_ha: Optional[float] = None
    valor_imposto: Optional[float] = None
    status_pagamento: Optional[str] = None


class CNPJData(BaseModel):
    cnpj: str
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    situacao_cadastral: Optional[str] = None
    data_situacao_cadastral: Optional[str] = None
    data_abertura: Optional[str] = None
    cnae_principal: Optional[str] = None
    cnaes_secundarios: Optional[list[str]] = None
    endereco: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    capital_social: Optional[float] = None
    socios: Optional[list] = None


class IBAMAEmbargo(BaseModel):
    auto_infracao: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    nome: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    area_embargada_ha: Optional[float] = None
    data_embargo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None


class SlaveLabourEntry(BaseModel):
    employer_name: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    establishment: Optional[str] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    workers_rescued: Optional[int] = None
    inspection_date: Optional[str] = None


class OverlapAnalysis(BaseModel):
    overlaps_indigenous_land: bool = False
    indigenous_land_name: Optional[str] = None
    indigenous_land_area_overlap_ha: Optional[float] = None
    overlaps_conservation_unit: bool = False
    conservation_unit_name: Optional[str] = None
    conservation_unit_category: Optional[str] = None
    overlaps_embargo: bool = False
    embargo_details: Optional[str] = None
    overlaps_deforestation: bool = False
    deforestation_area_ha: Optional[float] = None
    overlaps_settlement: bool = False
    settlement_name: Optional[str] = None
    overlaps_quilombo: bool = False
    quilombo_name: Optional[str] = None


# --- Financial Data ---

class RuralCreditRecord(BaseModel):
    """Registro de crédito rural (SICOR/BCB)."""
    contract_number: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    bank: Optional[str] = None
    credit_line: Optional[str] = None  # PRONAF, PRONAMP, etc.
    purpose: Optional[str] = None  # Custeio, investimento, comercialização
    amount: Optional[float] = None
    municipality: Optional[str] = None
    state: Optional[str] = None
    year: Optional[int] = None
    crop: Optional[str] = None


class LandPriceData(BaseModel):
    """Preço de terras por região."""
    municipality: Optional[str] = None
    state: Optional[str] = None
    land_type: Optional[str] = None  # Lavoura, pastagem, cerrado, mata
    price_per_ha: Optional[float] = None
    source: Optional[str] = None
    reference_date: Optional[str] = None


class FinancialSummary(BaseModel):
    """Resumo financeiro associado a um CPF/CNPJ ou região."""
    rural_credits: list[RuralCreditRecord] = []
    total_credit_amount: Optional[float] = None
    land_prices: list[LandPriceData] = []
    avg_land_price_per_ha: Optional[float] = None


# --- Risk Score ---

class RiskScore(BaseModel):
    overall: RiskLevel
    land_tenure: RiskLevel
    environmental: RiskLevel
    legal: RiskLevel
    labor: RiskLevel
    financial: RiskLevel = RiskLevel.LOW
    details: list[str] = []


# --- Reports ---

class DueDiligenceReport(BaseModel):
    """Relatório completo de due diligence de um imóvel rural."""
    report_id: str
    generated_at: datetime
    persona: Optional[PersonaType] = None

    # Dados do imóvel (todas as fontes)
    property_info: Optional[CARData] = None
    sigef_info: Optional[SIGEFData] = None
    matricula_info: Optional[MatriculaData] = None
    sncr_info: Optional[SNCRData] = None
    ccir_info: Optional[CCIRData] = None
    itr_info: Optional[ITRData] = None

    # Dados do proprietário
    owner_info: Optional[CNPJData] = None

    # Alertas ambientais
    ibama_embargos: list[IBAMAEmbargo] = []

    # Questões trabalhistas
    slave_labour: list[SlaveLabourEntry] = []

    # Processos judiciais
    lawsuits: list[LawsuitRecord] = []

    # Análise geoespacial
    overlap_analysis: Optional[OverlapAnalysis] = None

    # Dados financeiros
    financial_summary: Optional[FinancialSummary] = None

    # Score de risco
    risk_score: Optional[RiskScore] = None

    # Compliance MCR 2.9, EUDR (dict com checklists detalhados)
    compliance: Optional[dict] = None

    # Analise espacial detalhada (PostGIS cruzamentos)
    spatial_analysis: Optional[dict] = None

    # Dados de satelite (Earth Engine — se include_satellite=true)
    satellite_data: Optional[dict] = None

    # Alertas MapBiomas em tempo real (se include_realtime_alerts=true)
    mapbiomas_realtime: Optional[dict] = None

    # Fontes consultadas
    sources_consulted: list[str] = []


class PersonDossier(BaseModel):
    """Dossiê completo de uma pessoa (CPF/CNPJ)."""
    dossier_id: str
    generated_at: datetime
    cpf_cnpj: str
    person_type: str  # PF ou PJ

    # Dados cadastrais
    owner_info: Optional[CNPJData] = None

    # Imóveis vinculados
    properties: list[CARData] = []
    properties_count: int = 0

    # Questões ambientais
    ibama_embargos: list[IBAMAEmbargo] = []

    # Questões trabalhistas
    slave_labour: list[SlaveLabourEntry] = []

    # Processos judiciais
    lawsuits: list[LawsuitRecord] = []

    # Dados financeiros
    financial_summary: Optional[FinancialSummary] = None

    # Notícias públicas
    news_mentions: list["NewsArticle"] = []

    # Score de risco agregado
    risk_score: Optional[RiskScore] = None

    # Fontes consultadas
    sources_consulted: list[str] = []


class RegionReport(BaseModel):
    """Relatório de inteligência sobre uma região."""
    report_id: str
    generated_at: datetime
    municipality: Optional[str] = None
    state: Optional[str] = None

    # Estatísticas de imóveis
    total_properties: int = 0
    total_area_ha: float = 0
    certified_properties: int = 0

    # Questões ambientais na região
    ibama_embargos: list[IBAMAEmbargo] = []
    deforestation_alerts: int = 0

    # Dados econômicos
    financial_summary: Optional[FinancialSummary] = None
    main_crops: list[dict] = []

    # Dados de mercado
    quotes: list["MarketQuote"] = []

    # Notícias da região
    news: list["NewsArticle"] = []


# --- Market & News ---

class MarketQuote(BaseModel):
    commodity: str
    price: float
    unit: str
    date: str
    source: str
    variation_pct: Optional[float] = None
    location: Optional[str] = None


class NewsArticle(BaseModel):
    title: str
    url: str
    source: str
    published_at: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    related_cpf_cnpj: Optional[str] = None
    related_municipality: Optional[str] = None


# Fix forward references
PersonDossier.model_rebuild()
RegionReport.model_rebuild()
