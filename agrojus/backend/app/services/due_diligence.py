"""
Serviço de Due Diligence Rural.

Orquestra a coleta de dados de múltiplas fontes, realiza o cruzamento
e gera o relatório consolidado com score de risco.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from app.collectors.sicar import SICARCollector
from app.collectors.sigef import SIGEFCollector
from app.collectors.receita_federal import ReceitaFederalCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.processors.geospatial import GeospatialProcessor
from app.models.schemas import (
    DueDiligenceReport,
    PropertySearchRequest,
    RiskScore,
    RiskLevel,
)


class DueDiligenceService:
    """Serviço principal de due diligence rural automatizada."""

    def __init__(self):
        self.sicar = SICARCollector()
        self.sigef = SIGEFCollector()
        self.receita = ReceitaFederalCollector()
        self.ibama = IBAMACollector()
        self.slave_labour = SlaveLabourCollector()
        self.geo_processor = GeospatialProcessor()

    async def generate_report(self, request: PropertySearchRequest) -> DueDiligenceReport:
        """
        Gera um relatório completo de due diligence rural.

        Coleta dados de todas as fontes disponíveis, realiza cruzamentos
        e calcula o score de risco.
        """
        report = DueDiligenceReport(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
        )

        # 1. Buscar dados do CAR
        if request.car_code:
            report.property_info = await self.sicar.get_property_by_car(request.car_code)

            # Try to get geometry for overlap analysis
            geometry = await self.sicar.get_geometry_wfs(request.car_code)
            if geometry and report.property_info:
                report.property_info.geometry_wkt = geometry

        # 2. Buscar dados do SIGEF
        if request.car_code:
            # Try to find SIGEF parcel associated with the CAR
            sigef_data = await self.sigef.get_parcel_by_code(request.car_code)
            if sigef_data:
                report.sigef_info = sigef_data

        if request.latitude and request.longitude:
            # Search by location if coordinates provided
            parcels = await self.sigef.search_parcels_by_location(
                request.latitude, request.longitude
            )
            if parcels:
                report.sigef_info = parcels[0]

        # 3. Buscar dados do proprietário (CNPJ)
        if request.cpf_cnpj:
            validation = await self.receita.validate_cpf_cnpj(request.cpf_cnpj)
            if validation["type"] == "CNPJ" and validation["valid"]:
                report.owner_info = await self.receita.get_cnpj(request.cpf_cnpj)

        # 4. Buscar embargos IBAMA
        if request.cpf_cnpj:
            report.ibama_embargos = await self.ibama.search_embargos_by_cpf_cnpj(
                request.cpf_cnpj
            )
        elif report.property_info and report.property_info.municipality:
            state = report.property_info.state or request.state or ""
            report.ibama_embargos = await self.ibama.search_embargos_by_municipality(
                report.property_info.municipality, state
            )

        # 5. Verificar lista suja (trabalho escravo)
        if request.cpf_cnpj:
            report.slave_labour = await self.slave_labour.search_by_cpf_cnpj(
                request.cpf_cnpj
            )
        elif request.owner_name:
            report.slave_labour = await self.slave_labour.search_by_name(
                request.owner_name
            )

        # 6. Análise de sobreposição geoespacial
        if report.property_info and report.property_info.geometry_wkt:
            report.overlap_analysis = self.geo_processor.analyze_overlaps(
                report.property_info.geometry_wkt
            )

        # 7. Calcular score de risco
        report.risk_score = self._calculate_risk_score(report)

        return report

    def _calculate_risk_score(self, report: DueDiligenceReport) -> RiskScore:
        """
        Calcula o score de risco baseado nos dados coletados.

        Lógica de risco:
        - Cada área tem um nível de risco individual
        - O risco geral é o mais alto entre as áreas
        """
        details = []
        land_tenure_risk = RiskLevel.LOW
        environmental_risk = RiskLevel.LOW
        legal_risk = RiskLevel.LOW
        labor_risk = RiskLevel.LOW

        # --- Land Tenure Risk ---
        if report.property_info:
            if not report.property_info.car_code:
                land_tenure_risk = RiskLevel.HIGH
                details.append("Imóvel sem CAR cadastrado")

            if report.property_info.status and "cancelado" in report.property_info.status.lower():
                land_tenure_risk = RiskLevel.CRITICAL
                details.append(f"CAR com status: {report.property_info.status}")

        if report.sigef_info:
            if not report.sigef_info.certified:
                if land_tenure_risk.value < RiskLevel.MEDIUM.value:
                    land_tenure_risk = RiskLevel.MEDIUM
                details.append("Imóvel sem georreferenciamento certificado no SIGEF")
        else:
            if land_tenure_risk.value < RiskLevel.MEDIUM.value:
                land_tenure_risk = RiskLevel.MEDIUM
            details.append("Nenhuma parcela SIGEF encontrada para o imóvel")

        # --- Environmental Risk ---
        if report.ibama_embargos:
            environmental_risk = RiskLevel.CRITICAL
            details.append(
                f"{len(report.ibama_embargos)} embargo(s) IBAMA encontrado(s)"
            )

        if report.overlap_analysis:
            if report.overlap_analysis.overlaps_indigenous_land:
                environmental_risk = RiskLevel.CRITICAL
                details.append(
                    f"Sobreposição com Terra Indígena: {report.overlap_analysis.indigenous_land_name}"
                )

            if report.overlap_analysis.overlaps_conservation_unit:
                if environmental_risk != RiskLevel.CRITICAL:
                    environmental_risk = RiskLevel.HIGH
                details.append(
                    f"Sobreposição com Unidade de Conservação: {report.overlap_analysis.conservation_unit_name}"
                )

            if report.overlap_analysis.overlaps_deforestation:
                if environmental_risk != RiskLevel.CRITICAL:
                    environmental_risk = RiskLevel.HIGH
                details.append(
                    f"Desmatamento detectado: {report.overlap_analysis.deforestation_area_ha} ha"
                )

        # --- Legal Risk ---
        if report.owner_info:
            if report.owner_info.situacao_cadastral and "inapta" in report.owner_info.situacao_cadastral.lower():
                legal_risk = RiskLevel.HIGH
                details.append(f"CNPJ com situação: {report.owner_info.situacao_cadastral}")
        else:
            if report.owner_info is None and not details:
                details.append("Dados do proprietário não encontrados")

        # --- Labor Risk ---
        if report.slave_labour:
            labor_risk = RiskLevel.CRITICAL
            total_workers = sum(
                (e.workers_rescued or 0) for e in report.slave_labour
            )
            details.append(
                f"Encontrado na Lista Suja do Trabalho Escravo ({total_workers} trabalhadores resgatados)"
            )

        # Overall risk = worst of all areas
        risk_levels = [land_tenure_risk, environmental_risk, legal_risk, labor_risk]
        risk_order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        overall = max(risk_levels, key=lambda r: risk_order.index(r))

        if not details:
            details.append("Nenhum alerta encontrado nas fontes consultadas")

        return RiskScore(
            overall=overall,
            land_tenure=land_tenure_risk,
            environmental=environmental_risk,
            legal=legal_risk,
            labor=labor_risk,
            details=details,
        )
