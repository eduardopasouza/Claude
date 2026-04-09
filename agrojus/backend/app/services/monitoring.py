"""
Serviço de monitoramento e alertas.

Monitora mudanças em:
- Imóveis (novo embargo, alteração no CAR, desmatamento)
- Pessoas (novo processo, mudança cadastral, novo embargo)
- Regiões (novos embargos, alertas de desmatamento)

Em produção, rodaria como job periódico (cron/celery).
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from app.models.schemas import (
    PropertySearchRequest,
    PersonSearchRequest,
)

logger = logging.getLogger("agrojus")


class MonitoringAlert:
    """Representa um alerta gerado pelo monitoramento."""

    def __init__(
        self,
        alert_type: str,
        title: str,
        description: str,
        severity: str = "info",
        cpf_cnpj: str = None,
        car_code: str = None,
    ):
        self.id = str(uuid.uuid4())
        self.alert_type = alert_type
        self.title = title
        self.description = description
        self.severity = severity  # info, warning, critical
        self.cpf_cnpj = cpf_cnpj
        self.car_code = car_code
        self.created_at = datetime.now(timezone.utc)
        self.read = False


class MonitoringService:
    """Serviço de monitoramento de mudanças."""

    def __init__(self):
        # In production, these would be stored in the database
        self._monitored_properties: list[str] = []  # CAR codes
        self._monitored_persons: list[str] = []  # CPF/CNPJs
        self._alerts: list[MonitoringAlert] = []

    def add_property_monitor(self, car_code: str) -> bool:
        """Adiciona um imóvel ao monitoramento."""
        if car_code not in self._monitored_properties:
            self._monitored_properties.append(car_code)
            return True
        return False

    def remove_property_monitor(self, car_code: str) -> bool:
        """Remove um imóvel do monitoramento."""
        if car_code in self._monitored_properties:
            self._monitored_properties.remove(car_code)
            return True
        return False

    def add_person_monitor(self, cpf_cnpj: str) -> bool:
        """Adiciona uma pessoa ao monitoramento."""
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
        if clean not in self._monitored_persons:
            self._monitored_persons.append(clean)
            return True
        return False

    def remove_person_monitor(self, cpf_cnpj: str) -> bool:
        """Remove uma pessoa do monitoramento."""
        clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
        if clean in self._monitored_persons:
            self._monitored_persons.remove(clean)
            return True
        return False

    def get_alerts(
        self,
        cpf_cnpj: str = None,
        car_code: str = None,
        unread_only: bool = False,
    ) -> list[dict]:
        """Retorna alertas filtrados."""
        alerts = self._alerts

        if cpf_cnpj:
            clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
            alerts = [a for a in alerts if a.cpf_cnpj == clean]

        if car_code:
            alerts = [a for a in alerts if a.car_code == car_code]

        if unread_only:
            alerts = [a for a in alerts if not a.read]

        return [
            {
                "id": a.id,
                "alert_type": a.alert_type,
                "title": a.title,
                "description": a.description,
                "severity": a.severity,
                "cpf_cnpj": a.cpf_cnpj,
                "car_code": a.car_code,
                "created_at": a.created_at.isoformat(),
                "read": a.read,
            }
            for a in sorted(alerts, key=lambda x: x.created_at, reverse=True)
        ]

    def mark_alert_read(self, alert_id: str) -> bool:
        """Marca um alerta como lido."""
        for alert in self._alerts:
            if alert.id == alert_id:
                alert.read = True
                return True
        return False

    def get_monitored_items(self) -> dict:
        """Retorna itens monitorados."""
        return {
            "properties": self._monitored_properties,
            "persons": self._monitored_persons,
            "total_properties": len(self._monitored_properties),
            "total_persons": len(self._monitored_persons),
        }

    async def run_check_cycle(self):
        """
        Executa um ciclo de verificação de todas as entidades monitoradas.

        Em produção, seria executado periodicamente (ex: a cada 6 horas)
        via Celery beat ou cron job.
        """
        from app.collectors.ibama import IBAMACollector
        from app.collectors.sicar import SICARCollector

        ibama = IBAMACollector()
        sicar = SICARCollector()

        # Check monitored persons for new embargos
        for cpf_cnpj in self._monitored_persons:
            try:
                embargos = await ibama.search_embargos_by_cpf_cnpj(cpf_cnpj)
                # Compare with previously known embargos
                # If new ones found, create alert
                if embargos:
                    self._alerts.append(MonitoringAlert(
                        alert_type="new_embargo",
                        title=f"Novo embargo IBAMA detectado",
                        description=f"{len(embargos)} embargo(s) encontrado(s) para CPF/CNPJ {cpf_cnpj}",
                        severity="critical",
                        cpf_cnpj=cpf_cnpj,
                    ))
            except Exception as e:
                logger.warning("%s: %s", type(e).__name__, e)

        # Check monitored properties for CAR status changes
        for car_code in self._monitored_properties:
            try:
                car_data = await sicar.get_property_by_car(car_code)
                if car_data and car_data.status:
                    status = car_data.status.lower()
                    if "cancelado" in status or "suspenso" in status:
                        self._alerts.append(MonitoringAlert(
                            alert_type="car_status_change",
                            title=f"Alteracao no status do CAR",
                            description=f"CAR {car_code} com status: {car_data.status}",
                            severity="warning",
                            car_code=car_code,
                        ))
            except Exception as e:
                logger.warning("%s: %s", type(e).__name__, e)

        return len(self._alerts)
