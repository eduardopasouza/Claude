"""Tests for IBAMA CSV parser with coordinates."""
import pytest
from app.collectors.ibama_csv import parse_ibama_csv_row, search_ibama_by_cpf_cnpj, search_ibama_by_municipality


class TestParseIbamaCSV:
    def test_parse_valid_row(self):
        row = {
            "SEQ_AUTO_INFRACAO": "12345",
            "NUM_AUTO_INFRACAO": "9876543",
            "DAT_AUTO_INFRACAO": "2024-03-15",
            "NOM_RAZAO_SOCIAL": "Fazenda Teste LTDA",
            "CPF_CNPJ": "11.222.333/0001-81",
            "DES_AUTO_INFRACAO": "Desmatamento ilegal",
            "VAL_AUTO_INFRACAO": "50000.00",
            "DES_MUNICIPIO": "Sao Luis",
            "SIG_UF": "MA",
            "NUM_LATITUDE": "-2.5",
            "NUM_LONGITUDE": "-44.2",
        }
        result = parse_ibama_csv_row(row)
        assert result["id"] == "12345"
        assert result["cpf_cnpj"] == "11222333000181"
        assert result["lat"] == -2.5
        assert result["lon"] == -44.2
        assert result["municipality"] == "Sao Luis"
        assert result["state"] == "MA"
        assert result["value"] == 50000.0

    def test_parse_empty_coords(self):
        row = {
            "SEQ_AUTO_INFRACAO": "99",
            "NUM_LATITUDE": "",
            "NUM_LONGITUDE": "",
        }
        result = parse_ibama_csv_row(row)
        assert result["lat"] is None
        assert result["lon"] is None

    def test_parse_invalid_float(self):
        row = {
            "SEQ_AUTO_INFRACAO": "99",
            "VAL_AUTO_INFRACAO": "invalido",
            "NUM_LATITUDE": "abc",
        }
        result = parse_ibama_csv_row(row)
        assert result["value"] is None
        assert result["lat"] is None


class TestSearchIbama:
    @pytest.fixture
    def records(self):
        return [
            {"cpf_cnpj": "11222333000181", "municipality": "Sao Luis", "state": "MA"},
            {"cpf_cnpj": "11222333000181", "municipality": "Imperatriz", "state": "MA"},
            {"cpf_cnpj": "99888777000166", "municipality": "Belem", "state": "PA"},
        ]

    def test_search_by_cpf_cnpj(self, records):
        results = search_ibama_by_cpf_cnpj(records, "11.222.333/0001-81")
        assert len(results) == 2

    def test_search_by_municipality(self, records):
        results = search_ibama_by_municipality(records, "Sao Luis")
        assert len(results) == 1
        assert results[0]["municipality"] == "Sao Luis"

    def test_search_by_municipality_with_uf(self, records):
        results = search_ibama_by_municipality(records, "Imperatriz", uf="MA")
        assert len(results) == 1

    def test_search_no_results(self, records):
        results = search_ibama_by_cpf_cnpj(records, "00000000000000")
        assert len(results) == 0
