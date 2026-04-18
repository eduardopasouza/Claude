"""
Dispatcher de webhooks.

Usado por outros serviços (monitoring, publicacoes, mapbiomas, ibama) para
disparar POST JSON para URLs cadastradas quando eventos ocorrem.

Fluxo:
1. Chamar `dispatch(event_type, payload, car_code=..., cpf_cnpj=...)`
2. Dispatcher consulta webhooks ativos que batem com filtros (event_type
   deve estar em webhook.event_types; se webhook tem car_filter, só dispara
   se car_code bater; idem cpf_cnpj).
3. Faz POST httpx async com timeout curto.
4. Persiste WebhookDelivery com resultado.
5. Atualiza webhook.last_delivery_at / last_delivery_status.

Assinatura HMAC opcional: se webhook.secret estiver setado, adiciona header
X-AgroJus-Signature: sha256=<hex>
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Iterable, Optional

import httpx

from app.config import settings
from app.models.database import Webhook, WebhookDelivery, get_session

logger = logging.getLogger("agrojus.webhook")


# Event types suportados (manter em sync com frontend/docs)
EVENT_TYPES = [
    "mapbiomas_alert",       # novo alerta MapBiomas Alerta
    "deter_alert",            # novo polígono DETER
    "prodes_alert",           # novo polígono PRODES
    "ibama_embargo",          # novo embargo IBAMA
    "ibama_auto",             # novo auto de infração
    "djen_publicacao",        # nova publicação DJEN
    "datajud_movimento",      # novo movimento processual
    "car_status_change",      # mudança de status do CAR
    "slave_labour",           # aparição na lista suja
]


def _sign_payload(secret: str, payload_bytes: bytes) -> str:
    """Gera HMAC-SHA256 do payload (hex)."""
    mac = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256)
    return f"sha256={mac.hexdigest()}"


def _matches(
    webhook: Webhook,
    event_type: str,
    car_code: Optional[str],
    cpf_cnpj: Optional[str],
) -> bool:
    """Decide se o webhook casa com o evento."""
    if not webhook.active:
        return False
    events = webhook.event_types or []
    if event_type not in events and "*" not in events:
        return False
    if webhook.car_filter and car_code and webhook.car_filter != car_code:
        return False
    if webhook.cpf_cnpj_filter and cpf_cnpj:
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
        if webhook.cpf_cnpj_filter.replace(".", "").replace("/", "").replace("-", "") != clean:
            return False
    return True


async def _deliver(
    webhook: Webhook,
    event_type: str,
    payload: dict,
    attempt: int = 1,
) -> WebhookDelivery:
    """Faz POST ao webhook.url e retorna o objeto WebhookDelivery persistido."""
    started = time.time()
    body_bytes = json.dumps(payload, default=str, ensure_ascii=False).encode("utf-8")

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "AgroJus-Webhook/1.0",
        "X-AgroJus-Event": event_type,
        "X-AgroJus-Delivery-Attempt": str(attempt),
    }
    if webhook.secret:
        headers["X-AgroJus-Signature"] = _sign_payload(webhook.secret, body_bytes)

    status_code: Optional[int] = None
    response_body = ""
    error_text: Optional[str] = None
    success = False

    try:
        async with httpx.AsyncClient(timeout=settings.webhook_timeout_seconds) as client:
            resp = await client.post(webhook.url, content=body_bytes, headers=headers)
            status_code = resp.status_code
            response_body = (resp.text or "")[:2000]
            success = 200 <= resp.status_code < 300
    except httpx.TimeoutException:
        error_text = f"timeout após {settings.webhook_timeout_seconds}s"
    except httpx.RequestError as e:
        error_text = f"erro de conexão: {e!s}"[:500]
    except Exception as e:  # noqa: BLE001
        error_text = f"erro inesperado: {type(e).__name__}: {e!s}"[:500]

    duration_ms = int((time.time() - started) * 1000)

    # Persist delivery
    session = get_session()
    try:
        delivery = WebhookDelivery(
            webhook_id=webhook.id,
            event_type=event_type,
            payload=payload,
            status_code=status_code,
            response_body=response_body,
            success=success,
            attempt=attempt,
            error=error_text,
            duration_ms=duration_ms,
        )
        session.add(delivery)

        # Update webhook cached status
        wh = session.query(Webhook).filter(Webhook.id == webhook.id).first()
        if wh:
            wh.last_delivery_at = datetime.now(timezone.utc)
            wh.last_delivery_status = "success" if success else "failed"

        session.commit()
        session.refresh(delivery)
        return delivery
    finally:
        session.close()


async def dispatch(
    event_type: str,
    payload: dict,
    car_code: Optional[str] = None,
    cpf_cnpj: Optional[str] = None,
    user_id: Optional[int] = None,
) -> list[int]:
    """
    Dispara um evento para todos os webhooks aplicáveis.

    Retorna lista de delivery_ids criados.
    """
    if event_type not in EVENT_TYPES:
        logger.warning("dispatch chamado com event_type desconhecido: %s", event_type)
        # Continuamos — usuário pode ter wildcard "*"

    enriched = {
        **payload,
        "event_type": event_type,
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "car_code": car_code,
        "cpf_cnpj": cpf_cnpj,
    }

    session = get_session()
    try:
        query = session.query(Webhook).filter(Webhook.active.is_(True))
        if user_id is not None:
            query = query.filter((Webhook.user_id == user_id) | (Webhook.user_id.is_(None)))
        webhooks: Iterable[Webhook] = query.all()

        applicable = [w for w in webhooks if _matches(w, event_type, car_code, cpf_cnpj)]
    finally:
        session.close()

    if not applicable:
        return []

    tasks = [_deliver(w, event_type, enriched, attempt=1) for w in applicable]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    delivery_ids: list[int] = []
    for r in results:
        if isinstance(r, Exception):
            logger.warning("dispatch webhook falhou: %s", r)
            continue
        delivery_ids.append(r.id)

    logger.info(
        "dispatch event=%s car=%s cpf=%s hit=%d",
        event_type, car_code, cpf_cnpj, len(delivery_ids),
    )
    return delivery_ids


def dispatch_sync(*args: Any, **kwargs: Any) -> list[int]:
    """Versão síncrona — bloqueia até entregar. Útil em scripts/CLI."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    if loop.is_running():
        # Em contexto async, não pode bloquear. Cria tarefa background.
        return asyncio.run_coroutine_threadsafe(dispatch(*args, **kwargs), loop).result()
    return loop.run_until_complete(dispatch(*args, **kwargs))
