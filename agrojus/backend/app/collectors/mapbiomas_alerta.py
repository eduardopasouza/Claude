"""
Coletor MapBiomas Alerta — GraphQL API oficial.

Endpoint GraphQL:
  https://plataforma.alerta.mapbiomas.org/api/v2/graphql

Auth (descoberto sessão 7):
  - Queries básicas (version, alertDateRange, territoryOptions) → PÚBLICAS
  - Queries de alerts, ruralProperty → exigem JWT via mutation signIn
  - Login: mutation signIn(email!, password!) { token } retorna JWT
  - JWT no header: Authorization: Bearer <token>
  - Endpoint REST /auth/login retorna HTTP 500 (deprecated — não usar)

Schema (descoberto via introspect):
  Query principal:
    alerts(startDate, endDate, territoryIds, sources, page, limit, ...)
    alert(alertCode: Int, propertyCode: String)
    ruralProperty(propertyCode: String)    → alertas por CAR
    territoryOptions                        → territórios disponíveis
    alertDateRange                          → intervalo disponível
    version                                 → APIVersion { version, buildDate, ... }

  AlertData fields úteis:
    alertCode, areaHa, detectedAt, publishedAt, sources (LIST)
    crossedBiomes, crossedStates, crossedCities (LIST)
    crossedConservationUnits, crossedIndigenousLands
    crossedEmbargoesIds, crossedEmbargoesRuralPropertiesIds
    alertGeometry { geometryJson, bbox }
    coordenates { lat, lng }

  SourceTypes enum: All, Sad, Deter, Glad, SiradX, etc. (parcial via intro)

Cache: 1h para alertas recentes.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

import httpx

from app.collectors.base import BaseCollector
from app.config import settings

logger = logging.getLogger("agrojus")


MAPBIOMAS_GRAPHQL = "https://plataforma.alerta.mapbiomas.org/api/v2/graphql"


class MapBiomasAuth:
    """Singleton do JWT MapBiomas. Login via GraphQL signIn mutation."""

    _instance: Optional["MapBiomasAuth"] = None
    _token: Optional[str] = None
    _expires_at: float = 0.0

    def __new__(cls) -> "MapBiomasAuth":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_token(self) -> Optional[str]:
        """JWT válido. Refresh se restar <5 min."""
        now = time.time()
        if self._token and now < self._expires_at - 300:
            return self._token

        email = getattr(settings, "mapbiomas_email", None)
        password = getattr(settings, "mapbiomas_password", None)
        if not email or not password:
            logger.warning("MapBiomas: credenciais ausentes no .env")
            return None

        mutation = (
            "mutation($e: String!, $p: String!) "
            "{ signIn(email: $e, password: $p) { token } }"
        )
        try:
            async with httpx.AsyncClient(timeout=30.0) as c:
                r = await c.post(
                    MAPBIOMAS_GRAPHQL,
                    json={
                        "query": mutation,
                        "variables": {"e": email, "p": password},
                    },
                    headers={"Content-Type": "application/json"},
                )
            data = r.json()
            if data.get("errors") or not data.get("data", {}).get("signIn"):
                logger.warning("MapBiomas signIn errors: %s", data.get("errors"))
                return None
            token = data["data"]["signIn"].get("token")
            if not token:
                return None
            self._token = token
            # JWT da MapBiomas tem exp ~ 2 anos; guardamos 24h p/ segurança
            self._expires_at = now + 24 * 3600
            logger.info("MapBiomas JWT obtido (len=%d)", len(token))
            return token
        except Exception as e:
            logger.warning("MapBiomas signIn erro: %s", e)
            return None


class MapBiomasAlertaCollector(BaseCollector):
    """Cliente GraphQL do MapBiomas Alerta."""

    def __init__(self) -> None:
        super().__init__("mapbiomas_alerta")
        self.auth = MapBiomasAuth()

    async def _graphql(
        self, query: str, variables: Optional[dict] = None, auth_required: bool = True
    ) -> Any:
        """Executa GraphQL POST. Adiciona JWT se auth_required=True."""
        cache_key = f"gql:{hash(query)}:{sorted((variables or {}).items())}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        headers = {"Content-Type": "application/json"}
        if auth_required:
            token = await self.auth.get_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"

        try:
            async with httpx.AsyncClient(timeout=90.0) as c:
                r = await c.post(
                    MAPBIOMAS_GRAPHQL,
                    json={"query": query, "variables": variables or {}},
                    headers=headers,
                )
            if r.status_code != 200:
                logger.warning(
                    "MapBiomas GraphQL %d: %s", r.status_code, r.text[:200]
                )
                return {"error": f"HTTP {r.status_code}", "body": r.text[:500]}
            data = r.json()
            if data.get("errors"):
                logger.warning("MapBiomas GraphQL errors: %s", data["errors"][:2])
                return {"error": "GraphQL errors", "details": data["errors"]}
            result = data.get("data", {})
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.warning("MapBiomas GraphQL erro: %s", e)
            return {"error": str(e)}

    # --- Queries de alto nível ------------------------------------------

    async def version(self) -> Any:
        """APIVersion object (healthcheck — query pública)."""
        return await self._graphql(
            "{ version { version buildDate buildHash rubyVersion } }",
            auth_required=False,
        )

    async def date_range(self) -> Any:
        """Janela de datas disponível + última publicação."""
        return await self._graphql(
            """
            {
              alertDateRange {
                minDetectedAt maxDetectedAt
                minPublishedAt maxPublishedAt
              }
            }
            """
        )

    async def territory_options(self) -> Any:
        """Todos os territórios disponíveis para filtro."""
        q = """
        {
          territoryOptions {
            biomesOptions { id name }
            statesOptions { id name }
            citiesOptions { id name }
            conservationUnitsOptions { id name }
            indigenousLandsOptions { id name }
          }
        }
        """
        return await self._graphql(q)

    async def alerts(
        self,
        start_date: str,
        end_date: str,
        territory_ids: Optional[list[int]] = None,
        sources: Optional[list[str]] = None,
        page: int = 1,
        limit: int = 100,
    ) -> Any:
        """
        Busca alertas publicados.
        sources: lista do enum SourceTypes (ex: ['Sad', 'Deter', 'Glad'])
        """
        q = """
        query Alerts(
          $startDate: BaseDate
          $endDate: BaseDate
          $territoryIds: [Int!]
          $sources: [SourceTypes!]
          $page: Int
          $limit: Int
        ) {
          alerts(
            startDate: $startDate
            endDate: $endDate
            territoryIds: $territoryIds
            sources: $sources
            page: $page
            limit: $limit
          ) {
            collection {
              alertCode
              areaHa
              detectedAt
              publishedAt
              sources
              crossedBiomes
              crossedStates
              crossedCities
              coordenates { latitude longitude }
            }
            metadata {
              totalCount
              currentPage
              totalPages
            }
          }
        }
        """
        vars_ = {
            "startDate": start_date,
            "endDate": end_date,
            "territoryIds": territory_ids,
            "sources": sources,
            "page": page,
            "limit": limit,
        }
        return await self._graphql(q, vars_)

    async def alert_detail(self, alert_code: int) -> Any:
        """Detalhe completo de um alerta."""
        q = """
        query Alert($alertCode: Int!) {
          alert(alertCode: $alertCode) {
            alertCode
            areaHa
            detectedAt
            publishedAt
            sources
            crossedBiomes
            crossedStates
            crossedCities
            crossedConservationUnits
            crossedIndigenousLands
            crossedEmbargoesIds
            coordenates { latitude longitude }
            alertGeometry { bbox }
          }
        }
        """
        return await self._graphql(q, {"alertCode": alert_code})

    async def alerts_by_property(self, property_code: str) -> Any:
        """Alertas que intersectam um imóvel CAR."""
        q = """
        query Property($propertyCode: String!) {
          ruralProperty(propertyCode: $propertyCode) {
            propertyCode
            areaHa
            alerts {
              alertCode
              detectedAt
              areaHa
              sources
            }
          }
        }
        """
        return await self._graphql(q, {"propertyCode": property_code})
