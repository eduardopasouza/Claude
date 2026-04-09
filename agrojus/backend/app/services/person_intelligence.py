"""
Serviço de Inteligência sobre Pessoas (CPF/CNPJ).

Gera um dossiê completo sobre uma pessoa, cruzando:
- Dados cadastrais (Receita Federal)
- Imóveis vinculados (CAR, SNCR)
- Embargos ambientais (IBAMA)
- Lista Suja do trabalho escravo (MTE)
- Crédito rural (SICOR/BCB)
- Notícias públicas (RSS)
"""

import uuid
from datetime import datetime, timezone

from app.collectors.receita_federal import ReceitaFederalCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.collectors.news_aggregator import NewsAggregator
from app.collectors.financial import FinancialDataCollector
from app.models.schemas import (
    PersonSearchRequest,
    PersonDossier,
    RiskScore,
    RiskLevel,
)


class PersonIntelligenceService:
    """Gera dossiê completo de uma pessoa (CPF/CNPJ)."""

    def __init__(self):
        self.receita = ReceitaFederalCollector()
        self.ibama = IBAMACollector()
        self.slave_labour = SlaveLabourCollector()
        self.news = NewsAggregator()
        self.financial = FinancialDataCollector()

    async def generate_dossier(self, request: PersonSearchRequest) -> PersonDossier:
        """Gera dossiê completo de uma pessoa."""
        validation = await self.receita.validate_cpf_cnpj(request.cpf_cnpj)

        dossier = PersonDossier(
            dossier_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            cpf_cnpj=validation["document"],
            person_type=validation["type"],
        )

        sources = []

        # 1. Dados cadastrais
        if validation["type"] == "CNPJ" and validation["valid"]:
            dossier.owner_info = await self.receita.get_cnpj(request.cpf_cnpj)
            sources.append("Receita Federal (CNPJ)")

        # 2. Embargos ambientais
        if request.include_environmental:
            dossier.ibama_embargos = await self.ibama.search_embargos_by_cpf_cnpj(
                request.cpf_cnpj
            )
            sources.append("IBAMA (Embargos)")

        # 3. Lista Suja
        if request.include_labour:
            dossier.slave_labour = await self.slave_labour.search_by_cpf_cnpj(
                request.cpf_cnpj
            )
            sources.append("MTE (Lista Suja)")

        # 4. Dados financeiros
        if request.include_financial:
            financial = await self.financial.get_rural_credits_by_cpf_cnpj(
                request.cpf_cnpj
            )
            if financial:
                from app.models.schemas import FinancialSummary
                dossier.financial_summary = FinancialSummary(
                    rural_credits=financial,
                    total_credit_amount=sum(c.amount or 0 for c in financial),
                )
                sources.append("BCB/SICOR (Credito Rural)")

        # 5. Notícias públicas
        if request.include_news:
            name = ""
            if dossier.owner_info:
                name = dossier.owner_info.razao_social or dossier.owner_info.nome_fantasia or ""
            if name:
                all_news = await self.news.fetch_all_news(limit=100)
                dossier.news_mentions = [
                    article for article in all_news
                    if name.lower() in (article.title + " " + (article.summary or "")).lower()
                ]
                sources.append("Portais de Noticias (RSS)")

        # 6. Score de risco
        dossier.risk_score = self._calculate_person_risk(dossier)
        dossier.sources_consulted = sources

        return dossier

    def _calculate_person_risk(self, dossier: PersonDossier) -> RiskScore:
        """Calcula score de risco da pessoa."""
        details = []
        land_tenure_risk = RiskLevel.LOW
        environmental_risk = RiskLevel.LOW
        legal_risk = RiskLevel.LOW
        labor_risk = RiskLevel.LOW
        financial_risk = RiskLevel.LOW

        # Cadastral
        if dossier.owner_info:
            status = (dossier.owner_info.situacao_cadastral or "").lower()
            if "inapta" in status or "baixada" in status or "suspensa" in status:
                legal_risk = RiskLevel.HIGH
                details.append(f"Situacao cadastral: {dossier.owner_info.situacao_cadastral}")

        # Embargos
        if dossier.ibama_embargos:
            environmental_risk = RiskLevel.CRITICAL
            details.append(f"{len(dossier.ibama_embargos)} embargo(s) IBAMA")

        # Lista Suja
        if dossier.slave_labour:
            labor_risk = RiskLevel.CRITICAL
            details.append("Presente na Lista Suja do Trabalho Escravo")

        if not details:
            details.append("Nenhum alerta encontrado nas fontes consultadas")

        risk_order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        overall = max(
            [land_tenure_risk, environmental_risk, legal_risk, labor_risk, financial_risk],
            key=lambda r: risk_order.index(r),
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
