"""Testes dos validadores de CPF e CNPJ."""

import pytest
from app.collectors.receita_federal import ReceitaFederalCollector


class TestCPFValidation:
    def setup_method(self):
        self.collector = ReceitaFederalCollector()

    def test_valid_cpf(self):
        assert self.collector._validate_cpf("52998224725") is True

    def test_invalid_cpf_all_same(self):
        assert self.collector._validate_cpf("11111111111") is False

    def test_invalid_cpf_wrong_digits(self):
        assert self.collector._validate_cpf("12345678901") is False

    def test_invalid_cpf_short(self):
        assert self.collector._validate_cpf("123456789") is False


class TestCNPJValidation:
    def setup_method(self):
        self.collector = ReceitaFederalCollector()

    def test_valid_cnpj(self):
        assert self.collector._validate_cnpj("11222333000181") is True

    def test_invalid_cnpj_all_same(self):
        assert self.collector._validate_cnpj("11111111111111") is False

    def test_invalid_cnpj_wrong_digits(self):
        assert self.collector._validate_cnpj("12345678000199") is False

    def test_invalid_cnpj_short(self):
        assert self.collector._validate_cnpj("1234567800") is False
