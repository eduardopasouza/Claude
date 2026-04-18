"""
Middleware de rate limiting por plano de usuario.

Controla:
- searches_per_day: buscas por dia
- reports_per_month: relatorios por mes

Usa armazenamento in-memory (producao: Redis).
Thread-safe para requests concorrentes.
"""

import logging
import time
from collections import defaultdict
from threading import Lock

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.services.auth import decode_token, get_plan_limits

logger = logging.getLogger("agrojus.ratelimit")


class _RateBucket:
    """Contador thread-safe com janela de tempo."""

    def __init__(self):
        self._lock = Lock()
        self._counts: dict[str, list[float]] = defaultdict(list)

    def check_and_increment(self, key: str, window_seconds: int, max_count: int) -> tuple[bool, int]:
        """Retorna (allowed, remaining). Thread-safe."""
        with self._lock:
            now = time.time()
            cutoff = now - window_seconds

            # Remove entradas expiradas
            self._counts[key] = [t for t in self._counts[key] if t > cutoff]

            current = len(self._counts[key])

            if max_count == -1:  # unlimited
                self._counts[key].append(now)
                return True, -1

            if current >= max_count:
                return False, 0

            self._counts[key].append(now)
            return True, max_count - current - 1


# Buckets globais
_search_bucket = _RateBucket()
_report_bucket = _RateBucket()

# Rotas que contam como "search"
_SEARCH_PATHS = {"/api/v1/search/", "/api/v1/search/smart", "/api/v1/search/property"}
# Rotas que contam como "report"
_REPORT_PATHS = {"/api/v1/report/due-diligence", "/api/v1/report/buyer",
                 "/api/v1/report/lawyer", "/api/v1/report/investor",
                 "/api/v1/report/person", "/api/v1/report/region"}

DAY_SECONDS = 86400
MONTH_SECONDS = 86400 * 30


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware que limita requests por plano do usuario."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Apenas limitar rotas de search e report
        is_search = any(path.startswith(p) for p in _SEARCH_PATHS)
        is_report = any(path.startswith(p) for p in _REPORT_PATHS)

        if not is_search and not is_report:
            return await call_next(request)

        # Extrair plano do token JWT (ou default "free")
        plan = "free"
        user_key = request.client.host if request.client else "unknown"

        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = decode_token(token)
            if payload:
                plan = payload.get("plan", "free")
                user_key = payload.get("email", user_key)

        limits = get_plan_limits(plan)

        if is_search:
            max_count = limits.get("searches_per_day", 10)
            allowed, remaining = _search_bucket.check_and_increment(
                f"search:{user_key}", DAY_SECONDS, max_count
            )
            if not allowed:
                logger.warning("Rate limit exceeded: search for %s (plan=%s)", user_key, plan)
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Limite de buscas diarias atingido ({max_count}/dia no plano {plan})",
                        "plan": plan,
                        "limit": max_count,
                        "upgrade_hint": "Faca upgrade do plano para mais buscas",
                    },
                    headers={"Retry-After": "3600"},
                )
            response = await call_next(request)
            if remaining >= 0:
                response.headers["X-RateLimit-Remaining-Searches"] = str(remaining)
            return response

        if is_report:
            max_count = limits.get("reports_per_month", 3)
            allowed, remaining = _report_bucket.check_and_increment(
                f"report:{user_key}", MONTH_SECONDS, max_count
            )
            if not allowed:
                logger.warning("Rate limit exceeded: report for %s (plan=%s)", user_key, plan)
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Limite de relatorios mensais atingido ({max_count}/mes no plano {plan})",
                        "plan": plan,
                        "limit": max_count,
                        "upgrade_hint": "Faca upgrade do plano para mais relatorios",
                    },
                    headers={"Retry-After": "86400"},
                )
            response = await call_next(request)
            if remaining >= 0:
                response.headers["X-RateLimit-Remaining-Reports"] = str(remaining)
            return response

        return await call_next(request)
