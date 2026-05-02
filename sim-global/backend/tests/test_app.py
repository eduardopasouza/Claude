"""Smoke tests do backend FastAPI.

Usa TestClient como context manager para acionar lifespan (init_db,
autoseed do exemplo, criação de session_factory).
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from simglobal.main import create_app


@pytest.fixture
def client(monkeypatch):
    """TestClient com SQLite isolado em arquivo temporário."""
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        monkeypatch.setenv("SIMGLOBAL_DATABASE_URL", f"sqlite:///{db_path}")
        # Re-importa config: AppConfig pega default; vou forçar via monkeypatch
        # do load_config para usar o tmp database.
        import simglobal.main as main_module
        import simglobal.config as config_module
        original_load = config_module.load_config

        def patched_load(*args, **kwargs):
            cfg = original_load(*args, **kwargs)
            cfg.persistence.database_url = f"sqlite:///{db_path}"
            return cfg

        monkeypatch.setattr(config_module, "load_config", patched_load)
        monkeypatch.setattr(main_module, "load_config", patched_load)

        app = create_app()
        with TestClient(app) as c:
            yield c


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "agent_ready" in body


def test_examples_endpoint_lists_brasil_vargas_1930(client):
    resp = client.get("/api/examples")
    assert resp.status_code == 200
    assert "brasil-vargas-1930" in resp.json()


def test_autoseed_imports_brasil_vargas_1930(client):
    resp = client.get("/api/campaigns")
    assert resp.status_code == 200
    names = [c["name"] for c in resp.json()]
    assert "brasil-vargas-1930" in names


def test_state_endpoint_returns_brasil_vargas_initial(client):
    resp = client.get("/api/campaigns/brasil-vargas-1930/state")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["campaign"] == "brasil-vargas-1930"
    assert payload["state"]["player_polity"] == "Brasil"
    assert payload["state"]["current_date"] == "1930-11-03"
    assert len(payload["state"]["polities"]) == 11
    assert len(payload["state"]["regions"]) == 20
    assert payload["invariant_violations"] == []


def test_state_endpoint_unknown_campaign_returns_404(client):
    resp = client.get("/api/campaigns/inexistente/state")
    assert resp.status_code == 404


def test_index_renders_html_with_polity_panel(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.text
    assert "sim-global" in body
    assert "Brasil" in body
    assert "Polity" in body
    assert ("Nova ação" in body) or ("Avançar tempo" in body)
    assert "advisorThread" in body  # campaign() recebe agentReady arg


def test_advisor_history_endpoint_empty_by_default(client):
    r = client.get("/api/campaigns/brasil-vargas-1930/advisor/history")
    assert r.status_code == 200
    assert r.json() == []


def test_events_history_endpoint(client):
    r = client.get("/api/campaigns/brasil-vargas-1930/events")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_dm_history_endpoint_empty_by_default(client):
    r = client.get(
        "/api/campaigns/brasil-vargas-1930/dm/Argentina/history"
    )
    assert r.status_code == 200
    assert r.json() == []


def test_turn_submit_returns_503_when_agent_not_ready(client):
    r = client.post(
        "/api/campaigns/brasil-vargas-1930/turn", json={"months": 6}
    )
    assert r.status_code == 503


def test_turn_status_404_for_unknown_job(client):
    r = client.get(
        "/api/campaigns/brasil-vargas-1930/turn/inexistente"
    )
    assert r.status_code == 404


def test_turn_endpoint_returns_503_when_agent_not_ready(client):
    resp = client.post("/api/campaigns/brasil-vargas-1930/turn", json={"months": 6})
    assert resp.status_code == 503
    assert "OAUTH_TOKEN" in resp.json()["detail"] or "SDK" in resp.json()["detail"]


def test_advise_endpoint_returns_503_when_agent_not_ready(client):
    resp = client.post(
        "/api/campaigns/brasil-vargas-1930/advise",
        json={"question": "Qual minha prioridade estratégica?"},
    )
    assert resp.status_code == 503


def test_dm_endpoint_returns_503_when_agent_not_ready(client):
    resp = client.post(
        "/api/campaigns/brasil-vargas-1930/dm",
        json={"counterparty": "Argentina", "message": "olá"},
    )
    assert resp.status_code == 503


def test_static_serves_manifest(client):
    resp = client.get("/static/manifest.json")
    assert resp.status_code == 200
    assert resp.json()["name"] == "sim-global"


def test_assets_serves_world_map_svg(client):
    resp = client.get("/assets/map/world-political.svg")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("image/svg")


def test_assets_serves_brazil_flag(client):
    resp = client.get("/assets/catalog/flags/BRA.svg")
    assert resp.status_code == 200
