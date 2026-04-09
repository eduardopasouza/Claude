"""
Rotas de geração de relatórios.

Três tipos de relatório:
1. Due Diligence de Imóvel (para comprador/advogado/investidor)
2. Dossiê de Pessoa (CPF/CNPJ)
3. Relatório de Região (município/estado)
"""

import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import (
    PropertySearchRequest,
    PersonSearchRequest,
    RegionSearchRequest,
    PersonaType,
)
from app.services.due_diligence import DueDiligenceService
from app.services.person_intelligence import PersonIntelligenceService
from app.services.region_intelligence import RegionIntelligenceService
from app.services.pdf_report import PDFReportGenerator

router = APIRouter()


# === Due Diligence de Imóvel ===

@router.post("/due-diligence")
async def generate_due_diligence(request: PropertySearchRequest):
    """
    Gera relatório completo de due diligence de um imóvel rural.

    Aceita qualquer identificador: CAR, matrícula, SNCR, NIRF, CCIR,
    ITR, SIGEF, coordenadas, município ou CPF/CNPJ do proprietário.

    Fontes consultadas: SICAR/CAR, SIGEF/INCRA, Receita Federal,
    IBAMA, Lista Suja, análise geoespacial, crédito rural.
    """
    service = DueDiligenceService()
    return await service.generate_report(request)


@router.post("/due-diligence/pdf")
async def generate_due_diligence_pdf(request: PropertySearchRequest):
    """Gera relatório de due diligence em PDF."""
    service = DueDiligenceService()
    report = await service.generate_report(request)

    pdf_generator = PDFReportGenerator()
    pdf_bytes = pdf_generator.generate(report)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=due_diligence_{report.report_id}.pdf"
        },
    )


# === Atalhos por Persona ===

@router.post("/buyer")
async def buyer_report(request: PropertySearchRequest):
    """
    Relatório para COMPRADOR de imóvel rural.

    Foco: regularidade fundiária, ônus na matrícula, preço de mercado,
    sobreposições, embargos, situação do CAR/CCIR/ITR.
    """
    request.persona = PersonaType.BUYER
    service = DueDiligenceService()
    return await service.generate_report(request)


@router.post("/lawyer")
async def lawyer_report(request: PropertySearchRequest):
    """
    Relatório para ADVOGADO em diligência.

    Foco: processos judiciais, certidões negativas, regularidade
    documental completa, sobreposições, embargos, lista suja.
    """
    request.persona = PersonaType.LAWYER
    service = DueDiligenceService()
    return await service.generate_report(request)


@router.post("/investor")
async def investor_report(request: PropertySearchRequest):
    """
    Relatório para INVESTIDOR / banco / cooperativa.

    Foco: risco consolidado, crédito rural, preço de terra,
    produção agrícola da região, valuation.
    """
    request.persona = PersonaType.INVESTOR
    service = DueDiligenceService()
    return await service.generate_report(request)


# === Dossiê de Pessoa ===

@router.post("/person")
async def person_dossier(request: PersonSearchRequest):
    """
    Gera dossiê completo de uma pessoa (CPF/CNPJ).

    Inclui: dados cadastrais, imóveis vinculados, embargos IBAMA,
    lista suja, crédito rural, notícias públicas.
    """
    service = PersonIntelligenceService()
    return await service.generate_dossier(request)


# === Relatório de Região ===

@router.post("/region")
async def region_report(request: RegionSearchRequest):
    """
    Gera relatório de inteligência sobre uma região (município/estado).

    Inclui: estatísticas de imóveis, embargos na região, dados de
    produção agrícola, crédito rural, preços de terra, notícias locais.
    """
    service = RegionIntelligenceService()
    return await service.generate_report(request)
