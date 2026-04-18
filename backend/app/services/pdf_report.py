"""
Gerador de relatórios PDF de Due Diligence Rural.

Gera um PDF profissional com todas as informações coletadas,
análise de risco e recomendações.
"""

import io

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak  # noqa: F401
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY  # noqa: F401
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

from app.models.schemas import DueDiligenceReport, RiskLevel


# Brand colors (only available when reportlab is installed)
if HAS_REPORTLAB:
    GREEN = HexColor("#2D6A4F")
    RED = HexColor("#D62828")
    YELLOW = HexColor("#F77F00")
    GRAY = HexColor("#6C757D")
    LIGHT_GREEN = HexColor("#D8F3DC")
    LIGHT_RED = HexColor("#FFCDD2")
    LIGHT_YELLOW = HexColor("#FFF3CD")
    WHITE = HexColor("#FFFFFF")
    DARK = HexColor("#212529")

    def _risk_color(risk: RiskLevel):
        if risk == RiskLevel.CRITICAL:
            return RED
        elif risk == RiskLevel.HIGH:
            return HexColor("#E63946")
        elif risk == RiskLevel.MEDIUM:
            return YELLOW
        return GREEN

    def _risk_label(risk: RiskLevel) -> str:
        labels = {
            RiskLevel.LOW: "BAIXO",
            RiskLevel.MEDIUM: "MEDIO",
            RiskLevel.HIGH: "ALTO",
            RiskLevel.CRITICAL: "CRITICO",
        }
        return labels.get(risk, "N/A")

    def _risk_bg(risk: RiskLevel):
        if risk == RiskLevel.CRITICAL:
            return LIGHT_RED
        elif risk == RiskLevel.HIGH:
            return LIGHT_RED
        elif risk == RiskLevel.MEDIUM:
            return LIGHT_YELLOW
        return LIGHT_GREEN


class PDFReportGenerator:
    """Gera relatórios PDF de Due Diligence Rural."""

    def __init__(self):
        if not HAS_REPORTLAB:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Title"],
            fontSize=22,
            textColor=GREEN,
            spaceAfter=20,
        ))
        self.styles.add(ParagraphStyle(
            "SectionTitle",
            parent=self.styles["Heading2"],
            fontSize=14,
            textColor=GREEN,
            spaceBefore=15,
            spaceAfter=8,
            borderWidth=1,
            borderColor=GREEN,
            borderPadding=5,
        ))
        self.styles.add(ParagraphStyle(
            "BodyCustom",
            parent=self.styles["Normal"],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
        ))
        self.styles.add(ParagraphStyle(
            "SmallGray",
            parent=self.styles["Normal"],
            fontSize=8,
            textColor=GRAY,
        ))
        self.styles.add(ParagraphStyle(
            "RiskHigh",
            parent=self.styles["Normal"],
            fontSize=12,
            textColor=RED,
            alignment=TA_CENTER,
        ))

    @staticmethod
    def _safe(value, default="N/A") -> str:
        """Retorna valor formatado ou default se nulo."""
        if value is None:
            return default
        return str(value)

    @staticmethod
    def _safe_float_fmt(value, decimals=2, default="N/A") -> str:
        """Formata float ou retorna default se nulo."""
        if value is None:
            return default
        try:
            return f"{float(value):,.{decimals}f}"
        except (ValueError, TypeError):
            return default

    def generate(self, report: DueDiligenceReport) -> bytes:
        """Gera o PDF do relatório e retorna os bytes."""
        import logging
        logger = logging.getLogger("agrojus.pdf")

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        elements = []
        # Cada seção é protegida contra campos nulos
        section_builders = [
            self._build_header,
            self._build_risk_summary,
            self._build_compliance_section,
            self._build_property_section,
            self._build_registry_section,
            self._build_owner_section,
            self._build_environmental_section,
            self._build_labour_section,
            self._build_overlap_section,
            self._build_financial_section,
            self._build_details_section,
            self._build_sources_section,
            self._build_footer,
        ]
        for builder in section_builders:
            try:
                elements.extend(builder(report))
            except Exception as e:
                logger.warning("PDF section %s failed: %s", builder.__name__, e)
                # Adiciona mensagem de erro na seção em vez de crashar
                elements.append(Paragraph(
                    f"Secao indisponivel: {builder.__name__}",
                    self.styles["SmallGray"],
                ))
                elements.append(Spacer(1, 10))

        doc.build(elements)
        return buffer.getvalue()

    def _build_header(self, report: DueDiligenceReport) -> list:
        elements = []

        elements.append(Paragraph("AGROJUS", self.styles["CustomTitle"]))

        persona_labels = {
            "buyer": "Relatorio para Comprador de Imovel Rural",
            "lawyer": "Relatorio de Diligencia Juridica",
            "investor": "Relatorio de Analise para Investidor",
            "farmer": "Relatorio para Agropecuarista",
        }
        subtitle = persona_labels.get(
            report.persona.value if report.persona else "",
            "Relatorio de Due Diligence Rural",
        )
        elements.append(Paragraph(subtitle, self.styles["Heading3"]))
        elements.append(Spacer(1, 10))

        header_data = [
            ["ID do Relatorio:", report.report_id],
            ["Data de Geracao:", report.generated_at.strftime("%d/%m/%Y %H:%M UTC")],
        ]

        if report.property_info and report.property_info.car_code:
            header_data.append(["Codigo CAR:", report.property_info.car_code])
        if report.matricula_info and report.matricula_info.matricula_number:
            header_data.append(["Matricula:", report.matricula_info.matricula_number])
        if report.sncr_info and report.sncr_info.sncr_code:
            header_data.append(["SNCR:", report.sncr_info.sncr_code])
        if report.sncr_info and report.sncr_info.nirf:
            header_data.append(["NIRF:", report.sncr_info.nirf])
        if report.ccir_info and report.ccir_info.ccir_number:
            header_data.append(["CCIR:", report.ccir_info.ccir_number])

        if report.property_info and report.property_info.municipality:
            loc = f"{report.property_info.municipality}/{report.property_info.state or ''}"
            header_data.append(["Localizacao:", loc])

        table = Table(header_data, colWidths=[5 * cm, 12 * cm])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))
        return elements

    def _build_risk_summary(self, report: DueDiligenceReport) -> list:
        elements = []

        if not report.risk_score:
            return elements

        elements.append(Paragraph("RESUMO DE RISCO", self.styles["SectionTitle"]))

        rs = report.risk_score
        risk_data = [
            ["AREA", "NIVEL DE RISCO"],
            ["Risco Geral", _risk_label(rs.overall)],
            ["Regularidade Fundiaria", _risk_label(rs.land_tenure)],
            ["Ambiental", _risk_label(rs.environmental)],
            ["Juridico", _risk_label(rs.legal)],
            ["Trabalhista", _risk_label(rs.labor)],
            ["Financeiro", _risk_label(rs.financial)],
        ]

        table = Table(risk_data, colWidths=[9 * cm, 8 * cm])
        style_commands = [
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BACKGROUND", (0, 0), (-1, 0), GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWHEIGHT", (0, 0), (-1, -1), 25),
        ]

        # Color-code risk levels
        for i, row in enumerate(risk_data[1:], start=1):
            level_str = row[1]
            if level_str == "CRITICO":
                style_commands.append(("BACKGROUND", (1, i), (1, i), LIGHT_RED))
                style_commands.append(("TEXTCOLOR", (1, i), (1, i), RED))
            elif level_str == "ALTO":
                style_commands.append(("BACKGROUND", (1, i), (1, i), LIGHT_RED))
                style_commands.append(("TEXTCOLOR", (1, i), (1, i), RED))
            elif level_str == "MEDIO":
                style_commands.append(("BACKGROUND", (1, i), (1, i), LIGHT_YELLOW))
                style_commands.append(("TEXTCOLOR", (1, i), (1, i), YELLOW))
            else:
                style_commands.append(("BACKGROUND", (1, i), (1, i), LIGHT_GREEN))
                style_commands.append(("TEXTCOLOR", (1, i), (1, i), GREEN))

        table.setStyle(TableStyle(style_commands))
        elements.append(table)
        elements.append(Spacer(1, 15))
        return elements

    def _build_compliance_section(self, report: DueDiligenceReport) -> list:
        """Secao de compliance MCR 2.9 e EUDR."""
        elements = []

        if not report.compliance:
            return elements

        c = report.compliance
        elements.append(Paragraph("COMPLIANCE REGULATORIO", self.styles["SectionTitle"]))

        # Score geral
        score = c.get("overall_score", 0)
        risk = c.get("risk_level", "N/A")
        elements.append(Paragraph(
            f"Score Geral: {score}/1000 — Risco {risk}",
            self.styles["BodyCustom"],
        ))
        elements.append(Spacer(1, 8))

        # MCR 2.9
        mcr = c.get("mcr_29", {})
        mcr_status = "APROVADO" if mcr.get("passed") else "REPROVADO"
        mcr_color = GREEN if mcr.get("passed") else RED

        elements.append(Paragraph(
            f"MCR 2.9 (Credito Rural): {mcr_status} ({mcr.get('score', 0)}/100)",
            ParagraphStyle("MCRStatus", parent=self.styles["BodyCustom"],
                           textColor=mcr_color, fontSize=11),
        ))

        mcr_items = mcr.get("items", [])
        if mcr_items:
            data = [["Codigo", "Requisito", "Status"]]
            for item in mcr_items:
                status = "OK" if item.get("passed") else "FALHA"
                data.append([
                    item.get("code", ""),
                    item.get("description", ""),
                    status,
                ])
            table = Table(data, colWidths=[3 * cm, 10 * cm, 4 * cm])
            style_cmds = [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, 0), GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
                ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ]
            for i, item in enumerate(mcr_items, start=1):
                if not item.get("passed"):
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_RED))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), RED))
                else:
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_GREEN))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), GREEN))
            table.setStyle(TableStyle(style_cmds))
            elements.append(table)

        elements.append(Spacer(1, 10))

        # EUDR
        eudr = c.get("eudr", {})
        eudr_status = "CONFORME" if eudr.get("passed") else "NAO CONFORME"
        eudr_color = GREEN if eudr.get("passed") else RED

        elements.append(Paragraph(
            f"EUDR (Regulamento UE Desmatamento): {eudr_status} ({eudr.get('score', 0)}/100)",
            ParagraphStyle("EUDRStatus", parent=self.styles["BodyCustom"],
                           textColor=eudr_color, fontSize=11),
        ))

        eudr_items = eudr.get("items", [])
        if eudr_items:
            data = [["Codigo", "Requisito", "Status"]]
            for item in eudr_items:
                status = "OK" if item.get("passed") else "FALHA"
                data.append([
                    item.get("code", ""),
                    item.get("description", ""),
                    status,
                ])
            table = Table(data, colWidths=[3 * cm, 10 * cm, 4 * cm])
            style_cmds = [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, 0), GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
                ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ]
            for i, item in enumerate(eudr_items, start=1):
                if not item.get("passed"):
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_RED))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), RED))
                else:
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_GREEN))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), GREEN))
            table.setStyle(TableStyle(style_cmds))
            elements.append(table)

        # Resumo
        summary = c.get("summary", "")
        if summary:
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(summary, self.styles["SmallGray"]))

        elements.append(Spacer(1, 15))
        return elements

    def _build_property_section(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Paragraph("DADOS DO IMOVEL", self.styles["SectionTitle"]))

        if report.property_info:
            pi = report.property_info
            data = [
                ["Codigo CAR:", self._safe(pi.car_code)],
                ["Status CAR:", self._safe(pi.status)],
                ["Area Total (ha):", self._safe_float_fmt(pi.area_total_ha)],
                ["APP (ha):", self._safe_float_fmt(pi.area_app_ha)],
                ["Reserva Legal (ha):", self._safe_float_fmt(pi.area_reserva_legal_ha)],
                ["Municipio:", self._safe(pi.municipality)],
                ["UF:", self._safe(pi.state)],
            ]
        else:
            data = [["Dados do CAR:", "Nao encontrados"]]

        if report.sigef_info:
            si = report.sigef_info
            data.append(["", ""])  # separator
            data.append(["Parcela SIGEF:", self._safe(si.parcel_code)])
            data.append(["Certificada:", "Sim" if si.certified else "Nao"])
            data.append(["Area SIGEF (ha):", self._safe_float_fmt(si.area_ha)])
            data.append(["Data Certificacao:", self._safe(si.certification_date)])

        table = Table(data, colWidths=[6 * cm, 11 * cm])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 15))
        return elements

    def _build_owner_section(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Paragraph("DADOS DO PROPRIETARIO", self.styles["SectionTitle"]))

        if report.owner_info:
            oi = report.owner_info
            data = [
                ["CNPJ:", oi.cnpj],
                ["Razao Social:", oi.razao_social or "N/A"],
                ["Nome Fantasia:", oi.nome_fantasia or "N/A"],
                ["Situacao Cadastral:", oi.situacao_cadastral or "N/A"],
                ["CNAE Principal:", oi.cnae_principal or "N/A"],
                ["Endereco:", oi.endereco or "N/A"],
                ["Municipio/UF:", f"{oi.municipio or ''}/{oi.uf or ''}"],
            ]

            if oi.socios:
                data.append(["", ""])
                data.append(["SOCIOS:", ""])
                for socio in oi.socios:
                    nome = socio.get("nome", "N/A")
                    qual = socio.get("qualificacao", "")
                    data.append(["", f"{nome} ({qual})"])
        else:
            data = [["Dados do Proprietario:", "Nao encontrados (informe CPF/CNPJ para consulta)"]]

        table = Table(data, colWidths=[6 * cm, 11 * cm])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 15))
        return elements

    def _build_environmental_section(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Paragraph("SITUACAO AMBIENTAL (IBAMA)", self.styles["SectionTitle"]))

        if report.ibama_embargos:
            elements.append(Paragraph(
                f"ATENCAO: {len(report.ibama_embargos)} embargo(s) encontrado(s)",
                self.styles["RiskHigh"],
            ))
            elements.append(Spacer(1, 5))

            for embargo in report.ibama_embargos[:5]:
                data = [
                    ["Auto de Infracao:", embargo.auto_infracao or "N/A"],
                    ["Area Embargada (ha):", self._safe_float_fmt(embargo.area_embargada_ha)],
                    ["Data:", embargo.data_embargo or "N/A"],
                    ["Descricao:", embargo.descricao or "N/A"],
                    ["Status:", embargo.status or "N/A"],
                ]
                table = Table(data, colWidths=[6 * cm, 11 * cm])
                table.setStyle(TableStyle([
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_RED),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 5))
        else:
            elements.append(Paragraph(
                "Nenhum embargo IBAMA encontrado.",
                self.styles["BodyCustom"],
            ))

        elements.append(Spacer(1, 15))
        return elements

    def _build_labour_section(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Paragraph("LISTA SUJA - TRABALHO ESCRAVO", self.styles["SectionTitle"]))

        if report.slave_labour:
            elements.append(Paragraph(
                "ATENCAO: Proprietario encontrado na Lista Suja do Trabalho Escravo",
                self.styles["RiskHigh"],
            ))
            for entry in report.slave_labour:
                data = [
                    ["Empregador:", entry.employer_name or "N/A"],
                    ["Estabelecimento:", entry.establishment or "N/A"],
                    ["Municipio/UF:", f"{entry.municipality or ''}/{entry.state or ''}"],
                    ["Trabalhadores Resgatados:", str(entry.workers_rescued or 0)],
                    ["Data Fiscalizacao:", entry.inspection_date or "N/A"],
                ]
                table = Table(data, colWidths=[6 * cm, 11 * cm])
                table.setStyle(TableStyle([
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_RED),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                elements.append(table)
        else:
            elements.append(Paragraph(
                "Nenhum registro na Lista Suja do Trabalho Escravo.",
                self.styles["BodyCustom"],
            ))

        elements.append(Spacer(1, 15))
        return elements

    def _build_overlap_section(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Paragraph("ANALISE DE SOBREPOSICAO GEOESPACIAL", self.styles["SectionTitle"]))

        if report.overlap_analysis:
            oa = report.overlap_analysis
            data = [
                ["Sobreposicao com Terra Indigena:", "SIM" if oa.overlaps_indigenous_land else "NAO"],
                ["Sobreposicao com Unidade de Conservacao:", "SIM" if oa.overlaps_conservation_unit else "NAO"],
                ["Sobreposicao com Area Embargada:", "SIM" if oa.overlaps_embargo else "NAO"],
                ["Alerta de Desmatamento:", "SIM" if oa.overlaps_deforestation else "NAO"],
            ]

            if oa.indigenous_land_name:
                data.append(["TI:", oa.indigenous_land_name])
            if oa.conservation_unit_name:
                data.append(["UC:", oa.conservation_unit_name])

            table = Table(data, colWidths=[9 * cm, 8 * cm])
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph(
                "Analise geoespacial nao disponivel (geometria do imovel nao encontrada).",
                self.styles["BodyCustom"],
            ))

        elements.append(Spacer(1, 15))
        return elements

    def _build_details_section(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Paragraph("DETALHAMENTO", self.styles["SectionTitle"]))

        if report.risk_score and report.risk_score.details:
            for detail in report.risk_score.details:
                elements.append(Paragraph(f"- {detail}", self.styles["BodyCustom"]))
        else:
            elements.append(Paragraph(
                "Sem observacoes adicionais.",
                self.styles["BodyCustom"],
            ))

        elements.append(Spacer(1, 15))
        return elements

    def _build_registry_section(self, report: DueDiligenceReport) -> list:
        """Seção de dados registrais (matrícula, SNCR, CCIR, ITR)."""
        elements = []

        has_registry = (
            report.matricula_info or report.sncr_info
            or report.ccir_info or report.itr_info
        )
        if not has_registry:
            return elements

        elements.append(Paragraph("DADOS REGISTRAIS E CADASTRAIS", self.styles["SectionTitle"]))

        data = []

        if report.matricula_info:
            mi = report.matricula_info
            data.append(["--- MATRICULA ---", ""])
            data.append(["Numero:", mi.matricula_number or "N/A"])
            data.append(["Cartorio:", mi.cartorio or "N/A"])
            data.append(["Comarca:", mi.comarca or "N/A"])
            data.append(["Onus/Gravames:", "SIM" if mi.has_onus else "NAO" if mi.has_onus is not None else "N/A"])
            if mi.onus_description:
                data.append(["Descricao:", mi.onus_description])

        if report.sncr_info:
            si = report.sncr_info
            data.append(["--- SNCR/INCRA ---", ""])
            data.append(["Codigo SNCR:", si.sncr_code or "N/A"])
            data.append(["NIRF:", si.nirf or "N/A"])
            data.append(["Nome do Imovel:", si.property_name or "N/A"])
            data.append(["Classificacao:", si.classification or "N/A"])
            data.append(["Modulos Fiscais:", self._safe_float_fmt(si.modules_fiscais, 1)])

        if report.ccir_info:
            ci = report.ccir_info
            data.append(["--- CCIR ---", ""])
            data.append(["Numero CCIR:", ci.ccir_number or "N/A"])
            data.append(["Valido:", "SIM" if ci.valid else "NAO" if ci.valid is not None else "N/A"])
            data.append(["Vencimento:", ci.expiration_date or "N/A"])

        if report.itr_info:
            it = report.itr_info
            data.append(["--- ITR ---", ""])
            data.append(["NIRF:", it.nirf or "N/A"])
            data.append(["Ano:", str(it.year) if it.year else "N/A"])
            data.append(["VTI (R$):", self._safe_float_fmt(it.vti)])
            data.append(["Status Pagamento:", it.status_pagamento or "N/A"])

        if data:
            table = Table(data, colWidths=[6 * cm, 11 * cm])
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            elements.append(table)

        elements.append(Spacer(1, 15))
        return elements

    def _build_financial_section(self, report: DueDiligenceReport) -> list:
        """Seção de dados financeiros (crédito rural, preços de terra)."""
        elements = []

        if not report.financial_summary:
            return elements

        elements.append(Paragraph("DADOS FINANCEIROS", self.styles["SectionTitle"]))

        fs = report.financial_summary
        data = []

        if fs.total_credit_amount and fs.total_credit_amount > 0:
            data.append(["Credito Rural Total:", f"R$ {self._safe_float_fmt(fs.total_credit_amount)}"])
            data.append(["Operacoes:", str(len(fs.rural_credits))])

        if fs.avg_land_price_per_ha:
            data.append(["Preco Medio Terra (regiao):", f"R$ {self._safe_float_fmt(fs.avg_land_price_per_ha)}/ha"])

        if fs.land_prices:
            for lp in fs.land_prices[:3]:
                data.append([
                    f"  {lp.land_type or 'Terra'}:",
                    f"R$ {self._safe_float_fmt(lp.price_per_ha)}/ha" if lp.price_per_ha else "N/A",
                ])

        if data:
            table = Table(data, colWidths=[6 * cm, 11 * cm])
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph(
                "Dados financeiros nao disponiveis para esta consulta.",
                self.styles["BodyCustom"],
            ))

        elements.append(Spacer(1, 15))
        return elements

    def _build_sources_section(self, report: DueDiligenceReport) -> list:
        """Seção de fontes consultadas."""
        elements = []

        if not report.sources_consulted:
            return elements

        elements.append(Paragraph("FONTES CONSULTADAS", self.styles["SectionTitle"]))
        for source in report.sources_consulted:
            elements.append(Paragraph(f"- {source}", self.styles["BodyCustom"]))
        elements.append(Spacer(1, 15))
        return elements

    def _build_footer(self, report: DueDiligenceReport) -> list:
        elements = []
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            "AVISO LEGAL: Este relatorio foi gerado automaticamente com base em dados publicos "
            "disponiveis nas fontes indicadas. As informacoes sao fornecidas 'como estao' e nao "
            "substituem a analise juridica profissional. Recomenda-se a verificacao independente "
            "de todas as informacoes antes da tomada de decisao.",
            self.styles["SmallGray"],
        ))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            f"Gerado por AgroJus em {report.generated_at.strftime('%d/%m/%Y %H:%M UTC')} | "
            f"ID: {report.report_id}",
            self.styles["SmallGray"],
        ))
        return elements
