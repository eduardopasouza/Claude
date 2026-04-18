"""
Geração de PDF extenso do Dossiê Agrofundiário.

Produz relatório profissional multi-página (tipicamente 25-45 páginas) com:
  - Capa formal + identificação
  - Sumário executivo com red flags + scores consolidados
  - Análises cruzadas (correlações entre fontes)
  - 12 seções temáticas detalhadas (cada overlap listado individualmente)
  - Apêndice com fontes, metodologia e caveats

Depende apenas de reportlab (A4).
"""

from __future__ import annotations

import io
from datetime import datetime, timezone
from typing import Any


def render_dossie_pdf(dossie: dict) -> bytes:
    """Renderiza o dossiê completo em PDF A4."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
        KeepTogether, HRFlowable,
    )
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

    GREEN = HexColor("#22C55E")
    DARK = HexColor("#0F172A")
    SLATE = HexColor("#334155")
    GRAY = HexColor("#64748B")
    LIGHT_GRAY = HexColor("#F1F5F9")
    WHITE = HexColor("#FFFFFF")
    RED = HexColor("#DC2626")
    LIGHT_RED = HexColor("#FEE2E2")
    AMBER = HexColor("#D97706")
    LIGHT_AMBER = HexColor("#FEF3C7")
    LIGHT_GREEN = HexColor("#D1FAE5")
    BLUE = HexColor("#2563EB")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("DCover", parent=styles["Title"], fontSize=28, textColor=GREEN, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle("DH1", parent=styles["Heading1"], fontSize=18, textColor=DARK, spaceBefore=14, spaceAfter=10,
                               borderPadding=4, backColor=LIGHT_GRAY))
    styles.add(ParagraphStyle("DH2", parent=styles["Heading2"], fontSize=13, textColor=GREEN, spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle("DH3", parent=styles["Heading3"], fontSize=11, textColor=SLATE, spaceBefore=6, spaceAfter=4))
    styles.add(ParagraphStyle("DBody", parent=styles["Normal"], fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=4))
    styles.add(ParagraphStyle("DBold", parent=styles["Normal"], fontSize=10, leading=14, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle("DCenter", parent=styles["Normal"], fontSize=10, alignment=TA_CENTER))
    styles.add(ParagraphStyle("DSmall", parent=styles["Normal"], fontSize=8, textColor=GRAY, leading=11))
    styles.add(ParagraphStyle("DRedAlert", parent=styles["Normal"], fontSize=10, textColor=RED, fontName="Helvetica-Bold", leading=13))
    styles.add(ParagraphStyle("DAmberAlert", parent=styles["Normal"], fontSize=10, textColor=AMBER, fontName="Helvetica-Bold", leading=13))
    styles.add(ParagraphStyle("DDiscreet", parent=styles["Normal"], fontSize=9, textColor=GRAY, leading=12, alignment=TA_JUSTIFY))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        rightMargin=1.8 * cm, leftMargin=1.8 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title=dossie.get("title", "Dossiê Agrofundiário"),
    )

    ctx = dossie["contexto"]
    rec = dossie["recomendacao"]
    ac = dossie.get("analises_cruzadas", {})
    secoes = dossie["secoes"]

    e: list = []

    # ================= CAPA =================
    e.append(Spacer(1, 80))
    e.append(Paragraph("AGROJUS", styles["DCover"]))
    e.append(Paragraph("Dossiê Agrofundiário Completo", ParagraphStyle(
        "CoverSub", parent=styles["Normal"], fontSize=14, alignment=TA_CENTER, textColor=SLATE,
    )))
    e.append(Spacer(1, 30))
    e.append(Paragraph(dossie.get("title", ""), ParagraphStyle(
        "CoverTitle", parent=styles["Normal"], fontSize=16, alignment=TA_CENTER,
        textColor=DARK, spaceAfter=20,
    )))
    # Dados de capa em tabela
    capa_data = [
        ["Tipo de entrada:", ctx.get("input_type", "—").replace("_", " ").title()],
        ["Área:", f"{ctx.get('area_ha') or 0:,.2f} ha"],
        ["Localização:", f"{ctx.get('municipio') or '—'}/{ctx.get('uf') or '—'}"],
        ["Bioma:", ctx.get("bioma") or "—"],
    ]
    if ctx.get("car_code"):
        capa_data.append(["Código CAR:", ctx["car_code"]])
    if ctx.get("cpf_cnpj_mask"):
        capa_data.append(["CPF/CNPJ:", ctx["cpf_cnpj_mask"]])
    capa_data.extend([
        ["Centróide:", f"{(ctx.get('centroid') or {}).get('lat', 0):.5f}, {(ctx.get('centroid') or {}).get('lon', 0):.5f}"],
        ["Persona:", rec.get("persona", "—").capitalize()],
        ["Data de geração:", datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")],
        ["ID do dossiê:", dossie.get("dossie_id", "")],
    ])
    t = Table(capa_data, colWidths=[5 * cm, 11 * cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    e.append(t)
    e.append(Spacer(1, 30))
    e.append(HRFlowable(width="50%", thickness=0.5, color=GRAY, hAlign="CENTER"))
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        "Relatório técnico gerado automaticamente pelo sistema AgroJus a partir de fontes públicas oficiais",
        styles["DSmall"],
    ))
    e.append(PageBreak())

    # ================= ÍNDICE =================
    e.append(Paragraph("ÍNDICE", styles["DH1"]))
    toc = [
        ["1.", "Sumário executivo"],
        ["2.", "Análises cruzadas"],
        ["3.", "Identificação territorial"],
        ["4.", "Situação fundiária"],
        ["5.", "Compliance regulatório (MCR 2.9)"],
        ["6.", "Situação ambiental"],
        ["7.", "Dossiê do proprietário"],
        ["8.", "Crédito rural vinculado"],
        ["9.", "Mercado de commodities"],
        ["10.", "Logística e infraestrutura"],
        ["11.", "Energia (ANEEL)"],
        ["12.", "Valuation NBR 14.653-3"],
        ["13.", "Situação jurídica"],
        ["14.", "Agronomia e cobertura do solo"],
        ["15.", "Recomendação por persona"],
        ["16.", "Apêndice — fontes, metodologia e caveats"],
    ]
    t = Table(toc, colWidths=[1.5 * cm, 14 * cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    e.append(t)
    e.append(PageBreak())

    # ================= 1. SUMÁRIO EXECUTIVO =================
    e.append(Paragraph("1. SUMÁRIO EXECUTIVO", styles["DH1"]))
    # Classificação geral
    status = rec.get("overall_status", "?")
    risk = rec.get("risk_level", "?")
    score = rec.get("score", 0)
    status_label = {
        "approved": "APTO",
        "restricted": "RESTRITO",
        "blocked": "BLOQUEADO",
        "indeterminate": "INDETERMINADO",
    }.get(status, status.upper())
    status_color = {
        "approved": (LIGHT_GREEN, GREEN),
        "restricted": (LIGHT_AMBER, AMBER),
        "blocked": (LIGHT_RED, RED),
        "indeterminate": (LIGHT_GRAY, SLATE),
    }.get(status, (LIGHT_GRAY, SLATE))

    classif = [
        ["Classificação", status_label],
        ["Risco MCR 2.9", risk],
        ["Score MCR 2.9", f"{score}/1000"],
    ]
    # Scores domínio
    scores_dom = ac.get("scores_dominio", {})
    if scores_dom:
        classif += [
            ["Score Ambiental", f"{scores_dom.get('ambiental', 0)}/100"],
            ["Score Fundiário", f"{scores_dom.get('fundiario', 0)}/100"],
            ["Score Proprietário", f"{scores_dom.get('proprietario', 0)}/100"],
            ["Score Consolidado", f"{scores_dom.get('consolidado', 0)}/100 "
             f"({(ac.get('semaforo') or '—').upper()})"],
        ]
    t = Table(classif, colWidths=[6 * cm, 11 * cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BACKGROUND", (1, 0), (1, 0), status_color[0]),
        ("TEXTCOLOR", (1, 0), (1, 0), status_color[1]),
        ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (1, 0), (1, 0), 14),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    e.append(t)
    e.append(Spacer(1, 10))

    # Red flags
    red_flags = rec.get("red_flags") or []
    if red_flags:
        e.append(Paragraph("1.1. Pontos de atenção (Red Flags)", styles["DH2"]))
        for f in red_flags:
            e.append(Paragraph(f"⚠ {f}", styles["DRedAlert"]))
            e.append(Spacer(1, 4))
    else:
        e.append(Paragraph("1.1. Pontos de atenção", styles["DH2"]))
        e.append(Paragraph("Nenhum apontamento crítico identificado.", styles["DBody"]))
    e.append(PageBreak())

    # ================= 2. ANÁLISES CRUZADAS =================
    e.append(Paragraph("2. ANÁLISES CRUZADAS", styles["DH1"]))
    e.append(Paragraph(
        "Esta seção identifica correlações entre diferentes fontes que isoladamente "
        "poderiam passar despercebidas. Cada análise cruzada é uma detecção automática "
        "de padrões de risco que normalmente levariam horas de trabalho manual.",
        styles["DBody"],
    ))
    e.append(Spacer(1, 6))
    if ac.get("analises"):
        for i, a in enumerate(ac["analises"], 1):
            sev = a.get("severidade", "")
            color = (LIGHT_RED, RED) if sev == "bloqueante" else (LIGHT_AMBER, AMBER) if sev == "critico" else (LIGHT_GRAY, SLATE)
            e.append(Paragraph(f"2.{i}. {a.get('titulo', '')}", styles["DH3"]))
            box = Table([
                [Paragraph(f"<b>Severidade:</b> {sev.upper()}", styles["DBody"])],
                [Paragraph(a.get("descricao", ""), styles["DBody"])],
                [Paragraph(f"<b>Ação recomendada:</b> {a.get('acao', '—')}", styles["DBody"])],
            ], colWidths=[17 * cm])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), color[0]),
                ("BOX", (0, 0), (-1, -1), 1, color[1]),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            e.append(box)
            e.append(Spacer(1, 8))
    else:
        e.append(Paragraph(
            "Nenhuma correlação crítica detectada entre as fontes — área com perfil de baixo risco.",
            styles["DBody"],
        ))
    e.append(PageBreak())

    # ================= 3. IDENTIFICAÇÃO =================
    _render_section(e, styles, "3. IDENTIFICAÇÃO TERRITORIAL", secoes.get("identificacao"))
    e.append(PageBreak())

    # ================= 4. FUNDIÁRIO (detalhado) =================
    e.append(Paragraph("4. SITUAÇÃO FUNDIÁRIA", styles["DH1"]))
    fund = secoes.get("fundiario") or {}
    layer_meta = [
        ("cars_sobrepostos", "4.1. Outros CARs sobrepostos", "Sobreposição com outros cadastros ambientais rurais"),
        ("sigef_parcelas", "4.2. SIGEF/INCRA — Parcelas Certificadas", "Parcelas georreferenciadas certificadas pelo INCRA (pós-2013)"),
        ("terras_indigenas", "4.3. Terras Indígenas (FUNAI)", "Terras indígenas demarcadas, homologadas ou em estudo"),
        ("unidades_conservacao", "4.4. Unidades de Conservação (ICMBio/estaduais)", "UCs federais e estaduais (proteção integral e uso sustentável)"),
        ("assentamentos_incra", "4.5. Assentamentos INCRA", "Projetos de reforma agrária federal"),
        ("quilombolas_incra", "4.6. Áreas Quilombolas", "Territórios quilombolas (INCRA/Palmares)"),
        ("sigmine", "4.7. Processos Minerários (SIGMINE/ANM)", "Processos minerários registrados na Agência Nacional de Mineração"),
    ]
    for key, titulo, desc in layer_meta:
        d = fund.get(key) or {}
        items = d.get("items", [])
        e.append(Paragraph(titulo, styles["DH2"]))
        e.append(Paragraph(desc, styles["DSmall"]))
        if not items:
            e.append(Paragraph("Nenhuma sobreposição detectada.", styles["DDiscreet"]))
        else:
            # Tabela resumo
            resumo = [
                ["Sobreposições:", str(d.get("count", 0))],
                ["Área total interseção:", f"{d.get('total_intersecao_ha', 0):.2f} ha"],
                ["% do imóvel:", f"{d.get('pct_do_imovel', 0):.2f}%"],
            ]
            t = Table(resumo, colWidths=[5 * cm, 8 * cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            e.append(t)
            e.append(Spacer(1, 4))
            # Tabela com features
            _render_items_table(e, items, styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
        e.append(Spacer(1, 6))
    e.append(PageBreak())

    # ================= 5. COMPLIANCE =================
    e.append(Paragraph("5. COMPLIANCE REGULATÓRIO (MCR 2.9)", styles["DH1"]))
    comp = secoes.get("compliance") or {}
    if comp.get("axis_scores"):
        e.append(Paragraph(
            "Avaliação nos 32 critérios da Resolução CMN 5.193/2024 (Crédito Rural) "
            "agrupados em 5 eixos: Fundiário, Ambiental, Trabalhista, Jurídico e Financeiro.",
            styles["DBody"],
        ))
        # Tabela de scores
        ax_data = [["Eixo", "Aprovados", "Falhas", "Pendentes", "N/A", "Score %"]]
        for a in comp["axis_scores"]:
            ax_data.append([
                a["label"], str(a["passed"]), str(a["failed"]),
                str(a["pending"]), str(a["not_applicable"]),
                f"{a['weighted_score']:.1f}%",
            ])
        t = Table(ax_data, colWidths=[4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2 * cm, 3 * cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ]))
        e.append(t)
        e.append(Spacer(1, 10))

        # Detalhes dos 32 critérios agrupados por eixo
        axes_with_crits = {a["axis"]: a for a in comp["axis_scores"]}
        criterios_por_axis: dict[str, list] = {}
        for c in comp.get("criteria") or []:
            criterios_por_axis.setdefault(c["axis"], []).append(c)

        for axis_id, axis_data in axes_with_crits.items():
            crits = criterios_por_axis.get(axis_id, [])
            if not crits:
                continue
            e.append(Paragraph(f"5.{list(axes_with_crits).index(axis_id)+1}. {axis_data['label']}", styles["DH2"]))
            rows = [["Código", "Critério", "Status", "Peso"]]
            status_label_map = {
                "passed": "Aprovado", "failed": "FALHA",
                "pending": "Pendente", "not_applicable": "N/A",
            }
            for c in crits:
                rows.append([
                    c["code"],
                    c["title"],
                    status_label_map.get(c["status"], c["status"]),
                    f"{c['weight']:.1f}",
                ])
            t = Table(rows, colWidths=[2.3 * cm, 10.7 * cm, 2.5 * cm, 1.5 * cm])
            style_cmds = [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GRAY),
                ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
                ("ALIGN", (2, 0), (3, -1), "CENTER"),
            ]
            for i, c in enumerate(crits, start=1):
                if c["status"] == "failed":
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_RED))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), RED))
                elif c["status"] == "passed":
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_GREEN))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), GREEN))
                elif c["status"] == "pending":
                    style_cmds.append(("BACKGROUND", (2, i), (2, i), LIGHT_AMBER))
                    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), AMBER))
            t.setStyle(TableStyle(style_cmds))
            e.append(t)
            e.append(Spacer(1, 4))
            # Detalhamento: apenas falhas e pendentes
            for c in crits:
                if c["status"] in ("failed", "pending"):
                    txt = f"<b>{c['code']}:</b> {c['details']}  <i>({c['regulation']})</i>"
                    e.append(Paragraph(txt, styles["DBody"]))
            e.append(Spacer(1, 6))
    else:
        e.append(Paragraph("Compliance não avaliado.", styles["DBody"]))
    e.append(PageBreak())

    # ================= 6. AMBIENTAL =================
    e.append(Paragraph("6. SITUAÇÃO AMBIENTAL", styles["DH1"]))
    amb = secoes.get("ambiental") or {}
    # 6.1 PRODES por ano
    e.append(Paragraph("6.1. PRODES (desmatamento consolidado por ano)", styles["DH2"]))
    prodes_itens = amb.get("prodes_por_ano") or []
    if prodes_itens:
        _render_items_table(e, prodes_itens, styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
        e.append(Paragraph(
            f"<b>Total pós-2019:</b> {amb.get('prodes_total_pos_2019_ha', 0):.2f} ha "
            f"({amb.get('prodes_pct_do_imovel', 0):.2f}% do imóvel).",
            styles["DBody"],
        ))
    else:
        e.append(Paragraph("Sem detecções PRODES.", styles["DDiscreet"]))
    e.append(Spacer(1, 6))
    # 6.2 DETER
    e.append(Paragraph("6.2. DETER (alertas recentes — últimos 12 meses)", styles["DH2"]))
    deter = amb.get("deter_12m") or []
    if deter:
        _render_items_table(e, deter, styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
    else:
        e.append(Paragraph("Sem alertas DETER nos últimos 12 meses.", styles["DDiscreet"]))
    e.append(Spacer(1, 6))
    # 6.3 MapBiomas Alertas
    e.append(Paragraph("6.3. MapBiomas Alertas (validados por satélite)", styles["DH2"]))
    mb = amb.get("mapbiomas_alertas") or []
    if mb:
        _render_items_table(e, mb, styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
    else:
        e.append(Paragraph("Sem alertas MapBiomas.", styles["DDiscreet"]))
    e.append(Spacer(1, 6))
    # 6.4 Embargos IBAMA
    e.append(Paragraph("6.4. Embargos IBAMA (termos lavrados)", styles["DH2"]))
    emb_ibama = amb.get("embargos_ibama_lista") or []
    if emb_ibama:
        _render_items_table(e, emb_ibama, styles, RED, WHITE, LIGHT_RED, RED)
    else:
        e.append(Paragraph("Sem embargos IBAMA na área.", styles["DDiscreet"]))
    e.append(Spacer(1, 6))
    # 6.5 Embargos ICMBio
    e.append(Paragraph("6.5. Embargos ICMBio (unidades de conservação)", styles["DH2"]))
    emb_ic = amb.get("embargos_icmbio_lista") or []
    if emb_ic:
        _render_items_table(e, emb_ic, styles, RED, WHITE, LIGHT_RED, RED)
    else:
        e.append(Paragraph("Sem embargos ICMBio na área.", styles["DDiscreet"]))
    e.append(Spacer(1, 6))
    # 6.6 Autos IBAMA georreferenciados
    e.append(Paragraph("6.6. Autos IBAMA georreferenciados", styles["DH2"]))
    autos_geo = amb.get("autos_ibama_geo_lista") or []
    if autos_geo:
        _render_items_table(e, autos_geo, styles, RED, WHITE, LIGHT_RED, RED)
    else:
        e.append(Paragraph("Nenhum auto IBAMA georreferenciado na área.", styles["DDiscreet"]))
    e.append(PageBreak())

    # ================= 7. PROPRIETÁRIO =================
    e.append(Paragraph("7. DOSSIÊ DO PROPRIETÁRIO", styles["DH1"]))
    prop = secoes.get("proprietario") or {}
    if prop.get("note"):
        e.append(Paragraph(prop["note"], styles["DBody"]))
    else:
        e.append(Paragraph(f"<b>CPF/CNPJ:</b> {prop.get('cpf_cnpj_mask', '—')}", styles["DBody"]))
        e.append(Spacer(1, 6))

        # 7.1 Autos IBAMA consolidado
        ag = prop.get("autos_ibama_agregados") or {}
        if ag:
            e.append(Paragraph("7.1. Histórico de autuações IBAMA", styles["DH2"]))
            dados = [
                ["Total de autos:", str(ag.get("total", 0))],
                ["Multa total:", f"R$ {(ag.get('multa_total') or 0):,.2f}"],
                ["UFs com autuação:", str(ag.get("ufs_distintas", 0))],
                ["Mais antigo:", ag.get("mais_antigo") or "—"],
                ["Mais recente:", ag.get("mais_recente") or "—"],
            ]
            t = Table(dados, colWidths=[5 * cm, 10 * cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            e.append(t)
            e.append(Spacer(1, 4))
            if prop.get("autos_ibama_items"):
                _render_items_table(e, prop["autos_ibama_items"][:15], styles, RED, WHITE, LIGHT_RED, RED)

        # 7.2 CEIS
        ceis = prop.get("ceis_items") or []
        e.append(Paragraph("7.2. CEIS — Empresas Inidôneas e Suspensas (CGU)", styles["DH2"]))
        if ceis:
            _render_items_table(e, ceis, styles, RED, WHITE, LIGHT_RED, RED)
        else:
            e.append(Paragraph("Não consta no CEIS.", styles["DDiscreet"]))
        e.append(Spacer(1, 6))

        # 7.3 CNEP
        cnep = prop.get("cnep_items") or []
        e.append(Paragraph("7.3. CNEP — Empresas Punidas (Lei 12.846/13)", styles["DH2"]))
        if cnep:
            _render_items_table(e, cnep, styles, RED, WHITE, LIGHT_RED, RED)
        else:
            e.append(Paragraph("Não consta no CNEP.", styles["DDiscreet"]))
        e.append(Spacer(1, 6))

        # 7.4 Lista Suja
        ls = prop.get("lista_suja_mte_items") or []
        e.append(Paragraph("7.4. Lista Suja do Trabalho Escravo (MTE)", styles["DH2"]))
        if ls:
            _render_items_table(e, ls, styles, RED, WHITE, LIGHT_RED, RED)
        else:
            e.append(Paragraph("Não consta na Lista Suja.", styles["DDiscreet"]))
        e.append(Spacer(1, 6))

        # 7.5 Processos DataJud
        proc = prop.get("processos_datajud") or []
        e.append(Paragraph("7.5. Processos DataJud vinculados", styles["DH2"]))
        if proc:
            _render_items_table(e, proc, styles, AMBER, WHITE, LIGHT_AMBER, AMBER)
        else:
            e.append(Paragraph("Sem processos DataJud registrados.", styles["DDiscreet"]))
        e.append(Spacer(1, 6))

        # 7.6 Outros imóveis
        outros = prop.get("outros_imoveis") or []
        e.append(Paragraph("7.6. Outros imóveis do proprietário", styles["DH2"]))
        if outros:
            _render_items_table(e, outros, styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
        else:
            e.append(Paragraph("Nenhum outro imóvel identificado na base.", styles["DDiscreet"]))
    e.append(PageBreak())

    # ================= 8. CRÉDITO RURAL =================
    e.append(Paragraph("8. CRÉDITO RURAL VINCULADO (SICOR/BCB)", styles["DH1"]))
    cred = secoes.get("credito_rural") or {}
    if (cred.get("contratos") or 0) == 0:
        e.append(Paragraph("Nenhum contrato SICOR vinculado à área.", styles["DBody"]))
    else:
        # Resumo
        resumo_cred = [
            ["Contratos:", str(cred.get("contratos", 0))],
            ["Valor total:", f"R$ {(cred.get('total_rs') or 0):,.2f}"],
            ["Área financiada:", f"{(cred.get('area_ha') or 0):,.2f} ha"],
            ["Anos:", f"{cred.get('ano_mais_antigo', '—')} – {cred.get('ano_mais_recente', '—')}"],
            ["Instituições distintas:", str(cred.get("n_instituicoes", 0))],
        ]
        t = Table(resumo_cred, colWidths=[5 * cm, 10 * cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        e.append(t)
        e.append(Spacer(1, 8))
        # Série por ano
        e.append(Paragraph("8.1. Histórico por ano", styles["DH2"]))
        _render_items_table(e, cred.get("por_ano") or [], styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
        e.append(Spacer(1, 6))
        # Top contratos
        e.append(Paragraph("8.2. Maiores contratos", styles["DH2"]))
        _render_items_table(e, cred.get("contratos_top") or [], styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
    e.append(PageBreak())

    # ================= 9. MERCADO =================
    e.append(Paragraph("9. MERCADO DE COMMODITIES", styles["DH1"]))
    merc = secoes.get("mercado") or {}
    if merc.get("note"):
        e.append(Paragraph(merc["note"], styles["DBody"]))
    elif merc.get("precos_atuais"):
        e.append(Paragraph(f"9.1. Preços atuais em {merc.get('uf', '—')}", styles["DH2"]))
        _render_items_table(e, merc["precos_atuais"], styles, GREEN, WHITE, LIGHT_GRAY, GRAY)
        e.append(Spacer(1, 6))
        hist = merc.get("historico_12m") or {}
        if hist:
            e.append(Paragraph("9.2. Histórico 12 meses (principais commodities)", styles["DH2"]))
            for commodity, rows in hist.items():
                e.append(Paragraph(f"<b>{commodity.upper()}</b>", styles["DBody"]))
                _render_items_table(e, rows, styles, BLUE, WHITE, LIGHT_GRAY, GRAY)
                e.append(Spacer(1, 4))
    e.append(PageBreak())

    # ================= 10-14. Demais seções =================
    _render_section(e, styles, "10. LOGÍSTICA E INFRAESTRUTURA", secoes.get("logistica"),
                     colors=(GREEN, WHITE, LIGHT_GRAY, GRAY))
    e.append(PageBreak())
    _render_section(e, styles, "11. ENERGIA (ANEEL)", secoes.get("energia"),
                     colors=(GREEN, WHITE, LIGHT_GRAY, GRAY))
    e.append(PageBreak())

    # 12. Valuation com destaque especial
    e.append(Paragraph("12. VALUATION NBR 14.653-3 (ESTIMATIVA EXPEDITA)", styles["DH1"]))
    val = secoes.get("valuation") or {}
    if val.get("note"):
        e.append(Paragraph(val["note"], styles["DBody"]))
    else:
        e.append(Paragraph(val.get("metodologia", ""), styles["DDiscreet"]))
        e.append(Spacer(1, 4))
        dados_val = [
            ["Área:", f"{val.get('area_ha', 0):,.2f} ha"],
            ["Preço médio da UF:", f"R$ {val.get('preco_medio_ha_uf_rs', 0):,.2f}/ha"],
            ["Valor base:", f"R$ {val.get('valor_base_rs', 0):,.2f}"],
            ["Desconto:", f"{val.get('desconto_pct', 0):.1f}%"],
            ["Valor estimado:", f"R$ {val.get('valor_estimado_rs', 0):,.2f}"],
            ["Faixa de confiança:",
             f"R$ {val.get('faixa_confiança_rs', {}).get('min', 0):,.0f} — "
             f"R$ {val.get('faixa_confiança_rs', {}).get('max', 0):,.0f}"],
        ]
        t = Table(dados_val, colWidths=[6 * cm, 10 * cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BACKGROUND", (1, 4), (1, 4), LIGHT_GREEN),
            ("FONTNAME", (1, 4), (1, 4), "Helvetica-Bold"),
            ("FONTSIZE", (1, 4), (1, 4), 14),
            ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        e.append(t)
        e.append(Spacer(1, 6))
        # Motivos de desconto
        if val.get("desconto_motivos"):
            e.append(Paragraph("12.1. Memória de cálculo dos descontos", styles["DH2"]))
            for m in val["desconto_motivos"]:
                e.append(Paragraph(
                    f"• <b>{m.get('motivo', '')}</b>: desconto de {m.get('desconto_pct', 0)}%",
                    styles["DBody"],
                ))
            e.append(Spacer(1, 4))
        e.append(Paragraph(val.get("disclaimer", ""), styles["DDiscreet"]))
    e.append(PageBreak())

    _render_section(e, styles, "13. SITUAÇÃO JURÍDICA", secoes.get("juridico"),
                     colors=(AMBER, WHITE, LIGHT_AMBER, AMBER))
    e.append(PageBreak())
    _render_section(e, styles, "14. AGRONOMIA E COBERTURA DO SOLO", secoes.get("agronomia"),
                     colors=(GREEN, WHITE, LIGHT_GREEN, GREEN))
    e.append(PageBreak())

    # ================= 15. RECOMENDAÇÃO =================
    e.append(Paragraph(f"15. RECOMENDAÇÃO PARA {rec.get('persona', 'GERAL').upper()}", styles["DH1"]))
    if rec.get("tips"):
        for t_ in rec["tips"]:
            e.append(Paragraph(f"✓ {t_}", styles["DBody"]))
            e.append(Spacer(1, 3))
    else:
        e.append(Paragraph("Sem recomendações específicas para esta persona.", styles["DBody"]))
    e.append(PageBreak())

    # ================= 16. APÊNDICE =================
    e.append(Paragraph("16. APÊNDICE — FONTES E METODOLOGIA", styles["DH1"]))
    e.append(Paragraph("16.1. Fontes oficiais consultadas", styles["DH2"]))
    for f in dossie.get("metadata", {}).get("fontes", []):
        e.append(Paragraph(f"• {f}", styles["DBody"]))
    e.append(Spacer(1, 8))

    e.append(Paragraph("16.2. Caveats e disclaimers", styles["DH2"]))
    for c in dossie.get("metadata", {}).get("caveats", []):
        e.append(Paragraph(f"• {c}", styles["DDiscreet"]))
    e.append(Spacer(1, 8))

    e.append(Paragraph("16.3. Metodologia", styles["DH2"]))
    e.append(Paragraph(
        "Este dossiê é gerado automaticamente pelo sistema AgroJus a partir de ~15 fontes "
        "públicas oficiais, consolidando em tempo real as seguintes análises: (a) sobreposições "
        "geoespaciais via PostGIS (ST_Intersects, ST_Intersection) com cálculo de área em "
        "SRID 4326 convertido para geografia; (b) verificação dos 32 critérios do MCR 2.9 "
        "expandido (Resolução CMN 5.193/2024); (c) cruzamento do CPF/CNPJ do proprietário contra "
        "bases do CGU (CEIS/CNEP), MTE (Lista Suja), IBAMA SIFISC (autos e embargos) e CNJ "
        "(DataJud/DJEN); (d) análise de desmatamento multi-temporal INPE PRODES/DETER desde 2000; "
        "(e) valuation NBR 14.653-3 nível expedito com ajustes automáticos por overlap crítico; "
        "(f) consolidação de preços de commodities via Agrolink (série mensal por UF, até 265 meses).",
        styles["DBody"],
    ))
    e.append(Spacer(1, 8))

    e.append(Paragraph("16.4. Limitações", styles["DH2"]))
    e.append(Paragraph(
        "O dossiê sintetiza dados PÚBLICOS disponíveis na data de geração. Dados sigilosos "
        "(ITR, CCIR, eSocial, CNDT) exigem consulta individual. Critérios marcados como "
        "'pendente' no MCR 2.9 indicam fontes ainda não integradas ao sistema — não são "
        "falhas nem aprovações. Para decisão final, é obrigatória verificação humana da "
        "documentação pelo profissional habilitado responsável (advogado, avaliador, "
        "engenheiro agrônomo, etc.).",
        styles["DBody"],
    ))
    e.append(Spacer(1, 10))
    e.append(HRFlowable(width="100%", thickness=0.3, color=GRAY))
    e.append(Spacer(1, 6))
    e.append(Paragraph(
        f"Dossiê ID {dossie.get('dossie_id', '')} gerado em "
        f"{datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')} pelo sistema AgroJus.",
        styles["DSmall"],
    ))

    doc.build(e)
    buf.seek(0)
    return buf.getvalue()


# ==========================================================================
# Helpers
# ==========================================================================


def _render_section(e, styles, title, data, colors=None):
    """Renderização genérica de seção — fallback quando não há renderer específico."""
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import cm

    GREEN = HexColor("#22C55E")
    WHITE = HexColor("#FFFFFF")
    LIGHT_GRAY = HexColor("#F1F5F9")
    GRAY = HexColor("#64748B")
    hdr, txt, bg, bd = colors or (GREEN, WHITE, LIGHT_GRAY, GRAY)

    e.append(Paragraph(title, styles["DH1"]))
    if not data or (isinstance(data, dict) and data.get("note")):
        e.append(Paragraph(
            (data or {}).get("note") or "Sem dados coletados para esta seção.",
            styles["DBody"],
        ))
        return

    if isinstance(data, dict):
        # Listar chaves como par K/V; listas viram mini-tabelas
        for k, v in data.items():
            if k in ("error", "note"):
                continue
            label = k.replace("_", " ").capitalize()
            if isinstance(v, list):
                e.append(Paragraph(f"<b>{label}</b>", styles["DBody"]))
                if v and isinstance(v[0], dict):
                    _render_items_table(e, v[:20], styles, hdr, txt, bg, bd)
                else:
                    e.append(Paragraph(", ".join(str(x) for x in v), styles["DSmall"]))
                e.append(Spacer(1, 4))
            elif isinstance(v, dict):
                e.append(Paragraph(f"<b>{label}</b>", styles["DBody"]))
                kvs = [[kk, str(vv)[:100]] for kk, vv in v.items()]
                t = Table(kvs, colWidths=[5 * cm, 11 * cm])
                t.setStyle(TableStyle([
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))
                e.append(t)
                e.append(Spacer(1, 4))
            else:
                e.append(Paragraph(
                    f"<b>{label}:</b> {v if v not in (None, '') else '—'}",
                    styles["DBody"],
                ))


def _render_items_table(e, items: list[dict], styles, header_bg, header_fg, row_bg, border):
    """Renderiza lista de dicts como tabela com cabeçalho colorido."""
    from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
    from reportlab.lib.units import cm
    from reportlab.lib.colors import HexColor

    if not items:
        return

    # Pega colunas do primeiro item, até 6 colunas
    cols = list(items[0].keys())[:6]
    if not cols:
        return

    # Constrói rows com valores truncados
    body = [[col.replace("_", " ").capitalize()[:22] for col in cols]]
    for item in items:
        row = []
        for col in cols:
            val = item.get(col)
            if val is None:
                row.append("—")
            elif isinstance(val, float):
                row.append(f"{val:,.2f}")
            elif isinstance(val, (int,)):
                row.append(f"{val:,}")
            else:
                s = str(val)[:60]
                row.append(s)
        body.append(row)

    # Calcula largura disponível (17cm) dividida entre colunas
    col_w = 17 / len(cols) * cm
    t = Table(body, colWidths=[col_w] * len(cols), repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), header_fg),
        ("GRID", (0, 0), (-1, -1), 0.3, border),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), row_bg]),
    ]))
    e.append(t)
