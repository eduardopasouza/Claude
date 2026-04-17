"""
Coletor Embrapa AgroAPI — OAuth 2.0 + wrappers das 9 APIs assinadas.

Credenciais (Consumer Key, Secret, Access Token) em .env do container.
Gateway: https://api.cnptia.embrapa.br
Portal: https://www.agroapi.cnptia.embrapa.br/portal/

APIs assinadas (plano gratuito — até 100k req/mês por API):
  - Agritec v2            → ZARC, cultivares, produtividade, municípios
  - AGROFIT v1            → agrotóxicos registrados no MAPA
  - AgroTermos v1         → glossário técnico agropecuário (termos + relações)
  - Bioinsumos v2         → inoculantes + biológicos + pragas/plantas daninhas
  - BovTrace v1           → rastreabilidade bovina (raças, protocolos, GTA)
  - PlantAnnot v2         → anotação de genes/proteínas de plantas
  - RespondeAgro v1       → base de conhecimento Embrapa (Q&A)
  - SmartSolosExpert v1   → classificação SiBCS + verificação de perfil de solo
  - Sting v1              → descritores de estruturas proteicas (PDB)

Os 9 base paths foram confirmados via curl + swagger spec (sessão 7):
  /agritec/v2, /agrofit/v1, /agrotermos/v1, /bioinsumos/v2,
  /bovtrace/v1, /plantannot/v2, /respondeagro/v1,
  /smartsolos/expert/v1  (← note: difere de /smartsolos/v1),
  /sting/v1

OAuth 2.0 (client_credentials grant):
  POST {gateway}/token
    Authorization: Basic base64(consumer_key:consumer_secret)
    Body: grant_type=client_credentials
  Retorna: { access_token, token_type=Bearer, expires_in=3600 }

Estratégia: cachear token em memória por 55 min; renova automaticamente.
"""

from __future__ import annotations

import base64
import logging
import time
from typing import Any, Optional

import httpx

from app.collectors.base import BaseCollector
from app.config import settings

logger = logging.getLogger("agrojus")


EMBRAPA_GATEWAY = "https://api.cnptia.embrapa.br"


class EmbrapaAuth:
    """Gerencia o token OAuth 2.0 da Embrapa AgroAPI (singleton)."""

    _instance: Optional["EmbrapaAuth"] = None
    _access_token: Optional[str] = None
    _expires_at: float = 0.0

    def __new__(cls) -> "EmbrapaAuth":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_token(self) -> Optional[str]:
        """Retorna um access token válido (renova automaticamente)."""
        now = time.time()
        if self._access_token and now < self._expires_at - 60:
            return self._access_token

        # Sempre regerar via client_credentials (mais confiável que access_token fixo)
        if not settings.embrapa_consumer_key or not settings.embrapa_consumer_secret:
            # Fallback para token manual .env
            if settings.embrapa_access_token:
                self._access_token = settings.embrapa_access_token
                self._expires_at = now + 55 * 60
                return self._access_token
            logger.warning("Embrapa: Consumer Key/Secret ausentes")
            return None

        basic = base64.b64encode(
            f"{settings.embrapa_consumer_key}:{settings.embrapa_consumer_secret}".encode()
        ).decode()

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{EMBRAPA_GATEWAY}/token",
                    headers={
                        "Authorization": f"Basic {basic}",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={"grant_type": "client_credentials"},
                )
            if resp.status_code != 200:
                logger.warning("Embrapa token falhou: HTTP %d %s", resp.status_code, resp.text[:200])
                return None
            data = resp.json()
            self._access_token = data.get("access_token")
            ttl = int(data.get("expires_in", 3600))
            self._expires_at = now + ttl
            logger.info("Embrapa token renovado, ttl=%ds", ttl)
            return self._access_token
        except Exception as e:
            logger.warning("Embrapa token erro %s: %s", type(e).__name__, e)
            return None


class EmbrapaCollector(BaseCollector):
    """Cliente base para as 9 APIs Embrapa — paths validados via Swagger."""

    def __init__(self) -> None:
        super().__init__("embrapa")
        self.auth = EmbrapaAuth()
        self.timeout = 30.0

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> Any:
        """Request genérico GET/POST/DELETE com auth + cache SHA256 em disco."""
        token = await self.auth.get_token()
        if not token:
            return {"error": "Embrapa auth falhou — verifique credenciais .env"}

        # Cache key (apenas GET — POST/DELETE não cacheia)
        if method == "GET":
            cache_key = f"GET:{path}:{sorted((params or {}).items())}"
            cached = self._get_cached(cache_key)
            if cached is not None:
                return cached

        url = f"{EMBRAPA_GATEWAY}{path}"
        headers = {"Authorization": f"Bearer {token}"}
        if body is not None:
            headers["Content-Type"] = "application/json"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.request(
                    method, url, params=params, json=body, headers=headers
                )
            if resp.status_code == 204:
                # No Content — retorna status positivo sem cachear
                return {"status": "ok", "http": 204}
            if resp.status_code == 200 or resp.status_code == 201:
                try:
                    data = resp.json()
                except Exception:
                    data = {"raw": resp.text}
                if method == "GET":
                    self._set_cached(cache_key, data)
                return data
            logger.info(
                "Embrapa %s %s: HTTP %d %s",
                method,
                path,
                resp.status_code,
                resp.text[:200],
            )
            return {
                "error": f"HTTP {resp.status_code}",
                "body": resp.text[:500],
                "path": path,
            }
        except Exception as e:
            logger.warning("Embrapa %s %s erro: %s", method, path, e)
            return {"error": str(e), "path": path}

    # ======================================================================
    # Agritec v2 — /agritec/v2
    # Zoneamento Agrícola de Risco Climático (ZARC), cultivares, municípios
    # ======================================================================

    async def agritec_culturas(self) -> Any:
        """Lista todas as 188 culturas indexadas no Agritec."""
        return await self._request("GET", "/agritec/v2/culturas")

    async def agritec_cultura(self, id_cultura: int) -> Any:
        """Detalhe de uma cultura por id."""
        return await self._request("GET", f"/agritec/v2/culturas/{id_cultura}")

    async def agritec_municipios(self, uf: Optional[str] = None) -> Any:
        """Lista municípios atendidos pelo Agritec (todos ou por UF)."""
        params = {"uf": uf} if uf else None
        return await self._request("GET", "/agritec/v2/municipios", params=params)

    async def agritec_municipio(self, codigo_ibge: int) -> Any:
        """Detalhe de um município no Agritec (lat, lon, região de zoneamento)."""
        return await self._request("GET", f"/agritec/v2/municipios/{codigo_ibge}")

    async def agritec_culturas_municipio(self, codigo_ibge: int) -> Any:
        """Culturas disponíveis (com ZARC) para um município."""
        return await self._request(
            "GET", f"/agritec/v2/municipios/{codigo_ibge}/culturas"
        )

    async def agritec_zoneamento(
        self,
        id_cultura: int,
        codigo_ibge: int,
        risco: str = "20",
    ) -> Any:
        """
        ZARC — janelas de plantio por município + cultura + risco (20/30/40/todos).
        Risco 20% = mais conservador; 40% = mais permissivo.
        """
        return await self._request(
            "GET",
            "/agritec/v2/zoneamento",
            params={
                "idCultura": id_cultura,
                "codigoIBGE": codigo_ibge,
                "risco": risco,
            },
        )

    async def agritec_cultivares(
        self,
        safra: str,
        id_cultura: int,
        uf: str,
        regiao: Optional[str] = None,
    ) -> Any:
        """Cultivares recomendadas por safra + cultura + UF."""
        params = {"safra": safra, "idCultura": id_cultura, "uf": uf}
        if regiao:
            params["regiao"] = regiao
        return await self._request("GET", "/agritec/v2/cultivares", params=params)

    async def agritec_obtentores(self, safra: str, id_cultura: Optional[int] = None) -> Any:
        """Obtentores/mantenedores de cultivares para uma safra."""
        params: dict = {"safra": safra}
        if id_cultura:
            params["idCultura"] = id_cultura
        return await self._request("GET", "/agritec/v2/obtentores", params=params)

    # ======================================================================
    # AGROFIT v1 — /agrofit/v1
    # Agrotóxicos/defensivos registrados no MAPA
    # ======================================================================

    async def agrofit_culturas(self) -> Any:
        """Lista de todas as culturas do AGROFIT."""
        return await self._request("GET", "/agrofit/v1/culturas")

    async def agrofit_titulares(self) -> Any:
        """Titulares de registro (empresas fabricantes)."""
        return await self._request("GET", "/agrofit/v1/titulares-registros")

    async def agrofit_tecnicas_aplicacoes(self) -> Any:
        """Técnicas de aplicação reconhecidas."""
        return await self._request("GET", "/agrofit/v1/tecnicas-aplicacoes")

    async def agrofit_busca_produtos_formulados(
        self,
        cultura: Optional[str] = None,
        praga: Optional[str] = None,
        titular: Optional[str] = None,
    ) -> Any:
        """Busca produtos formulados (agrotóxicos) por cultura/praga/titular."""
        params = {k: v for k, v in {"cultura": cultura, "praga": praga, "titular": titular}.items() if v}
        return await self._request(
            "GET", "/agrofit/v1/search/produtos-formulados", params=params
        )

    async def agrofit_produto_tecnico(self, numero_registro: str) -> Any:
        """Detalhe de produto técnico pelo número de registro."""
        return await self._request(
            "GET", f"/agrofit/v1/produtos-tecnicos/{numero_registro}"
        )

    async def agrofit_pragas_nomes_comuns(self) -> Any:
        """Lista pragas por nome comum (search pattern)."""
        return await self._request("GET", "/agrofit/v1/search/pragas-nomes-comuns")

    # ======================================================================
    # Bioinsumos v2 — /bioinsumos/v2
    # Inoculantes, biológicos, pragas, plantas daninhas
    # ======================================================================

    async def bioinsumos_busca_inoculantes(self, cultura: Optional[str] = None) -> Any:
        """Inoculantes registrados (bactérias fixadoras de N, micorrizas, etc)."""
        params = {"cultura": cultura} if cultura else None
        return await self._request(
            "GET", "/bioinsumos/v2/search/inoculantes", params=params
        )

    async def bioinsumos_busca_produtos_biologicos(
        self, cultura: Optional[str] = None, praga: Optional[str] = None
    ) -> Any:
        """Produtos biológicos registrados (controle de pragas)."""
        params = {k: v for k, v in {"cultura": cultura, "praga": praga}.items() if v}
        return await self._request(
            "GET", "/bioinsumos/v2/search/produtos-biologicos", params=params
        )

    async def bioinsumos_pragas(self) -> Any:
        """Lista todas as pragas com cultura hospedeira e link agrofit."""
        return await self._request("GET", "/bioinsumos/v2/pragas")

    async def bioinsumos_plantas_daninhas(self) -> Any:
        """Lista plantas daninhas catalogadas."""
        return await self._request("GET", "/bioinsumos/v2/plantas-daninhas")

    # ======================================================================
    # AgroTermos v1 — /agrotermos/v1
    # Glossário técnico agropecuário (vocabulário controlado Agrovoc)
    # ======================================================================

    async def agrotermos_termo(self, descricao: str) -> Any:
        """Busca exata por termo."""
        return await self._request(
            "GET", "/agrotermos/v1/termo", params={"descricao": descricao}
        )

    async def agrotermos_termo_parcial(self, descricao: str) -> Any:
        """Busca parcial (contém) — melhor para autocomplete."""
        return await self._request(
            "GET", "/agrotermos/v1/termoParcial", params={"descricao": descricao}
        )

    async def agrotermos_termo_com_relacoes(self, descricao: str) -> Any:
        """Termo + todas as relações (sinônimos, hipônimos, etc)."""
        return await self._request(
            "GET",
            "/agrotermos/v1/termoComRelacoes",
            params={"descricao": descricao},
        )

    async def agrotermos_relacoes(self) -> Any:
        """Lista tipos de relações disponíveis no vocabulário."""
        return await self._request("GET", "/agrotermos/v1/relacoes")

    # ======================================================================
    # BovTrace v1 — /bovtrace/v1
    # Rastreabilidade bovina (raças, protocolos, trânsitos GTA)
    # ======================================================================

    async def bovtrace_racas(self) -> Any:
        """Lista raças bovinas reconhecidas."""
        return await self._request("GET", "/bovtrace/v1/racas")

    async def bovtrace_protocolos(self) -> Any:
        """Protocolos de rastreabilidade (SISBOV, Angus GO, etc)."""
        return await self._request("GET", "/bovtrace/v1/protocolos")

    async def bovtrace_transito(self, codigo: str) -> Any:
        """Detalhe de trânsito por código."""
        return await self._request("GET", f"/bovtrace/v1/transitos/{codigo}")

    async def bovtrace_transacao(self, token: str) -> Any:
        """Consulta transação por token."""
        return await self._request("GET", f"/bovtrace/v1/transacoes/{token}")

    # ======================================================================
    # RespondeAgro v1 — /respondeagro/v1
    # Q&A base de conhecimento Embrapa
    # ======================================================================

    async def respondeagro_documento(self, doc_id: str) -> Any:
        """Par pergunta+resposta específico por id."""
        return await self._request("GET", f"/respondeagro/v1/_doc/{doc_id}")

    async def respondeagro_buscar(
        self,
        query: str,
        template: str = "query_all",
        tamanho: int = 10,
    ) -> Any:
        """
        Busca na base de conhecimento.
        Templates: query_one_book, query_all, autocomplete_one_book,
                   autocomplete_all, book_ids
        """
        body = {
            "id": template,
            "params": {
                "query_string": query,
                "size": tamanho,
            },
        }
        return await self._request(
            "POST", "/respondeagro/v1/_search/template", body=body
        )

    # ======================================================================
    # SmartSolosExpert v1 — /smartsolos/expert/v1
    # Classificação SiBCS (Sistema Brasileiro de Classificação de Solos)
    # ======================================================================

    async def smartsolos_health(self) -> Any:
        """Healthcheck do SmartSolos."""
        return await self._request("GET", "/smartsolos/expert/v1/health")

    async def smartsolos_classify(self, profile_list: list[dict]) -> Any:
        """
        Classifica perfis de solo segundo SiBCS (até 4 níveis categóricos).
        profile_list: lista de perfis com ID_PONTO, DRENAGEM, HORIZONTES, etc.
        """
        return await self._request(
            "POST",
            "/smartsolos/expert/v1/classification",
            body={"ProfileList": profile_list},
        )

    async def smartsolos_verify(self, profile_list: list[dict]) -> Any:
        """Verifica perfis de solo (validação antes de classificar)."""
        return await self._request(
            "POST",
            "/smartsolos/expert/v1/verification",
            body={"ProfileList": profile_list},
        )

    # ======================================================================
    # PlantAnnot v2 — /plantannot/v2
    # Anotação de genes/proteínas (pouco útil para AgroJus — stub minimal)
    # ======================================================================

    async def plantannot_autocomplete(self, query: str) -> Any:
        """Autocomplete de genes/proteínas (bioinformática)."""
        return await self._request(
            "GET", "/plantannot/v2/autocomplete", params={"q": query}
        )

    # ======================================================================
    # Sting v1 — /sting/v1
    # Descritores de estruturas proteicas (não relevante para AgroJus — stub)
    # ======================================================================

    async def sting_health(self) -> Any:
        """Healthcheck do Sting (PDB)."""
        return await self._request("GET", "/sting/v1/health")
