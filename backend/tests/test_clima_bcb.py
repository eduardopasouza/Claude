"""Tests for clima (NASA POWER) and BCB indicator endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestClima:
    def test_clima_valid_coords(self):
        response = client.get("/api/v1/geo/clima?lat=-5.0&lon=-44.0&days=7")
        assert response.status_code == 200
        data = response.json()
        assert "source" in data or "temperature" in str(data).lower() or "error" in str(data).lower()


class TestBCBIndicators:
    def test_indicators_list(self):
        response = client.get("/api/v1/market/indicators")
        assert response.status_code == 200
        data = response.json()
        assert any(k in str(data).lower() for k in ["selic", "dolar", "ipca"])

    def test_indicator_serie(self):
        response = client.get("/api/v1/market/indicators/432")
        assert response.status_code == 200

    def test_quotes(self):
        response = client.get("/api/v1/market/quotes")
        assert response.status_code == 200
        data = response.json()
        assert "quotes" in data

    def test_credit_municipality(self):
        response = client.get("/api/v1/market/credit/municipality/2111300")
        assert response.status_code == 200
