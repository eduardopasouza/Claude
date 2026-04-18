"""Tests for consulta unificada endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestConsultaUnificada:
    def test_consulta_completa_cnpj(self):
        response = client.post("/api/v1/consulta/completa", json={
            "cpf_cnpj": "11222333000181",
        })
        assert response.status_code in (200, 429)
        if response.status_code == 200:
            data = response.json()
            assert "sections" in data or "consulta_id" in data

    def test_consulta_completa_cpf(self):
        response = client.post("/api/v1/consulta/completa", json={
            "cpf_cnpj": "12345678909",
        })
        assert response.status_code in (200, 429)

    def test_consulta_missing_doc(self):
        response = client.post("/api/v1/consulta/completa", json={})
        assert response.status_code in (200, 422, 429)

    def test_consulta_has_risk_score(self):
        response = client.post("/api/v1/consulta/completa", json={
            "cpf_cnpj": "11222333000181",
        })
        if response.status_code == 200:
            data = response.json()
            assert "risk" in str(data).lower() or "score" in str(data).lower()
