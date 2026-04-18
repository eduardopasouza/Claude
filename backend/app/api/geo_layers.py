"""
Endpoint genérico de camadas geoespaciais PostGIS.

Substitui os múltiplos `elif layer_id == "..."` em geo.py por um
registry declarativo. Cada camada declara:
  - tabela PostGIS
  - coluna de geometria
  - colunas de atributos a expor
  - coluna de id (para inspector)
  - limite default de features

Um endpoint único `/api/v1/geo/postgis/{layer_id}/geojson` responde todas.

Camadas disponíveis hoje (com dados reais):
  - 7 ambientais (PRODES, DETER Amazônia/Cerrado, UCs, Embargos/Autos ICMBio, MapBiomas Alertas)
  - 3 fundiárias (CAR, SICAR, SIGEF, Terras Indígenas)
  - 5 infraestrutura (rodovias, ferrovias, portos, armazéns, frigoríficos)
  - 1 crédito (MapBiomas Crédito Rural)
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.models.database import get_session

logger = logging.getLogger("agrojus")
router = APIRouter()


# ---------------------------------------------------------------------------
# Registry de camadas PostGIS
# ---------------------------------------------------------------------------
# Cada entrada: {table, geom_col, id_col, attrs: [colunas a expor], category,
#                color, default_max, theme}
#
# `attrs` são incluídos no `properties` do GeoJSON; são o que aparece no
# inspector on-click do frontend.
# ---------------------------------------------------------------------------

LAYER_REGISTRY: dict[str, dict] = {
    # === AMBIENTAL ===
    "prodes": {
        "table": "geo_prodes",
        "geom_col": "geometry",
        "id_col": "id",
        "attrs": ["class_name", "main_class", "year", "state", "area_km", "image_date", "satellite", "sensor"],
        "category": "ambiental",
        "color": "#7E22CE",
        "default_max": 500,
        "name": "PRODES (desmatamento anual)",
        "description": "Desmatamento consolidado anual — INPE. Corte MCR 2.9 = 2019.",
    },
    "deter_amazonia": {
        "table": "geo_deter_amazonia",
        "geom_col": "geometry",
        "id_col": "gid",
        "attrs": ["classname", "view_date", "sensor", "satellite", "areamunkm", "municipali", "uf"],
        "category": "ambiental",
        "color": "#F59E0B",
        "default_max": 1000,
        "name": "DETER Amazônia (alertas)",
        "description": "Alertas DETER tempo real — INPE bioma Amazônia",
    },
    "deter_cerrado": {
        "table": "geo_deter_cerrado",
        "geom_col": "geometry",
        "id_col": "gid",
        "attrs": ["classname", "view_date", "sensor", "satellite", "areatotalkm", "municipality", "uf"],
        "category": "ambiental",
        "color": "#F97316",
        "default_max": 1000,
        "name": "DETER Cerrado (alertas)",
        "description": "Alertas DETER tempo real — INPE bioma Cerrado",
    },
    "mapbiomas_alertas": {
        "table": "geo_mapbiomas_alertas",
        "geom_col": "geometry",
        "id_col": "index",
        "attrs": ["CODEALERTA", "DATADETEC", "BIOMA", "ESTADO", "MUNICIPIO", "AREAHA", "FONTE", "VPRESSAO"],
        "category": "ambiental",
        "color": "#DC2626",
        "default_max": 1000,
        "name": "MapBiomas Alertas (fogo/desmatamento)",
        "description": "515k+ alertas validados MapBiomas cruzados com CAR",
    },
    "terras_indigenas": {
        "table": "geo_terras_indigenas",
        "geom_col": "geometry",
        "id_col": "gid",
        "attrs": ["terrai_nom", "etnia_nome", "fase_ti", "modalidade", "superficie", "uf_sigla"],
        "category": "ambiental",
        "color": "#6366F1",
        "default_max": 1000,
        "name": "Terras Indígenas",
        "description": "655 TIs demarcadas — FUNAI",
    },
    "unidades_conservacao": {
        "table": "geo_unidades_conservacao",
        "geom_col": "geometry",
        "id_col": "id",
        "attrs": ["nomeuc", "siglacateg", "grupouc", "esferaadm", "criacaoano", "areahaalb", "biomas", "ufabrang"],
        "category": "ambiental",
        "color": "#0EA5E9",
        "default_max": 1000,
        "name": "Unidades de Conservação",
        "description": "346 UCs federais — ICMBio (parques, APAs, reservas)",
    },
    "embargos_icmbio": {
        "table": "geo_embargos_icmbio",
        "geom_col": "geometry",
        "id_col": "id",
        "attrs": ["numero_emb", "data", "nome_uc", "municipio", "uf", "area", "desc_infra", "julgamento", "autuado", "cpf_cnpj"],
        "category": "ambiental",
        "color": "#EF4444",
        "default_max": 1000,
        "name": "Embargos ICMBio",
        "description": "Embargos em UCs federais",
    },
    "autos_icmbio": {
        "table": "geo_autos_icmbio",
        "geom_col": "geometry",
        "id_col": "id",
        "attrs": ["numero_ai", "data", "autuado", "cpf_cnpj", "nome_uc", "municipio", "uf", "tipo_infra", "valor_mult", "julgamento"],
        "category": "ambiental",
        "color": "#F43F5E",
        "default_max": 1000,
        "name": "Autos de Infração ICMBio",
        "description": "Autos de infração ambiental em UCs",
    },
    "autos_ibama": {
        "table": "geo_autos_ibama",
        "geom_col": "geometry",
        "id_col": "id",
        "attrs": ["num_auto", "data_auto", "nome", "cpf_cnpj", "descricao", "valor", "municipio", "uf"],
        "category": "ambiental",
        "color": "#DC2626",
        "default_max": 5000,
        "name": "Autos de Infração IBAMA (pontos)",
        "description": "Autos de infração com coordenadas — dados abertos IBAMA SIFISC",
    },

    # === FUNDIÁRIO ===
    "sicar_completo": {
        "table": "sicar_completo",
        "geom_col": "geometry",
        "id_col": "cod_imovel",
        "attrs": ["cod_imovel", "tipo_imovel", "m_fiscal", "area", "status_imovel", "cod_municipio_ibge", "uf", "condicao"],
        "category": "fundiario",
        "color": "#10B981",
        "default_max": 500,
        "name": "CAR (SICAR)",
        "description": "Imóveis rurais cadastrados no CAR — base BigQuery",
    },
    "geo_car": {
        "table": "geo_car",
        "geom_col": "geometry",
        "id_col": "id",
        "attrs": ["cod_imovel", "municipio", "uf", "area", "status_imovel", "tipo_imovel", "m_fiscal", "condicao"],
        "category": "fundiario",
        "color": "#059669",
        "default_max": 500,
        "name": "CAR (WFS nacional)",
        "description": "Imóveis CAR via WFS nacional — 135k registros",
    },
    "sigef_parcelas": {
        "table": "sigef_parcelas",
        "geom_col": "geometry",
        "id_col": "parcela_co",
        "attrs": ["parcela_co", "nome_area", "situacao_i", "status", "data_aprov", "rt", "art", "codigo_imo", "uf_id"],
        "category": "fundiario",
        "color": "#EC4899",
        "default_max": 500,
        "name": "SIGEF (parcelas certificadas)",
        "description": "1.7M+ parcelas certificadas INCRA",
    },

    # === INFRAESTRUTURA ===
    "rodovias_federais": {
        "table": "geo_rodovias_federais",
        "geom_col": "geometry",
        "id_col": "index",
        "attrs": ["tipovia", "jurisdicao", "revestimen", "operaciona"],
        "category": "infraestrutura",
        "color": "#FBBF24",
        "default_max": 3000,
        "name": "Rodovias Federais",
        "description": "Malha rodoviária federal — DNIT",
    },
    "ferrovias": {
        "table": "geo_ferrovias",
        "geom_col": "geometry",
        "id_col": "ID",
        "attrs": ["SIGLA", "BITOLA", "CATEGORIA", "NAME", "TIP_SITUAC"],
        "category": "infraestrutura",
        "color": "#A78BFA",
        "default_max": 2000,
        "name": "Ferrovias",
        "description": "Malha ferroviária — ANTT/DNIT",
    },
    "portos": {
        "table": "geo_portos",
        "geom_col": "geometry",
        "id_col": "idseq",
        "attrs": ["nome", "tipo", "cidade", "estado", "modalidade", "situacao"],
        "category": "infraestrutura",
        "color": "#38BDF8",
        "default_max": 100,
        "name": "Portos",
        "description": "Portos marítimos e fluviais — ANTAQ",
    },
    "armazens_silos": {
        "table": "geo_armazens_silos",
        "geom_col": "geometry",
        "id_col": "gid",
        "attrs": ["index"],
        "category": "infraestrutura",
        "color": "#F59E0B",
        "default_max": 3000,
        "name": "Armazéns e Silos",
        "description": "CONAB SICARM — ~16k unidades armazenadoras",
    },
    "frigorificos": {
        "table": "geo_frigorificos",
        "geom_col": "geometry",
        "id_col": "gid",
        "attrs": ["index"],
        "category": "infraestrutura",
        "color": "#F87171",
        "default_max": 500,
        "name": "Frigoríficos",
        "description": "Frigoríficos SIF — MAPA",
    },

    # === CRÉDITO ===
    "mapbiomas_credito_rural": {
        "table": "mapbiomas_credito_rural",
        "geom_col": "geom",
        "id_col": "id",
        "attrs": ["order_number", "year", "car_code", "vl_parc_credito", "vl_area_financ", "dt_emissao", "cnpj_if"],
        "category": "credito",
        "color": "#3B82F6",
        "default_max": 500,
        "name": "Crédito Rural (MapBiomas)",
        "description": "5.6M+ parcelas financiadas cruzadas com cobertura — SICOR+MapBiomas",
    },
}


# ---------------------------------------------------------------------------
# GET /api/v1/geo/postgis/catalog
# ---------------------------------------------------------------------------
@router.get("/catalog")
async def get_catalog():
    """Devolve o registry completo (frontend consome para montar painel de camadas)."""
    return {
        "total": len(LAYER_REGISTRY),
        "layers": [
            {
                "id": lid,
                "name": cfg["name"],
                "category": cfg["category"],
                "color": cfg["color"],
                "description": cfg.get("description", ""),
                "default_max": cfg.get("default_max", 500),
            }
            for lid, cfg in LAYER_REGISTRY.items()
        ],
    }


# ---------------------------------------------------------------------------
# GET /api/v1/geo/postgis/{layer_id}/geojson
# ---------------------------------------------------------------------------
@router.get("/{layer_id}/geojson")
async def get_layer_geojson(
    layer_id: str,
    bbox: Optional[str] = None,
    max_features: int = 500,
):
    """
    Retorna GeoJSON (FeatureCollection) de uma camada PostGIS.

    - bbox: "west,south,east,north" (EPSG:4326)
    - max_features: limite de features (default 500, max 5000)
    """
    cfg = LAYER_REGISTRY.get(layer_id)
    if not cfg:
        raise HTTPException(
            status_code=404,
            detail=f"Camada '{layer_id}' não encontrada no registry PostGIS",
        )

    max_features = min(max(1, max_features), cfg.get("default_max", 500) * 2, 5000)

    table = cfg["table"]
    geom_col = cfg["geom_col"]
    id_col = cfg["id_col"]
    attrs = cfg["attrs"]

    # Constrói lista de colunas para projeção JSON dos atributos
    # Usa nome original (sem aspas) como chave, e identificador citado como valor
    attr_exprs = ", ".join([f"'{a}', t.{_safe_col(a)}" for a in attrs])
    attr_exprs_with_id = f"'_id', t.{_safe_col(id_col)}::text, '_layer', '{layer_id}'"
    if attr_exprs:
        attr_exprs_with_id += ", " + attr_exprs

    geom_quoted = _safe_col(geom_col)

    # Filtro bbox opcional
    bbox_where = ""
    params: dict = {"limit": max_features}
    if bbox:
        try:
            west, south, east, north = [float(x) for x in bbox.split(",")]
            bbox_where = (
                f"WHERE ST_Intersects({geom_quoted}, "
                f"ST_MakeEnvelope(:west, :south, :east, :north, 4326))"
            )
            params.update({"west": west, "south": south, "east": east, "north": north})
        except Exception:
            pass

    # Query: monta FeatureCollection manualmente via json_build_object
    query = f"""
    SELECT json_build_object(
      'type', 'FeatureCollection',
      'features', COALESCE(json_agg(
        json_build_object(
          'type', 'Feature',
          'geometry', ST_AsGeoJSON(t.{geom_quoted})::json,
          'properties', json_build_object({attr_exprs_with_id})
        )
      ), '[]'::json)
    )
    FROM (
      SELECT * FROM {_safe_table(table)}
      {bbox_where}
      LIMIT :limit
    ) t;
    """

    db = get_session()
    try:
        result = db.execute(text(query), params).scalar()
        if result is None:
            return {"type": "FeatureCollection", "features": []}
        result["source"] = cfg.get("name", layer_id)
        result["layer_id"] = layer_id
        result["total"] = len(result.get("features", []))
        result["color"] = cfg["color"]
        return result
    except Exception as e:
        logger.error("geo_layers %s error: %s", layer_id, e)
        raise HTTPException(status_code=500, detail=f"Erro PostGIS: {e}")
    finally:
        db.close()


# ---------------------------------------------------------------------------
# GET /api/v1/geo/postgis/{layer_id}/feature/{feature_id}
# ---------------------------------------------------------------------------
@router.get("/{layer_id}/feature/{feature_id}")
async def get_feature_detail(layer_id: str, feature_id: str):
    """
    Retorna TODOS os atributos de uma feature específica (para inspector drawer
    exibir quando usuário clica numa feição no mapa).
    """
    cfg = LAYER_REGISTRY.get(layer_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Layer não encontrada")

    table = cfg["table"]
    id_col = cfg["id_col"]

    # SELECT * devolve todas as colunas (exceto geom, que é pesado)
    query = f"""
    SELECT row_to_json(t.*) as data
    FROM (
      SELECT *
      FROM {_safe_table(table)}
      WHERE {_safe_col(id_col)}::text = :fid
      LIMIT 1
    ) t;
    """  # noqa: S608 (identifiers passam por _safe_col)

    db = get_session()
    try:
        result = db.execute(text(query), {"fid": str(feature_id)}).scalar()
        if not result:
            raise HTTPException(status_code=404, detail="Feature não encontrada")

        # Remove campos de geometria (pesados) do retorno
        cleaned = {
            k: v
            for k, v in result.items()
            if k not in (cfg["geom_col"], "geom", "geometry", "geometria")
        }
        return {
            "layer_id": layer_id,
            "layer_name": cfg.get("name"),
            "feature_id": feature_id,
            "attributes": cleaned,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("feature detail error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Safety helpers (anti SQL injection em identificadores)
# Retorna identificador JÁ citado com aspas duplas (case-sensitive no Postgres)
# ---------------------------------------------------------------------------

_SAFE_IDENT = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


def _safe_col(name: str) -> str:
    """Valida e cita nome de coluna. Aspas duplas preservam case-sensitivity."""
    if not name or not all(c in _SAFE_IDENT for c in name):
        raise HTTPException(status_code=400, detail=f"Coluna inválida: {name}")
    return f'"{name}"'


def _safe_table(name: str) -> str:
    """Valida e cita nome de tabela."""
    return _safe_col(name)
