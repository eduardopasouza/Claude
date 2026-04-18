"""
Testes unit das primitivas puras do AgrolinkCollector.

Função sob teste:
  app.collectors.agrolink._parse_brl(s) -> float | None
  AGROLINK_PATHS (dict de commodities suportadas)
"""

from __future__ import annotations

import pytest

from app.collectors.agrolink import AGROLINK_PATHS, _parse_brl


@pytest.mark.unit
class TestParseBrl:
    # --- formatos brasileiros válidos ---
    @pytest.mark.parametrize(
        "entrada,esperado",
        [
            ("1.234,56", 1234.56),
            ("0,00", 0.0),
            ("10,00", 10.0),
            ("1.000.000,00", 1_000_000.0),
            ("150,50", 150.5),
            ("0,50", 0.5),
            ("7,89", 7.89),
        ],
    )
    def test_formatos_brl_validos(self, entrada, esperado):
        assert _parse_brl(entrada) == esperado

    # --- whitespace ---
    def test_trim_whitespace(self):
        assert _parse_brl("  1.234,56  ") == 1234.56
        assert _parse_brl("\t10,00\n") == 10.0

    # --- inválidos ---
    @pytest.mark.parametrize(
        "entrada",
        [
            None,
            "",
            "abc",
            "R$ 10,00",   # símbolo R$ quebra (não remove)
            "--",
        ],
    )
    def test_invalidos_retornam_none(self, entrada):
        assert _parse_brl(entrada) is None

    def test_formato_americano_e_interpretado_erroneamente_limitacao_conhecida(self):
        """
        Limitação documentada: '1,234.56' (formato US) é interpretado
        como 1.23456 porque o parser faz replace literal. Se receber
        string misturada, o resultado é lixo. Upstream do Agrolink só
        manda BRL, então na prática não dá problema.

        Issue aberta: sessão 12 avalia se precisa detectar locale.
        """
        assert _parse_brl("1,234.56") == 1.23456


@pytest.mark.unit
class TestAgrolinkPaths:
    def test_nao_vazio(self):
        assert len(AGROLINK_PATHS) > 0

    def test_contem_commodities_core_do_agro_br(self):
        # Commodities-chave que o dashboard consome
        core = {"soja", "milho", "cafe", "boi", "arroz"}
        presentes = set(AGROLINK_PATHS.keys())
        faltantes = core - presentes
        assert not faltantes, f"commodities core ausentes: {faltantes}"

    def test_cada_commodity_tem_unit_e_label(self):
        for slug, info in AGROLINK_PATHS.items():
            assert "unit" in info, f"{slug}: sem unit"
            assert "label" in info, f"{slug}: sem label"
            assert info["unit"].startswith("R$"), f"{slug}: unit {info['unit']!r} não tem R$"

    def test_slugs_em_lowercase_sem_espacos(self):
        for slug in AGROLINK_PATHS:
            assert slug.islower() or slug.replace("_", "").isalpha(), f"{slug!r}"
            assert " " not in slug
