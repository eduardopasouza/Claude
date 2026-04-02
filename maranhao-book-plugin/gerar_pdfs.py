#!/usr/bin/env python3
"""
Gerador de PDFs por Parte - Quem é o Maranhão?
Paleta: Ocre #C8952E, Terracota #B5533E, Verde-mata #2D6A4F,
        Azul-mar #1B4965, Creme #FAF3E8, Carvão #2B2B2B
"""

import os
import re
import yaml
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Frame, PageTemplate
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# === CORES ===
OCRE = HexColor('#C8952E')
TERRACOTA = HexColor('#B5533E')
VERDE_MATA = HexColor('#2D6A4F')
AZUL_MAR = HexColor('#1B4965')
AREIA = HexColor('#E8D5B7')
CREME = HexColor('#FAF3E8')
CARVAO = HexColor('#2B2B2B')
VERMELHO = HexColor('#C1292E')
ROXO = HexColor('#5E3A7E')

# Cores de acento por parte
PARTE_CORES = {
    'I': VERDE_MATA, 'II': TERRACOTA, 'III': AZUL_MAR,
    'IV': ROXO, 'V': OCRE, 'VI': AZUL_MAR,
    'VII': TERRACOTA, 'VIII': VERMELHO, 'IX': OCRE,
    'X': CARVAO, 'XI': VERDE_MATA, 'epilogo': OCRE
}

PARTE_NOMES = {
    'I': 'O Chão', 'II': 'Os Primeiros', 'III': 'A Conquista',
    'IV': 'O Povo Negro', 'V': 'Apogeu e Queda', 'VI': 'São Luís: A Ilha',
    'VII': 'O Povo e a Identidade', 'VIII': 'As Criações', 'IX': 'A Economia',
    'X': 'O Estado e a Estrutura', 'XI': 'O Maranhão no Mundo',
    'epilogo': 'Epílogo'
}

BASE = Path(r"C:\Users\eduar\OneDrive\Escritório\_Pessoal\Almanaque do Maranhão")
VERBETES = BASE / "verbetes"
OUTPUT = BASE / "pdfs"
OUTPUT.mkdir(exist_ok=True)


def parse_texto(filepath):
    """Parse texto.md: extract YAML frontmatter and markdown body."""
    text = filepath.read_text(encoding='utf-8')

    # Split YAML frontmatter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
            except:
                meta = {}
            body = parts[2].strip()
        else:
            meta = {}
            body = text
    else:
        meta = {}
        body = text

    return meta, body


def markdown_to_paragraphs(body, styles):
    """Convert simplified markdown to reportlab paragraphs."""
    elements = []
    lines = body.split('\n')
    current_para = []

    for line in lines:
        stripped = line.strip()

        # Skip HTML comments (layout marks)
        if stripped.startswith('<!--') or stripped.startswith('<!-- '):
            continue
        if stripped.endswith('-->'):
            continue

        # Heading 1
        if stripped.startswith('# ') and not stripped.startswith('## '):
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    elements.append(Paragraph(text, styles['Body']))
                current_para = []
            title = stripped[2:].strip()
            elements.append(Paragraph(title, styles['VerbeteTitle']))
            elements.append(Spacer(1, 8*mm))
            continue

        # Heading 2
        if stripped.startswith('## '):
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    elements.append(Paragraph(text, styles['Body']))
                current_para = []
            subtitle = stripped[3:].strip()
            elements.append(Spacer(1, 6*mm))
            elements.append(Paragraph(subtitle, styles['QMHeading2']))
            elements.append(Spacer(1, 3*mm))
            continue

        # Heading 3 (boxes)
        if stripped.startswith('### '):
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    elements.append(Paragraph(text, styles['Body']))
                current_para = []
            box_title = stripped[4:].strip()
            elements.append(Spacer(1, 4*mm))
            elements.append(Paragraph(box_title, styles['BoxTitle']))
            continue

        # Blockquote (epigraph)
        if stripped.startswith('> '):
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    elements.append(Paragraph(text, styles['Body']))
                current_para = []
            quote = stripped[2:].strip().replace('*', '')
            elements.append(Paragraph(f'<i>{quote}</i>', styles['Epigraph']))
            continue

        # Horizontal rule
        if stripped == '---':
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    elements.append(Paragraph(text, styles['Body']))
                current_para = []
            elements.append(Spacer(1, 5*mm))
            continue

        # Empty line = paragraph break
        if not stripped:
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    # Clean markdown formatting
                    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
                    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
                    text = re.sub(r'↗\s*V\d+', '', text)
                    # Sanitize unclosed tags
                    text = re.sub(r'<(?!/?[bi]>)[^>]*>', '', text)
                    try:
                        elements.append(Paragraph(text, styles['Body']))
                    except:
                        clean = re.sub(r'<[^>]+>', '', text)
                        elements.append(Paragraph(clean, styles['Body']))
                current_para = []
            continue

        # Normal text
        # Skip footnote references and source sections
        if stripped.startswith('**Fontes**') or stripped.startswith('**Veja'):
            if current_para:
                text = ' '.join(current_para)
                if text.strip():
                    elements.append(Paragraph(text, styles['Body']))
                current_para = []
            # Add sources as small text
            elements.append(Spacer(1, 5*mm))
            elements.append(Paragraph(stripped.replace('**', ''), styles['Footnote']))
            continue

        if re.match(r'^[¹²³⁴⁵⁶⁷⁸⁹⁰]+\s', stripped):
            # Footnote
            elements.append(Paragraph(stripped, styles['Footnote']))
            continue

        current_para.append(stripped)

    # Flush remaining
    if current_para:
        text = ' '.join(current_para)
        if text.strip():
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
            text = re.sub(r'<(?!/?[bi]>)[^>]*>', '', text)
            try:
                elements.append(Paragraph(text, styles['Body']))
            except:
                clean = re.sub(r'<[^>]+>', '', text)
                elements.append(Paragraph(clean, styles['Body']))

    return elements


def create_styles(accent_color):
    """Create paragraph styles with project palette."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'VerbeteTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=CARVAO,
        spaceAfter=4*mm,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'PartTitle',
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=accent_color,
        spaceAfter=8*mm,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'PartSubtitle',
        fontName='Helvetica',
        fontSize=16,
        leading=20,
        textColor=CARVAO,
        spaceAfter=15*mm,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'QMHeading2',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=accent_color,
        spaceBefore=4*mm,
        spaceAfter=2*mm
    ))

    styles.add(ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=CARVAO,
        alignment=TA_JUSTIFY,
        spaceAfter=3*mm,
        firstLineIndent=5*mm
    ))

    styles.add(ParagraphStyle(
        'Epigraph',
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=15,
        textColor=HexColor('#666666'),
        alignment=TA_LEFT,
        leftIndent=15*mm,
        rightIndent=15*mm,
        spaceAfter=5*mm
    ))

    styles.add(ParagraphStyle(
        'BoxTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceBefore=3*mm,
        spaceAfter=2*mm,
        leftIndent=5*mm
    ))

    styles.add(ParagraphStyle(
        'Footnote',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=HexColor('#888888'),
        spaceAfter=1*mm
    ))

    styles.add(ParagraphStyle(
        'Logo',
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=HexColor('#999999'),
        alignment=TA_CENTER
    ))

    return styles


def generate_part_pdf(parte_num, parte_name, verbete_dirs, accent_color):
    """Generate a PDF for one part."""
    safe_name = parte_name.replace(' ', '-').replace(':', '').replace('?', '').replace('ã', 'a').replace('í', 'i').replace('é', 'e').replace('ç', 'c').replace('ô', 'o').replace('ú', 'u')
    filename = f"Parte-{parte_num}-{safe_name}.pdf"
    filepath = OUTPUT / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=3*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )

    styles = create_styles(accent_color)
    elements = []

    # === COVER PAGE ===
    elements.append(Spacer(1, 60*mm))
    elements.append(Paragraph(f"PARTE {parte_num}", styles['PartTitle']))
    elements.append(Paragraph(parte_name.upper(), styles['PartSubtitle']))
    elements.append(Spacer(1, 30*mm))
    elements.append(Paragraph("Quem é o Maranhão?", styles['Logo']))
    elements.append(Paragraph("@quemeomaranhao", styles['Logo']))
    elements.append(PageBreak())

    # === VERBETES ===
    for vdir in sorted(verbete_dirs):
        texto_path = vdir / "texto.md"
        if not texto_path.exists():
            continue

        meta, body = parse_texto(texto_path)

        if not body:
            continue

        # Convert markdown to paragraphs
        try:
            paras = markdown_to_paragraphs(body, styles)
            if paras:
                elements.extend(paras)
                elements.append(PageBreak())
        except Exception as e:
            print(f"    WARN: erro em {vdir.name}: {str(e)[:80]}")
            # Add plain text fallback
            clean = re.sub(r'<[^>]+>', '', body[:500])
            elements.append(Paragraph(f"[Erro de formatacao - {vdir.name}]", styles['Body']))
            elements.append(PageBreak())

    if len(elements) > 3:  # More than just cover
        doc.build(elements)
        print(f"  OK {filename} ({len(verbete_dirs)} verbetes)")
        return filepath
    else:
        print(f"  WARN {filename} - sem conteúdo")
        return None


def main():
    print("=" * 60)
    print("GERANDO PDFs - Quem é o Maranhão?")
    print("=" * 60)

    partes = {
        'I': [], 'II': [], 'III': [], 'IV': [], 'V': [],
        'VI': [], 'VII': [], 'VIII': [], 'IX': [], 'X': [], 'XI': []
    }

    # Map directories to parts
    for parte_dir in sorted(VERBETES.iterdir()):
        if not parte_dir.is_dir():
            continue
        name = parte_dir.name

        # Extract roman numeral
        if name.startswith('parte-'):
            numeral = name.replace('parte-', '').upper()
            if numeral in partes:
                for vdir in sorted(parte_dir.iterdir()):
                    if vdir.is_dir() and (vdir / "texto.md").exists():
                        partes[numeral].append(vdir)

    # Generate PDFs
    generated = []
    for parte_num in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']:
        vdirs = partes[parte_num]
        if vdirs:
            accent = PARTE_CORES.get(parte_num, OCRE)
            nome = PARTE_NOMES.get(parte_num, f'Parte {parte_num}')
            print(f"\nParte {parte_num} - {nome} ({len(vdirs)} verbetes)")
            result = generate_part_pdf(parte_num, nome, vdirs, accent)
            if result:
                generated.append(result)

    # Epilogo
    epilogo_dir = VERBETES / "epilogo" / "V106-epilogo"
    if epilogo_dir.exists() and (epilogo_dir / "texto.md").exists():
        print(f"\nEpílogo (1 verbete)")
        result = generate_part_pdf('Epilogo', 'Quem é o Maranhão?', [epilogo_dir], OCRE)
        if result:
            generated.append(result)

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {len(generated)} PDFs gerados em {OUTPUT}")
    print("=" * 60)


if __name__ == '__main__':
    main()
