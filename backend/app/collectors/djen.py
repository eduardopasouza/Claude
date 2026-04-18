"""
Coletor de publicações e intimações judiciais via DJEN / Comunica.PJe (CNJ).

O DJEN (Diário de Justiça Eletrônico Nacional) é a plataforma unificada
do CNJ para publicação de intimações não-pessoais. Substitui
progressivamente os DJs estaduais e integra publicações de PJe, e-Proc,
e-SAJ e tribunais migrados.

API pública: https://comunicaapi.pje.jus.br/api/v1/comunicacao
Swagger:     https://comunicaapi.pje.jus.br/
Base legal:  Lei 14.195/2021 + Resoluções CNJ 455/2022, 569/2024.

Acesso: público, SEM autenticação, SEM convênio.
Rate limit: não documentado; usar parcimônia (delay entre requests).
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Optional

import httpx

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


DJEN_BASE_URL = "https://comunicaapi.pje.jus.br/api/v1"


class DJENCollector(BaseCollector):
    """Coleta publicações do DJEN/Comunica.PJe por OAB, CPF/CNPJ ou processo."""

    def __init__(self) -> None:
        super().__init__("djen")
        # DJEN costuma responder rápido — 60s é folgado
        self.timeout = 60.0

    # ------------------------------------------------------------------
    # Busca por OAB (caso de uso mais comum — advogado monitora suas intimações)
    # ------------------------------------------------------------------
    async def buscar_por_oab(
        self,
        numero_oab: str,
        uf_oab: str,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        itens_por_pagina: int = 50,
        pagina: int = 1,
    ) -> dict:
        """
        Busca publicações no DJEN por número de OAB + UF.

        Retorna dict com {status, count, items, pagina, itens_por_pagina}.
        """
        # Default: últimos 30 dias
        if data_fim is None:
            data_fim = date.today()
        if data_inicio is None:
            data_inicio = data_fim - timedelta(days=30)

        numero_oab = str(numero_oab).strip().lstrip("0")
        uf_oab = uf_oab.strip().upper()

        cache_key = (
            f"oab:{numero_oab}:{uf_oab}:"
            f"{data_inicio.isoformat()}:{data_fim.isoformat()}:"
            f"p{pagina}:i{itens_por_pagina}"
        )
        cached = self._get_cached(cache_key)
        if cached:
            logger.info("djen.cache_hit oab=%s/%s", numero_oab, uf_oab)
            return cached

        params = {
            "numeroOab": numero_oab,
            "ufOab": uf_oab,
            "dataDisponibilizacaoInicio": data_inicio.isoformat(),
            "dataDisponibilizacaoFim": data_fim.isoformat(),
            "itensPorPagina": itens_por_pagina,
            "pagina": pagina,
        }

        data = await self._fetch(params)
        if data:
            # cache TTL padrão (24h) é agressivo para publicações que podem
            # chegar ao longo do dia; reduzimos para 1h.
            self._set_cached_short(cache_key, data, ttl_seconds=3600)
        return data

    # ------------------------------------------------------------------
    # Busca por CPF/CNPJ (monitorar cliente)
    # ------------------------------------------------------------------
    async def buscar_por_documento(
        self,
        cpf_cnpj: str,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        itens_por_pagina: int = 50,
        pagina: int = 1,
    ) -> dict:
        """
        Busca publicações que mencionem um CPF/CNPJ.

        DJEN não indexa partes por CPF/CNPJ diretamente — a busca é feita
        no nome da parte. Aqui passamos o texto completo para match
        aproximado. Para busca precisa, é melhor passar o nome.
        """
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

        if data_fim is None:
            data_fim = date.today()
        if data_inicio is None:
            data_inicio = data_fim - timedelta(days=30)

        cache_key = (
            f"doc:{clean}:{data_inicio.isoformat()}:{data_fim.isoformat()}:"
            f"p{pagina}:i{itens_por_pagina}"
        )
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        params = {
            "texto": clean,
            "dataDisponibilizacaoInicio": data_inicio.isoformat(),
            "dataDisponibilizacaoFim": data_fim.isoformat(),
            "itensPorPagina": itens_por_pagina,
            "pagina": pagina,
        }

        data = await self._fetch(params)
        if data:
            self._set_cached_short(cache_key, data, ttl_seconds=3600)
        return data

    # ------------------------------------------------------------------
    # Busca por número de processo
    # ------------------------------------------------------------------
    async def buscar_por_processo(
        self,
        numero_processo: str,
        itens_por_pagina: int = 100,
        pagina: int = 1,
    ) -> dict:
        """Busca todas as publicações de um processo CNJ específico."""
        # Remove mascara se houver
        clean = numero_processo.replace("-", "").replace(".", "")

        cache_key = f"proc:{clean}:p{pagina}:i{itens_por_pagina}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        params = {
            "numeroProcesso": clean,
            "itensPorPagina": itens_por_pagina,
            "pagina": pagina,
        }

        data = await self._fetch(params)
        if data:
            # processo: cache maior (12h) — publicações antigas não mudam
            self._set_cached_short(cache_key, data, ttl_seconds=43200)
        return data

    # ------------------------------------------------------------------
    # Busca textual livre
    # ------------------------------------------------------------------
    async def buscar_por_texto(
        self,
        texto: str,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        itens_por_pagina: int = 50,
        pagina: int = 1,
    ) -> dict:
        """Busca por texto livre no conteúdo das publicações."""
        if data_fim is None:
            data_fim = date.today()
        if data_inicio is None:
            data_inicio = data_fim - timedelta(days=30)

        cache_key = (
            f"texto:{texto}:{data_inicio.isoformat()}:{data_fim.isoformat()}:"
            f"p{pagina}:i{itens_por_pagina}"
        )
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        params = {
            "texto": texto,
            "dataDisponibilizacaoInicio": data_inicio.isoformat(),
            "dataDisponibilizacaoFim": data_fim.isoformat(),
            "itensPorPagina": itens_por_pagina,
            "pagina": pagina,
        }

        data = await self._fetch(params)
        if data:
            self._set_cached_short(cache_key, data, ttl_seconds=3600)
        return data

    # ------------------------------------------------------------------
    # HTTP base
    # ------------------------------------------------------------------
    async def _fetch(self, params: dict) -> dict:
        """Chamada HTTP básica ao DJEN com tratamento de erro graceful."""
        url = f"{DJEN_BASE_URL}/comunicacao"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, params=params)

            if resp.status_code != 200:
                logger.warning(
                    "djen.http_error status=%d params=%s",
                    resp.status_code,
                    params,
                )
                return {
                    "status": "error",
                    "http_status": resp.status_code,
                    "count": 0,
                    "items": [],
                }

            data = resp.json()
            # Normaliza shape: garante campos count e items mesmo em vazio
            if "items" not in data:
                data["items"] = []
            if "count" not in data:
                data["count"] = len(data.get("items", []))
            return data

        except httpx.TimeoutException:
            logger.warning("djen.timeout params=%s", params)
            return {"status": "timeout", "count": 0, "items": []}
        except Exception as e:
            logger.warning("djen.error %s: %s", type(e).__name__, e)
            return {"status": "error", "message": str(e), "count": 0, "items": []}

    # ------------------------------------------------------------------
    # Cache com TTL customizável (BaseCollector usa TTL fixo global)
    # ------------------------------------------------------------------
    def _set_cached_short(self, query: str, data: dict, ttl_seconds: int) -> None:
        """Salva cache com TTL curto (override do TTL global de 24h)."""
        import json
        from datetime import datetime, timezone, timedelta
        key = self._cache_key(query)
        cache_file = self.cache_dir / f"{key}.json"
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
        cached = {
            "data": data,
            "expires_at": expires_at.isoformat(),
            "source": self.source_name,
            "query": query,
        }
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cached, f, ensure_ascii=False, default=str)


# ----------------------------------------------------------------------
# Helpers de normalização / classificação
# ----------------------------------------------------------------------

def classificar_urgencia(data_disponibilizacao: str) -> str:
    """
    Classifica urgência de uma publicação com base na data.

    Prazos processuais CPC/CPP contam, via de regra, em dias úteis a
    partir da data de disponibilização no DJEN (+1 dia publicação).
    Aqui simplificamos:
      critico: ≤ 5 dias corridos desde a publicação
      alto:    ≤ 10 dias
      medio:   ≤ 15 dias
      baixo:   > 15 dias
    """
    try:
        # Aceita formato ISO (YYYY-MM-DD) ou BR (DD/MM/YYYY)
        if "/" in data_disponibilizacao:
            d = datetime.strptime(data_disponibilizacao, "%d/%m/%Y").date()
        else:
            d = date.fromisoformat(data_disponibilizacao[:10])
    except Exception:
        return "desconhecida"

    dias = (date.today() - d).days
    if dias <= 5:
        return "critico"
    if dias <= 10:
        return "alto"
    if dias <= 15:
        return "medio"
    return "baixo"


def extrair_resumo(texto: str, max_chars: int = 300) -> str:
    """Extrai resumo curto do texto da publicação (para cards de feed)."""
    if not texto:
        return ""
    # Remove múltiplos espaços e quebras
    limpo = " ".join(texto.split())
    if len(limpo) <= max_chars:
        return limpo
    return limpo[:max_chars].rsplit(" ", 1)[0] + "..."
