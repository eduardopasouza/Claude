"""Testes de integração da API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestHealthEndpoints:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "AgroJus API"
        assert data["status"] == "running"

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestSearchEndpoints:
    def test_validate_valid_cnpj(self):
        response = client.get("/api/v1/search/validate/11222333000181")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "CNPJ"
        assert data["valid"] is True

    def test_validate_invalid_cpf(self):
        response = client.get("/api/v1/search/validate/12345678901")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "CPF"
        assert data["valid"] is False


class TestMapEndpoints:
    def test_list_layers(self):
        response = client.get("/api/v1/map/layers")
        assert response.status_code == 200
        data = response.json()
        assert "layers" in data
        layer_ids = [l["id"] for l in data["layers"]]
        assert "car" in layer_ids
        assert "sigef" in layer_ids
        assert "embargos" in layer_ids
        assert "terras_indigenas" in layer_ids


class TestMarketEndpoints:
    def test_get_quotes(self):
        response = client.get("/api/v1/market/quotes")
        assert response.status_code == 200
        data = response.json()
        assert "quotes" in data

    def test_get_commodity_quote(self):
        response = client.get("/api/v1/market/quotes/soja")
        assert response.status_code == 200


class TestNewsEndpoints:
    def test_get_news(self):
        response = client.get("/api/v1/news/?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "articles" in data

    def test_get_legal_news(self):
        response = client.get("/api/v1/news/legal?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert data.get("category") == "juridico"


class TestAuthEndpoints:
    def test_register_and_login(self):
        # Register
        response = client.post("/api/v1/auth/register", json={
            "email": "test@agrojus.com",
            "password": "senha_forte_123",
            "name": "Test User",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        token = data["access_token"]

        # Get profile
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@agrojus.com"

    def test_login_wrong_password(self):
        # Register first
        client.post("/api/v1/auth/register", json={
            "email": "test2@agrojus.com",
            "password": "senha_correta_123",
            "name": "Test",
        })
        # Login with wrong password
        response = client.post("/api/v1/auth/login", json={
            "email": "test2@agrojus.com",
            "password": "senha_errada",
        })
        assert response.status_code == 401

    def test_plan_limits(self):
        response = client.get("/api/v1/auth/plan-limits")
        assert response.status_code == 200
        data = response.json()
        assert data["plan"] == "free"


class TestMonitoringEndpoints:
    def test_add_and_get_monitor(self):
        # Add property
        response = client.post("/api/v1/monitoring/property", json={
            "car_code": "MT-123456"
        })
        assert response.status_code == 200
        assert response.json()["monitored"] is True

        # Check status
        response = client.get("/api/v1/monitoring/status")
        assert response.status_code == 200
        data = response.json()
        assert "MT-123456" in data["properties"]

    def test_get_alerts(self):
        response = client.get("/api/v1/monitoring/alerts")
        assert response.status_code == 200
        assert "alerts" in response.json()
