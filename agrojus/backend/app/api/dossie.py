"""
API do Dossiê Agrofundiário — endpoint único que aceita múltiplas entradas
e devolve relatório completo multi-persona.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.dossie_generator import gerar_dossie

logger = logging.getLogger("agrojus.dossie_api")
router = APIRouter()


class DossieRequest(BaseModel):
    # Identificadores (pelo menos um obrigatório)
    car_code: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    matricula: Optional[str] = None
    sigef_code: Optional[str] = None

    # Geometria direta (GeoJSON Polygon/MultiPolygon)
    geometry: Optional[dict] = None

    # Ponto + raio
    point: Optional[dict] = None  # {"lat": ..., "lon": ...}
    radius_km: Optional[float] = 5

    # Bounding box
    bbox: Optional[list[float]] = None  # [w, s, e, n]

    # Município
    municipio_ibge: Optional[str] = None

    # Metadata
    persona: Optional[str] = "geral"
    name: Optional[str] = None


@router.post("")
@router.post("/")
def gerar_dossie_endpoint(req: DossieRequest):
    """
    Gera dossiê consolidado multi-persona.

    Aceita um dentre: `car_code`, `geometry`, `point` (+ radius_km), `bbox`,
    `municipio_ibge` ou `cpf_cnpj`.
    """
    body = req.model_dump(exclude_none=True)
    if not any(body.get(k) for k in (
        "car_code", "cpf_cnpj", "geometry", "point", "bbox", "municipio_ibge"
    )):
        raise HTTPException(
            status_code=400,
            detail="Informe ao menos um: car_code, cpf_cnpj, geometry, point, bbox ou municipio_ibge",
        )

    try:
        return gerar_dossie(body)
    except Exception as e:
        logger.exception("dossie falhou")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@router.post("/pdf")
def gerar_dossie_pdf(req: DossieRequest):
    """Exporta dossiê como PDF extenso (25-45 páginas A4)."""
    body = req.model_dump(exclude_none=True)
    if not any(body.get(k) for k in (
        "car_code", "cpf_cnpj", "geometry", "point", "bbox", "municipio_ibge"
    )):
        raise HTTPException(status_code=400, detail="Informe ao menos um identificador ou geometria")

    from app.services.dossie_pdf import render_dossie_pdf
    import io
    dossie = gerar_dossie(body)

    try:
        pdf_bytes = render_dossie_pdf(dossie)
    except Exception as exc:
        logger.exception("erro ao renderizar PDF")
        raise HTTPException(status_code=500, detail=f"Erro PDF: {exc}")

    from fastapi.responses import StreamingResponse
    filename = f"dossie_{dossie['dossie_id']}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/_legacy_pdf")
def gerar_dossie_pdf_legacy(req: DossieRequest):
    """Versão simples antiga (fallback)."""
    import io
    body = req.model_dump(exclude_none=True)
    if not any(body.get(k) for k in (
        "car_code", "cpf_cnpj", "geometry", "point", "bbox", "municipio_ibge"
    )):
        raise HTTPException(status_code=400, detail="Informe ao menos um identificador ou geometria")

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
        )
        from reportlab.lib.enums import TA_JUSTIFY
    except ImportError:
        raise HTTPException(status_code=500, detail="reportlab não instalado")

    dossie = gerar_dossie(body)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        rightMargin=1.5 * cm, leftMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )

    GREEN = HexColor("#22C55E")
    DARK = HexColor("#0F172A")
    GRAY = HexColor("#64748B")
    RED = HexColor("#DC2626")
    LIGHT_GRAY = HexColor("#F1F5F9")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("DTitle", parent=styles["Title"], fontSize=20, textColor=GREEN, spaceAfter=8))
    styles.add(ParagraphStyle("DSection", parent=styles["Heading2"], fontSize=13, textColor=DARK, spaceBefore=14, spaceAfter=6, borderColor=GREEN))
    styles.add(ParagraphStyle("DBody", parent=styles["Normal"], fontSize=10, leading=13, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle("DSmall", parent=styles["Normal"], fontSize=8, textColor=GRAY))

    e: list = []
    ctx = dossie["contexto"]
    rec = dossie["recomendacao"]

    # CAPA
    e.append(Paragraph("AGROJUS · DOSSIÊ AGROFUNDIÁRIO", styles["DTitle"]))
    e.append(Paragraph(dossie["title"], styles["Heading3"]))
    e.append(Spacer(1, 10))
    capa = [
        ["Tipo de entrada:", ctx.get("input_type", "")],
        ["Área:", f"{ctx.get('area_ha') or 0:,.2f} ha"],
        ["Localização:", f"{ctx.get('municipio','')}/{ctx.get('uf','')}"],
        ["Bioma:", ctx.get("bioma", "—")],
        ["Persona:", rec["persona"]],
        ["Status:", rec["overall_status"].upper()],
        ["Risco:", rec["risk_level"]],
        ["Score MCR 2.9:", f"{rec['score']}/1000"],
        ["Gerado em:", dossie["generated_at"]],
    ]
    if ctx.get("car_code"):
        capa.insert(1, ["CAR:", ctx["car_code"]])
    if ctx.get("cpf_cnpj_mask"):
        capa.insert(1, ["CPF/CNPJ:", ctx["cpf_cnpj_mask"]])
    t = Table(capa, colWidths=[4 * cm, 14 * cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    e.append(t)
    e.append(Spacer(1, 12))

    # Red flags
    if rec["red_flags"]:
        e.append(Paragraph("🚨 PONTOS DE ATENÇÃO (RED FLAGS)", styles["DSection"]))
        for f in rec["red_flags"]:
            e.append(Paragraph(
                f"• {f}",
                ParagraphStyle("Red", parent=styles["DBody"], textColor=RED, fontName="Helvetica-Bold"),
            ))
        e.append(Spacer(1, 8))

    # Recomendação por persona
    if rec["tips"]:
        e.append(Paragraph(f"RECOMENDAÇÃO · {rec['persona'].upper()}", styles["DSection"]))
        for t_ in rec["tips"]:
            e.append(Paragraph(f"• {t_}", styles["DBody"]))
        e.append(Spacer(1, 10))

    # SEÇÕES principais com summary
    secoes = dossie["secoes"]
    section_titles = [
        ("identificacao", "1. IDENTIFICAÇÃO TERRITORIAL"),
        ("fundiario", "2. SITUAÇÃO FUNDIÁRIA"),
        ("compliance", "3. COMPLIANCE REGULATÓRIO (MCR 2.9)"),
        ("ambiental", "4. SITUAÇÃO AMBIENTAL"),
        ("proprietario", "5. DOSSIÊ DO PROPRIETÁRIO"),
        ("credito_rural", "6. CRÉDITO RURAL VINCULADO"),
        ("mercado", "7. MERCADO DE COMMODITIES (UF)"),
        ("logistica", "8. LOGÍSTICA (KNN)"),
        ("energia", "9. ENERGIA (ANEEL)"),
        ("valuation", "10. VALUATION ESTIMATIVO"),
        ("juridico", "11. SITUAÇÃO JURÍDICA"),
        ("agronomia", "12. AGRONOMIA E COBERTURA"),
    ]

    for key, title in section_titles:
        d = secoes.get(key, {})
        if not d or (isinstance(d, dict) and d.get("note")):
            continue
        e.append(Paragraph(title, styles["DSection"]))
        # Renderiza dict como tabela simples
        rows = []
        for k, v in (d.items() if isinstance(d, dict) else []):
            if k == "error":
                continue
            if isinstance(v, list):
                rows.append([_fmt_key(k), f"{len(v)} item(ns)"])
                for item in v[:3]:
                    if isinstance(item, dict):
                        rows.append(["  ", ", ".join(f"{kk}={vv}" for kk, vv in list(item.items())[:3])])
            elif isinstance(v, dict):
                rows.append([_fmt_key(k), ""])
                for kk, vv in list(v.items())[:5]:
                    rows.append([f"  {_fmt_key(kk)}", str(vv)[:80]])
            else:
                rows.append([_fmt_key(k), str(v)[:100]])
        if rows:
            t = Table(rows, colWidths=[6 * cm, 12 * cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_GRAY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
            ]))
            e.append(t)
        e.append(Spacer(1, 6))

    # Metadata
    e.append(PageBreak())
    e.append(Paragraph("FONTES E AVISOS", styles["DSection"]))
    e.append(Paragraph(
        "<b>Fontes consultadas:</b> " + ", ".join(dossie["metadata"]["fontes"]),
        styles["DBody"],
    ))
    e.append(Spacer(1, 8))
    for c in dossie["metadata"]["caveats"]:
        e.append(Paragraph(f"• {c}", styles["DSmall"]))

    doc.build(e)
    buf.seek(0)

    from fastapi.responses import StreamingResponse
    filename = f"dossie_{dossie['dossie_id']}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def _fmt_key(k: str) -> str:
    return k.replace("_", " ").capitalize()
