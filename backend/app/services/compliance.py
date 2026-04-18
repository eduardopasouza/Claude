"""
Compliance Calculator — MCR 2.9, EUDR e Score Geral.

Recebe o resultado da analise espacial (SpatialAnalysisResult)
e calcula checklists de compliance e score consolidado 0-1000.

MCR 2.9 (Manual de Credito Rural, Res. BCB 140/2021):
  - CAR ativo e regular
  - Sem desmatamento ilegal pos-2019 (PRODES)
  - Sem embargo IBAMA/ICMBio ativo
  - Sem sobreposicao com TI ou UC de Protecao Integral
  - Sem inclusao na Lista Suja do Trabalho Escravo

EUDR (EU Deforestation Regulation, 2023/1115):
  - Sem desmatamento pos-31/12/2020 (qualquer fonte)
  - Sem degradacao florestal pos-31/12/2020
  - Producao em conformidade com legislacao nacional
  - Rastreabilidade de geolocalizacao comprovada
"""

from dataclasses import dataclass, field
from typing import Optional

from app.services.postgis_analyzer import SpatialAnalysisResult


# ---------------------------------------------------------------------------
# Resultado de compliance
# ---------------------------------------------------------------------------

@dataclass
class ChecklistItem:
    """Um item individual de checklist."""
    code: str           # Ex: "MCR-01"
    description: str    # Ex: "CAR ativo e regular"
    passed: bool = False
    details: str = ""   # Detalhes sobre falha ou sucesso
    weight: float = 1.0 # Peso no score (maior = mais impacto)


@dataclass
class ComplianceResult:
    """Resultado consolidado de compliance."""
    # MCR 2.9
    mcr_items: list[ChecklistItem] = field(default_factory=list)
    mcr_passed: bool = False
    mcr_score: int = 0       # 0-100

    # EUDR
    eudr_items: list[ChecklistItem] = field(default_factory=list)
    eudr_passed: bool = False
    eudr_score: int = 0      # 0-100

    # Score geral
    overall_score: int = 0   # 0-1000
    risk_level: str = "INDETERMINADO"  # BAIXO, MEDIO, ALTO, CRITICO
    summary: str = ""


# ---------------------------------------------------------------------------
# Calculator
# ---------------------------------------------------------------------------

class ComplianceCalculator:
    """Calcula compliance MCR 2.9, EUDR e score geral."""

    def calculate(
        self,
        spatial: SpatialAnalysisResult,
        has_slave_labour: bool = False,
        car_status: Optional[str] = None,
    ) -> ComplianceResult:
        """
        Calcula todas as metricas de compliance.

        Args:
            spatial: Resultado da analise PostGIS
            has_slave_labour: Se o proprietario esta na Lista Suja
            car_status: Status do CAR (AT=ativo, PE=pendente, CA=cancelado, SU=suspenso)
        """
        result = ComplianceResult()

        # Usar status do PostGIS se nao fornecido
        if car_status is None and spatial.property_info:
            car_status = spatial.property_info.status

        result.mcr_items = self._check_mcr(spatial, has_slave_labour, car_status)
        result.mcr_passed = all(item.passed for item in result.mcr_items)
        result.mcr_score = self._weighted_score(result.mcr_items)

        result.eudr_items = self._check_eudr(spatial, car_status)
        result.eudr_passed = all(item.passed for item in result.eudr_items)
        result.eudr_score = self._weighted_score(result.eudr_items)

        result.overall_score = self._calculate_overall(spatial, result, has_slave_labour)
        result.risk_level = self._classify_risk(result.overall_score)
        result.summary = self._generate_summary(result, spatial)

        return result

    # ------------------------------------------------------------------
    # MCR 2.9
    # ------------------------------------------------------------------

    def _check_mcr(
        self,
        spatial: SpatialAnalysisResult,
        has_slave_labour: bool,
        car_status: Optional[str],
    ) -> list[ChecklistItem]:
        items = []

        # MCR-01: CAR ativo e regular
        car_ok = car_status in ("AT", "ATV", "ATIVO")
        items.append(ChecklistItem(
            code="MCR-01",
            description="CAR ativo e regular",
            passed=car_ok,
            details=f"Status: {car_status or 'N/A'}",
            weight=2.0,
        ))

        # MCR-02: Sem PRODES pos-2019
        prodes_ok = not spatial.has_prodes_post_2019
        prodes_detail = "Nenhum desmatamento PRODES pos-2019"
        if not prodes_ok:
            years = [h.details.get("year") for h in spatial.prodes_desmatamento if h.details.get("year", 0) >= 2019]
            prodes_detail = f"Desmatamento PRODES detectado: {years}"
        items.append(ChecklistItem(
            code="MCR-02",
            description="Sem desmatamento ilegal PRODES pos-2019",
            passed=prodes_ok,
            details=prodes_detail,
            weight=3.0,
        ))

        # MCR-03: Sem embargo ativo
        embargo_ok = not spatial.has_embargo_ativo
        embargo_detail = "Nenhum embargo ativo"
        if not embargo_ok:
            n_icmbio = len(spatial.embargos_icmbio)
            n_ibama = len(spatial.embargos_ibama)
            embargo_detail = f"{n_icmbio} embargo(s) ICMBio, {n_ibama} embargo(s) IBAMA"
        items.append(ChecklistItem(
            code="MCR-03",
            description="Sem embargo IBAMA/ICMBio ativo",
            passed=embargo_ok,
            details=embargo_detail,
            weight=3.0,
        ))

        # MCR-04: Sem sobreposicao TI
        ti_ok = not spatial.has_terra_indigena
        ti_detail = "Sem sobreposicao com Terra Indigena"
        if not ti_ok:
            nomes = [h.name for h in spatial.terras_indigenas]
            ti_detail = f"Sobreposicao com TI: {', '.join(nomes)}"
        items.append(ChecklistItem(
            code="MCR-04",
            description="Sem sobreposicao com Terra Indigena",
            passed=ti_ok,
            details=ti_detail,
            weight=3.0,
        ))

        # MCR-05: Sem sobreposicao UC Protecao Integral
        uc_ok = not spatial.has_uc_protecao_integral
        uc_detail = "Sem sobreposicao com UC de Protecao Integral"
        if not uc_ok:
            nomes = [
                h.name for h in spatial.unidades_conservacao
                if h.details.get("grupo") == "Proteção Integral"
            ]
            uc_detail = f"Sobreposicao com UC PI: {', '.join(nomes)}"
        items.append(ChecklistItem(
            code="MCR-05",
            description="Sem sobreposicao com UC de Protecao Integral",
            passed=uc_ok,
            details=uc_detail,
            weight=2.0,
        ))

        # MCR-06: Fora da Lista Suja
        items.append(ChecklistItem(
            code="MCR-06",
            description="Sem inclusao na Lista Suja do Trabalho Escravo",
            passed=not has_slave_labour,
            details="Na Lista Suja" if has_slave_labour else "Fora da Lista Suja",
            weight=3.0,
        ))

        return items

    # ------------------------------------------------------------------
    # EUDR
    # ------------------------------------------------------------------

    def _check_eudr(
        self,
        spatial: SpatialAnalysisResult,
        car_status: Optional[str],
    ) -> list[ChecklistItem]:
        items = []

        # EUDR-01: Sem desmatamento pos-2020 (qualquer fonte)
        has_deforestation_post_2020 = spatial.has_prodes_post_2020
        # Tambem checar DETER e MapBiomas apos 2020
        if not has_deforestation_post_2020:
            for hit in spatial.deter_alertas:
                date_str = hit.date or ""
                if date_str[:4].isdigit() and int(date_str[:4]) >= 2021:
                    has_deforestation_post_2020 = True
                    break
        if not has_deforestation_post_2020:
            for hit in spatial.mapbiomas_alertas:
                year = hit.details.get("year", 0)
                if year >= 2021:
                    has_deforestation_post_2020 = True
                    break

        defor_detail = "Nenhum desmatamento detectado pos-31/12/2020"
        if has_deforestation_post_2020:
            sources = []
            if spatial.has_prodes_post_2020:
                sources.append("PRODES")
            if any(h.date and h.date[:4].isdigit() and int(h.date[:4]) >= 2021 for h in spatial.deter_alertas):
                sources.append("DETER")
            if any(h.details.get("year", 0) >= 2021 for h in spatial.mapbiomas_alertas):
                sources.append("MapBiomas")
            defor_detail = f"Desmatamento pos-2020 detectado: {', '.join(sources)}"

        items.append(ChecklistItem(
            code="EUDR-01",
            description="Sem desmatamento pos-31/12/2020",
            passed=not has_deforestation_post_2020,
            details=defor_detail,
            weight=4.0,
        ))

        # EUDR-02: Sem degradacao florestal
        # Usamos alertas DETER tipo degradacao como proxy
        has_degradation = any(
            "DEGRADACAO" in (h.details.get("classe", "").upper())
            for h in spatial.deter_alertas
            if h.date and h.date[:4].isdigit() and int(h.date[:4]) >= 2021
        )
        items.append(ChecklistItem(
            code="EUDR-02",
            description="Sem degradacao florestal pos-31/12/2020",
            passed=not has_degradation,
            details="Degradacao detectada via DETER" if has_degradation else "Sem degradacao detectada",
            weight=3.0,
        ))

        # EUDR-03: Conformidade com legislacao nacional
        legal_ok = (car_status in ("AT", "ATV", "ATIVO")) and not spatial.has_embargo_ativo
        items.append(ChecklistItem(
            code="EUDR-03",
            description="Producao em conformidade com legislacao local",
            passed=legal_ok,
            details="CAR ativo e sem embargos" if legal_ok else f"CAR={car_status or 'N/A'}, Embargo={'Sim' if spatial.has_embargo_ativo else 'Nao'}",
            weight=2.0,
        ))

        # EUDR-04: Rastreabilidade (CAR com geometria)
        has_geo = spatial.property_info is not None and bool(spatial.property_info.geometry_geojson)
        items.append(ChecklistItem(
            code="EUDR-04",
            description="Geolocalizacao do imovel rastreavel",
            passed=has_geo,
            details="Geometria CAR disponivel" if has_geo else "Sem geometria associada ao CAR",
            weight=2.0,
        ))

        return items

    # ------------------------------------------------------------------
    # Score geral 0-1000
    # ------------------------------------------------------------------

    def _calculate_overall(
        self,
        spatial: SpatialAnalysisResult,
        compliance: ComplianceResult,
        has_slave_labour: bool,
    ) -> int:
        """
        Score 0-1000 onde:
        - 1000 = imovel perfeito (tudo limpo)
        - 0 = multiplos problemas criticos

        Eixos:
        - Compliance MCR (30%): 300 pontos max
        - Compliance EUDR (25%): 250 pontos max
        - Ambiental (25%): 250 pontos max
        - Fundiario (10%): 100 pontos max
        - Trabalhista (10%): 100 pontos max
        """
        score = 0

        # MCR: 300 pontos
        score += int(compliance.mcr_score * 3)

        # EUDR: 250 pontos
        score += int(compliance.eudr_score * 2.5)

        # Ambiental: 250 pontos (descontar por problemas)
        env_score = 250
        n_alertas = len(spatial.mapbiomas_alertas) + len(spatial.deter_alertas)
        env_score -= min(100, n_alertas * 15)  # -15 por alerta, max -100
        if spatial.has_embargo_ativo:
            env_score -= 80
        if spatial.has_terra_indigena:
            env_score -= 50
        if spatial.has_uc_protecao_integral:
            env_score -= 30
        for hit in spatial.embargos_icmbio:
            env_score -= 20
        score += max(0, env_score)

        # Fundiario: 100 pontos
        fund_score = 100
        prop = spatial.property_info
        if prop and prop.status not in ("AT", "ATV", "ATIVO"):
            fund_score -= 50
        if not prop or not prop.geometry_geojson:
            fund_score -= 30
        if prop and prop.modulos_fiscais == 0:
            fund_score -= 10  # informacao incompleta
        score += max(0, fund_score)

        # Trabalhista: 100 pontos
        if has_slave_labour:
            score += 0  # zero
        else:
            score += 100

        return min(1000, max(0, score))

    def _classify_risk(self, score: int) -> str:
        if score >= 800:
            return "BAIXO"
        if score >= 600:
            return "MEDIO"
        if score >= 300:
            return "ALTO"
        return "CRITICO"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _weighted_score(items: list[ChecklistItem]) -> int:
        """Score ponderado 0-100 baseado nos pesos dos itens."""
        if not items:
            return 0
        total_weight = sum(item.weight for item in items)
        passed_weight = sum(item.weight for item in items if item.passed)
        return int((passed_weight / total_weight) * 100) if total_weight > 0 else 0

    @staticmethod
    def _generate_summary(result: ComplianceResult, spatial: SpatialAnalysisResult) -> str:
        parts = []

        if result.mcr_passed:
            parts.append("Elegivel para credito rural (MCR 2.9)")
        else:
            failed = [i.code for i in result.mcr_items if not i.passed]
            parts.append(f"Inelegivel MCR 2.9 ({', '.join(failed)})")

        if result.eudr_passed:
            parts.append("Conforme EUDR")
        else:
            failed = [i.code for i in result.eudr_items if not i.passed]
            parts.append(f"Nao conforme EUDR ({', '.join(failed)})")

        n_alertas = len(spatial.mapbiomas_alertas) + len(spatial.deter_alertas)
        if n_alertas > 0:
            parts.append(f"{n_alertas} alerta(s) de desmatamento")

        parts.append(f"Score: {result.overall_score}/1000 ({result.risk_level})")

        return ". ".join(parts) + "."
