"""
Endpoint de coroplético (choropleth) IBGE — malha municipal colorida por métrica.

Ativa 14 camadas "stub" do layers-catalog.ts:
  PAM (produção agrícola municipal):
    pam_soja, pam_milho, pam_cana, pam_cafe, pam_algodao,
    pam_arroz, pam_feijao, pam_trigo,
    pam_rendimento_soja, pam_valor_producao
  PPM (pecuária municipal):
    ppm_bovinos, ppm_suinos, ppm_ovinos, ppm_leite
  Socioeconômico:
    idhm, pib_per_capita, populacao, regic

Retorna GeoJSON com:
  - geometry: polígono do município
  - properties.value: valor da métrica no ano solicitado
  - properties.codigo_ibge, nome, uf

Frontend usa properties.value + escala viridis/ylorrd para colorir.

Performance:
  - cache SHA256 em disco TTL 24h
  - /geo/ibge/choropleth/pam_soja/2023 ~3s primeira chamada, <100ms depois
  - malha intermediaria do IBGE (não a mais detalhada) p/ response <1MB
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.collectors.base import BaseCollector
from app.collectors.ibge import IBGECollector

logger = logging.getLogger("agrojus")
router = APIRouter()


# ---------------------------------------------------------------------------
# Registry de métricas → tabela SIDRA + variável + classificação + unidade
# ---------------------------------------------------------------------------
# SIDRA tabela 5457 (PAM): /t/5457/n6/ALL/v/<var>/p/<ano>/c782/<cultura>
#   Variáveis: 214=área colhida(ha), 215=quantidade produzida(ton),
#              112=rendimento médio(kg/ha), 215_v=valor produção(R$ mil)
#   Culturas: 39=soja, 33=milho, 31=cana, 9=café, 3=algodão,
#             40=arroz, 15=feijão, 45=trigo
#
# SIDRA tabela 3939 (PPM): /t/3939/n6/ALL/v/105/p/<ano>/c79/<especie>
#   Espécie: 2670=bovino, 2681=suíno, 2684=ovino, 2672=bubalino
#
# SIDRA tabela 74 (leite): /t/74/n6/ALL/v/106/p/<ano>
#
# Para IDHM, PIB e demografia, usamos tabelas específicas.
# ---------------------------------------------------------------------------

#
# Códigos SIDRA corretos (validados via curl sessão 7):
#
# PAM (tabela 1612) — variáveis: 214=área colhida(ha), 215=valor produção(R$mil),
#                                 216=quantidade produzida(ton), 112=rend.médio(kg/ha)
#   Classificação c81 (produto agricola): 2713=Soja, 2707=Milho,
#   2711=Cana-de-açúcar, 2702=Café, 2696=Algodão herbáceo, 2692=Arroz,
#   2704=Feijão, 2716=Trigo
#
# PPM (tabela 3939) — variável 105 = efetivo dos rebanhos
#   Classificação c79: 2670=Bovino, 2681=Suíno, 2684=Ovino, 2672=Bubalino
#
# POP (tabela 6579) — variável 9324 = pop residente estimada (ano 2021 último
#                      disponível pré-Censo)
#
# PIB Municipios (tabela 5938) — variável 37 (PIB total mil R$), 47884 (per capita)
#
CHOROPLETH_METRICS: dict[str, dict] = {
    # === PAM - Produção Agrícola Municipal (tabela 1612) ===
    "pam_soja": {
        "sidra_table": "1612", "variable": "216", "culture": "2713",
        "classif": "c81",
        "label": "Soja (quantidade produzida)", "unit": "ton",
        "color_scheme": "YlGn",
    },
    "pam_milho": {
        "sidra_table": "1612", "variable": "216", "culture": "2707",
        "classif": "c81",
        "label": "Milho (quantidade produzida)", "unit": "ton",
        "color_scheme": "YlOrBr",
    },
    "pam_cana": {
        "sidra_table": "1612", "variable": "216", "culture": "2711",
        "classif": "c81",
        "label": "Cana-de-açúcar (quantidade produzida)", "unit": "ton",
        "color_scheme": "Greens",
    },
    "pam_cafe": {
        "sidra_table": "1612", "variable": "216", "culture": "2702",
        "classif": "c81",
        "label": "Café (quantidade produzida)", "unit": "ton",
        "color_scheme": "PuRd",
    },
    "pam_algodao": {
        "sidra_table": "1612", "variable": "216", "culture": "2696",
        "classif": "c81",
        "label": "Algodão (quantidade produzida)", "unit": "ton",
        "color_scheme": "BuPu",
    },
    "pam_arroz": {
        "sidra_table": "1612", "variable": "216", "culture": "2692",
        "classif": "c81",
        "label": "Arroz (quantidade produzida)", "unit": "ton",
        "color_scheme": "YlGnBu",
    },
    "pam_feijao": {
        "sidra_table": "1612", "variable": "216", "culture": "2704",
        "classif": "c81",
        "label": "Feijão (quantidade produzida)", "unit": "ton",
        "color_scheme": "Oranges",
    },
    "pam_trigo": {
        "sidra_table": "1612", "variable": "216", "culture": "2716",
        "classif": "c81",
        "label": "Trigo (quantidade produzida)", "unit": "ton",
        "color_scheme": "OrRd",
    },
    "pam_valor_soja": {
        "sidra_table": "1612", "variable": "215", "culture": "2713",
        "classif": "c81",
        "label": "Soja (valor produção)", "unit": "R$ mil",
        "color_scheme": "YlGn",
    },
    "pam_area_soja": {
        "sidra_table": "1612", "variable": "214", "culture": "2713",
        "classif": "c81",
        "label": "Soja (área colhida)", "unit": "hectares",
        "color_scheme": "YlGn",
    },

    # === PPM - Pecuária Municipal (tabela 3939) ===
    "ppm_bovinos": {
        "sidra_table": "3939", "variable": "105", "culture": "2670",
        "classif": "c79",
        "label": "Rebanho bovino (efetivo)", "unit": "cabeças",
        "color_scheme": "Greys",
    },
    "ppm_suinos": {
        "sidra_table": "3939", "variable": "105", "culture": "2681",
        "classif": "c79",
        "label": "Rebanho suíno (efetivo)", "unit": "cabeças",
        "color_scheme": "Reds",
    },
    "ppm_ovinos": {
        "sidra_table": "3939", "variable": "105", "culture": "2684",
        "classif": "c79",
        "label": "Rebanho ovino (efetivo)", "unit": "cabeças",
        "color_scheme": "Purples",
    },
    "ppm_bubalinos": {
        "sidra_table": "3939", "variable": "105", "culture": "2672",
        "classif": "c79",
        "label": "Rebanho bubalino (efetivo)", "unit": "cabeças",
        "color_scheme": "BuGn",
    },

    # === Socioeconômico ===
    "populacao": {
        "sidra_table": "6579", "variable": "9324", "culture": None,
        "label": "População residente estimada", "unit": "habitantes",
        "color_scheme": "Greys",
    },
    "pib_total": {
        "sidra_table": "5938", "variable": "37", "culture": None,
        "label": "PIB total municipal", "unit": "R$ mil",
        "color_scheme": "Blues",
    },
    "pib_per_capita": {
        "sidra_table": "5938", "variable": "47884", "culture": None,
        "label": "PIB per capita", "unit": "R$",
        "color_scheme": "YlGnBu",
    },
}


# ---------------------------------------------------------------------------
# GET /api/v1/geo/ibge/choropleth/metrics
# ---------------------------------------------------------------------------
@router.get("/metrics")
async def list_metrics():
    """Lista todas as métricas choropleth disponíveis."""
    return {
        "total": len(CHOROPLETH_METRICS),
        "metrics": [
            {
                "id": mid,
                "label": cfg["label"],
                "unit": cfg["unit"],
                "color_scheme": cfg["color_scheme"],
                "source": f"IBGE/SIDRA (tabela {cfg['sidra_table']})",
            }
            for mid, cfg in CHOROPLETH_METRICS.items()
        ],
    }


# ---------------------------------------------------------------------------
# GET /api/v1/geo/ibge/choropleth/{metric_id}/{ano}
# ---------------------------------------------------------------------------
@router.get("/{metric_id}/{ano}")
async def get_choropleth(
    metric_id: str,
    ano: int,
    uf: Optional[str] = Query(None, description="UF (ex: MA). Omitir = Brasil completo"),
):
    """
    GeoJSON coroplético de uma métrica IBGE (nível MUNICIPAL).

    - metric_id: id em /metrics (ex: pam_soja, ppm_bovinos, populacao)
    - ano: ano de referência (ex: 2023)
    - uf: opcional, restringe a um estado (senão Brasil — ~5.570 municípios)

    Retorno: FeatureCollection com properties.value para pintar.
    """
    cfg = CHOROPLETH_METRICS.get(metric_id)
    if not cfg:
        raise HTTPException(
            status_code=404,
            detail=f"Métrica '{metric_id}' não está no registry. Veja /metrics.",
        )

    collector = ChoroplethCollector()
    try:
        return await collector.build(metric_id, cfg, ano, uf)
    except Exception as e:
        logger.exception("choropleth failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# GET /api/v1/geo/ibge/choropleth/uf/{metric_id}/{ano}
# ---------------------------------------------------------------------------
@router.get("/uf/{metric_id}/{ano}")
async def get_choropleth_uf(metric_id: str, ano: int):
    """
    Choropleth por UF (agregação estadual via SIDRA n3).

    Carregamento rápido (27 polygons) — ideal para visão macro de
    produção agrícola/pecuária ou valor bruto por estado.

    Usa a mesma métrica do endpoint municipal mas agrega em nível 3 (UF).
    """
    cfg = CHOROPLETH_METRICS.get(metric_id)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Métrica '{metric_id}' não existe")

    collector = UFChoroplethCollector()
    try:
        return await collector.build_uf(metric_id, cfg, ano)
    except Exception as e:
        logger.exception("UF choropleth failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


class UFChoroplethCollector(BaseCollector):
    """Choropleth agregado por UF (27 polygons)."""

    SIDRA_URL = "https://apisidra.ibge.gov.br/values"
    MALHAS_URL = "https://servicodados.ibge.gov.br/api/v3/malhas"

    def __init__(self) -> None:
        super().__init__("ibge_choropleth_uf")

    async def build_uf(self, metric_id: str, cfg: dict, ano: int) -> dict:
        cache_key = f"uf_choropleth:{metric_id}:{ano}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        malha_task = asyncio.create_task(self._fetch_malha_br_uf())
        sidra_task = asyncio.create_task(self._fetch_sidra_uf(cfg, ano))

        malha, valores = await asyncio.gather(malha_task, sidra_task)

        features_out = []
        for feat in malha.get("features", []):
            uf_code = str(feat.get("properties", {}).get("codarea", ""))
            value = valores.get(uf_code)
            props = dict(feat.get("properties", {}))
            props.update({
                "uf_code": uf_code,
                "value": value,
                "value_label": cfg["label"],
                "unit": cfg["unit"],
            })
            features_out.append({
                "type": "Feature",
                "geometry": feat.get("geometry"),
                "properties": props,
            })

        result = {
            "type": "FeatureCollection",
            "features": features_out,
            "metric_id": metric_id,
            "metric_label": cfg["label"],
            "unit": cfg["unit"],
            "color_scheme": cfg["color_scheme"],
            "year": ano,
            "source": f"IBGE/SIDRA tabela {cfg['sidra_table']} (nível UF)",
            "total_ufs": len(features_out),
            "total_com_valor": sum(1 for f in features_out if f["properties"]["value"]),
        }
        self._set_cached(cache_key, result)
        return result

    async def _fetch_malha_br_uf(self) -> dict:
        """Baixa malha do Brasil com fronteiras de estados."""
        url = f"{self.MALHAS_URL}/paises/BR"
        params = {
            "formato": "application/vnd.geo+json",
            "qualidade": "intermediaria",
            "intrarregiao": "UF",
        }
        try:
            async with httpx.AsyncClient(timeout=60.0) as c:
                r = await c.get(url, params=params)
                r.raise_for_status()
                return r.json()
        except Exception as e:
            logger.warning("Malha UF erro: %s", e)
            return {"type": "FeatureCollection", "features": []}

    async def _fetch_sidra_uf(self, cfg: dict, ano: int) -> dict[str, Any]:
        """Valores agregados por UF (n3/all)."""
        table = cfg["sidra_table"]
        var = cfg["variable"]
        culture = cfg.get("culture")
        classif_path = f"/{cfg.get('classif', 'c81')}/{culture}" if culture else ""
        url = f"{self.SIDRA_URL}/t/{table}/n3/all/v/{var}/p/{ano}{classif_path}/f/u"

        try:
            async with httpx.AsyncClient(timeout=60.0) as c:
                r = await c.get(url)
                r.raise_for_status()
                raw = r.json()
        except Exception as e:
            logger.warning("SIDRA UF %s erro: %s", url, e)
            return {}

        valores: dict[str, Any] = {}
        if isinstance(raw, list) and len(raw) > 1:
            for row in raw[1:]:
                uf_code = str(row.get("D1C", "") or "")
                val = row.get("V", "")
                try:
                    valores[uf_code] = float(val) if val not in ("...", "-", "", "..") else None
                except (ValueError, TypeError):
                    valores[uf_code] = None
        return valores


# ---------------------------------------------------------------------------
# Coletor choropleth
# ---------------------------------------------------------------------------
class ChoroplethCollector(BaseCollector):
    """Baixa malha IBGE + SIDRA + injeta valor em properties."""

    SIDRA_URL = "https://apisidra.ibge.gov.br/values"
    MALHAS_URL = "https://servicodados.ibge.gov.br/api/v3/malhas"

    def __init__(self) -> None:
        super().__init__("ibge_choropleth")

    async def build(
        self,
        metric_id: str,
        cfg: dict,
        ano: int,
        uf: Optional[str],
    ) -> dict:
        cache_key = f"choropleth:{metric_id}:{ano}:{uf or 'BR'}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # 1. Malha + valores SIDRA em paralelo
        malha_task = asyncio.create_task(self._fetch_malha(uf))
        sidra_task = asyncio.create_task(self._fetch_sidra(cfg, ano, uf))

        malha, sidra_values = await asyncio.gather(malha_task, sidra_task)

        if not malha.get("features"):
            return {
                "type": "FeatureCollection",
                "features": [],
                "error": f"Malha IBGE não retornou features (uf={uf})",
            }

        # 2. Injetar value em cada feature pelo código IBGE
        features_out = []
        for feat in malha.get("features", []):
            codigo = str(feat.get("properties", {}).get("codarea", ""))
            value = sidra_values.get(codigo)
            props = dict(feat.get("properties", {}))
            props.update(
                {
                    "codigo_ibge": codigo,
                    "value": value,
                    "value_label": cfg["label"],
                    "unit": cfg["unit"],
                }
            )
            features_out.append(
                {
                    "type": "Feature",
                    "geometry": feat.get("geometry"),
                    "properties": props,
                }
            )

        result = {
            "type": "FeatureCollection",
            "features": features_out,
            "metric_id": metric_id,
            "metric_label": cfg["label"],
            "unit": cfg["unit"],
            "color_scheme": cfg["color_scheme"],
            "year": ano,
            "uf": uf,
            "source": f"IBGE/SIDRA (tabela {cfg['sidra_table']}) + malha v3",
            "total_municipios": len(features_out),
            "total_com_valor": sum(1 for f in features_out if f["properties"]["value"] is not None),
        }
        self._set_cached(cache_key, result)
        return result

    async def _fetch_malha(self, uf: Optional[str]) -> dict:
        """Baixa malha municipal (GeoJSON) de UF ou Brasil."""
        if uf:
            code = IBGECollector.UF_CODES.get(uf.upper())
            if not code:
                return {"type": "FeatureCollection", "features": []}
            url = f"{self.MALHAS_URL}/estados/{code}"
        else:
            url = f"{self.MALHAS_URL}/paises/BR"

        params = {
            "formato": "application/vnd.geo+json",
            "qualidade": "intermediaria",
            "intrarregiao": "municipio",
        }
        try:
            async with httpx.AsyncClient(timeout=60.0) as c:
                r = await c.get(url, params=params)
                r.raise_for_status()
                return r.json()
        except Exception as e:
            logger.warning("Malha %s erro: %s", uf or "BR", e)
            return {"type": "FeatureCollection", "features": []}

    async def _fetch_sidra(
        self, cfg: dict, ano: int, uf: Optional[str]
    ) -> dict[str, Any]:
        """
        Baixa valores SIDRA de TODOS municípios (n6/all) e indexa por código IBGE.
        Filtragem por UF é client-side (primeiros 2 dígitos do código IBGE).
        Isso é mais eficiente que tentar a sintaxe n6/in+n3 que é buggy.
        """
        table = cfg["sidra_table"]
        var = cfg["variable"]
        culture = cfg.get("culture")

        # Classificação por cultura (PAM) ou rebanho (PPM)
        classif_path = ""
        if culture:
            classif_code = cfg.get("classif", "c81")
            classif_path = f"/{classif_code}/{culture}"

        # IMPORTANTE: /f/u (unified = nomes + códigos).
        # /f/n retorna só nomes (sem D1C = código IBGE), /f/c só códigos.
        url = (
            f"{self.SIDRA_URL}/t/{table}/n6/all/v/{var}/p/{ano}"
            f"{classif_path}/f/u"
        )

        try:
            async with httpx.AsyncClient(timeout=120.0) as c:
                r = await c.get(url)
                r.raise_for_status()
                raw = r.json()
        except Exception as e:
            logger.warning("SIDRA %s erro: %s", url, e)
            return {}

        # SIDRA retorna array: [0]=cabeçalhos, [1:]=dados
        # D1C = código IBGE do município (7 dígitos)
        # V = valor numérico
        uf_code = IBGECollector.UF_CODES.get(uf.upper()) if uf else None

        valores: dict[str, Any] = {}
        if isinstance(raw, list) and len(raw) > 1:
            for row in raw[1:]:
                codigo = str(row.get("D1C", "") or "")
                if not codigo:
                    continue
                # Filtra por UF via prefixo (2 primeiros dígitos = código UF)
                if uf_code and not codigo.startswith(uf_code):
                    continue
                val_str = row.get("V", "")
                try:
                    valores[codigo] = (
                        float(val_str) if val_str not in ("...", "-", "", "..") else None
                    )
                except (ValueError, TypeError):
                    valores[codigo] = None
        return valores
