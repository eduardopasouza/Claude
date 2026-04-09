"""Rotas de geração de relatórios de due diligence."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io

from app.models.schemas import PropertySearchRequest
from app.services.due_diligence import DueDiligenceService
from app.services.pdf_report import PDFReportGenerator

router = APIRouter()


@router.post("/due-diligence")
async def generate_due_diligence(request: PropertySearchRequest):
    """
    Gera um relatório de due diligence rural completo.

    Coleta dados de: SICAR/CAR, SIGEF/INCRA, Receita Federal,
    IBAMA (embargos), Lista Suja (trabalho escravo).
    """
    service = DueDiligenceService()
    report = await service.generate_report(request)
    return report


@router.post("/due-diligence/pdf")
async def generate_due_diligence_pdf(request: PropertySearchRequest):
    """
    Gera um relatório de due diligence rural em formato PDF.
    """
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
