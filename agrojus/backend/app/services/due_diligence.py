"""
Servico de Due Diligence Rural — v2 (PostGIS-first).

Estrategia:
1. PostGIS local (10M+ registros) como fonte primaria
2. APIs externas (Receita, DataJud, Lista Suja) como enriquecimento
3. ComplianceCalculator para MCR 2.9, EUDR e score 0-1000
"""

import logging
import uuid
from dataclasses import asdict
from datetime import datetime, timezone

from app.services.postgis_analyzer import PostGISAnalyzer, SpatialAnalysisResult
from app.services.compliance import ComplianceCalculator
from app.collectors.receita_federal import ReceitaFederalCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.collectors.datajud import DataJudCollector
from app.models.schemas import (
    DueDiligenceReport,
    PropertySearchRequest,
    CARData,
    IBAMAEmbargo,
    OverlapAnalysis,
    RiskScore,
    RiskLevel,
    FinancialSummary,
)

logger = logging.getLogger("agrojus.due_diligence")


class DueDiligenceService:
    """Servico principal de due diligence rural automatizada."""

    def __init__(self):
        self.postgis = PostGISAnalyzer()
        self.compliance = ComplianceCalculator()
        self.receita = ReceitaFederalCollector()
        self.ibama = IBAMACollector()
        self.slave_labour = SlaveLabourCollector()
        self.datajud = DataJudCollector()

    async def generate_report(self, request: PropertySearchRequest) -> DueDiligenceReport:
        """
        Gera relatorio completo de due diligence rural.

        Pipeline:
        1. Busca geometria e cruza com 12+ camadas PostGIS
        2. Enriquece com APIs externas (CNPJ, processos, lista suja)
        3. Calcula compliance MCR 2.9 / EUDR
        4. Retorna relatorio consolidado
        """
        report = DueDiligenceReport(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            persona=request.persona,
        )
        sources = []

        # ===================================================================
        # ETAPA 1: Analise PostGIS (fonte primaria)
        # ===================================================================

        spatial = None
        if request.car_code:
            logger.info("Iniciando analise PostGIS para CAR %s", request.car_code)
            spatial = self.postgis.analyze(request.car_code)

            if spatial.property_info:
                prop = spatial.property_info
                report.property_info = CARData(
                    car_code=prop.car_code,
                    status=prop.status,
                    area_total_ha=prop.area_ha,
                    municipality=prop.municipio,
                    state=prop.uf,
                    geometry_wkt=prop.geometry_geojson,
                )
                sources.append(f"PostGIS local ({spatial.layers_checked} camadas, {spatial.query_time_ms:.0f}ms)")

                # Converter cruzamentos para OverlapAnalysis (compatibilidade com PDF)
                report.overlap_analysis = self._build_overlap(spatial)

                # Converter embargos PostGIS para schema existente
                report.ibama_embargos = self._build_embargos(spatial)
                if report.ibama_embargos:
                    sources.append(f"PostGIS: {len(report.ibama_embargos)} embargo(s)")
            else:
                logger.warning("CAR %s nao encontrado no PostGIS", request.car_code)

        # ===================================================================
        # ETAPA 2: Enriquecimento via APIs externas
        # ===================================================================

        # 2A. Dados do proprietario (CNPJ)
        if request.cpf_cnpj:
            try:
                validation = await self.receita.validate_cpf_cnpj(request.cpf_cnpj)
                if validation["type"] == "CNPJ" and validation["valid"]:
                    report.owner_info = await self.receita.get_cnpj(request.cpf_cnpj)
                    sources.append("BrasilAPI (CNPJ)")
            except Exception as e:
                logger.warning("Erro consulta CNPJ: %s", e)

        # 2B. Lista Suja do Trabalho Escravo
        has_slave_labour = False
        if request.cpf_cnpj:
            try:
                report.slave_labour = await self.slave_labour.search_by_cpf_cnpj(
                    request.cpf_cnpj
                )
                has_slave_labour = bool(report.slave_labour)
                if has_slave_labour:
                    sources.append("MTE (Lista Suja)")
            except Exception as e:
                logger.warning("Erro consulta Lista Suja: %s", e)
        elif request.owner_name:
            try:
                report.slave_labour = await self.slave_labour.search_by_name(
                    request.owner_name
                )
                has_slave_labour = bool(report.slave_labour)
            except Exception as e:
                logger.warning("Erro consulta Lista Suja por nome: %s", e)

        # 2C. Processos judiciais (DataJud/CNJ)
        if request.cpf_cnpj:
            try:
                report.lawsuits = await self.datajud.search_by_cpf_cnpj(
                    request.cpf_cnpj
                )
                if report.lawsuits:
                    sources.append(f"DataJud/CNJ ({len(report.lawsuits)} processos)")
            except Exception as e:
                logger.warning("Erro consulta DataJud: %s", e)

        # ===================================================================
        # ETAPA 3: Compliance e Risk Score
        # ===================================================================

        if spatial and spatial.property_info:
            compliance_result = self.compliance.calculate(
                spatial,
                has_slave_labour=has_slave_labour,
            )

            # Mapear compliance para risk score existente
            report.risk_score = self._build_risk_score(spatial, compliance_result, report)

            # Guardar compliance completo nos raw_data para o frontend
            report.compliance = {
                "mcr_29": {
                    "passed": compliance_result.mcr_passed,
                    "score": compliance_result.mcr_score,
                    "items": [asdict(item) for item in compliance_result.mcr_items],
                },
                "eudr": {
                    "passed": compliance_result.eudr_passed,
                    "score": compliance_result.eudr_score,
                    "items": [asdict(item) for item in compliance_result.eudr_items],
                },
                "overall_score": compliance_result.overall_score,
                "risk_level": compliance_result.risk_level,
                "summary": compliance_result.summary,
            }

            # Guardar dados espaciais detalhados
            report.spatial_analysis = self._build_spatial_summary(spatial)

            sources.append(f"Compliance: {compliance_result.overall_score}/1000 ({compliance_result.risk_level})")
        else:
            report.risk_score = self._calculate_risk_score_fallback(report)

        # ===================================================================
        # ETAPA 4: Enriquecimentos opcionais (lentos)
        # ===================================================================

        # 4A. Earth Engine (satelite) — ~20s
        if request.include_satellite and spatial and spatial.property_info:
            try:
                from app.services.earth_engine import analyze_property_satellite
                logger.info("Iniciando analise Earth Engine para CAR %s", request.car_code)
                report.satellite_data = analyze_property_satellite(
                    spatial.property_info.geometry_geojson
                )
                if report.satellite_data.get("available"):
                    sources.append(f"Earth Engine ({report.satellite_data.get('query_time_ms', 0):.0f}ms)")
            except Exception as e:
                logger.warning("Earth Engine error: %s", e)
                report.satellite_data = {"available": False, "error": str(e)}

        # 4B. MapBiomas Alerta GraphQL (tempo real) — ~3s
        if request.include_realtime_alerts and request.car_code:
            try:
                from app.services.mapbiomas_alerta import query_alerts_by_car
                logger.info("Consultando MapBiomas GraphQL para CAR %s", request.car_code)
                report.mapbiomas_realtime = query_alerts_by_car(request.car_code)
                if report.mapbiomas_realtime.get("available"):
                    n = report.mapbiomas_realtime.get("total_count", 0)
                    sources.append(f"MapBiomas GraphQL ({n} alertas)")
            except Exception as e:
                logger.warning("MapBiomas GraphQL error: %s", e)
                report.mapbiomas_realtime = {"available": False, "error": str(e)}

        report.sources_consulted = sources
        return report

    # ------------------------------------------------------------------
    # Conversores PostGIS -> schemas existentes
    # ------------------------------------------------------------------

    @staticmethod
    def _build_overlap(spatial: SpatialAnalysisResult) -> OverlapAnalysis:
        """Converte resultado PostGIS para OverlapAnalysis (schema existente)."""
        oa = OverlapAnalysis()

        if spatial.terras_indigenas:
            oa.overlaps_indigenous_land = True
            oa.indigenous_land_name = ", ".join(h.name for h in spatial.terras_indigenas)
            oa.indigenous_land_area_overlap_ha = sum(
                h.overlap_area_ha for h in spatial.terras_indigenas
            )

        if spatial.unidades_conservacao:
            oa.overlaps_conservation_unit = True
            oa.conservation_unit_name = ", ".join(h.name for h in spatial.unidades_conservacao)
            oa.conservation_unit_category = ", ".join(
                h.details.get("categoria", "") for h in spatial.unidades_conservacao
            )

        if spatial.embargos_icmbio or spatial.embargos_ibama:
            oa.overlaps_embargo = True
            n = len(spatial.embargos_icmbio) + len(spatial.embargos_ibama)
            oa.embargo_details = f"{n} embargo(s) sobrepostos ao imovel"

        if spatial.prodes_desmatamento or spatial.deter_alertas or spatial.mapbiomas_alertas:
            oa.overlaps_deforestation = True
            total_ha = sum(h.overlap_area_ha for h in spatial.prodes_desmatamento)
            total_ha += sum(h.overlap_area_ha for h in spatial.deter_alertas)
            total_ha += sum(h.overlap_area_ha for h in spatial.mapbiomas_alertas)
            oa.deforestation_area_ha = round(total_ha, 2)

        return oa

    @staticmethod
    def _build_embargos(spatial: SpatialAnalysisResult) -> list[IBAMAEmbargo]:
        """Converte embargos PostGIS para lista de IBAMAEmbargo."""
        embargos = []

        for h in spatial.embargos_icmbio:
            embargos.append(IBAMAEmbargo(
                auto_infracao=h.details.get("auto_infracao"),
                cpf_cnpj=h.details.get("cpf_cnpj"),
                nome=h.name,
                municipio=h.details.get("municipio"),
                uf=h.details.get("uf"),
                data_embargo=h.date,
                descricao=h.details.get("descricao"),
                status="Embargo ICMBio",
            ))

        for h in spatial.embargos_ibama:
            embargos.append(IBAMAEmbargo(
                alert_type=h.details.get("tipo"),
                cpf_cnpj=h.details.get("cpf_cnpj"),
                nome=h.name,
                area_embargada_ha=h.details.get("area_ha"),
                data_embargo=h.date,
                descricao=h.name,
                status="Embargo IBAMA",
            ))

        return embargos

    @staticmethod
    def _build_spatial_summary(spatial: SpatialAnalysisResult) -> dict:
        """Resume dados espaciais para incluir no JSON de resposta."""
        return {
            "property": {
                "car_code": spatial.car_code,
                "municipio": spatial.property_info.municipio if spatial.property_info else "",
                "uf": spatial.property_info.uf if spatial.property_info else "",
                "area_ha": spatial.property_info.area_ha if spatial.property_info else 0,
            },
            "terras_indigenas": [
                {"nome": h.name, "overlap_ha": h.overlap_area_ha, **h.details}
                for h in spatial.terras_indigenas
            ],
            "unidades_conservacao": [
                {"nome": h.name, "overlap_ha": h.overlap_area_ha, **h.details}
                for h in spatial.unidades_conservacao
            ],
            "embargos": [
                {"nome": h.name, "data": h.date, **h.details}
                for h in spatial.embargos_icmbio + spatial.embargos_ibama
            ],
            "desmatamento": {
                "prodes": [
                    {"ano": h.details.get("year"), "overlap_ha": h.overlap_area_ha}
                    for h in spatial.prodes_desmatamento
                ],
                "deter": [
                    {"classe": h.details.get("classe"), "data": h.date, "overlap_ha": h.overlap_area_ha}
                    for h in spatial.deter_alertas
                ],
                "mapbiomas": [
                    {"ano": h.details.get("year"), "bioma": h.details.get("bioma"),
                     "overlap_ha": h.overlap_area_ha}
                    for h in spatial.mapbiomas_alertas
                ],
            },
            "autos_icmbio": [
                {"nome": h.name, "data": h.date, **h.details}
                for h in spatial.autos_icmbio
            ],
            "credito_rural": [
                {"programa": h.details.get("programa"), "valor": h.details.get("valor"),
                 "ano": h.details.get("ano")}
                for h in spatial.credito_rural
            ],
            "infraestrutura": {
                "armazens": [
                    {"nome": h.name, "distancia_km": h.distance_km}
                    for h in spatial.armazens_proximos
                ],
                "frigorificos": [
                    {"nome": h.name, "distancia_km": h.distance_km}
                    for h in spatial.frigorificos_proximos
                ],
                "rodovias": [
                    {"nome": h.name, "distancia_km": h.distance_km}
                    for h in spatial.rodovias_proximas
                ],
                "portos": [
                    {"nome": h.name, "distancia_km": h.distance_km}
                    for h in spatial.portos_proximos
                ],
            },
            "flags": {
                "prodes_pos_2019": spatial.has_prodes_post_2019,
                "prodes_pos_2020": spatial.has_prodes_post_2020,
                "embargo_ativo": spatial.has_embargo_ativo,
                "terra_indigena": spatial.has_terra_indigena,
                "uc_protecao_integral": spatial.has_uc_protecao_integral,
            },
            "metadata": {
                "layers_checked": spatial.layers_checked,
                "layers_with_hits": spatial.layers_with_hits,
                "query_time_ms": spatial.query_time_ms,
                "errors": spatial.errors,
            },
        }

    # ------------------------------------------------------------------
    # Risk Score
    # ------------------------------------------------------------------

    def _build_risk_score(
        self,
        spatial: SpatialAnalysisResult,
        compliance_result,
        report: DueDiligenceReport,
    ) -> RiskScore:
        """Constroi RiskScore baseado no PostGIS + compliance."""
        details = []
        land_tenure = RiskLevel.LOW
        environmental = RiskLevel.LOW
        legal = RiskLevel.LOW
        labor = RiskLevel.LOW
        financial = RiskLevel.LOW

        # Fundiario
        prop = spatial.property_info
        if prop:
            if prop.status not in ("AT", "ATV", "ATIVO"):
                land_tenure = RiskLevel.HIGH
                details.append(f"CAR com status: {prop.status}")
            if spatial.has_terra_indigena:
                land_tenure = RiskLevel.CRITICAL
                nomes = ", ".join(h.name for h in spatial.terras_indigenas)
                details.append(f"Sobreposicao com TI: {nomes}")

        # Ambiental
        if spatial.has_embargo_ativo:
            environmental = RiskLevel.CRITICAL
            n = len(spatial.embargos_icmbio) + len(spatial.embargos_ibama)
            details.append(f"{n} embargo(s) ativo(s)")
        if spatial.has_prodes_post_2019:
            environmental = max(environmental, RiskLevel.HIGH, key=lambda r: self._risk_severity(r))
            details.append("Desmatamento PRODES pos-2019")
        n_alertas = len(spatial.mapbiomas_alertas) + len(spatial.deter_alertas)
        if n_alertas > 0:
            environmental = max(environmental, RiskLevel.MEDIUM, key=lambda r: self._risk_severity(r))
            details.append(f"{n_alertas} alerta(s) de desmatamento (DETER/MapBiomas)")
        if spatial.has_uc_protecao_integral:
            environmental = max(environmental, RiskLevel.HIGH, key=lambda r: self._risk_severity(r))
            nomes = ", ".join(h.name for h in spatial.unidades_conservacao)
            details.append(f"Sobreposicao com UC: {nomes}")

        # Juridico
        if report.lawsuits:
            n = len(report.lawsuits)
            if n >= 5:
                legal = RiskLevel.HIGH
            elif n >= 1:
                legal = RiskLevel.MEDIUM
            details.append(f"{n} processo(s) judicial(is)")

        if report.owner_info:
            status = (report.owner_info.situacao_cadastral or "").lower()
            if any(kw in status for kw in ("inapta", "baixada", "suspensa")):
                legal = RiskLevel.HIGH
                details.append(f"CNPJ: {report.owner_info.situacao_cadastral}")

        # Trabalhista
        if report.slave_labour:
            labor = RiskLevel.CRITICAL
            total = sum((e.workers_rescued or 0) for e in report.slave_labour)
            details.append(f"Lista Suja ({total} trabalhadores)")

        # Compliance
        details.append(f"MCR 2.9: {'APROVADO' if compliance_result.mcr_passed else 'REPROVADO'} ({compliance_result.mcr_score}/100)")
        details.append(f"EUDR: {'CONFORME' if compliance_result.eudr_passed else 'NAO CONFORME'} ({compliance_result.eudr_score}/100)")
        details.append(f"Score geral: {compliance_result.overall_score}/1000")

        # Credito rural do PostGIS
        if spatial.credito_rural:
            total_credito = sum(h.details.get("valor", 0) or 0 for h in spatial.credito_rural)
            if total_credito > 0:
                details.append(f"Credito rural georreferenciado: R$ {total_credito:,.2f}")

        overall = max(
            [land_tenure, environmental, legal, labor, financial],
            key=lambda r: self._risk_severity(r),
        )

        return RiskScore(
            overall=overall,
            land_tenure=land_tenure,
            environmental=environmental,
            legal=legal,
            labor=labor,
            financial=financial,
            details=details,
        )

    @staticmethod
    def _risk_severity(level: RiskLevel) -> int:
        return {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2, RiskLevel.CRITICAL: 3}[level]

    def _calculate_risk_score_fallback(self, report: DueDiligenceReport) -> RiskScore:
        """Fallback sem PostGIS (CAR nao fornecido)."""
        details = ["Analise sem CAR — dados espaciais indisponiveis"]
        legal = RiskLevel.LOW
        labor = RiskLevel.LOW

        if report.lawsuits:
            n = len(report.lawsuits)
            legal = RiskLevel.HIGH if n >= 5 else RiskLevel.MEDIUM if n >= 1 else RiskLevel.LOW
            details.append(f"{n} processo(s) judicial(is)")

        if report.slave_labour:
            labor = RiskLevel.CRITICAL
            details.append("Na Lista Suja")

        overall = max([legal, labor], key=lambda r: self._risk_severity(r))
        return RiskScore(
            overall=overall,
            land_tenure=RiskLevel.LOW,
            environmental=RiskLevel.LOW,
            legal=legal,
            labor=labor,
            financial=RiskLevel.LOW,
            details=details,
        )
