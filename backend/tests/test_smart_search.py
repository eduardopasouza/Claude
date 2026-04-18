"""Testes do detector de tipo de input (smart search)."""

import pytest
from app.api.smart_search import detect_input_type


class TestDetectInputType:
    def test_cnpj_formatted(self):
        result_type, parsed = detect_input_type("11.222.333/0001-81")
        assert result_type == "cnpj"
        assert parsed["cpf_cnpj"] == "11222333000181"

    def test_cnpj_raw(self):
        result_type, parsed = detect_input_type("11222333000181")
        assert result_type == "cnpj"

    def test_cpf_formatted(self):
        result_type, parsed = detect_input_type("529.982.247-25")
        assert result_type == "cpf"
        assert parsed["cpf_cnpj"] == "52998224725"

    def test_cpf_raw(self):
        result_type, parsed = detect_input_type("52998224725")
        assert result_type == "cpf"

    def test_car_code(self):
        result_type, parsed = detect_input_type("MT-5107925-ABC12345")
        assert result_type == "car"
        assert parsed["car_code"] == "MT-5107925-ABC12345"

    def test_coordinates(self):
        result_type, parsed = detect_input_type("-15.7801, -47.9292")
        assert result_type == "coordinates"
        assert parsed["latitude"] == pytest.approx(-15.7801)
        assert parsed["longitude"] == pytest.approx(-47.9292)

    def test_coordinates_semicolon(self):
        result_type, parsed = detect_input_type("-12.9714;-38.5124")
        assert result_type == "coordinates"

    def test_cnj_lawsuit(self):
        result_type, parsed = detect_input_type("0001234-56.2024.8.26.0001")
        assert result_type == "lawsuit"

    def test_uuid_sigef(self):
        result_type, parsed = detect_input_type("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
        assert result_type == "sigef"

    def test_municipality_uf(self):
        result_type, parsed = detect_input_type("Sorriso/MT")
        assert result_type == "municipality"
        assert parsed["municipality"] == "Sorriso"
        assert parsed["state"] == "MT"

    def test_municipality_dash(self):
        result_type, parsed = detect_input_type("Balsas - MA")
        assert result_type == "municipality"
        assert parsed["state"] == "MA"

    def test_matricula(self):
        result_type, parsed = detect_input_type("matrícula 12345")
        assert result_type == "matricula"
        assert parsed["matricula"] == "12345"

    def test_nirf(self):
        result_type, parsed = detect_input_type("nirf 1234567")
        assert result_type == "nirf"

    def test_ccir(self):
        result_type, parsed = detect_input_type("ccir 1234567890")
        assert result_type == "ccir"

    def test_owner_name_fallback(self):
        result_type, parsed = detect_input_type("Fazenda Boa Vista Ltda")
        assert result_type == "owner_name"
        assert parsed["owner_name"] == "Fazenda Boa Vista Ltda"

    def test_invalid_state_not_matched(self):
        result_type, _ = detect_input_type("Sorriso/XX")
        assert result_type == "owner_name"  # XX is not a valid state

    def test_ibama_auto(self):
        result_type, parsed = detect_input_type("1234567")
        assert result_type == "ibama_auto"

    def test_anm_process(self):
        result_type, parsed = detect_input_type("831.123/2024")
        assert result_type == "anm_process"
