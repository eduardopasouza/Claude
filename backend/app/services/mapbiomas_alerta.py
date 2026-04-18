"""
MapBiomas Alerta GraphQL Service — alertas em tempo real por CAR.

Complementa os 515k alertas ja no PostGIS com consulta direta
ao GraphQL do MapBiomas para alertas mais recentes.
"""

import logging
import time
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger("agrojus.mapbiomas")

GRAPHQL_URL = "https://plataforma.alerta.mapbiomas.org/api/v2/graphql"

_token: Optional[str] = None
_token_expires: float = 0


def _get_token() -> Optional[str]:
    """Autentica no MapBiomas e retorna JWT (cache por 1h)."""
    global _token, _token_expires

    if _token and time.time() < _token_expires:
        return _token

    email = settings.mapbiomas_email
    password = settings.mapbiomas_password
    if not email or not password:
        logger.warning("MapBiomas credentials nao configuradas em .env")
        return None

    mutation = """
    mutation {
        signIn(email: "%s", password: "%s") {
            token
        }
    }
    """ % (email, password)

    try:
        r = httpx.post(GRAPHQL_URL, json={"query": mutation}, timeout=15)
        data = r.json()
        _token = data["data"]["signIn"]["token"]
        _token_expires = time.time() + 3600  # 1h
        logger.info("MapBiomas token obtido")
        return _token
    except Exception as e:
        logger.warning("MapBiomas auth falhou: %s", e)
        return None


def query_alerts_by_car(car_code: str, limit: int = 50) -> dict:
    """
    Consulta alertas MapBiomas para um CAR especifico via GraphQL.

    Retorna alertas mais recentes nao necessariamente no PostGIS local.
    """
    token = _get_token()
    if not token:
        return {"available": False, "error": "Token indisponivel"}

    start = time.time()

    query = """
    {
        alerts(
            filters: {
                territoryCarCode: "%s"
            }
            limit: %d
            page: 1
            orderBy: { field: DETECTED_AT, order: DESC }
        ) {
            data {
                alertCode
                areaHa
                detectedAt
                source
                biome
                state
                city
                statusName
                carCode
                images {
                    before { url date }
                    after { url date }
                }
            }
            metadata {
                totalCount
                totalPages
            }
        }
    }
    """ % (car_code, limit)

    try:
        r = httpx.post(
            GRAPHQL_URL,
            json={"query": query},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        data = r.json()

        alerts_data = data.get("data", {}).get("alerts", {})
        alerts = alerts_data.get("data", [])
        metadata = alerts_data.get("metadata", {})

        elapsed = (time.time() - start) * 1000
        logger.info(
            "MapBiomas GraphQL: %d alertas para CAR %s em %.0fms",
            len(alerts), car_code, elapsed,
        )

        return {
            "available": True,
            "total_count": metadata.get("totalCount", 0),
            "alerts": [
                {
                    "alert_code": a.get("alertCode"),
                    "area_ha": a.get("areaHa"),
                    "detected_at": a.get("detectedAt"),
                    "source": a.get("source"),
                    "biome": a.get("biome"),
                    "state": a.get("state"),
                    "city": a.get("city"),
                    "status": a.get("statusName"),
                    "car_code": a.get("carCode"),
                    "images": a.get("images"),
                }
                for a in alerts
            ],
            "query_time_ms": round(elapsed, 0),
        }
    except Exception as e:
        logger.warning("MapBiomas GraphQL error: %s", e)
        return {"available": False, "error": str(e)}
