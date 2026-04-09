from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PropertySearchRequest(BaseModel):
    car_code: Optional[str] = Field(None, description="Código CAR do imóvel")
    cpf_cnpj: Optional[str] = Field(None, description="CPF ou CNPJ do proprietário")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    municipality: Optional[str] = Field(None, description="Nome do município")
    state: Optional[str] = Field(None, description="Sigla do estado (UF)")
    owner_name: Optional[str] = Field(None, description="Nome do proprietário")


class CARData(BaseModel):
    car_code: str
    status: Optional[str] = None
    area_total_ha: Optional[float] = None
    area_app_ha: Optional[float] = None
    area_reserva_legal_ha: Optional[float] = None
    area_uso_consolidado_ha: Optional[float] = None
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


class CNPJData(BaseModel):
    cnpj: str
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    situacao_cadastral: Optional[str] = None
    data_situacao_cadastral: Optional[str] = None
    cnae_principal: Optional[str] = None
    endereco: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
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
    overlaps_conservation_unit: bool = False
    conservation_unit_name: Optional[str] = None
    overlaps_embargo: bool = False
    embargo_details: Optional[str] = None
    overlaps_deforestation: bool = False
    deforestation_area_ha: Optional[float] = None


class RiskScore(BaseModel):
    overall: RiskLevel
    land_tenure: RiskLevel
    environmental: RiskLevel
    legal: RiskLevel
    labor: RiskLevel
    details: list[str] = []


class DueDiligenceReport(BaseModel):
    report_id: str
    generated_at: datetime
    property_info: Optional[CARData] = None
    sigef_info: Optional[SIGEFData] = None
    owner_info: Optional[CNPJData] = None
    ibama_embargos: list[IBAMAEmbargo] = []
    slave_labour: list[SlaveLabourEntry] = []
    overlap_analysis: Optional[OverlapAnalysis] = None
    risk_score: Optional[RiskScore] = None


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
