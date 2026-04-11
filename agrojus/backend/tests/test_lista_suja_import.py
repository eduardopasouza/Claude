"""Tests for Lista Suja CSV parser."""
import pytest
from app.collectors.lista_suja_csv import parse_lista_suja_row, search_by_cpf_cnpj, search_by_state


class TestParseListaSuja:
    def test_parse_valid_row(self):
        row = {
            "Ano da acao fiscal": "2023",
            "UF": "MA",
            "Empregador": "Fazenda Exemplo",
            "CNPJ/CPF": "11.222.333/0001-81",
            "Estabelecimento": "Fazenda Exemplo Unidade",
            "Trabalhadores envolvidos": "15",
            "CNAE": "0111301",
            "Decisao administrativa": "Inclusao",
        }
        result = parse_lista_suja_row(row)
        assert result["year"] == 2023
        assert result["state"] == "MA"
        assert result["employer"] == "Fazenda Exemplo"
        assert result["cpf_cnpj"] == "11222333000181"
        assert result["workers"] == 15

    def test_parse_empty_workers(self):
        row = {
            "Ano da acao fiscal": "2022",
            "UF": "PA",
            "Empregador": "Teste",
            "CNPJ/CPF": "123.456.789-09",
            "Estabelecimento": "",
            "Trabalhadores envolvidos": "",
            "CNAE": "",
            "Decisao administrativa": "",
        }
        result = parse_lista_suja_row(row)
        assert result["workers"] == 0
        assert result["cpf_cnpj"] == "12345678909"

    def test_parse_invalid_year(self):
        row = {"Ano da acao fiscal": "invalido"}
        result = parse_lista_suja_row(row)
        assert result["year"] == 0


class TestSearchListaSuja:
    @pytest.fixture
    def records(self):
        return [
            {"cpf_cnpj": "11222333000181", "state": "MA", "employer": "Fazenda A"},
            {"cpf_cnpj": "99888777000166", "state": "PA", "employer": "Fazenda B"},
            {"cpf_cnpj": "11222333000181", "state": "MA", "employer": "Fazenda C"},
        ]

    def test_search_by_cpf(self, records):
        results = search_by_cpf_cnpj(records, "11.222.333/0001-81")
        assert len(results) == 2

    def test_search_by_state(self, records):
        results = search_by_state(records, "PA")
        assert len(results) == 1
        assert results[0]["employer"] == "Fazenda B"

    def test_search_no_results(self, records):
        results = search_by_cpf_cnpj(records, "00000000000000")
        assert len(results) == 0
