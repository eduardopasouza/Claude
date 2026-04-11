"""Tests for jurisdicao endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestJurisdicao:
    def test_get_estado_ma(self):
        response = client.get("/api/v1/jurisdicao/estado/MA")
        assert response.status_code == 200
        data = response.json()
        assert data.get("uf") == "MA" or "estado" in str(data).lower()

    def test_get_estado_invalid(self):
        response = client.get("/api/v1/jurisdicao/estado/XX")
        assert response.status_code in (200, 404)

    def test_list_all_estados(self):
        response = client.get("/api/v1/jurisdicao/estados")
        assert response.status_code == 200
        data = response.json()
        assert len(data.get("estados", data.get("data", []))) >= 27

    def test_reserva_legal(self):
        response = client.get("/api/v1/jurisdicao/reserva-legal?uf=MA&bioma=amazonia")
        assert response.status_code == 200

    def test_comparar_estados(self):
        response = client.get("/api/v1/jurisdicao/comparar?uf1=MA&uf2=PA")
        assert response.status_code == 200
        data = response.json()
        assert "MA" in str(data) and "PA" in str(data)
