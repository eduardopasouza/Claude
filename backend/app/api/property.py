"""
Endpoints de busca e visualizacao de imoveis rurais.

- Busca de CARs por municipio, UF, texto
- GeoJSON do imovel para renderizar no Leaflet
- GeoJSON das camadas sobrepostas (TI, UC, embargos, alertas)
"""

import logging
from typing import Optional

from fastapi import APIRouter, Query
from sqlalchemy import text

from app.models.database import get_engine

logger = logging.getLogger("agrojus.property")
router = APIRouter()


def _get_car_table(engine) -> str:
    """Retorna tabela CAR preferida (sicar_completo > geo_car)."""
    try:
        with engine.connect() as conn:
            n = conn.execute(text("SELECT COUNT(*) FROM sicar_completo")).scalar()
            if n and n > 0:
                return "sicar_completo"
    except Exception:
        pass
    return "geo_car"


@router.get("/search")
def search_properties(
    q: Optional[str] = Query(None, description="Texto livre (codigo CAR, municipio, etc)"),
    uf: Optional[str] = Query(None, description="Sigla do estado (MA, PA, MT...)"),
    municipio: Optional[str] = Query(None, description="Nome do municipio"),
    status: Optional[str] = Query(None, description="Status do CAR (AT, PE, CA, SU)"),
    area_min: Optional[float] = Query(None, description="Area minima em hectares"),
    area_max: Optional[float] = Query(None, description="Area maxima em hectares"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """
    Busca imoveis rurais no PostGIS.

    Aceita filtros combinados. Retorna lista paginada com dados basicos.
    Ideal para autocomplete e listagem.
    """
    engine = get_engine()
    conditions = []
    params = {}

    # Usa sicar_completo (BigQuery, 79M) se existir, senao geo_car (WFS, 135k)
    table = _get_car_table(engine)
    has_municipio = table == "geo_car"

    if q:
        if has_municipio:
            conditions.append("(cod_imovel ILIKE :q OR municipio ILIKE :q_mun)")
            params["q_mun"] = f"%{q}%"
        else:
            conditions.append("cod_imovel ILIKE :q")
        params["q"] = f"%{q}%"

    if uf:
        conditions.append("uf = :uf")
        params["uf"] = uf.upper()

    if municipio and has_municipio:
        conditions.append("municipio ILIKE :municipio")
        params["municipio"] = f"%{municipio}%"

    if status:
        conditions.append("status_imovel = :status")
        params["status"] = status.upper()

    if area_min is not None:
        conditions.append("area >= :area_min")
        params["area_min"] = area_min

    if area_max is not None:
        conditions.append("area <= :area_max")
        params["area_max"] = area_max

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    offset = (page - 1) * page_size
    params["limit"] = page_size
    params["offset"] = offset

    municipio_col = "municipio" if has_municipio else "'' as municipio"

    sql_count = f"SELECT COUNT(*) FROM {table} {where}"
    sql_data = f"""
        SELECT
            cod_imovel,
            {municipio_col},
            uf,
            area,
            COALESCE(status_imovel, '') as status,
            COALESCE(tipo_imovel, '') as tipo,
            COALESCE(m_fiscal, 0) as modulos_fiscais,
            cod_municipio_ibge,
            ST_X(ST_Centroid(geometry)) as centroid_lon,
            ST_Y(ST_Centroid(geometry)) as centroid_lat
        FROM {table}
        {where}
        ORDER BY uf, cod_imovel
        LIMIT :limit OFFSET :offset
    """

    with engine.connect() as conn:
        total = conn.execute(text(sql_count), params).scalar()
        rows = conn.execute(text(sql_data), params).mappings().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total else 0,
        "results": [
            {
                "car_code": r["cod_imovel"],
                "municipio": r["municipio"],
                "uf": r["uf"],
                "area_ha": r["area"],
                "status": r["status"],
                "tipo": r["tipo"],
                "modulos_fiscais": r["modulos_fiscais"],
                "cod_municipio_ibge": r["cod_municipio_ibge"],
                "centroid": {
                    "lat": r["centroid_lat"],
                    "lon": r["centroid_lon"],
                } if r["centroid_lat"] else None,
            }
            for r in rows
        ],
    }


@router.get("/ufs")
def list_ufs():
    """Lista UFs disponiveis com contagem de CARs."""
    engine = get_engine()
    sql = """
        SELECT uf, COUNT(*) as total, ROUND(AVG(area)::numeric, 1) as area_media
        FROM geo_car
        WHERE uf IS NOT NULL
        GROUP BY uf
        ORDER BY uf
    """
    with engine.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return {
        "total_ufs": len(rows),
        "ufs": [
            {"uf": r["uf"], "total_cars": r["total"], "area_media_ha": float(r["area_media"] or 0)}
            for r in rows
        ],
    }


@router.get("/municipios")
def list_municipios(uf: str = Query(..., description="Sigla do estado")):
    """Lista municipios de uma UF com contagem de CARs."""
    engine = get_engine()
    sql = """
        SELECT municipio, COUNT(*) as total,
               ROUND(AVG(area)::numeric, 1) as area_media,
               cod_municipio_ibge
        FROM geo_car
        WHERE uf = :uf AND municipio IS NOT NULL
        GROUP BY municipio, cod_municipio_ibge
        ORDER BY municipio
    """
    with engine.connect() as conn:
        rows = conn.execute(text(sql), {"uf": uf.upper()}).mappings().all()

    return {
        "uf": uf.upper(),
        "total_municipios": len(rows),
        "municipios": [
            {
                "nome": r["municipio"],
                "total_cars": r["total"],
                "area_media_ha": float(r["area_media"] or 0),
                "cod_ibge": r["cod_municipio_ibge"],
            }
            for r in rows
        ],
    }


def _find_car_geojson(engine, car_code: str):
    """Busca GeoJSON do CAR em sicar_completo (prioridade) ou geo_car."""
    # sicar_completo primeiro (308k+ CARs)
    sql_sicar = text("""
        SELECT
            cod_imovel,
            '' as municipio,
            uf,
            area,
            COALESCE(status_imovel, '') as status,
            COALESCE(tipo_imovel, '') as tipo,
            COALESCE(m_fiscal, 0) as modulos_fiscais,
            ST_AsGeoJSON(geometry)::json as geojson
        FROM sicar_completo
        WHERE cod_imovel = :car_code
          AND geometry IS NOT NULL
        LIMIT 1
    """)
    sql_geocar = text("""
        SELECT
            cod_imovel,
            municipio,
            uf,
            area,
            COALESCE(status_imovel, '') as status,
            COALESCE(tipo_imovel, '') as tipo,
            COALESCE(m_fiscal, 0) as modulos_fiscais,
            ST_AsGeoJSON(geometry)::json as geojson
        FROM geo_car
        WHERE cod_imovel = :car_code
          AND geometry IS NOT NULL
        LIMIT 1
    """)
    with engine.connect() as conn:
        try:
            row = conn.execute(sql_sicar, {"car_code": car_code}).mappings().first()
            if row:
                return row
        except Exception:
            pass
        return conn.execute(sql_geocar, {"car_code": car_code}).mappings().first()


@router.get("/{car_code}/geojson")
def get_property_geojson(car_code: str):
    """
    Retorna GeoJSON FeatureCollection do imovel para Leaflet.

    Busca em sicar_completo (308k+) e geo_car (135k) como fallback.
    """
    engine = get_engine()
    row = _find_car_geojson(engine, car_code)

    if not row:
        return {"error": f"CAR {car_code} nao encontrado"}

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": row["cod_imovel"],
                "properties": {
                    "car_code": row["cod_imovel"],
                    "municipio": row["municipio"],
                    "uf": row["uf"],
                    "area_ha": row["area"],
                    "status": row["status"],
                    "tipo": row["tipo"],
                    "modulos_fiscais": float(row["modulos_fiscais"] or 0),
                    "layer": "imovel",
                },
                "geometry": row["geojson"],
            }
        ],
    }


_OVERLAP_CTE = """
    WITH car_geom AS (
        SELECT geometry FROM sicar_completo
        WHERE cod_imovel = :car_code AND geometry IS NOT NULL
        UNION ALL
        SELECT geometry FROM geo_car
        WHERE cod_imovel = :car_code AND geometry IS NOT NULL
        LIMIT 1
    )
"""


@router.get("/{car_code}/overlaps/geojson")
def get_overlaps_geojson(car_code: str):
    """
    Retorna GeoJSON FeatureCollection com TODAS as camadas
    que se sobrepoem ao imovel. Busca em sicar_completo e geo_car.

    Camadas incluidas: TI, UC, embargos ICMBio, PRODES, DETER,
    MapBiomas alertas, SIGEF parcelas.
    """
    engine = get_engine()

    overlap_queries = {
        "terras_indigenas": f"""
            {_OVERLAP_CTE}
            SELECT
                ti.terrai_nom as nome,
                ti.etnia_nome as etnia,
                ti.fase_ti as fase,
                'terra_indigena' as layer,
                '#FF0000' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, ti.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_terras_indigenas ti ON ST_Intersects(c.geometry, ti.geometry)
        """,
        "unidades_conservacao": f"""
            {_OVERLAP_CTE}
            SELECT
                uc.nomeuc as nome,
                uc.siglacateg as categoria,
                uc.grupouc as grupo,
                'unidade_conservacao' as layer,
                '#00AA00' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, uc.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_unidades_conservacao uc ON ST_Intersects(c.geometry, uc.geometry)
        """,
        "embargos_icmbio": f"""
            {_OVERLAP_CTE}
            SELECT
                e.autuado as nome,
                e.desc_infra as descricao,
                e.data as data_embargo,
                'embargo_icmbio' as layer,
                '#FF6600' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, e.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_embargos_icmbio e ON ST_Intersects(c.geometry, e.geometry)
        """,
        "prodes": f"""
            {_OVERLAP_CTE}
            SELECT
                p.year as ano,
                p.class_name as classe,
                'prodes' as layer,
                '#8B0000' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, p.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_prodes p ON ST_Intersects(c.geometry, p.geometry)
        """,
        "deter_amazonia": f"""
            {_OVERLAP_CTE}
            SELECT
                d.classname as classe,
                d.view_date::text as data,
                'deter_amazonia' as layer,
                '#FF4500' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, d.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_deter_amazonia d ON ST_Intersects(c.geometry, d.geometry)
        """,
        "deter_cerrado": f"""
            {_OVERLAP_CTE}
            SELECT
                d.classname as classe,
                d.view_date::text as data,
                'deter_cerrado' as layer,
                '#FF8C00' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, d.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_deter_cerrado d ON ST_Intersects(c.geometry, d.geometry)
        """,
        "mapbiomas_alertas": f"""
            {_OVERLAP_CTE}
            SELECT
                m."BIOMA" as bioma,
                m."ANODETEC"::int as ano,
                m."VPRESSAO" as vetor_pressao,
                'mapbiomas_alerta' as layer,
                '#CC00CC' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, m.geometry))::json as geojson
            FROM car_geom c
            JOIN geo_mapbiomas_alertas m ON ST_Intersects(c.geometry, m.geometry)
        """,
        "sigef_parcelas": f"""
            {_OVERLAP_CTE}
            SELECT
                s.parcela_codigo as nome,
                s.status,
                s.nome_area,
                'sigef' as layer,
                '#0066FF' as color,
                ST_AsGeoJSON(ST_Intersection(c.geometry, s.geometry))::json as geojson
            FROM car_geom c
            JOIN sigef_parcelas s ON ST_Intersects(c.geometry, s.geometry)
        """,
    }

    features = []
    layers_found = []

    with engine.connect() as conn:
        for layer_name, sql in overlap_queries.items():
            try:
                rows = conn.execute(text(sql), {"car_code": car_code}).mappings().all()
                for row in rows:
                    props = {k: v for k, v in dict(row).items() if k != "geojson"}
                    features.append({
                        "type": "Feature",
                        "properties": props,
                        "geometry": row["geojson"],
                    })
                if rows:
                    layers_found.append(layer_name)
            except Exception as e:
                logger.warning("Overlap query %s failed: %s", layer_name, e)

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "car_code": car_code,
            "total_features": len(features),
            "layers_found": layers_found,
            "layers_checked": list(overlap_queries.keys()),
        },
    }


# ---------------------------------------------------------------------------
# Logística: pontos de interesse mais próximos (KNN via PostGIS)
# ---------------------------------------------------------------------------
@router.get("/{car_code}/neighbors")
def get_nearest_logistics(car_code: str, limit_each: int = 5):
    """
    Retorna os pontos de interesse mais próximos do centróide do imóvel.

    Calcula distância em km (ST_Distance_Sphere) para:
      - armazéns/silos (CONAB SICARM)
      - frigoríficos (MAPA SIF)
      - portos (ANTAQ)
      - rodovias federais (DNIT) — ponto mais próximo
      - ferrovias (ANTT)
    """
    engine = get_engine()

    # Query o centroide do CAR
    with engine.connect() as conn:
        centroid = conn.execute(
            text(
                """
                SELECT ST_X(ST_Centroid(geometry)) as lon,
                       ST_Y(ST_Centroid(geometry)) as lat
                FROM sicar_completo
                WHERE cod_imovel = :car
                UNION ALL
                SELECT ST_X(ST_Centroid(geometry)) as lon,
                       ST_Y(ST_Centroid(geometry)) as lat
                FROM geo_car
                WHERE cod_imovel = :car
                LIMIT 1
                """
            ),
            {"car": car_code},
        ).mappings().first()

    if not centroid:
        return {"error": f"CAR {car_code} não encontrado"}

    lat, lon = centroid["lat"], centroid["lon"]

    # KNN para cada categoria — distância em km usando ST_DistanceSphere
    queries = {
        "armazens_silos": """
            SELECT ST_X(ST_Centroid(geometry)) as lon,
                   ST_Y(ST_Centroid(geometry)) as lat,
                   ST_DistanceSphere(ST_Centroid(geometry),
                     ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                   ) / 1000.0 as dist_km,
                   'Armazém/Silo' as tipo,
                   '' as nome
            FROM geo_armazens_silos
            ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
            LIMIT :lim
        """,
        "frigorificos": """
            SELECT ST_X(ST_Centroid(geometry)) as lon,
                   ST_Y(ST_Centroid(geometry)) as lat,
                   ST_DistanceSphere(ST_Centroid(geometry),
                     ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                   ) / 1000.0 as dist_km,
                   'Frigorífico' as tipo,
                   '' as nome
            FROM geo_frigorificos
            ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
            LIMIT :lim
        """,
        "portos": """
            SELECT ST_X(ST_Centroid(geometry)) as lon,
                   ST_Y(ST_Centroid(geometry)) as lat,
                   ST_DistanceSphere(ST_Centroid(geometry),
                     ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                   ) / 1000.0 as dist_km,
                   'Porto' as tipo,
                   COALESCE(nome, '') as nome
            FROM geo_portos
            ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
            LIMIT :lim
        """,
    }

    results: dict[str, list[dict]] = {}
    with engine.connect() as conn:
        for key, sql in queries.items():
            try:
                rows = conn.execute(
                    text(sql), {"lon": lon, "lat": lat, "lim": limit_each}
                ).mappings().all()
                results[key] = [
                    {
                        "tipo": r["tipo"],
                        "nome": r["nome"],
                        "lat": r["lat"],
                        "lon": r["lon"],
                        "distancia_km": round(r["dist_km"], 2),
                    }
                    for r in rows
                ]
            except Exception as e:
                logger.warning("neighbors %s failed: %s", key, e)
                results[key] = []

        # Distância ao ponto mais próximo de rodovia/ferrovia (não KNN, apenas min)
        for table, label in [
            ("geo_rodovias_federais", "rodovia_federal"),
            ("geo_ferrovias", "ferrovia"),
        ]:
            try:
                row = conn.execute(
                    text(
                        f"""
                        SELECT MIN(
                          ST_DistanceSphere(
                            ST_ClosestPoint(geometry, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)),
                            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                          )
                        ) / 1000.0 as dist_km
                        FROM {table}
                        WHERE ST_DWithin(geometry, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326), 5.0)
                        """
                    ),
                    {"lon": lon, "lat": lat},
                ).mappings().first()
                results[label] = [
                    {
                        "tipo": label.replace("_", " ").title(),
                        "distancia_km": round(row["dist_km"], 2) if row and row["dist_km"] else None,
                    }
                ]
            except Exception as e:
                logger.warning("neighbors %s failed: %s", label, e)
                results[label] = []

    return {
        "car_code": car_code,
        "centroid": {"lat": lat, "lon": lon},
        "neighbors": results,
    }


# ---------------------------------------------------------------------------
# Crédito rural: contratos MapBiomas (SICOR) intersectando o CAR
# ---------------------------------------------------------------------------
@router.get("/{car_code}/credit")
def get_credit_records(car_code: str, limit: int = 50):
    """
    Contratos de crédito rural com geometria cruzada ao CAR.

    Fonte: MapBiomas Crédito Rural (tabela mapbiomas_credito_rural, 5.6M registros)
    que já cruza SICOR/BCB com cobertura MapBiomas.
    """
    engine = get_engine()

    sql = text(
        """
        WITH car_geom AS (
            SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
            UNION ALL
            SELECT geometry FROM geo_car WHERE cod_imovel = :car
            LIMIT 1
        )
        SELECT
            mcr.order_number,
            mcr.year,
            mcr.car_code,
            mcr.vl_parc_credito,
            mcr.vl_area_financ,
            mcr.dt_emissao::text as dt_emissao,
            mcr.cnpj_if
        FROM car_geom c
        JOIN mapbiomas_credito_rural mcr
          ON ST_Intersects(c.geometry, mcr.geom)
        ORDER BY mcr.year DESC, mcr.vl_parc_credito DESC NULLS LAST
        LIMIT :lim
        """
    )

    try:
        with engine.connect() as conn:
            rows = conn.execute(sql, {"car": car_code, "lim": limit}).mappings().all()
    except Exception as e:
        logger.warning("credit query failed: %s", e)
        return {"error": str(e), "records": []}

    total_credito = sum((r.get("vl_parc_credito") or 0) for r in rows) if rows else 0
    total_area = sum((r.get("vl_area_financ") or 0) for r in rows) if rows else 0
    by_year: dict[str, dict] = {}
    for r in rows:
        y = str(r.get("year", "s/ano"))
        by_year.setdefault(y, {"year": y, "valor_total": 0, "area_total": 0, "contratos": 0})
        by_year[y]["valor_total"] += r.get("vl_parc_credito") or 0
        by_year[y]["area_total"] += r.get("vl_area_financ") or 0
        by_year[y]["contratos"] += 1

    return {
        "car_code": car_code,
        "summary": {
            "total_contratos": len(rows),
            "valor_total_rs": round(total_credito, 2),
            "area_financiada_ha": round(total_area, 2),
            "por_ano": sorted(by_year.values(), key=lambda x: x["year"]),
        },
        "records": [dict(r) for r in rows],
    }


# ---------------------------------------------------------------------------
# Valuation simplificado — NBR 14.653-3 nível 1 (inferência por região)
# ---------------------------------------------------------------------------
@router.get("/{car_code}/valuation")
def get_valuation(car_code: str):
    """
    Estima valor do imóvel baseado em:
      1. Área do imóvel (ha)
      2. Preço médio de terra por região (tabela land_prices ou heurística por UF)
      3. Aptidão agrícola inferida (se tem soja/milho PAM no município = valorizado)
      4. Desconto por sobreposições (TI -100%, UC -50%, embargo -40%)

    NBR 14.653-3 nível expedito. Laudo detalhado requer avaliador credenciado.
    """
    engine = get_engine()

    with engine.connect() as conn:
        # Área do imóvel + UF + cod_municipio_ibge
        prop = conn.execute(
            text(
                """
                SELECT cod_imovel, uf, area, cod_municipio_ibge
                FROM sicar_completo WHERE cod_imovel = :car
                UNION ALL
                SELECT cod_imovel, uf, area, ''::text as cod_municipio_ibge
                FROM geo_car WHERE cod_imovel = :car
                LIMIT 1
                """
            ),
            {"car": car_code},
        ).mappings().first()

    if not prop or not prop.get("area"):
        return {"error": "CAR não encontrado ou sem área"}

    area_ha = float(prop["area"])
    uf = prop["uf"]

    # Preço médio por ha por UF (heurística conservadora 2025 — bovinocultura+lavoura)
    # Fonte: Informa Economics / IMEA / Scot Consultoria
    PRECO_POR_UF = {
        "MT": 40_000, "MS": 35_000, "GO": 38_000, "MG": 32_000,
        "SP": 55_000, "PR": 48_000, "SC": 42_000, "RS": 38_000,
        "BA": 22_000, "PI": 15_000, "MA": 13_000, "TO": 14_000,
        "PA": 18_000, "RO": 16_000, "AC": 10_000, "AM": 8_000,
        "RR": 8_000, "AP": 7_000,
        "CE": 12_000, "RN": 11_000, "PB": 11_000, "PE": 13_000,
        "AL": 15_000, "SE": 14_000, "ES": 28_000, "RJ": 40_000,
        "DF": 60_000,
    }
    preco_ha_base = PRECO_POR_UF.get(uf, 20_000)

    # Ajuste por produção agrícola do município (se há soja, +15%; milho, +10%)
    # Vamos checar via SIDRA no cache (se disponível) — simplificação: só usa area
    valor_base = area_ha * preco_ha_base

    # Desconto por overlaps (reutiliza lógica do overlaps)
    discount = 0
    overlaps_detail = []
    try:
        with engine.connect() as conn:
            ti = conn.execute(
                text(
                    """
                    WITH c AS (SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
                               UNION ALL SELECT geometry FROM geo_car WHERE cod_imovel = :car LIMIT 1)
                    SELECT COUNT(*) FROM c JOIN geo_terras_indigenas t ON ST_Intersects(c.geometry, t.geometry)
                    """
                ),
                {"car": car_code},
            ).scalar() or 0
            uc = conn.execute(
                text(
                    """
                    WITH c AS (SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
                               UNION ALL SELECT geometry FROM geo_car WHERE cod_imovel = :car LIMIT 1)
                    SELECT COUNT(*) FROM c JOIN geo_unidades_conservacao u ON ST_Intersects(c.geometry, u.geometry)
                    """
                ),
                {"car": car_code},
            ).scalar() or 0
            emb = conn.execute(
                text(
                    """
                    WITH c AS (SELECT geometry FROM sicar_completo WHERE cod_imovel = :car
                               UNION ALL SELECT geometry FROM geo_car WHERE cod_imovel = :car LIMIT 1)
                    SELECT COUNT(*) FROM c JOIN geo_embargos_icmbio e ON ST_Intersects(c.geometry, e.geometry)
                    """
                ),
                {"car": car_code},
            ).scalar() or 0
            if ti > 0:
                discount += 1.0  # TI = ilíquido
                overlaps_detail.append({"layer": "terra_indigena", "count": ti, "pct": -100})
            elif uc > 0:
                discount += 0.5
                overlaps_detail.append({"layer": "unidade_conservacao", "count": uc, "pct": -50})
            elif emb > 0:
                discount += 0.4
                overlaps_detail.append({"layer": "embargo_icmbio", "count": emb, "pct": -40})
    except Exception as e:
        logger.warning("valuation overlaps failed: %s", e)

    discount_factor = min(discount, 1.0)
    valor_ajustado = valor_base * (1 - discount_factor)

    return {
        "car_code": car_code,
        "area_ha": area_ha,
        "uf": uf,
        "metodologia": "NBR 14.653-3 nível expedito (inferência regional)",
        "preco_medio_ha_uf": preco_ha_base,
        "valor_base_rs": round(valor_base, 2),
        "descontos": overlaps_detail,
        "fator_desconto_total": discount_factor,
        "valor_estimado_rs": round(valor_ajustado, 2),
        "fonte_precos": "Heurística 2025 — Informa/IMEA/Scot",
        "disclaimer": "Estimativa indicativa. Laudo NBR 14.653-3 requer avaliador credenciado.",
    }
