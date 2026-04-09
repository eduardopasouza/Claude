"""
Serviço de Due Diligence Rural - Versão Expandida.

Aceita qualquer identificador de imóvel (CAR, matrícula, SNCR, NIRF, CCIR,
ITR, SIGEF, coordenadas) e gera relatório completo cruzando todas as fontes.

Adapta o nível de detalhe conforme o perfil do solicitante (persona):
- Comprador: foco em regularidade, ônus, preço de mercado
- Advogado: foco em processos, certidões, sobreposições
- Agropecuarista: foco em produção, crédito, clima
- Investidor: foco em risco, retorno, valuation
"""

import uuid
from datetime import datetime, timezone

from app.collectors.sicar import SICARCollector
from app.collectors.sigef import SIGEFCollector
from app.collectors.receita_federal import ReceitaFederalCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.collectors.financial import FinancialDataCollector
from app.collectors.datajud import DataJudCollector
from app.processors.geospatial import GeospatialProcessor
from app.models.schemas import (
    DueDiligenceReport,
    PropertySearchRequest,
    RiskScore,
    RiskLevel,
    PersonaType,
    FinancialSummary,
)


class DueDiligenceService:
    """Serviço principal de due diligence rural automatizada."""

    def __init__(self):
        self.sicar = SICARCollector()
        self.sigef = SIGEFCollector()
        self.receita = ReceitaFederalCollector()
        self.ibama = IBAMACollector()
        self.slave_labour = SlaveLabourCollector()
        self.financial = FinancialDataCollector()
        self.datajud = DataJudCollector()
        self.geo_processor = GeospatialProcessor()

    async def generate_report(self, request: PropertySearchRequest) -> DueDiligenceReport:
        """
        Gera relatório completo de due diligence rural.

        Estratégia de resolução:
        1. Tenta usar o identificador mais completo fornecido
        2. Cruza informações para descobrir identificadores faltantes
        3. Busca em todas as fontes usando todos os identificadores disponíveis
        """
        report = DueDiligenceReport(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            persona=request.persona,
        )

        sources = []

        # === ETAPA 1: Resolução do imóvel ===

        # 1A. CAR
        if request.car_code:
            report.property_info = await self.sicar.get_property_by_car(request.car_code)
            geometry = await self.sicar.get_geometry_wfs(request.car_code)
            if geometry and report.property_info:
                report.property_info.geometry_wkt = geometry
            sources.append("SICAR/CAR")

        # 1B. SIGEF (por código ou coordenadas)
        if request.sigef_code:
            report.sigef_info = await self.sigef.get_parcel_by_code(request.sigef_code)
            sources.append("SIGEF/INCRA")
        elif request.latitude and request.longitude:
            parcels = await self.sigef.search_parcels_by_location(
                request.latitude, request.longitude
            )
            if parcels:
                report.sigef_info = parcels[0]
                sources.append("SIGEF/INCRA")

        # 1C. Matrícula (seria via scraping do cartório - placeholder)
        if request.matricula:
            from app.models.schemas import MatriculaData
            report.matricula_info = MatriculaData(
                matricula_number=request.matricula,
                # Em produção: scraping do sistema do cartório ou ONR
            )
            sources.append("Cartorio de RI (matricula)")

        # 1D. SNCR/INCRA
        if request.sncr_code or request.nirf:
            from app.models.schemas import SNCRData
            report.sncr_info = SNCRData(
                sncr_code=request.sncr_code,
                nirf=request.nirf,
                # Em produção: consulta ao SNCR/CNIR
            )
            sources.append("SNCR/INCRA")

        # 1E. CCIR
        if request.ccir:
            from app.models.schemas import CCIRData
            report.ccir_info = CCIRData(
                ccir_number=request.ccir,
                # Em produção: consulta ao SNCR para validar CCIR
            )
            sources.append("CCIR/INCRA")

        # 1F. ITR
        if request.itr_number or request.nirf:
            from app.models.schemas import ITRData
            report.itr_info = ITRData(
                nirf=request.nirf or request.itr_number,
                # Em produção: consulta à Receita Federal
            )
            sources.append("ITR/Receita Federal")

        # 1G. Busca por município (se nenhum identificador direto)
        if not report.property_info and request.municipality and request.state:
            results = await self.sicar.search_by_municipality(
                request.municipality, request.state
            )
            if results:
                report.property_info = results[0]
                sources.append("SICAR/CAR (por municipio)")

        # === ETAPA 2: Dados do proprietário ===

        if request.cpf_cnpj:
            validation = await self.receita.validate_cpf_cnpj(request.cpf_cnpj)
            if validation["type"] == "CNPJ" and validation["valid"]:
                report.owner_info = await self.receita.get_cnpj(request.cpf_cnpj)
                sources.append("Receita Federal (CNPJ)")

        # === ETAPA 3: Alertas ambientais ===

        if request.cpf_cnpj:
            report.ibama_embargos = await self.ibama.search_embargos_by_cpf_cnpj(
                request.cpf_cnpj
            )
        elif report.property_info and report.property_info.municipality:
            state = report.property_info.state or request.state or ""
            report.ibama_embargos = await self.ibama.search_embargos_by_municipality(
                report.property_info.municipality, state
            )
        if report.ibama_embargos:
            sources.append("IBAMA (Embargos)")

        # === ETAPA 4: Lista Suja ===

        if request.cpf_cnpj:
            report.slave_labour = await self.slave_labour.search_by_cpf_cnpj(
                request.cpf_cnpj
            )
        elif request.owner_name:
            report.slave_labour = await self.slave_labour.search_by_name(
                request.owner_name
            )
        if report.slave_labour:
            sources.append("MTE (Lista Suja)")

        # === ETAPA 4B: Processos judiciais (DataJud/CNJ) ===

        if request.cpf_cnpj:
            report.lawsuits = await self.datajud.search_by_cpf_cnpj(
                request.cpf_cnpj
            )
            if report.lawsuits:
                sources.append("DataJud/CNJ (Processos Judiciais)")

        # === ETAPA 5: Análise geoespacial ===

        if report.property_info and report.property_info.geometry_wkt:
            report.overlap_analysis = self.geo_processor.analyze_overlaps(
                report.property_info.geometry_wkt
            )
            sources.append("Analise Geoespacial")

        # === ETAPA 6: Dados financeiros ===

        municipality_code = None
        if report.property_info and report.property_info.municipality:
            # In production, would resolve municipality to IBGE code
            pass

        if request.cpf_cnpj:
            credits = await self.financial.get_rural_credits_by_cpf_cnpj(request.cpf_cnpj)
            if credits:
                report.financial_summary = FinancialSummary(
                    rural_credits=credits,
                    total_credit_amount=sum(c.amount or 0 for c in credits),
                )
                sources.append("BCB/SICOR (Credito Rural)")

        # Try to get land prices for the region
        state = request.state or (report.property_info.state if report.property_info else None)
        municipality = request.municipality or (report.property_info.municipality if report.property_info else None)
        if state:
            land_prices = await self.financial.get_land_prices(state, municipality)
            if land_prices:
                if not report.financial_summary:
                    report.financial_summary = FinancialSummary()
                report.financial_summary.land_prices = land_prices
                if land_prices:
                    avg = sum(p.price_per_ha or 0 for p in land_prices) / len(land_prices)
                    report.financial_summary.avg_land_price_per_ha = avg
                sources.append("Precos de Terras")

        # === ETAPA 7: Score de risco ===

        report.risk_score = self._calculate_risk_score(report)
        report.sources_consulted = sources

        return report

    @staticmethod
    def _risk_severity(level: RiskLevel) -> int:
        """Returns numeric severity for risk comparison (higher = worse)."""
        return {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2, RiskLevel.CRITICAL: 3}[level]

    def _escalate(self, current: RiskLevel, minimum: RiskLevel) -> RiskLevel:
        """Escalate risk level to at least `minimum`, never downgrade."""
        if self._risk_severity(current) < self._risk_severity(minimum):
            return minimum
        return current

    def _calculate_risk_score(self, report: DueDiligenceReport) -> RiskScore:
        """Calcula score de risco baseado em todos os dados coletados."""
        details = []
        land_tenure_risk = RiskLevel.LOW
        environmental_risk = RiskLevel.LOW
        legal_risk = RiskLevel.LOW
        labor_risk = RiskLevel.LOW
        financial_risk = RiskLevel.LOW

        # --- Regularidade Fundiária ---
        identifiers_found = 0
        identifiers_expected = 4  # CAR, SIGEF, matrícula, CCIR

        if report.property_info and report.property_info.car_code:
            identifiers_found += 1
            if report.property_info.status:
                status = report.property_info.status.lower()
                if "cancelado" in status or "suspenso" in status:
                    land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.CRITICAL)
                    details.append(f"CAR com status: {report.property_info.status}")
                elif "pendente" in status:
                    land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.MEDIUM)
                    details.append(f"CAR com status pendente")
        else:
            details.append("Imovel sem CAR cadastrado ou nao encontrado")
            land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.HIGH)

        if report.sigef_info:
            identifiers_found += 1
            if not report.sigef_info.certified:
                land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.MEDIUM)
                details.append("Georreferenciamento SIGEF nao certificado")
        else:
            details.append("Nenhuma parcela SIGEF encontrada")

        if report.matricula_info and report.matricula_info.matricula_number:
            identifiers_found += 1
            if report.matricula_info.has_onus:
                land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.HIGH)
                details.append(f"Matricula com onus/gravame: {report.matricula_info.onus_description or 'verificar'}")

        if report.ccir_info and report.ccir_info.ccir_number:
            identifiers_found += 1
            if report.ccir_info.valid is False:
                land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.HIGH)
                details.append("CCIR vencido ou invalido")

        if report.itr_info:
            if report.itr_info.status_pagamento and "atraso" in (report.itr_info.status_pagamento or "").lower():
                land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.MEDIUM)
                details.append("ITR com pagamento em atraso")

        # Penalizar falta de identificadores
        if identifiers_found < 2:
            details.append(f"Apenas {identifiers_found} de {identifiers_expected} identificadores encontrados - documentacao incompleta")
            land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.MEDIUM)

        # --- Ambiental ---
        if report.ibama_embargos:
            environmental_risk = self._escalate(environmental_risk, RiskLevel.CRITICAL)
            details.append(f"{len(report.ibama_embargos)} embargo(s) IBAMA encontrado(s)")

        if report.overlap_analysis:
            if report.overlap_analysis.overlaps_indigenous_land:
                environmental_risk = self._escalate(environmental_risk, RiskLevel.CRITICAL)
                details.append(f"Sobreposicao com Terra Indigena: {report.overlap_analysis.indigenous_land_name}")
            if report.overlap_analysis.overlaps_conservation_unit:
                environmental_risk = self._escalate(environmental_risk, RiskLevel.HIGH)
                details.append(f"Sobreposicao com UC: {report.overlap_analysis.conservation_unit_name}")
            if report.overlap_analysis.overlaps_quilombo:
                environmental_risk = self._escalate(environmental_risk, RiskLevel.HIGH)
                details.append(f"Sobreposicao com Quilombo: {report.overlap_analysis.quilombo_name}")
            if report.overlap_analysis.overlaps_settlement:
                environmental_risk = self._escalate(environmental_risk, RiskLevel.HIGH)
                details.append(f"Sobreposicao com Assentamento: {report.overlap_analysis.settlement_name}")
            if report.overlap_analysis.overlaps_deforestation:
                environmental_risk = self._escalate(environmental_risk, RiskLevel.HIGH)
                details.append(f"Desmatamento detectado: {report.overlap_analysis.deforestation_area_ha} ha")

        # --- Jurídico ---
        if report.owner_info:
            status = (report.owner_info.situacao_cadastral or "").lower()
            if "inapta" in status or "baixada" in status or "suspensa" in status:
                legal_risk = self._escalate(legal_risk, RiskLevel.HIGH)
                details.append(f"CNPJ com situacao: {report.owner_info.situacao_cadastral}")

        # --- Processos Judiciais ---
        if report.lawsuits:
            lawsuit_count = len(report.lawsuits)
            if lawsuit_count >= 5:
                legal_risk = self._escalate(legal_risk, RiskLevel.HIGH)
            elif lawsuit_count >= 1:
                legal_risk = self._escalate(legal_risk, RiskLevel.MEDIUM)
            details.append(f"{lawsuit_count} processo(s) judicial(is) encontrado(s) no DataJud")

            # Check for specific concerning subjects
            for lawsuit in report.lawsuits:
                for subject in lawsuit.subjects:
                    subject_lower = subject.lower()
                    if any(kw in subject_lower for kw in ["ambiental", "desmatamento", "embargo"]):
                        environmental_risk = self._escalate(environmental_risk, RiskLevel.HIGH)
                        details.append(f"Processo ambiental: {lawsuit.case_number}")
                        break
                    if any(kw in subject_lower for kw in ["possessoria", "usucapiao", "reintegracao"]):
                        land_tenure_risk = self._escalate(land_tenure_risk, RiskLevel.HIGH)
                        details.append(f"Disputa possessoria: {lawsuit.case_number}")
                        break

        # --- Trabalhista ---
        if report.slave_labour:
            labor_risk = RiskLevel.CRITICAL
            total_workers = sum((e.workers_rescued or 0) for e in report.slave_labour)
            details.append(f"Lista Suja do Trabalho Escravo ({total_workers} trabalhadores resgatados)")

        # --- Financeiro ---
        if report.financial_summary:
            if report.financial_summary.total_credit_amount and report.financial_summary.total_credit_amount > 0:
                details.append(f"Credito rural total: R$ {report.financial_summary.total_credit_amount:,.2f}")
            if report.financial_summary.avg_land_price_per_ha:
                details.append(f"Preco medio da terra na regiao: R$ {report.financial_summary.avg_land_price_per_ha:,.2f}/ha")

        if not details:
            details.append("Nenhum alerta encontrado nas fontes consultadas")

        overall = max(
            [land_tenure_risk, environmental_risk, legal_risk, labor_risk, financial_risk],
            key=lambda r: self._risk_severity(r),
        )

        return RiskScore(
            overall=overall,
            land_tenure=land_tenure_risk,
            environmental=environmental_risk,
            legal=legal_risk,
            labor=labor_risk,
            financial=financial_risk,
            details=details,
        )
