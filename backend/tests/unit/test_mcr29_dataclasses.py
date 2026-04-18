"""
Testes unit das dataclasses e metadados do MCR 2.9 expandido.

Foco no que é puro (sem banco):
  - CriterionResult / AxisScore / MCR29FullResult → to_dict()
  - WEIGHTS (pesos dos 32 critérios)
  - AXIS_LABELS (labels dos 5 eixos)
  - list_criteria_metadata() (contrato do endpoint GET /criteria)

Não testa as 32 funções `check_*` individualmente — elas fazem SQL e vão
para integration tests / fixtures de banco.
"""

from __future__ import annotations

import pytest

from app.services.mcr29_expanded import (
    AXIS_LABELS,
    WEIGHTS,
    AxisScore,
    CriterionResult,
    MCR29FullResult,
    list_criteria_metadata,
)


# ---------------------------------------------------------------------------
# WEIGHTS
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestWeights:
    def test_tem_32_criterios(self):
        assert len(WEIGHTS) == 32

    def test_cobertura_por_eixo(self):
        """Cada eixo tem a quantidade certa de critérios.

        Cuidado: 'F' começa fundiário MAS 'FI' começa financeiro (5 critérios
        a mais). Precisamos excluir FI antes de contar F.
        """
        fundiario = [k for k in WEIGHTS if k.startswith("F") and not k.startswith("FI")]
        ambiental = [k for k in WEIGHTS if k.startswith("A")]
        trabalhista = [k for k in WEIGHTS if k.startswith("T")]
        juridico = [k for k in WEIGHTS if k.startswith("J")]
        financeiro = [k for k in WEIGHTS if k.startswith("FI")]

        assert len(fundiario) == 8  # F01-F08
        assert len(ambiental) == 8  # A01-A08
        assert len(trabalhista) == 6  # T01-T06
        assert len(juridico) == 5  # J01-J05
        assert len(financeiro) == 5  # FI01-FI05

    def test_pesos_sao_numeros_positivos(self):
        for code, w in WEIGHTS.items():
            assert isinstance(w, (int, float))
            assert w > 0, f"{code}: peso {w} não é positivo"

    def test_pesos_criticos_sao_3_0(self):
        """Peso 3.0 = bloqueante. F01, F03, A01, A04, T01 devem ser 3.0."""
        bloqueantes_esperados = {"F01", "F03", "A01", "A04", "T01"}
        for code in bloqueantes_esperados:
            assert WEIGHTS[code] == 3.0, f"{code} deveria ter peso 3.0"


# ---------------------------------------------------------------------------
# AXIS_LABELS
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAxisLabels:
    def test_5_eixos(self):
        assert len(AXIS_LABELS) == 5

    def test_labels_em_portugues(self):
        assert AXIS_LABELS == {
            "fundiario": "Fundiário",
            "ambiental": "Ambiental",
            "trabalhista": "Trabalhista",
            "juridico": "Jurídico",
            "financeiro": "Financeiro",
        }


# ---------------------------------------------------------------------------
# CriterionResult
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCriterionResult:
    def test_cria_com_campos_minimos(self):
        c = CriterionResult(
            code="X",
            axis="ambiental",
            title="Test",
            description="",
            regulation="",
            status="passed",
            passed=True,
            details="",
        )
        assert c.weight == 1.0  # default
        assert c.evidence == {}  # default

    def test_to_dict_preserva_todos_os_campos(self):
        c = CriterionResult(
            code="MCR-F01",
            axis="fundiario",
            title="CAR ativo",
            description="Inscrição ativa no SICAR",
            regulation="MCR 2-2-9",
            status="passed",
            passed=True,
            details="CAR encontrado e ativo.",
            weight=3.0,
            evidence={"source": "SICAR", "car_code": "MA-X"},
        )
        d = c.to_dict()
        assert d["code"] == "MCR-F01"
        assert d["axis"] == "fundiario"
        assert d["status"] == "passed"
        assert d["passed"] is True
        assert d["weight"] == 3.0
        assert d["evidence"]["source"] == "SICAR"

    @pytest.mark.parametrize(
        "status,passed",
        [
            ("passed", True),
            ("failed", False),
            ("pending", None),
            ("not_applicable", None),
        ],
    )
    def test_combinacoes_validas_de_status_passed(self, status, passed):
        c = CriterionResult(
            code="X", axis="fundiario", title="", description="",
            regulation="", status=status, passed=passed, details="",
        )
        assert c.status == status
        assert c.passed == passed


# ---------------------------------------------------------------------------
# AxisScore
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAxisScore:
    def test_cria_e_to_dict(self):
        s = AxisScore(
            axis="fundiario",
            label="Fundiário",
            total_criteria=8,
            passed=5,
            failed=1,
            pending=2,
            not_applicable=0,
            weighted_score=62.5,
        )
        d = s.to_dict()
        assert d == {
            "axis": "fundiario",
            "label": "Fundiário",
            "total_criteria": 8,
            "passed": 5,
            "failed": 1,
            "pending": 2,
            "not_applicable": 0,
            "weighted_score": 62.5,
        }

    def test_weighted_score_arredondado_pra_1_decimal(self):
        s = AxisScore(
            axis="x", label="X", total_criteria=1,
            passed=1, failed=0, pending=0, not_applicable=0,
            weighted_score=62.555555,
        )
        assert s.to_dict()["weighted_score"] == 62.6


# ---------------------------------------------------------------------------
# MCR29FullResult.to_dict
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestMCR29FullResult:
    def _sample_result(self) -> MCR29FullResult:
        axis = AxisScore(
            axis="fundiario", label="Fundiário", total_criteria=1,
            passed=1, failed=0, pending=0, not_applicable=0,
            weighted_score=100.0,
        )
        criterion = CriterionResult(
            code="F01", axis="fundiario", title="CAR", description="",
            regulation="", status="passed", passed=True, details="ok",
        )
        return MCR29FullResult(
            car_code="MA-X",
            cpf_cnpj=None,
            generated_at="2026-04-18T12:00:00Z",
            overall_status="approved",
            overall_score=850.5,
            risk_level="LOW",
            axis_scores=[axis],
            criteria=[criterion],
            summary="Tudo ok",
            recommendation="Prosseguir",
            sources_consulted=["SICAR"],
            pending_sources=[],
        )

    def test_to_dict_estrutura_completa(self):
        d = self._sample_result().to_dict()
        for campo in [
            "car_code", "cpf_cnpj", "generated_at", "overall_status",
            "overall_score", "risk_level", "axis_scores", "criteria",
            "summary", "recommendation", "sources_consulted", "pending_sources",
        ]:
            assert campo in d

    def test_axis_scores_serializados_como_dicts(self):
        d = self._sample_result().to_dict()
        assert isinstance(d["axis_scores"], list)
        assert isinstance(d["axis_scores"][0], dict)
        assert "weighted_score" in d["axis_scores"][0]

    def test_criteria_serializados_como_dicts(self):
        d = self._sample_result().to_dict()
        assert isinstance(d["criteria"], list)
        assert isinstance(d["criteria"][0], dict)
        assert "code" in d["criteria"][0]

    def test_overall_score_arredondado_pra_1_decimal(self):
        r = self._sample_result()
        r.overall_score = 850.555
        assert r.to_dict()["overall_score"] == 850.6


# ---------------------------------------------------------------------------
# list_criteria_metadata — contrato do GET /criteria (frontend /compliance)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestListCriteriaMetadata:
    def test_retorna_todos_32_criterios(self):
        meta = list_criteria_metadata()
        assert len(meta) == 32

    def test_cada_item_tem_campos_obrigatorios(self):
        meta = list_criteria_metadata()
        for item in meta:
            assert "code" in item
            assert "axis" in item
            assert "title" in item
            assert "weight" in item
            assert "regulation" in item

    def test_todos_codigos_comecam_com_MCR(self):
        meta = list_criteria_metadata()
        for item in meta:
            assert item["code"].startswith("MCR-")

    def test_axis_de_cada_item_pertence_aos_5_eixos_validos(self):
        meta = list_criteria_metadata()
        for item in meta:
            assert item["axis"] in AXIS_LABELS

    def test_pesos_batem_com_WEIGHTS(self):
        meta = list_criteria_metadata()
        for item in meta:
            # item.code = "MCR-F01", queremos ver se WEIGHTS["F01"] bate
            key = item["code"].removeprefix("MCR-")
            assert item["weight"] == WEIGHTS[key], (
                f"{item['code']}: metadata diz {item['weight']}, "
                f"WEIGHTS diz {WEIGHTS[key]}"
            )

    def test_sem_codigos_duplicados(self):
        codes = [item["code"] for item in list_criteria_metadata()]
        assert len(codes) == len(set(codes))
