"""Testes do cálculo de score de risco."""

import pytest
from app.services.due_diligence import DueDiligenceService
from app.models.schemas import (
    DueDiligenceReport, CARData, SIGEFData, CNPJData,
    IBAMAEmbargo, SlaveLabourEntry, OverlapAnalysis,
    RiskLevel, LawsuitRecord,
)
from datetime import datetime, timezone


class TestRiskScore:
    def setup_method(self):
        self.service = DueDiligenceService()

    def _base_report(self) -> DueDiligenceReport:
        return DueDiligenceReport(
            report_id="test-123",
            generated_at=datetime.now(timezone.utc),
        )

    def test_clean_property_low_risk(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.sigef_info = SIGEFData(parcel_code="P123", certified=True)

        score = self.service._calculate_risk_score(report)
        assert score.land_tenure == RiskLevel.LOW

    def test_no_car_high_risk(self):
        report = self._base_report()
        # No property_info at all

        score = self.service._calculate_risk_score(report)
        assert score.land_tenure == RiskLevel.HIGH
        assert "sem CAR" in " ".join(score.details).lower() or "nao encontrado" in " ".join(score.details).lower()

    def test_cancelled_car_critical_risk(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Cancelado")

        score = self.service._calculate_risk_score(report)
        assert score.land_tenure == RiskLevel.CRITICAL

    def test_ibama_embargo_critical_environmental(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.ibama_embargos = [
            IBAMAEmbargo(auto_infracao="123", area_embargada_ha=50.0)
        ]

        score = self.service._calculate_risk_score(report)
        assert score.environmental == RiskLevel.CRITICAL

    def test_slave_labour_critical(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.slave_labour = [
            SlaveLabourEntry(employer_name="Test", workers_rescued=10)
        ]

        score = self.service._calculate_risk_score(report)
        assert score.labor == RiskLevel.CRITICAL

    def test_indigenous_land_overlap_critical(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.overlap_analysis = OverlapAnalysis(
            overlaps_indigenous_land=True,
            indigenous_land_name="TI Xingu",
        )

        score = self.service._calculate_risk_score(report)
        assert score.environmental == RiskLevel.CRITICAL

    def test_lawsuits_increase_legal_risk(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.lawsuits = [
            LawsuitRecord(case_number=f"000{i}", tribunal="TRF1", subjects=["Cível"])
            for i in range(5)
        ]

        score = self.service._calculate_risk_score(report)
        assert score.legal == RiskLevel.HIGH

    def test_environmental_lawsuit_increases_env_risk(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.lawsuits = [
            LawsuitRecord(
                case_number="0001",
                tribunal="TRF1",
                subjects=["Dano Ambiental"],
            )
        ]

        score = self.service._calculate_risk_score(report)
        assert score.environmental == RiskLevel.HIGH

    def test_overall_is_worst(self):
        report = self._base_report()
        report.property_info = CARData(car_code="MT-1234", status="Ativo")
        report.slave_labour = [
            SlaveLabourEntry(employer_name="Test", workers_rescued=5)
        ]
        # labor = CRITICAL, everything else lower

        score = self.service._calculate_risk_score(report)
        assert score.overall == RiskLevel.CRITICAL
