"""Testes do dossie de pessoa (person intelligence)."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth import create_token


client = TestClient(app)

# Token pro para evitar rate limiting durante testes
_PRO_TOKEN = create_token(900, "test-dossier@agrojus.com", "enterprise")
_AUTH_HEADERS = {"Authorization": f"Bearer {_PRO_TOKEN}"}


class TestPersonDossierEndpoint:
    def test_person_dossier_returns_structure(self):
        """O endpoint deve retornar a estrutura completa do dossie."""
        response = client.post("/api/v1/report/person", headers=_AUTH_HEADERS, json={
            "cpf_cnpj": "12345678000190",
            "include_properties": True,
            "include_legal": True,
            "include_environmental": True,
            "include_labour": True,
            "include_news": True,
            "include_financial": True,
        })
        assert response.status_code == 200
        data = response.json()

        # Estrutura basica do dossie
        assert "dossier_id" in data
        assert "generated_at" in data
        assert "cpf_cnpj" in data
        assert "person_type" in data
        assert "risk_score" in data
        assert "sources_consulted" in data

    def test_person_dossier_has_risk_score(self):
        """O dossie deve conter risk score com todas as dimensoes."""
        response = client.post("/api/v1/report/person", headers=_AUTH_HEADERS, json={
            "cpf_cnpj": "12345678000190",
        })
        data = response.json()
        rs = data["risk_score"]

        assert rs["overall"] in ["low", "medium", "high", "critical"]
        assert "land_tenure" in rs
        assert "environmental" in rs
        assert "legal" in rs
        assert "labor" in rs
        assert "financial" in rs
        assert isinstance(rs["details"], list)

    def test_person_with_slave_labour_gets_critical(self):
        """CPF/CNPJ na Lista Suja deve gerar risco trabalhista critico."""
        response = client.post("/api/v1/report/person", headers=_AUTH_HEADERS, json={
            "cpf_cnpj": "12345678000190",
            "include_labour": True,
        })
        data = response.json()

        # Este CPF esta no dataset de referencia da Lista Suja
        assert len(data.get("slave_labour", [])) > 0
        assert data["risk_score"]["labor"] == "critical"

    def test_person_minimal_request(self):
        """Deve funcionar com apenas cpf_cnpj."""
        response = client.post("/api/v1/report/person", headers=_AUTH_HEADERS, json={
            "cpf_cnpj": "11222333000181",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["cpf_cnpj"] == "11222333000181"
        assert data["person_type"] in ["CPF", "CNPJ"]

    def test_person_cpf_detected(self):
        """CPF deve ser detectado como tipo PF."""
        response = client.post("/api/v1/report/person", headers=_AUTH_HEADERS, json={
            "cpf_cnpj": "52998224725",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["person_type"] == "CPF"
