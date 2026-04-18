"""
Ações da aba Ações da ficha do imóvel:

  GET  /property/{car}/laudo.pdf          — laudo consolidado em PDF (reportlab)
  GET  /property/{car}/export.geojson     — geometria + overlaps como GeoJSON
  GET  /property/{car}/export.gpkg        — GeoPackage OGC (via geopandas)
  GET  /property/{car}/export.shp.zip     — Shapefile zipado (via geopandas)
  POST /property/{car}/minuta             — gera minuta jurídica via Claude API

Consome dados internamente (sem HTTP) — mais rápido e robusto.
"""

from __future__ import annotations

import io
import json
import logging
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel
from sqlalchemy import text

from app.models.database import get_engine
from app.services.minuta_generator import MINUTA_PROMPTS, generate_minuta

logger = logging.getLogger("agrojus.property_actions")
router = APIRouter()


# ==========================================================================
# Helpers: fetch dados consolidados do imóvel (sem sair da instância)
# ==========================================================================


def _fetch_property_base(car_code: str) -> Optional[dict]:
    """Dados básicos: CAR + município + UF + área + status + centróide + WKT."""
    engine = get_engine()
    sql = text("""
        SELECT
            cod_imovel, uf,
            COALESCE(municipio, '') AS municipio,
            area::float AS area_ha,
            COALESCE(status_imovel, '') AS status,
            COALESCE(tipo_imovel, '') AS tipo,
            COALESCE(m_fiscal, 0)::float AS modulos_fiscais,
            COALESCE(cod_municipio_ibge, '') AS cod_municipio_ibge,
            ST_X(ST_Centroid(geometry)) AS lon,
            ST_Y(ST_Centroid(geometry)) AS lat,
            ST_AsGeoJSON(geometry) AS geojson
        FROM (
            SELECT cod_imovel, uf, NULL::text AS municipio, area, status_imovel,
                   tipo_imovel, m_fiscal,
                   cod_municipio_ibge::text AS cod_municipio_ibge,
                   geometry
            FROM sicar_completo WHERE cod_imovel = :car
            UNION ALL
            SELECT cod_imovel, uf, municipio, area, status_imovel,
                   tipo_imovel, m_fiscal,
                   cod_municipio_ibge::text AS cod_municipio_ibge,
                   geometry
            FROM geo_car WHERE cod_imovel = :car
        ) t
        WHERE geometry IS NOT NULL
        LIMIT 1
    """)
    with engine.connect() as conn:
        row = conn.execute(sql, {"car": car_code}).mappings().first()
    return dict(row) if row else None


def _fetch_overlaps_summary(car_code: str) -> dict:
    """Conta overlaps por camada (sem geometria)."""
    engine = get_engine()
    layers = {
        "terras_indigenas": "geo_terras_indigenas",
        "unidades_conservacao": "geo_unidades_conservacao",
        "embargos_icmbio": "geo_embargos_icmbio",
        "prodes": "geo_prodes",
        "deter_amazonia": "geo_deter_amazonia",
        "deter_cerrado": "geo_deter_cerrado",
        "mapbiomas_alertas": "geo_mapbiomas_alertas",
        "sigef_parcelas": "sigef_parcelas",
        "autos_ibama": "geo_autos_ibama",
    }
    result: dict = {}
    with engine.connect() as conn:
        for key, table in layers.items():
            try:
                n = conn.execute(text(f"""
                    WITH c AS (
                      SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
                      UNION ALL
                      SELECT geometry FROM geo_car WHERE cod_imovel = :car
                      LIMIT 1
                    )
                    SELECT COUNT(*) FROM c
                    JOIN {table} l ON ST_Intersects(c.geometry, l.geometry)
                """), {"car": car_code}).scalar() or 0
                result[key] = int(n)
            except Exception:  # noqa: BLE001
                result[key] = 0
    return result


def _fetch_credit_summary(car_code: str) -> dict:
    engine = get_engine()
    sql = text("""
        WITH c AS (
          SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
          UNION ALL SELECT geometry FROM geo_car WHERE cod_imovel = :car LIMIT 1
        )
        SELECT
          COUNT(*) AS contratos,
          COALESCE(SUM(mcr.vl_parc_credito),0)::float AS total_rs,
          COALESCE(SUM(mcr.vl_area_financ),0)::float AS area_total_ha,
          MAX(mcr.year)::int AS ano_mais_recente
        FROM c JOIN mapbiomas_credito_rural mcr
          ON ST_Intersects(c.geometry, mcr.geom)
    """)
    try:
        with engine.connect() as conn:
            row = conn.execute(sql, {"car": car_code}).mappings().first()
            return dict(row) if row else {}
    except Exception:  # noqa: BLE001
        return {}


# ==========================================================================
# Laudo PDF
# ==========================================================================


@router.get("/{car_code}/laudo.pdf")
def generate_laudo_pdf(car_code: str):
    """
    Gera laudo consolidado em PDF consumindo os dados reais do imóvel.

    Conteúdo: capa, identificação, situação cadastral, compliance resumido,
    overlaps por camada, crédito rural vinculado, valuation estimativa,
    avisos legais e assinatura.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
        )
        from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
    except ImportError:
        raise HTTPException(status_code=500, detail="reportlab não instalado")

    prop = _fetch_property_base(car_code)
    if not prop:
        raise HTTPException(status_code=404, detail=f"CAR {car_code} não encontrado")

    overlaps = _fetch_overlaps_summary(car_code)
    credit = _fetch_credit_summary(car_code)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )

    # Estilos
    GREEN = HexColor("#22C55E")
    DARK = HexColor("#0F172A")
    GRAY = HexColor("#64748B")
    LIGHT = HexColor("#F1F5F9")
    RED = HexColor("#DC2626")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "AJTitle", parent=styles["Title"],
        fontSize=20, textColor=GREEN, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        "AJSection", parent=styles["Heading2"],
        fontSize=13, textColor=DARK, spaceBefore=12, spaceAfter=6,
        borderWidth=0, borderColor=GREEN,
    ))
    styles.add(ParagraphStyle(
        "AJBody", parent=styles["Normal"],
        fontSize=10, leading=14, alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        "AJSmall", parent=styles["Normal"],
        fontSize=8, textColor=GRAY,
    ))

    elements: list = []

    # --- Capa ---
    elements.append(Paragraph("AGROJUS", styles["AJTitle"]))
    elements.append(Paragraph(
        "Laudo de Due Diligence Rural — Ficha Consolidada",
        styles["Heading3"],
    ))
    elements.append(Spacer(1, 14))

    cabec = [
        ["Código CAR:", prop["cod_imovel"]],
        ["Município/UF:", f"{prop.get('municipio','')}/{prop.get('uf','')}"],
        ["Área:", f"{prop.get('area_ha') or 0:,.2f} ha"],
        ["Status CAR:", prop.get("status") or "—"],
        ["Módulos Fiscais:", f"{prop.get('modulos_fiscais') or 0:.1f}"],
        ["Centróide (lat, lon):", f"{prop.get('lat'):.5f}, {prop.get('lon'):.5f}"],
        ["Gerado em:", datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")],
    ]
    t = Table(cabec, colWidths=[5 * cm, 12 * cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 18))

    # --- Sobreposições ---
    elements.append(Paragraph("SOBREPOSIÇÕES GEOESPACIAIS", styles["AJSection"]))
    LAYER_LABELS = {
        "terras_indigenas": "Terras Indígenas (FUNAI)",
        "unidades_conservacao": "Unidades de Conservação (ICMBio)",
        "embargos_icmbio": "Embargos ICMBio",
        "autos_ibama": "Autos de Infração IBAMA",
        "prodes": "PRODES (desmate consolidado)",
        "deter_amazonia": "DETER Amazônia (alertas)",
        "deter_cerrado": "DETER Cerrado (alertas)",
        "mapbiomas_alertas": "MapBiomas Alerta",
        "sigef_parcelas": "SIGEF/INCRA (parcelas certificadas)",
    }
    overlap_data = [["Camada", "Interseções"]]
    critical_overlap = False
    for k, label in LAYER_LABELS.items():
        n = overlaps.get(k, 0)
        overlap_data.append([label, f"{n}" if n else "nenhuma"])
        if k in ("terras_indigenas", "embargos_icmbio", "autos_ibama") and n > 0:
            critical_overlap = True
    t = Table(overlap_data, colWidths=[11 * cm, 6 * cm])
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]
    # Destaca linhas com n>0 em critical
    for i, (_, n) in enumerate(overlap_data[1:], start=1):
        if n != "nenhuma":
            style_cmds.append(("TEXTCOLOR", (1, i), (1, i), RED))
            style_cmds.append(("FONTNAME", (1, i), (1, i), "Helvetica-Bold"))
    t.setStyle(TableStyle(style_cmds))
    elements.append(t)
    elements.append(Spacer(1, 14))

    if critical_overlap:
        elements.append(Paragraph(
            "<b>ATENÇÃO:</b> Foram identificadas sobreposições em camadas críticas "
            "(TI, embargos IBAMA ou autos de infração). Recomenda-se análise "
            "geoespacial detalhada antes de qualquer transação ou tomada de crédito.",
            ParagraphStyle("Warn", parent=styles["AJBody"], textColor=RED),
        ))
        elements.append(Spacer(1, 10))

    # --- Crédito rural ---
    if credit and (credit.get("contratos") or 0) > 0:
        elements.append(Paragraph("CRÉDITO RURAL VINCULADO (SICOR/BCB)", styles["AJSection"]))
        c_data = [
            ["Contratos detectados:", f"{credit['contratos']}"],
            ["Valor total financiado:", f"R$ {credit.get('total_rs') or 0:,.2f}"],
            ["Área financiada total:", f"{credit.get('area_total_ha') or 0:,.2f} ha"],
            ["Ano do contrato mais recente:", str(credit.get("ano_mais_recente") or "—")],
        ]
        t = Table(c_data, colWidths=[7 * cm, 10 * cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

    # --- Avisos ---
    elements.append(PageBreak())
    elements.append(Paragraph("METODOLOGIA E AVISOS", styles["AJSection"]))
    elements.append(Paragraph(
        "Este laudo foi gerado automaticamente pela plataforma AgroJus a partir "
        "de fontes públicas: Sistema Nacional de Cadastro Ambiental Rural (SICAR), "
        "SIGEF/INCRA, IBAMA dados abertos, ICMBio, INPE (PRODES/DETER), MapBiomas "
        "Alerta, Banco Central do Brasil (SICOR) e DataJud/CNJ. A análise "
        "geoespacial utiliza operações de interseção sobre geometrias em SRID 4326 "
        "(WGS84). O laudo tem caráter informativo e não substitui diligência "
        "presencial, consulta ao cartório de imóveis competente ou parecer de "
        "profissional habilitado. Em caso de divergência entre este documento e "
        "os dados oficiais de origem, prevalecem os dados oficiais na data da "
        "consulta.",
        styles["AJBody"],
    ))
    elements.append(Spacer(1, 14))
    elements.append(Paragraph(
        f"AgroJus — Gerado em {datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')} — "
        f"CAR {car_code}",
        styles["AJSmall"],
    ))

    doc.build(elements)
    buf.seek(0)

    filename = f"laudo_{car_code}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ==========================================================================
# Export: GeoJSON, GeoPackage, Shapefile
# ==========================================================================


def _collect_features(car_code: str, include_overlaps: bool = True) -> list[dict]:
    """Monta lista de features: CAR + overlaps."""
    engine = get_engine()
    features: list[dict] = []

    # CAR principal
    with engine.connect() as conn:
        prop_row = conn.execute(text("""
            SELECT cod_imovel, uf, COALESCE(municipio,'') AS municipio,
                   area::float AS area_ha,
                   COALESCE(status_imovel,'') AS status,
                   ST_AsGeoJSON(geometry)::json AS geojson
            FROM (
              SELECT cod_imovel, uf, NULL::text AS municipio, area, status_imovel, geometry
              FROM sicar_completo WHERE cod_imovel = :car
              UNION ALL
              SELECT cod_imovel, uf, municipio, area, status_imovel, geometry
              FROM geo_car WHERE cod_imovel = :car
            ) t
            WHERE geometry IS NOT NULL LIMIT 1
        """), {"car": car_code}).mappings().first()

    if not prop_row:
        return features

    features.append({
        "type": "Feature",
        "properties": {
            "layer": "imovel",
            "car_code": prop_row["cod_imovel"],
            "municipio": prop_row["municipio"],
            "uf": prop_row["uf"],
            "area_ha": prop_row["area_ha"],
            "status": prop_row["status"],
        },
        "geometry": prop_row["geojson"],
    })

    if not include_overlaps:
        return features

    overlap_queries = {
        "terra_indigena": """
            SELECT ti.terrai_nom AS nome, 'terra_indigena' AS layer,
                   ST_AsGeoJSON(ST_Intersection(c.geometry, ti.geometry))::json AS geojson
            FROM c JOIN geo_terras_indigenas ti ON ST_Intersects(c.geometry, ti.geometry)
        """,
        "unidade_conservacao": """
            SELECT uc.nomeuc AS nome, 'unidade_conservacao' AS layer,
                   ST_AsGeoJSON(ST_Intersection(c.geometry, uc.geometry))::json AS geojson
            FROM c JOIN geo_unidades_conservacao uc ON ST_Intersects(c.geometry, uc.geometry)
        """,
        "embargo_icmbio": """
            SELECT e.autuado AS nome, 'embargo_icmbio' AS layer,
                   ST_AsGeoJSON(ST_Intersection(c.geometry, e.geometry))::json AS geojson
            FROM c JOIN geo_embargos_icmbio e ON ST_Intersects(c.geometry, e.geometry)
        """,
        "prodes": """
            SELECT p.year::text AS nome, 'prodes' AS layer,
                   ST_AsGeoJSON(ST_Intersection(c.geometry, p.geometry))::json AS geojson
            FROM c JOIN geo_prodes p ON ST_Intersects(c.geometry, p.geometry)
        """,
        "deter": """
            SELECT d.classname AS nome, 'deter_amazonia' AS layer,
                   ST_AsGeoJSON(ST_Intersection(c.geometry, d.geometry))::json AS geojson
            FROM c JOIN geo_deter_amazonia d ON ST_Intersects(c.geometry, d.geometry)
        """,
    }

    cte = """WITH c AS (
        SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
        UNION ALL SELECT geometry FROM geo_car WHERE cod_imovel = :car LIMIT 1
    )"""

    with engine.connect() as conn:
        for sql in overlap_queries.values():
            try:
                rows = conn.execute(text(cte + sql), {"car": car_code}).mappings().all()
                for r in rows:
                    if r["geojson"]:
                        features.append({
                            "type": "Feature",
                            "properties": {"layer": r["layer"], "nome": r["nome"]},
                            "geometry": r["geojson"],
                        })
            except Exception as e:  # noqa: BLE001
                logger.warning("overlap export failed: %s", e)

    return features


@router.get("/{car_code}/export.geojson")
def export_geojson(car_code: str, overlaps: bool = Query(True)):
    """Exporta GeoJSON com o polígono do CAR + overlaps opcionais."""
    features = _collect_features(car_code, include_overlaps=overlaps)
    if not features:
        raise HTTPException(status_code=404, detail=f"CAR {car_code} sem geometria")

    fc = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "car_code": car_code,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": "AgroJus",
            "crs": "EPSG:4326",
        },
    }
    body = json.dumps(fc, ensure_ascii=False, default=str)
    return Response(
        content=body,
        media_type="application/geo+json",
        headers={"Content-Disposition": f'attachment; filename="{car_code}.geojson"'},
    )


def _features_to_gdf(features: list[dict]):
    """Converte lista de GeoJSON features → GeoDataFrame."""
    import geopandas as gpd
    from shapely.geometry import shape
    import pandas as pd  # noqa: F401

    rows = []
    geoms = []
    for f in features:
        props = dict(f.get("properties") or {})
        rows.append(props)
        geoms.append(shape(f["geometry"]))
    gdf = gpd.GeoDataFrame(rows, geometry=geoms, crs="EPSG:4326")
    return gdf


@router.get("/{car_code}/export.gpkg")
def export_gpkg(car_code: str, overlaps: bool = Query(True)):
    """Exporta GeoPackage (OGC SQLite container). 1 layer por tipo."""
    features = _collect_features(car_code, include_overlaps=overlaps)
    if not features:
        raise HTTPException(status_code=404, detail=f"CAR {car_code} sem geometria")

    gdf = _features_to_gdf(features)

    with tempfile.NamedTemporaryFile(suffix=".gpkg", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        # Escreve uma camada por layer distinto (mais útil em QGIS/ArcGIS)
        for layer_name, subdf in gdf.groupby("layer"):
            subdf.to_file(tmp_path, layer=str(layer_name), driver="GPKG")
        with open(tmp_path, "rb") as f:
            data = f.read()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    return Response(
        content=data,
        media_type="application/geopackage+sqlite3",
        headers={"Content-Disposition": f'attachment; filename="{car_code}.gpkg"'},
    )


@router.get("/{car_code}/export.shp.zip")
def export_shapefile_zip(car_code: str, overlaps: bool = Query(True)):
    """Exporta Shapefile zipado (4 arquivos shp/dbf/shx/prj)."""
    features = _collect_features(car_code, include_overlaps=overlaps)
    if not features:
        raise HTTPException(status_code=404, detail=f"CAR {car_code} sem geometria")

    gdf = _features_to_gdf(features)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Um .shp por layer (SHP não suporta múltiplas camadas)
        written = []
        for layer_name, subdf in gdf.groupby("layer"):
            safe = str(layer_name).replace("/", "_")
            shp_path = os.path.join(tmpdir, f"{car_code}_{safe}.shp")
            subdf.to_file(shp_path, driver="ESRI Shapefile")
            written.append(shp_path)

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for shp in written:
                base = shp[:-4]
                for ext in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
                    fp = base + ext
                    if os.path.exists(fp):
                        zf.write(fp, arcname=os.path.basename(fp))
        buf.seek(0)
        return Response(
            content=buf.getvalue(),
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{car_code}_shp.zip"'},
        )


# ==========================================================================
# Minuta jurídica via Claude API
# ==========================================================================


class MinutaRequest(BaseModel):
    tipo: str = "livre"
    destinatario: Optional[str] = None
    observacoes: Optional[str] = None
    processos: Optional[list[str]] = None  # lista de números de processo/autos
    extra_context: Optional[str] = None


@router.get("/minuta/tipos")
def list_minuta_tipos():
    """Lista tipos de minuta suportados."""
    return {
        "tipos": [
            {"key": k, "description": v.split(".")[0] + "."}
            for k, v in MINUTA_PROMPTS.items()
        ],
    }


@router.post("/{car_code}/minuta")
def generate_property_minuta(car_code: str, body: MinutaRequest):
    """
    Gera minuta jurídica para o CAR usando Claude API.

    Monta contexto com dados do imóvel (CAR, município, UF, área, overlaps)
    + observações do advogado + tipo da peça, envia ao Claude, retorna
    markdown pronto para revisão.

    Requer ANTHROPIC_API_KEY no backend/.env.
    """
    prop = _fetch_property_base(car_code)
    if not prop:
        raise HTTPException(status_code=404, detail=f"CAR {car_code} não encontrado")

    overlaps = _fetch_overlaps_summary(car_code)
    credit = _fetch_credit_summary(car_code)

    ctx = {
        "car_code": prop["cod_imovel"],
        "municipality": prop.get("municipio"),
        "uf": prop.get("uf"),
        "area_ha": prop.get("area_ha"),
        "status": prop.get("status"),
        "modulos_fiscais": prop.get("modulos_fiscais"),
        "overlaps": {k: v for k, v in overlaps.items() if v > 0},
        "compliance": {
            "overlaps_criticos": sum(
                overlaps.get(k, 0) for k in
                ("terras_indigenas", "embargos_icmbio", "autos_ibama")
            ),
            "credito_vinculado_rs": credit.get("total_rs") if credit else None,
        },
        "processos": body.processos or [],
        "extra": body.extra_context,
    }

    try:
        result = generate_minuta(
            tipo=body.tipo,
            property_context=ctx,
            observacoes=body.observacoes,
            destinatario=body.destinatario,
        )
    except RuntimeError as e:
        # API key ausente ou SDK não instalada — devolve 501 com instrução
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:  # noqa: BLE001
        logger.exception("erro ao gerar minuta")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar minuta: {e}")

    return result
