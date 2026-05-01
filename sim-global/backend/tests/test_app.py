"""Smoke tests do backend FastAPI."""
from __future__ import annotations

from fastapi.testclient import TestClient

from simglobal.main import create_app


def test_health_endpoint():
    client = TestClient(create_app())
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_examples_endpoint_lists_brasil_vargas_1930():
    client = TestClient(create_app())
    resp = client.get("/api/examples")
    assert resp.status_code == 200
    assert "brasil-vargas-1930" in resp.json()


def test_state_endpoint_returns_brasil_vargas_initial():
    client = TestClient(create_app())
    resp = client.get("/api/state/brasil-vargas-1930")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["campaign"] == "brasil-vargas-1930"
    assert payload["state"]["player_polity"] == "Brasil"
    assert payload["state"]["current_date"] == "1930-11-03"
    assert len(payload["state"]["polities"]) == 11
    assert len(payload["state"]["regions"]) == 20
    assert payload["invariant_violations"] == []


def test_state_endpoint_unknown_campaign_returns_404():
    client = TestClient(create_app())
    resp = client.get("/api/state/inexistente")
    assert resp.status_code == 404


def test_index_renders_html_with_polity_panel():
    client = TestClient(create_app())
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.text
    assert "sim-global" in body
    assert "Brasil" in body
    assert "Polity selecionada" in body
    assert "Action Box" in body
