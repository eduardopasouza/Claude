"""Rotas de monitoramento e alertas."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.monitoring import MonitoringService

router = APIRouter()

# Singleton (production: proper DI)
_monitoring = MonitoringService()


class MonitorRequest(BaseModel):
    car_code: Optional[str] = None
    cpf_cnpj: Optional[str] = None


@router.post("/property")
async def add_property_monitor(request: MonitorRequest):
    """Adiciona um imóvel ao monitoramento."""
    if not request.car_code:
        raise HTTPException(status_code=400, detail="car_code obrigatorio")
    added = _monitoring.add_property_monitor(request.car_code)
    return {"monitored": added, "car_code": request.car_code}


@router.delete("/property/{car_code}")
async def remove_property_monitor(car_code: str):
    """Remove um imóvel do monitoramento."""
    removed = _monitoring.remove_property_monitor(car_code)
    return {"removed": removed, "car_code": car_code}


@router.post("/person")
async def add_person_monitor(request: MonitorRequest):
    """Adiciona uma pessoa ao monitoramento."""
    if not request.cpf_cnpj:
        raise HTTPException(status_code=400, detail="cpf_cnpj obrigatorio")
    added = _monitoring.add_person_monitor(request.cpf_cnpj)
    return {"monitored": added, "cpf_cnpj": request.cpf_cnpj}


@router.delete("/person/{cpf_cnpj}")
async def remove_person_monitor(cpf_cnpj: str):
    """Remove uma pessoa do monitoramento."""
    removed = _monitoring.remove_person_monitor(cpf_cnpj)
    return {"removed": removed, "cpf_cnpj": cpf_cnpj}


@router.get("/alerts")
async def get_alerts(
    cpf_cnpj: Optional[str] = None,
    car_code: Optional[str] = None,
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 50,
):
    """Retorna alertas de monitoramento com paginacao."""
    all_alerts = _monitoring.get_alerts(cpf_cnpj, car_code, unread_only)
    total = len(all_alerts)
    page = all_alerts[skip:skip + limit]
    return {"alerts": page, "total": total, "skip": skip, "limit": limit}


@router.put("/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: str):
    """Marca um alerta como lido."""
    marked = _monitoring.mark_alert_read(alert_id)
    return {"marked": marked, "alert_id": alert_id}


@router.get("/status")
async def monitoring_status():
    """Retorna status do monitoramento (itens monitorados)."""
    return _monitoring.get_monitored_items()


@router.post("/run-check")
async def run_check():
    """Executa um ciclo de verificação manual (admin only)."""
    count = await _monitoring.run_check_cycle()
    return {"alerts_generated": count}
