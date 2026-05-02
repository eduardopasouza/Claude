"""HTTP Basic Auth opcional, ativado via env vars.

Quando `SIMGLOBAL_AUTH_USER` e `SIMGLOBAL_AUTH_PASSWORD_HASH` (sha256
hex) estão definidos, todas as rotas exceto `/api/health` exigem
Basic Auth com credenciais que batem. Quando ausentes (modo dev),
o middleware passa transparente.

Health endpoint sempre fica aberto pra healthcheck do Fly/Vercel
não falhar com 401.
"""
from __future__ import annotations

import base64
import hashlib
import os
import secrets

from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


_AUTH_HEADERS = [(b"www-authenticate", b'Basic realm="sim-global"')]


def _unauthorized() -> Response:
    return Response(
        status_code=401,
        content="autenticação requerida",
        headers={"WWW-Authenticate": 'Basic realm="sim-global"'},
    )


def _bad_credentials() -> Response:
    return Response(
        status_code=401,
        content="usuário ou senha inválidos",
        headers={"WWW-Authenticate": 'Basic realm="sim-global"'},
    )


class BasicAuthMiddleware:
    """Pure-ASGI middleware. Mais leve que BaseHTTPMiddleware do Starlette."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        # /api/health sempre aberto pra healthchecks externos.
        if path == "/api/health":
            await self.app(scope, receive, send)
            return

        user_env = os.getenv("SIMGLOBAL_AUTH_USER")
        hash_env = os.getenv("SIMGLOBAL_AUTH_PASSWORD_HASH")
        if not user_env or not hash_env:
            # modo dev: auth desabilitada
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        auth = headers.get(b"authorization", b"").decode("ascii", errors="ignore")
        if not auth.startswith("Basic "):
            await _unauthorized()(scope, receive, send)
            return
        try:
            decoded = base64.b64decode(auth[6:]).decode("utf-8")
        except Exception:
            await _bad_credentials()(scope, receive, send)
            return
        if ":" not in decoded:
            await _bad_credentials()(scope, receive, send)
            return
        user, password = decoded.split(":", 1)
        user_ok = secrets.compare_digest(user, user_env)
        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        pw_ok = secrets.compare_digest(pw_hash, hash_env)
        if not (user_ok and pw_ok):
            await _bad_credentials()(scope, receive, send)
            return

        await self.app(scope, receive, send)
