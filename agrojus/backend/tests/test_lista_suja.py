"""Testes do collector e endpoints da Lista Suja do Trabalho Escravo."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.collectors.slave_labour import SlaveLabourCollector


client = TestClient(app)


class TestSlaveLabourCollector:
    def setup_method(self):
        self.collector = SlaveLabourCollector()

    @pytest.mark.asyncio
    async def test_search_by_cpf_cnpj_found(self):
        results = await self.collector.search_by_cpf_cnpj("12345678000190")
        assert len(results) == 1
        assert results[0].employer_name == "Fazenda Bela Vista Agropecuaria Ltda"
        assert results[0].municipality == "Sao Felix do Xingu"

    @pytest.mark.asyncio
    async def test_search_by_cpf_cnpj_not_found(self):
        results = await self.collector.search_by_cpf_cnpj("00000000000000")
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_search_by_name(self):
        results = await self.collector.search_by_name("Carvoaria")
        assert len(results) == 1
        assert results[0].state == "MA"

    @pytest.mark.asyncio
    async def test_search_by_name_partial(self):
        results = await self.collector.search_by_name("fazenda")
        assert len(results) >= 3  # Multiple fazendas

    @pytest.mark.asyncio
    async def test_search_by_municipality(self):
        results = await self.collector.search_by_municipality("Paragominas", "PA")
        assert len(results) == 1
        assert results[0].workers_rescued == 12

    @pytest.mark.asyncio
    async def test_search_by_state_only(self):
        results = self.collector._search_reference_data(state_filter="PA")
        assert len(results) >= 5  # Most entries are in PA

    @pytest.mark.asyncio
    async def test_get_all(self):
        results = await self.collector.get_all()
        assert len(results) == 12


class TestSlaveLabourEndpoints:
    def test_lista_suja_all(self):
        response = client.get("/api/v1/search/lista-suja")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 12
        assert data["source"] == "MTE (Lista Suja)"

    def test_lista_suja_pagination(self):
        response = client.get("/api/v1/search/lista-suja?skip=0&limit=3")
        data = response.json()
        assert len(data["records"]) == 3
        assert data["total"] == 12

        response2 = client.get("/api/v1/search/lista-suja?skip=3&limit=3")
        data2 = response2.json()
        assert len(data2["records"]) == 3
        assert data2["records"][0] != data["records"][0]

    def test_lista_suja_by_state(self):
        response = client.get("/api/v1/search/lista-suja?state=PA")
        data = response.json()
        assert data["total"] >= 5
        for record in data["records"]:
            assert record["state"] == "PA"

    def test_lista_suja_by_name(self):
        response = client.get("/api/v1/search/lista-suja?name=Usina")
        data = response.json()
        assert data["total"] == 1
        assert "Usina" in data["records"][0]["employer_name"]

    def test_lista_suja_by_cpf_cnpj(self):
        response = client.get("/api/v1/search/lista-suja/12345678000190")
        data = response.json()
        assert data["found"] is True
        assert data["total"] == 1

    def test_lista_suja_by_cpf_cnpj_not_found(self):
        response = client.get("/api/v1/search/lista-suja/00000000000000")
        data = response.json()
        assert data["found"] is False
        assert data["total"] == 0
