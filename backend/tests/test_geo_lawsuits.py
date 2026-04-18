"""Testes dos novos endpoints geo e lawsuits."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestGeoEndpoints:
    def test_terras_indigenas_no_state(self):
        response = client.get("/api/v1/geo/terras-indigenas")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "FUNAI GeoServer"

    def test_terras_indigenas_by_state(self):
        response = client.get("/api/v1/geo/terras-indigenas?uf=MA")
        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "MA"

    def test_check_overlap_ti(self):
        response = client.get("/api/v1/geo/terras-indigenas/check?lat=-3.0&lon=-47.0")
        assert response.status_code == 200
        data = response.json()
        assert "overlaps" in data
        assert data["coordinates"]["lat"] == -3.0

    def test_deforestation_alerts(self):
        response = client.get("/api/v1/geo/desmatamento/alertas?biome=amazonia&max_features=5")
        assert response.status_code == 200
        data = response.json()
        assert data["biome"] == "amazonia"

    def test_check_deforestation(self):
        response = client.get("/api/v1/geo/desmatamento/check?lat=-10.0&lon=-55.0&radius_km=2.0")
        assert response.status_code == 200
        data = response.json()
        assert "alerts_found" in data

    def test_biomas(self):
        response = client.get("/api/v1/geo/biomas")
        assert response.status_code == 200


class TestLawsuitsEndpoints:
    def test_list_tribunais(self):
        response = client.get("/api/v1/lawsuits/tribunais")
        assert response.status_code == 200
        data = response.json()
        assert "TRF1" in data["tribunais"]
        assert "10432" in data["assuntos_agro"]  # Usucapião

    def test_search_by_document(self):
        response = client.get("/api/v1/lawsuits/search/11222333000181")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "DataJud/CNJ"
        assert "total" in data

    def test_search_by_subject(self):
        response = client.get("/api/v1/lawsuits/subject/10432?tribunal=TRF1&max_results=5")
        assert response.status_code == 200
        data = response.json()
        assert data["subject_code"] == "10432"
