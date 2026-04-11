"""Tests for compliance endpoints (MCR 2.9, EUDR)."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestMCR29Compliance:
    def test_mcr29_valid_request(self):
        response = client.post("/api/v1/compliance/mcr29", json={
            "cpf_cnpj": "11222333000181",
            "property_car": "MA-2100055-abc123",
            "lat": -5.0,
            "lon": -44.0,
        })
        assert response.status_code == 200
        data = response.json()
        assert "compliant" in data or "checks" in data

    def test_mcr29_missing_fields(self):
        response = client.post("/api/v1/compliance/mcr29", json={})
        assert response.status_code in (200, 422)


class TestEUDRCompliance:
    def test_eudr_valid_request(self):
        response = client.post("/api/v1/compliance/eudr", json={
            "cpf_cnpj": "11222333000181",
            "lat": -5.0,
            "lon": -44.0,
            "product": "soja",
        })
        assert response.status_code == 200
        data = response.json()
        assert "compliant" in data or "checks" in data

    def test_eudr_missing_fields(self):
        response = client.post("/api/v1/compliance/eudr", json={})
        assert response.status_code in (200, 422)
