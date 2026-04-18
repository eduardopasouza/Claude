"""
CRUD de webhooks + teste manual + logs de entregas.

Rotas:
  GET    /webhooks                  — lista webhooks do usuário
  POST   /webhooks                  — cria
  GET    /webhooks/{id}             — detalhe
  PUT    /webhooks/{id}             — atualiza
  DELETE /webhooks/{id}             — remove
  POST   /webhooks/{id}/test        — dispara delivery de teste
  GET    /webhooks/{id}/deliveries  — lista entregas (logs)
  GET    /webhooks/event-types      — lista eventos suportados
"""

from __future__ import annotations

import logging
import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, HttpUrl

from app.api.auth import get_current_user
from app.models.database import Webhook, WebhookDelivery, get_session
from app.services.webhook_dispatcher import EVENT_TYPES, dispatch, _deliver

logger = logging.getLogger("agrojus.webhooks")
router = APIRouter()


# ------------------------- Schemas -------------------------


class WebhookCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    url: HttpUrl
    event_types: list[str] = Field(..., min_length=1)
    car_filter: Optional[str] = None
    cpf_cnpj_filter: Optional[str] = None
    secret: Optional[str] = None  # se vazio, gera automaticamente
    active: bool = True


class WebhookUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    event_types: Optional[list[str]] = None
    car_filter: Optional[str] = None
    cpf_cnpj_filter: Optional[str] = None
    secret: Optional[str] = None
    active: Optional[bool] = None


class WebhookOut(BaseModel):
    id: int
    user_id: Optional[int]
    name: str
    url: str
    event_types: list[str]
    car_filter: Optional[str]
    cpf_cnpj_filter: Optional[str]
    secret: Optional[str]  # retornado somente no create — depois mascarado
    active: bool
    created_at: Optional[str]
    updated_at: Optional[str]
    last_delivery_at: Optional[str]
    last_delivery_status: Optional[str]


def _to_out(wh: Webhook, *, reveal_secret: bool = False) -> dict:
    return {
        "id": wh.id,
        "user_id": wh.user_id,
        "name": wh.name,
        "url": wh.url,
        "event_types": wh.event_types or [],
        "car_filter": wh.car_filter,
        "cpf_cnpj_filter": wh.cpf_cnpj_filter,
        "secret": wh.secret if reveal_secret else ("****" + wh.secret[-4:] if wh.secret else None),
        "active": wh.active,
        "created_at": wh.created_at.isoformat() if wh.created_at else None,
        "updated_at": wh.updated_at.isoformat() if wh.updated_at else None,
        "last_delivery_at": wh.last_delivery_at.isoformat() if wh.last_delivery_at else None,
        "last_delivery_status": wh.last_delivery_status,
    }


# ------------------------- Rotas -------------------------


@router.get("/event-types")
def list_event_types():
    """Lista event_types suportados."""
    return {"event_types": EVENT_TYPES}


@router.get("")
def list_webhooks(
    active_only: bool = Query(False),
    user: Optional[dict] = Depends(get_current_user),
):
    """Lista webhooks do usuário (ou todos, se sem auth)."""
    session = get_session()
    try:
        q = session.query(Webhook)
        if user and user.get("user_id"):
            q = q.filter((Webhook.user_id == user["user_id"]) | (Webhook.user_id.is_(None)))
        if active_only:
            q = q.filter(Webhook.active.is_(True))
        rows = q.order_by(Webhook.created_at.desc()).all()
        return {"total": len(rows), "webhooks": [_to_out(w) for w in rows]}
    finally:
        session.close()


@router.post("")
def create_webhook(
    data: WebhookCreate,
    user: Optional[dict] = Depends(get_current_user),
):
    """Cria um novo webhook. Retorna o secret em plano (não-mascarado) só uma vez."""
    invalid = [e for e in data.event_types if e not in EVENT_TYPES and e != "*"]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"event_types inválidos: {invalid}. Válidos: {EVENT_TYPES}",
        )

    secret = data.secret or secrets.token_urlsafe(32)

    session = get_session()
    try:
        wh = Webhook(
            user_id=user["user_id"] if user else None,
            name=data.name,
            url=str(data.url),
            event_types=data.event_types,
            car_filter=data.car_filter,
            cpf_cnpj_filter=(data.cpf_cnpj_filter or "").replace(".", "").replace("/", "").replace("-", "") or None,
            secret=secret,
            active=data.active,
        )
        session.add(wh)
        session.commit()
        session.refresh(wh)
        return _to_out(wh, reveal_secret=True)
    finally:
        session.close()


@router.get("/{webhook_id}")
def get_webhook(webhook_id: int, user: Optional[dict] = Depends(get_current_user)):
    """Detalhe de um webhook."""
    session = get_session()
    try:
        wh = session.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not wh:
            raise HTTPException(status_code=404, detail="Webhook não encontrado")
        return _to_out(wh)
    finally:
        session.close()


@router.put("/{webhook_id}")
def update_webhook(
    webhook_id: int,
    data: WebhookUpdate,
    user: Optional[dict] = Depends(get_current_user),
):
    """Atualiza um webhook. Campos não informados permanecem inalterados."""
    session = get_session()
    try:
        wh = session.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not wh:
            raise HTTPException(status_code=404, detail="Webhook não encontrado")

        if data.event_types is not None:
            invalid = [e for e in data.event_types if e not in EVENT_TYPES and e != "*"]
            if invalid:
                raise HTTPException(status_code=400, detail=f"event_types inválidos: {invalid}")
            wh.event_types = data.event_types
        if data.name is not None:
            wh.name = data.name
        if data.url is not None:
            wh.url = str(data.url)
        if data.car_filter is not None:
            wh.car_filter = data.car_filter or None
        if data.cpf_cnpj_filter is not None:
            clean = (data.cpf_cnpj_filter or "").replace(".", "").replace("/", "").replace("-", "")
            wh.cpf_cnpj_filter = clean or None
        if data.secret is not None:
            wh.secret = data.secret or None
        if data.active is not None:
            wh.active = data.active

        session.commit()
        session.refresh(wh)
        return _to_out(wh)
    finally:
        session.close()


@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: int, user: Optional[dict] = Depends(get_current_user)):
    """Remove um webhook e seus deliveries históricos."""
    session = get_session()
    try:
        wh = session.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not wh:
            raise HTTPException(status_code=404, detail="Webhook não encontrado")
        session.query(WebhookDelivery).filter(WebhookDelivery.webhook_id == webhook_id).delete()
        session.delete(wh)
        session.commit()
        return {"deleted": True, "id": webhook_id}
    finally:
        session.close()


@router.post("/{webhook_id}/test")
async def test_webhook(webhook_id: int, user: Optional[dict] = Depends(get_current_user)):
    """Dispara entrega de teste para o webhook (payload sintético)."""
    session = get_session()
    try:
        wh = session.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not wh:
            raise HTTPException(status_code=404, detail="Webhook não encontrado")
        # Snapshot — o objeto se desgarra da sessão
        webhook_snapshot = wh
        session.expunge(webhook_snapshot)
    finally:
        session.close()

    payload = {
        "test": True,
        "message": "Evento de teste disparado pelo próprio usuário",
        "car_code": webhook_snapshot.car_filter,
        "cpf_cnpj": webhook_snapshot.cpf_cnpj_filter,
    }
    delivery = await _deliver(webhook_snapshot, event_type="*", payload=payload, attempt=1)
    return {
        "delivery_id": delivery.id,
        "status_code": delivery.status_code,
        "success": delivery.success,
        "duration_ms": delivery.duration_ms,
        "error": delivery.error,
    }


@router.post("/{webhook_id}/dispatch")
async def manual_dispatch(
    webhook_id: int,
    event_type: str,
    payload: dict,
    user: Optional[dict] = Depends(get_current_user),
):
    """Admin-only: força dispatch de um evento real (não sintético)."""
    session = get_session()
    try:
        wh = session.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not wh:
            raise HTTPException(status_code=404, detail="Webhook não encontrado")
        session.expunge(wh)
    finally:
        session.close()

    delivery = await _deliver(wh, event_type=event_type, payload=payload, attempt=1)
    return {
        "delivery_id": delivery.id,
        "status_code": delivery.status_code,
        "success": delivery.success,
    }


@router.get("/{webhook_id}/deliveries")
def list_deliveries(
    webhook_id: int,
    skip: int = 0,
    limit: int = 50,
    success_only: Optional[bool] = None,
    user: Optional[dict] = Depends(get_current_user),
):
    """Lista entregas (logs) paginado, mais recentes primeiro."""
    session = get_session()
    try:
        q = session.query(WebhookDelivery).filter(WebhookDelivery.webhook_id == webhook_id)
        if success_only is True:
            q = q.filter(WebhookDelivery.success.is_(True))
        elif success_only is False:
            q = q.filter(WebhookDelivery.success.is_(False))
        total = q.count()
        rows = q.order_by(WebhookDelivery.attempted_at.desc()).offset(skip).limit(limit).all()
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "deliveries": [
                {
                    "id": d.id,
                    "event_type": d.event_type,
                    "success": d.success,
                    "status_code": d.status_code,
                    "attempt": d.attempt,
                    "attempted_at": d.attempted_at.isoformat() if d.attempted_at else None,
                    "duration_ms": d.duration_ms,
                    "error": d.error,
                    "response_body": d.response_body,
                    "payload": d.payload,
                }
                for d in rows
            ],
        }
    finally:
        session.close()
