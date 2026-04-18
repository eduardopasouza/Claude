"""
Testes unit dos validadores de CPF e CNPJ.

Função sob teste:
  ReceitaFederalCollector._validate_cpf    (staticmethod)
  ReceitaFederalCollector._validate_cnpj   (staticmethod)
  ReceitaFederalCollector.validate_cpf_cnpj (coroutine, pública)

Algoritmo:
  CPF  — 2 dígitos verificadores via pesos decrescentes, módulo 11
  CNPJ — 2 dígitos verificadores via pesos [5,4,3,2,9,8,7,6,5,4,3,2]
"""

from __future__ import annotations

import pytest

from app.collectors.receita_federal import ReceitaFederalCollector


@pytest.mark.unit
class TestValidateCPF:
    # --- válidos ---
    @pytest.mark.parametrize(
        "cpf",
        [
            # CPFs válidos conhecidos
            "11144477735",
            "12345678909",
            "52998224725",
        ],
    )
    def test_cpfs_validos_passam(self, cpf):
        assert ReceitaFederalCollector._validate_cpf(cpf) is True

    # --- inválidos ---
    @pytest.mark.parametrize(
        "cpf",
        [
            "11111111111",      # todos iguais
            "00000000000",
            "99999999999",
            "11144477730",      # dígito errado
            "12345678900",
            "11144477731",
        ],
    )
    def test_cpfs_invalidos_falham(self, cpf):
        assert ReceitaFederalCollector._validate_cpf(cpf) is False

    def test_tamanho_errado_falha(self):
        assert ReceitaFederalCollector._validate_cpf("123") is False
        assert ReceitaFederalCollector._validate_cpf("1234567890") is False   # 10 dígitos
        assert ReceitaFederalCollector._validate_cpf("123456789012") is False  # 12


@pytest.mark.unit
class TestValidateCNPJ:
    @pytest.mark.parametrize(
        "cnpj",
        [
            # CNPJs válidos (gerados por algoritmo, sem empresa real)
            "11222333000181",
            "47960950000121",   # Magazine Luiza SA histórico
            "00000000000191",   # Banco do Brasil
        ],
    )
    def test_cnpjs_validos_passam(self, cnpj):
        assert ReceitaFederalCollector._validate_cnpj(cnpj) is True

    @pytest.mark.parametrize(
        "cnpj",
        [
            "11111111111111",   # todos iguais
            "00000000000000",
            "11222333000180",   # dígito final errado
            "11222333000182",
            "47960950000122",
        ],
    )
    def test_cnpjs_invalidos_falham(self, cnpj):
        assert ReceitaFederalCollector._validate_cnpj(cnpj) is False

    def test_tamanho_errado_falha(self):
        assert ReceitaFederalCollector._validate_cnpj("123") is False
        assert ReceitaFederalCollector._validate_cnpj("1122233300018") is False   # 13
        assert ReceitaFederalCollector._validate_cnpj("112223330001811") is False  # 15


@pytest.mark.unit
class TestValidateCpfCnpjPublic:
    """Testa a função pública que detecta tipo e valida."""

    @pytest.mark.asyncio
    async def test_cpf_valido_detecta_e_valida(self):
        collector = ReceitaFederalCollector()
        result = await collector.validate_cpf_cnpj("111.444.777-35")
        assert result["type"] == "CPF"
        assert result["valid"] is True
        assert result["document"] == "11144477735"

    @pytest.mark.asyncio
    async def test_cnpj_valido_detecta_e_valida(self):
        collector = ReceitaFederalCollector()
        result = await collector.validate_cpf_cnpj("11.222.333/0001-81")
        assert result["type"] == "CNPJ"
        assert result["valid"] is True
        assert result["document"] == "11222333000181"

    @pytest.mark.asyncio
    async def test_cpf_invalido_detecta_tipo_mas_marca_invalido(self):
        collector = ReceitaFederalCollector()
        result = await collector.validate_cpf_cnpj("12345678901")
        assert result["type"] == "CPF"
        assert result["valid"] is False

    @pytest.mark.asyncio
    async def test_tamanho_nao_reconhecido_retorna_unknown(self):
        collector = ReceitaFederalCollector()
        result = await collector.validate_cpf_cnpj("12345")
        assert result["type"] == "unknown"
        assert result["valid"] is False

    @pytest.mark.asyncio
    async def test_mascara_e_removida_antes_da_validacao(self):
        collector = ReceitaFederalCollector()
        result = await collector.validate_cpf_cnpj("111.444.777-35")
        assert result["document"] == "11144477735"  # limpo

    @pytest.mark.asyncio
    async def test_string_com_caracteres_extras_remove_so_pontuacao(self):
        collector = ReceitaFederalCollector()
        # Só `.`, `/`, `-` são removidos
        result = await collector.validate_cpf_cnpj("111.444.777-35")
        assert result["document"] == "11144477735"
