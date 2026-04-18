"""
Dossiê Agrofundiário Multi-Persona — gerador consolidado de relatório rural.

Recebe QUALQUER filtro que identifique uma área/entidade no mapa:
  - car_code: "MA-2100055-..."              → usa geometria do CAR
  - geometry: GeoJSON Polygon/MultiPolygon  → usa geometria direta
  - point + radius_km                       → cria buffer e usa
  - bbox: [west, south, east, north]        → retângulo
  - municipio_codigo + uf                   → usa polígono do município
  - cpf_cnpj                                → dossiê do proprietário (múltiplos imóveis)
  - matricula / sigef_code                  → resolve via cadastro

E produz dossiê estruturado em 14 seções cobrindo:
  Identificação · Fundiário · Compliance · Ambiental · Proprietário ·
  Agronomia & Solos · Clima · Crédito Rural · Mercado · Logística ·
  Valuation · Jurídico · Recomendação por Persona · Metadata

O output é um dict rico que pode ser serializado para JSON, renderizado em
HTML/React ou transformado em PDF (reportlab/weasyprint).

Arquitetura modular: cada seção é uma função coletora independente. Falhas em
uma seção geram campo `errors[<section>]` mas não quebram o dossiê inteiro.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from sqlalchemy import text

from app.models.database import get_engine

logger = logging.getLogger("agrojus.dossie")


# ==========================================================================
# Contexto e schema de entrada
# ==========================================================================


@dataclass
class DossieContext:
    """Contexto resolvido após identificar a área — base pra toda consulta."""
    input_type: str  # car | geometry | point_radius | bbox | municipio | cpf_cnpj
    geometry_wkt: Optional[str] = None  # área em WKT SRID 4326
    centroid: Optional[dict] = None  # {"lat":..., "lon":...}
    area_ha: Optional[float] = None
    bbox: Optional[list[float]] = None
    # Identificadores opcionais (enriquecem queries)
    car_code: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    owner_name: Optional[str] = None
    municipio: Optional[str] = None
    municipio_ibge: Optional[str] = None
    uf: Optional[str] = None
    bioma: Optional[str] = None
    persona: str = "geral"  # comprador | advogado | investidor | consultor | produtor | trading | geral
    nome_dossie: Optional[str] = None
    raw_request: dict = field(default_factory=dict)


# ==========================================================================
# Resolver input → contexto
# ==========================================================================


def resolve_input(req: dict) -> DossieContext:
    """Aceita o payload de /dossie e descobre a geometria + identificadores."""
    engine = get_engine()
    ctx = DossieContext(
        input_type=(req.get("input_type") or _infer_type(req)),
        persona=(req.get("persona") or "geral").lower(),
        nome_dossie=req.get("name"),
        raw_request=req,
    )

    # --- 1) CAR ---
    if req.get("car_code"):
        ctx.input_type = "car"
        ctx.car_code = req["car_code"].strip()
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT cod_imovel, uf, COALESCE(municipio,'') AS municipio,
                       area::float AS area_ha,
                       ST_X(ST_Centroid(geometry)) AS lon,
                       ST_Y(ST_Centroid(geometry)) AS lat,
                       ST_AsText(geometry) AS wkt,
                       ST_XMin(geometry) AS xmin, ST_YMin(geometry) AS ymin,
                       ST_XMax(geometry) AS xmax, ST_YMax(geometry) AS ymax
                FROM (
                  SELECT cod_imovel, uf, NULL::text AS municipio, area, geometry
                  FROM sicar_completo WHERE cod_imovel = :car
                  UNION ALL
                  SELECT cod_imovel, uf, municipio, area, geometry
                  FROM geo_car WHERE cod_imovel = :car
                ) t WHERE geometry IS NOT NULL LIMIT 1
            """), {"car": ctx.car_code}).mappings().first()
        if row:
            ctx.geometry_wkt = row["wkt"]
            ctx.centroid = {"lat": row["lat"], "lon": row["lon"]}
            ctx.area_ha = row["area_ha"]
            ctx.uf = row["uf"]
            ctx.municipio = row["municipio"]
            ctx.bbox = [row["xmin"], row["ymin"], row["xmax"], row["ymax"]]

    # --- 2) Geometria direta ---
    elif req.get("geometry"):
        ctx.input_type = "geometry"
        import json as _json
        geom_json = req["geometry"] if isinstance(req["geometry"], dict) else _json.loads(req["geometry"])
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT ST_AsText(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326)) AS wkt,
                       ST_Area(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326)::geography) / 10000.0 AS area_ha,
                       ST_X(ST_Centroid(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326))) AS lon,
                       ST_Y(ST_Centroid(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326))) AS lat,
                       ST_XMin(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326)) AS xmin,
                       ST_YMin(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326)) AS ymin,
                       ST_XMax(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326)) AS xmax,
                       ST_YMax(ST_SetSRID(ST_GeomFromGeoJSON(:g), 4326)) AS ymax
            """), {"g": _json.dumps(geom_json)}).mappings().first()
        if row:
            ctx.geometry_wkt = row["wkt"]
            ctx.centroid = {"lat": row["lat"], "lon": row["lon"]}
            ctx.area_ha = row["area_ha"]
            ctx.bbox = [row["xmin"], row["ymin"], row["xmax"], row["ymax"]]

    # --- 3) Point + radius ---
    elif req.get("point"):
        ctx.input_type = "point_radius"
        p = req["point"]
        radius_km = float(req.get("radius_km", 5))
        lat = float(p.get("lat") or p.get("latitude"))
        lon = float(p.get("lon") or p.get("longitude"))
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT ST_AsText(ST_Buffer(
                         ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                         :r * 1000
                       )::geometry) AS wkt,
                       ST_XMin(ST_Buffer(
                         ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                         :r * 1000
                       )::geometry) AS xmin,
                       ST_YMin(ST_Buffer(
                         ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                         :r * 1000
                       )::geometry) AS ymin,
                       ST_XMax(ST_Buffer(
                         ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                         :r * 1000
                       )::geometry) AS xmax,
                       ST_YMax(ST_Buffer(
                         ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                         :r * 1000
                       )::geometry) AS ymax
            """), {"lat": lat, "lon": lon, "r": radius_km}).mappings().first()
        ctx.geometry_wkt = row["wkt"]
        ctx.centroid = {"lat": lat, "lon": lon}
        ctx.area_ha = 3.14159 * (radius_km ** 2) * 100  # pi*r² em ha
        ctx.bbox = [row["xmin"], row["ymin"], row["xmax"], row["ymax"]]

    # --- 4) BBox ---
    elif req.get("bbox"):
        ctx.input_type = "bbox"
        bb = req["bbox"]  # [w, s, e, n]
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT ST_AsText(ST_MakeEnvelope(:w, :s, :e, :n, 4326)) AS wkt,
                       ST_Area(ST_MakeEnvelope(:w, :s, :e, :n, 4326)::geography) / 10000.0 AS area_ha,
                       ST_X(ST_Centroid(ST_MakeEnvelope(:w, :s, :e, :n, 4326))) AS lon,
                       ST_Y(ST_Centroid(ST_MakeEnvelope(:w, :s, :e, :n, 4326))) AS lat
            """), {"w": bb[0], "s": bb[1], "e": bb[2], "n": bb[3]}).mappings().first()
        ctx.geometry_wkt = row["wkt"]
        ctx.centroid = {"lat": row["lat"], "lon": row["lon"]}
        ctx.area_ha = row["area_ha"]
        ctx.bbox = list(bb)

    # --- 5) Município ---
    elif req.get("municipio_ibge"):
        ctx.input_type = "municipio"
        ctx.municipio_ibge = str(req["municipio_ibge"])
        # Polígono do município via bigquery_geo_municipios se existir
        try:
            with engine.connect() as conn:
                row = conn.execute(text("""
                    SELECT COALESCE(name,'') AS municipio, uf_sigla AS uf,
                           ST_AsText(geometry) AS wkt,
                           ST_Area(geometry::geography) / 10000.0 AS area_ha,
                           ST_X(ST_Centroid(geometry)) AS lon,
                           ST_Y(ST_Centroid(geometry)) AS lat
                    FROM bigquery_geo_municipios
                    WHERE id_municipio::text = :code
                    LIMIT 1
                """), {"code": ctx.municipio_ibge}).mappings().first()
            if row:
                ctx.geometry_wkt = row["wkt"]
                ctx.centroid = {"lat": row["lat"], "lon": row["lon"]}
                ctx.area_ha = row["area_ha"]
                ctx.municipio = row["municipio"]
                ctx.uf = row["uf"]
        except Exception:
            pass

    # --- 6) CPF/CNPJ (dossiê da pessoa — agrega todos os imóveis) ---
    elif req.get("cpf_cnpj"):
        ctx.input_type = "cpf_cnpj"
        ctx.cpf_cnpj = str(req["cpf_cnpj"]).replace(".", "").replace("/", "").replace("-", "")
        # Não há geometria — coleta dados por CPF

    # --- Campos extras ---
    if req.get("cpf_cnpj") and not ctx.cpf_cnpj:
        ctx.cpf_cnpj = str(req["cpf_cnpj"]).replace(".", "").replace("/", "").replace("-", "")

    return ctx


def _infer_type(req: dict) -> str:
    for k, v in (("car_code", "car"), ("geometry", "geometry"), ("point", "point_radius"),
                 ("bbox", "bbox"), ("municipio_ibge", "municipio"), ("cpf_cnpj", "cpf_cnpj")):
        if req.get(k):
            return v
    return "unknown"


# ==========================================================================
# Coletores por seção — cada um retorna um dict da sua seção
# ==========================================================================


def _safe(fn: Callable[[DossieContext], dict], section: str, errors: dict) -> dict:
    """Roda coletor e captura erro em dict errors sem quebrar o todo."""
    try:
        return fn(ctx_for_wrapper) if False else fn(_current_ctx)
    except Exception as e:  # pragma: no cover (placeholder)
        logger.exception("seção %s falhou", section)
        errors[section] = f"{type(e).__name__}: {e}"
        return {}


def coletar_identificacao(ctx: DossieContext) -> dict:
    """Seção 1 — identificação e contexto territorial."""
    d: dict[str, Any] = {
        "input_type": ctx.input_type,
        "car_code": ctx.car_code,
        "cpf_cnpj_mask": _mask_cpf_cnpj(ctx.cpf_cnpj) if ctx.cpf_cnpj else None,
        "owner_name": ctx.owner_name,
        "centroid": ctx.centroid,
        "area_ha": round(ctx.area_ha, 4) if ctx.area_ha else None,
        "bbox": ctx.bbox,
        "municipio": ctx.municipio,
        "uf": ctx.uf,
    }

    # Preenche município/UF via centróide se faltar
    if ctx.centroid and not (ctx.uf and ctx.municipio):
        engine = get_engine()
        try:
            with engine.connect() as conn:
                row = conn.execute(text("""
                    SELECT COALESCE(name,'') AS municipio, uf_sigla AS uf
                    FROM bigquery_geo_municipios
                    WHERE ST_Contains(geometry, ST_SetSRID(ST_MakePoint(:lon,:lat),4326))
                    LIMIT 1
                """), ctx.centroid).mappings().first()
                if row:
                    d["municipio"] = ctx.municipio = row["municipio"]
                    d["uf"] = ctx.uf = row["uf"]
        except Exception:
            pass

    # Bioma
    if ctx.centroid:
        engine = get_engine()
        try:
            with engine.connect() as conn:
                row = conn.execute(text("""
                    SELECT name AS bioma FROM bigquery_geo_biomas
                    WHERE ST_Contains(geometry, ST_SetSRID(ST_MakePoint(:lon,:lat),4326))
                    LIMIT 1
                """), ctx.centroid).mappings().first()
                if row:
                    d["bioma"] = ctx.bioma = row["bioma"]
        except Exception:
            pass

    d["amazonia_legal"] = (ctx.uf or "") in ("AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO")
    return d


def coletar_fundiario(ctx: DossieContext) -> dict:
    """Seção 2 — situação fundiária e sobreposições."""
    if not ctx.geometry_wkt:
        return {"note": "Sem geometria para análise fundiária"}

    engine = get_engine()
    d: dict[str, Any] = {}

    layers = [
        ("cars_sobrepostos", "sicar_completo", "cod_imovel, area AS area_ha, uf, status_imovel AS status"),
        ("sigef_parcelas", "sigef_parcelas", "parcela_codigo, nome_area AS nome, status"),
        ("terras_indigenas", "geo_terras_indigenas", "terrai_nom AS nome, etnia_nome AS etnia, fase_ti AS fase"),
        ("unidades_conservacao", "geo_unidades_conservacao", "nomeuc AS nome, siglacateg AS categoria, grupouc AS grupo"),
        ("assentamentos_incra", "incra_assentamentos", "nome_proje AS nome, area_ha, num_famili AS familias, forma_obte AS forma"),
        ("quilombolas_incra", "incra_quilombolas", "nome, area_ha, fase"),
        ("sigmine", "sigmine_processos", "processo, fase, subs AS substancia, area_ha"),
    ]
    wkt = f"ST_GeomFromText('{ctx.geometry_wkt}', 4326)"

    with engine.connect() as conn:
        for key, table, cols in layers:
            try:
                rows = conn.execute(text(f"""
                    SELECT {cols}
                    FROM {table}
                    WHERE ST_Intersects(geometry, {wkt})
                    LIMIT 20
                """)).mappings().all()
                d[key] = [dict(r) for r in rows]
            except Exception as e:
                d[key] = []
                logger.warning("fundiario %s falhou: %s", key, e)

    d["summary"] = {
        k: len(v) if isinstance(v, list) else 0
        for k, v in d.items() if k != "summary"
    }
    return d


def coletar_compliance(ctx: DossieContext) -> dict:
    """Seção 3 — MCR 2.9 expandido (32 critérios)."""
    try:
        from app.services.mcr29_expanded import evaluate_mcr29_full
        result = evaluate_mcr29_full(ctx.car_code, ctx.cpf_cnpj)
        return result.to_dict()
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def coletar_ambiental(ctx: DossieContext) -> dict:
    """Seção 4 — desmatamento, embargos, autos."""
    if not ctx.geometry_wkt:
        return {}
    engine = get_engine()
    wkt = f"ST_GeomFromText('{ctx.geometry_wkt}', 4326)"
    d: dict[str, Any] = {}

    try:
        with engine.connect() as conn:
            d["prodes_pos_2019_count"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM geo_prodes WHERE year >= 2019 AND ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
            d["deter_12m_amazonia"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM geo_deter_amazonia
                WHERE view_date >= CURRENT_DATE - INTERVAL '12 months'
                AND ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
            d["deter_12m_cerrado"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM geo_deter_cerrado
                WHERE view_date >= CURRENT_DATE - INTERVAL '12 months'
                AND ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
            d["mapbiomas_alerts_pos_2019"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM geo_mapbiomas_alertas
                WHERE "ANODETEC"::int >= 2019 AND ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
            d["embargos_icmbio"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM geo_embargos_icmbio WHERE ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
            d["embargos_ibama"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM ibama_embargos WHERE ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
            d["autos_ibama_geo"] = int(conn.execute(text(f"""
                SELECT COUNT(*) FROM geo_autos_ibama WHERE ST_Intersects(geometry, {wkt})
            """)).scalar() or 0)
    except Exception as e:
        d["error"] = str(e)

    return d


def coletar_proprietario(ctx: DossieContext) -> dict:
    """Seção 5 — dossiê do proprietário por CPF/CNPJ."""
    if not ctx.cpf_cnpj:
        return {"note": "CPF/CNPJ não informado"}

    engine = get_engine()
    cpf = ctx.cpf_cnpj
    d: dict[str, Any] = {"cpf_cnpj_mask": _mask_cpf_cnpj(cpf)}

    try:
        with engine.connect() as conn:
            d["lista_suja_mte"] = int(conn.execute(text("""
                SELECT COUNT(*) FROM environmental_alerts
                WHERE source='MTE' AND cpf_cnpj = :cpf
            """), {"cpf": cpf}).scalar() or 0)

            d["ceis"] = int(conn.execute(text("""
                SELECT COUNT(*) FROM ceis_registros WHERE cpf_cnpj = :cpf
            """), {"cpf": cpf}).scalar() or 0)
            d["cnep"] = int(conn.execute(text("""
                SELECT COUNT(*) FROM cnep_registros WHERE cpf_cnpj = :cpf
            """), {"cpf": cpf}).scalar() or 0)

            d["autos_ibama_sifisc"] = int(conn.execute(text("""
                SELECT COUNT(*) FROM ibama_autos_infracao WHERE cpf_cnpj_infrator = :cpf
            """), {"cpf": cpf}).scalar() or 0)
            d["multa_total_ibama_rs"] = float(conn.execute(text("""
                SELECT COALESCE(SUM(valor_auto), 0) FROM ibama_autos_infracao
                WHERE cpf_cnpj_infrator = :cpf
            """), {"cpf": cpf}).scalar() or 0)

            # Outros imóveis do mesmo proprietário
            try:
                out = conn.execute(text("""
                    SELECT cod_imovel, uf, area FROM sicar_completo WHERE cod_imovel IN (
                        SELECT car_code FROM properties WHERE owner_cpf_cnpj = :cpf
                    ) LIMIT 20
                """), {"cpf": cpf}).mappings().all()
                d["outros_imoveis"] = [dict(r) for r in out]
            except Exception:
                d["outros_imoveis"] = []
    except Exception as e:
        d["error"] = str(e)

    return d


def coletar_credito(ctx: DossieContext) -> dict:
    """Seção 6 — crédito rural (SICOR via MapBiomas Crédito Rural)."""
    if not ctx.geometry_wkt:
        return {}
    engine = get_engine()
    wkt = f"ST_GeomFromText('{ctx.geometry_wkt}', 4326)"
    try:
        with engine.connect() as conn:
            row = conn.execute(text(f"""
                SELECT
                    COUNT(*)::int AS contratos,
                    COALESCE(SUM(vl_parc_credito), 0)::float AS total_rs,
                    COALESCE(SUM(vl_area_financ), 0)::float AS area_ha,
                    MAX(year)::int AS ano_mais_recente,
                    ARRAY_AGG(DISTINCT cnpj_if) FILTER (WHERE cnpj_if IS NOT NULL) AS bancos
                FROM mapbiomas_credito_rural
                WHERE ST_Intersects(geom, {wkt})
            """)).mappings().first()
            return dict(row) if row else {}
    except Exception as e:
        return {"error": str(e)}


def coletar_mercado(ctx: DossieContext) -> dict:
    """Seção 7 — preços das commodities na UF."""
    if not ctx.uf:
        return {"note": "UF não identificada"}
    engine = get_engine()
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT commodity, preco_estadual, preco_nacional, unit, mes_ano
                FROM market_prices_uf
                WHERE uf = :uf
                  AND mes_ano = (
                    SELECT mes_ano FROM market_prices_uf
                    WHERE uf = :uf ORDER BY collected_at DESC LIMIT 1
                  )
                ORDER BY commodity
            """), {"uf": ctx.uf}).mappings().all()
            return {
                "uf": ctx.uf,
                "commodities": [dict(r) for r in rows],
                "observacao": "Preços do último mês disponível via Agrolink",
            }
    except Exception as e:
        return {"error": str(e)}


def coletar_logistica(ctx: DossieContext) -> dict:
    """Seção 8 — distância a armazéns, frigoríficos, portos, rodovias, ferrovias."""
    if not ctx.centroid:
        return {}
    engine = get_engine()
    lat, lon = ctx.centroid["lat"], ctx.centroid["lon"]
    d: dict[str, Any] = {}
    try:
        with engine.connect() as conn:
            def _nearest(table, limit=3, label="tipo"):
                rows = conn.execute(text(f"""
                    SELECT ST_Y(ST_Centroid(geometry)) AS lat,
                           ST_X(ST_Centroid(geometry)) AS lon,
                           ST_DistanceSphere(
                             ST_Centroid(geometry),
                             ST_SetSRID(ST_MakePoint(:lon,:lat), 4326)
                           )/1000.0 AS dist_km
                    FROM {table}
                    ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(:lon,:lat), 4326)
                    LIMIT :lim
                """), {"lat": lat, "lon": lon, "lim": limit}).mappings().all()
                return [
                    {"lat": r["lat"], "lon": r["lon"], "distancia_km": round(r["dist_km"], 2)}
                    for r in rows
                ]
            d["armazens"] = _nearest("geo_armazens_silos")
            d["frigorificos"] = _nearest("geo_frigorificos")
            d["portos"] = _nearest("geo_portos")
            # Distância à rodovia/ferrovia mais próxima
            for table, label in [
                ("geo_rodovias_federais", "rodovia_federal_km"),
                ("geo_ferrovias", "ferrovia_km"),
            ]:
                try:
                    row = conn.execute(text(f"""
                        SELECT MIN(ST_DistanceSphere(
                                 ST_ClosestPoint(geometry, ST_SetSRID(ST_MakePoint(:lon,:lat), 4326)),
                                 ST_SetSRID(ST_MakePoint(:lon,:lat), 4326)
                               ))/1000.0 AS dist_km
                        FROM {table}
                        WHERE ST_DWithin(geometry, ST_SetSRID(ST_MakePoint(:lon,:lat), 4326), 5.0)
                    """), {"lat": lat, "lon": lon}).mappings().first()
                    d[label] = round(row["dist_km"], 2) if row and row["dist_km"] else None
                except Exception:
                    d[label] = None
    except Exception as e:
        d["error"] = str(e)
    return d


def coletar_energia(ctx: DossieContext) -> dict:
    """Seção 9 — ANEEL usinas e linhas de transmissão no perímetro."""
    if not ctx.geometry_wkt:
        return {}
    engine = get_engine()
    wkt = f"ST_GeomFromText('{ctx.geometry_wkt}', 4326)"
    try:
        with engine.connect() as conn:
            usinas = conn.execute(text(f"""
                SELECT nome, tipo, potencia_mw, municipio
                FROM aneel_usinas
                WHERE geometry IS NOT NULL AND ST_Intersects(geometry, {wkt})
                LIMIT 20
            """)).mappings().all()
            linhas = conn.execute(text(f"""
                SELECT nome, tensao_kv, operador, comprimento_km
                FROM aneel_linhas_transmissao
                WHERE geometry IS NOT NULL AND ST_Intersects(geometry, {wkt})
                LIMIT 20
            """)).mappings().all()
            return {
                "usinas_no_perimetro": [dict(r) for r in usinas],
                "linhas_transmissao_no_perimetro": [dict(r) for r in linhas],
            }
    except Exception as e:
        return {"error": str(e)}


def coletar_valuation(ctx: DossieContext) -> dict:
    """Seção 10 — valuation NBR 14.653-3 nível expedito."""
    if not ctx.area_ha or not ctx.uf:
        return {"note": "Sem área ou UF suficientes para valuation"}
    PRECO_POR_UF = {
        "MT": 40_000, "MS": 35_000, "GO": 38_000, "MG": 32_000,
        "SP": 55_000, "PR": 48_000, "SC": 42_000, "RS": 38_000,
        "BA": 22_000, "PI": 15_000, "MA": 13_000, "TO": 14_000,
        "PA": 18_000, "RO": 16_000, "AC": 10_000, "AM": 8_000,
        "RR": 8_000, "AP": 7_000, "CE": 12_000, "RN": 11_000,
        "PB": 11_000, "PE": 13_000, "AL": 15_000, "SE": 14_000,
        "ES": 28_000, "RJ": 40_000, "DF": 60_000,
    }
    preco_ha = PRECO_POR_UF.get(ctx.uf or "", 20_000)
    valor_base = ctx.area_ha * preco_ha

    # Desconto por overlaps críticos (usa ambiental)
    amb = coletar_ambiental(ctx)
    fundiario = coletar_fundiario(ctx)
    desconto_pct = 0
    detalhes = []
    if fundiario.get("terras_indigenas"):
        desconto_pct += 1.0
        detalhes.append({"motivo": "sobreposição com Terra Indígena", "desconto_pct": 100})
    elif fundiario.get("unidades_conservacao"):
        desconto_pct += 0.5
        detalhes.append({"motivo": "sobreposição com UC", "desconto_pct": 50})
    elif amb.get("embargos_ibama", 0) + amb.get("embargos_icmbio", 0) > 0:
        desconto_pct += 0.4
        detalhes.append({"motivo": "embargo ambiental ativo", "desconto_pct": 40})
    elif amb.get("prodes_pos_2019_count", 0) > 0:
        desconto_pct += 0.2
        detalhes.append({"motivo": "desmate PRODES pós-2019", "desconto_pct": 20})

    desconto_pct = min(desconto_pct, 1.0)
    valor_ajustado = valor_base * (1 - desconto_pct)

    return {
        "metodologia": "NBR 14.653-3 nível expedito (inferência regional)",
        "preco_medio_ha_uf_rs": preco_ha,
        "area_ha": round(ctx.area_ha, 2),
        "valor_base_rs": round(valor_base, 2),
        "desconto_pct": desconto_pct * 100,
        "desconto_motivos": detalhes,
        "valor_estimado_rs": round(valor_ajustado, 2),
        "faixa_confiança_rs": {
            "min": round(valor_ajustado * 0.75, 2),
            "max": round(valor_ajustado * 1.25, 2),
        },
        "disclaimer": "Estimativa indicativa. Laudo NBR 14.653-3 completo exige avaliador credenciado com visita e análise comparativa de elementos.",
    }


def coletar_juridico(ctx: DossieContext) -> dict:
    """Seção 11 — processos e publicações DJEN/DataJud."""
    if not ctx.cpf_cnpj:
        return {"note": "CPF/CNPJ não informado"}
    engine = get_engine()
    try:
        with engine.connect() as conn:
            processos = int(conn.execute(text("""
                SELECT COUNT(*) FROM legal_records WHERE cpf_cnpj = :cpf
            """), {"cpf": ctx.cpf_cnpj}).scalar() or 0)
            execucoes = int(conn.execute(text("""
                SELECT COUNT(*) FROM legal_records
                WHERE cpf_cnpj = :cpf AND (
                    description ILIKE '%execu%o fiscal%' OR record_type = 'debt'
                )
            """), {"cpf": ctx.cpf_cnpj}).scalar() or 0)
            return {
                "datajud_total": processos,
                "execucoes_fiscais": execucoes,
                "observacao": "Consulta por CPF/CNPJ na base legal_records local",
            }
    except Exception as e:
        return {"error": str(e)}


def coletar_agronomia(ctx: DossieContext) -> dict:
    """Seção 12 — aptidão agrícola e cobertura atual."""
    if not ctx.geometry_wkt:
        return {}
    engine = get_engine()
    wkt = f"ST_GeomFromText('{ctx.geometry_wkt}', 4326)"
    d: dict[str, Any] = {}
    # MapBiomas cobertura do último ano
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(f"""
                SELECT class_name, SUM(area_ha) AS area_ha
                FROM mapbiomas_cobertura_2024
                WHERE ST_Intersects(geom, {wkt})
                GROUP BY class_name
                ORDER BY area_ha DESC
                LIMIT 10
            """)).mappings().all()
            d["cobertura_2024"] = [dict(r) for r in rows]
    except Exception:
        d["cobertura_2024"] = []
    # ZARC (via endpoint Embrapa) — aqui só marca que está disponível
    d["zarc_endpoint"] = f"/api/v1/embrapa/agritec/zarc?municipio_ibge={ctx.municipio_ibge}" if ctx.municipio_ibge else None
    return d


# ==========================================================================
# Recomendações por persona
# ==========================================================================


def gerar_recomendacao(ctx: DossieContext, secoes: dict) -> dict:
    """Conclusão adaptada ao tipo de usuário final."""
    persona = ctx.persona
    comp = secoes.get("compliance", {}) or {}
    amb = secoes.get("ambiental", {}) or {}
    fund = secoes.get("fundiario", {}) or {}
    val = secoes.get("valuation", {}) or {}

    risk = comp.get("risk_level", "?")
    status = comp.get("overall_status", "?")
    score = comp.get("overall_score", 0)

    red_flags: list[str] = []
    if fund.get("terras_indigenas"):
        red_flags.append(f"BLOQUEANTE: sobreposição com {len(fund['terras_indigenas'])} Terra(s) Indígena(s)")
    if fund.get("unidades_conservacao"):
        red_flags.append(f"CRÍTICO: {len(fund['unidades_conservacao'])} sobreposição(ões) com Unidade de Conservação")
    n_emb = (amb.get("embargos_ibama", 0) or 0) + (amb.get("embargos_icmbio", 0) or 0)
    if n_emb > 0:
        red_flags.append(f"BLOQUEANTE: {n_emb} embargo(s) ambiental(is) ativo(s) na área")
    if amb.get("prodes_pos_2019_count", 0) > 0:
        red_flags.append(f"MCR 2.9: desmatamento PRODES pós-2019 ({amb['prodes_pos_2019_count']} polígonos)")
    if amb.get("deter_12m_amazonia", 0) + amb.get("deter_12m_cerrado", 0) > 0:
        red_flags.append(f"Alertas DETER nos últimos 12 meses: {amb.get('deter_12m_amazonia',0) + amb.get('deter_12m_cerrado',0)}")

    base = {
        "persona": persona,
        "risk_level": risk,
        "overall_status": status,
        "score": score,
        "red_flags": red_flags,
    }

    tips: list[str] = []
    if persona == "comprador":
        tips = [
            f"Valor estimado: R$ {val.get('valor_estimado_rs', 0):,.0f} (faixa {val.get('faixa_confiança_rs',{}).get('min',0):,.0f}–{val.get('faixa_confiança_rs',{}).get('max',0):,.0f}).",
            "Solicite matrícula atualizada, CCIR e ITR dos últimos 5 anos ao vendedor.",
            "Consulte certidões negativas (federal, estadual, trabalhista, criminal) do vendedor.",
            "Em caso de red flags, exija descontos proporcionais ou desista da negociação.",
        ]
    elif persona == "advogado":
        tips = [
            "Monte a diligência documental usando a seção 'Fundiário' como checklist.",
            "Se houver processos DataJud, verifique risco de penhora ou constrição.",
            "Se o imóvel estiver em embargo/Lista Suja, avalie via inibitória ou ação declaratória.",
            "Use `/property/{car}/minuta` para redigir peças pré-formatadas com os dados do dossiê.",
        ]
    elif persona == "investidor":
        tips = [
            f"Score MCR 2.9: {score}/1000 ({risk}). Abaixo de 600 dificulta estruturação de FII Agro.",
            "A seção 'Mercado' mostra preço das commodities na UF — base para projeção de receita.",
            "Embargos/autos ativos impedem uso como garantia fiduciária (CPR-F, CDA-WA).",
        ]
    elif persona == "trading":
        tips = [
            "Veja a seção 'Logística' para distância a armazéns, frigoríficos e portos.",
            "Compliance EUDR: se houver desmate pós-31/12/2020, produto bloqueado para UE.",
            "Cotações da UF estão na seção 'Mercado' (13 commodities × últimos meses).",
        ]
    elif persona == "consultor":
        tips = [
            "Use a seção 'Compliance MCR 2.9' como base do parecer ambiental.",
            "APP/RL nos dados declarativos do CAR — verificar geometrias no SICAR oficial.",
            "Em caso de irregularidade, proponha PRAD, CRA (Cota Reserva) ou TAC.",
        ]
    elif persona == "produtor":
        tips = [
            "Seção 'Agronomia' mostra cobertura MapBiomas e culturas do município.",
            "Compliance MCR 2.9: resolver pendências antes de solicitar crédito rural.",
            "Preços atuais na UF estão em 'Mercado' — útil para decisão de venda.",
        ]

    base["tips"] = tips
    return base


# ==========================================================================
# Orquestrador
# ==========================================================================


# Precisamos de um global de contexto para _safe — simplificação do MVP
_current_ctx: Optional[DossieContext] = None  # type: ignore


def gerar_dossie(req: dict) -> dict:
    """Pipeline principal. Recebe payload, devolve dossiê estruturado."""
    global _current_ctx
    ctx = resolve_input(req)
    _current_ctx = ctx
    errors: dict[str, str] = {}

    secoes: dict[str, Any] = {}

    # Rodar cada coletor isoladamente
    for key, fn in [
        ("identificacao", coletar_identificacao),
        ("fundiario", coletar_fundiario),
        ("compliance", coletar_compliance),
        ("ambiental", coletar_ambiental),
        ("proprietario", coletar_proprietario),
        ("credito_rural", coletar_credito),
        ("mercado", coletar_mercado),
        ("logistica", coletar_logistica),
        ("energia", coletar_energia),
        ("valuation", coletar_valuation),
        ("juridico", coletar_juridico),
        ("agronomia", coletar_agronomia),
    ]:
        try:
            secoes[key] = fn(ctx)
        except Exception as e:
            logger.exception("seção %s falhou", key)
            errors[key] = f"{type(e).__name__}: {e}"
            secoes[key] = {"error": errors[key]}

    recomendacao = gerar_recomendacao(ctx, secoes)

    return {
        "dossie_id": _gen_id(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": ctx.nome_dossie or _default_title(ctx),
        "persona": ctx.persona,
        "contexto": {
            "input_type": ctx.input_type,
            "car_code": ctx.car_code,
            "cpf_cnpj_mask": _mask_cpf_cnpj(ctx.cpf_cnpj) if ctx.cpf_cnpj else None,
            "area_ha": round(ctx.area_ha, 4) if ctx.area_ha else None,
            "centroid": ctx.centroid,
            "bbox": ctx.bbox,
            "municipio": ctx.municipio,
            "uf": ctx.uf,
            "bioma": ctx.bioma,
        },
        "secoes": secoes,
        "recomendacao": recomendacao,
        "errors": errors,
        "metadata": {
            "generator": "AgroJus Dossiê v1",
            "fontes": [
                "SICAR/SFB", "SIGEF/INCRA", "FUNAI", "ICMBio", "IBAMA dados abertos",
                "INPE TerraBrasilis (PRODES/DETER)", "MapBiomas Alerta", "MapBiomas Cobertura",
                "BCB SICOR", "IBGE", "Agrolink", "ANEEL", "CGU Portal Transparência",
                "CNJ DataJud", "CNJ DJEN",
            ],
            "caveats": [
                "Dados sujeitos a atualização nas fontes oficiais",
                "Valuation é indicativo — NBR 14.653-3 completa exige avaliador credenciado",
                "Verificação humana da documentação é obrigatória antes de decisão final",
            ],
        },
    }


# ==========================================================================
# Helpers
# ==========================================================================


def _gen_id() -> str:
    import uuid
    return uuid.uuid4().hex[:12]


def _mask_cpf_cnpj(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    if len(s) >= 11:
        return s[:3] + "." + "*" * (len(s) - 6) + s[-4:]
    return s


def _default_title(ctx: DossieContext) -> str:
    if ctx.car_code:
        return f"Dossiê Rural · CAR {ctx.car_code[:25]}…"
    if ctx.cpf_cnpj:
        return f"Dossiê de Proprietário · {_mask_cpf_cnpj(ctx.cpf_cnpj)}"
    if ctx.input_type == "point_radius":
        return f"Dossiê · Área circular {ctx.area_ha:.0f} ha"
    if ctx.input_type == "geometry":
        return f"Dossiê · Polígono ({ctx.area_ha or 0:.0f} ha)"
    if ctx.municipio:
        return f"Dossiê · {ctx.municipio}/{ctx.uf}"
    return "Dossiê Agrofundiário"
