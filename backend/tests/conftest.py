"""
Fixtures compartilhadas dos testes do AgroJus.

Filosofia (Anti-Vibe Coding):
- Cada teste é reprodutível e determinístico. Sem flakiness aceita.
- Testes que tocam upstream real são marcados com @pytest.mark.live e
  pulam por padrão — só rodam em auditoria semanal explicitamente.
- Contract tests usam VCR cassettes. Quando o upstream muda o contrato,
  o teste quebra — e aí a gente atualiza o cassette com intenção.
- Integration tests usam banco isolado em container separado (porta 5433).
- Unit tests não tocam banco, rede ou filesystem.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Config & paths
# ---------------------------------------------------------------------------

CASSETTES_DIR = Path(__file__).parent / "contract" / "cassettes"


# ---------------------------------------------------------------------------
# VCR para contract tests
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def vcr_config():
    """Config padrão do VCR — filtra headers sensíveis e casa por URL+body."""
    return {
        "cassette_library_dir": str(CASSETTES_DIR),
        "filter_headers": [
            "authorization",
            "x-api-key",
            "apikey",
            "cookie",
            "set-cookie",
        ],
        "filter_query_parameters": ["token", "api_key", "key", "access_token"],
        # Record once, replay forever. Se upstream mudar contrato, renomear
        # cassette e forçar nova gravação: `pytest --record-mode=once`.
        "record_mode": os.environ.get("VCR_RECORD_MODE", "none"),
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "decode_compressed_response": True,
    }


@pytest.fixture
def cassette_path(request) -> Path:
    """
    Retorna o path do cassette deste teste: cassettes/<module>/<test_name>.yaml

    Uso:
        def test_x(cassette_path, vcr_cassette):
            ...
    """
    module = request.module.__name__.split(".")[-1]
    return CASSETTES_DIR / module / f"{request.node.name}.yaml"


# ---------------------------------------------------------------------------
# App / TestClient
# ---------------------------------------------------------------------------


@pytest.fixture
def client() -> TestClient:
    """TestClient reutilizável do FastAPI."""
    from app.main import app

    return TestClient(app)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@pytest.fixture
def auth_token(client: TestClient) -> str:
    """Registra um usuário de teste e retorna o token JWT."""
    payload = {
        "email": "fixture@agrojus.com",
        "password": "fixture_senha_123",
        "name": "Fixture User",
        "plan": "pro",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    if response.status_code == 409:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": payload["email"], "password": payload["password"]},
        )
    data = response.json()
    assert "access_token" in data, f"Auth falhou: {data}"
    return data["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Headers com Bearer token para rotas autenticadas."""
    return {"Authorization": f"Bearer {auth_token}"}


# ---------------------------------------------------------------------------
# DB de teste — só quando integration
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def test_db_url() -> str:
    """
    URL do banco de teste. Usa TEST_DATABASE_URL se definida, senão a default
    do compose test profile (porta 5433 separada do dev em 5432).
    """
    return os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql://agrojus:agrojus@localhost:5433/agrojus_test",
    )


@pytest.fixture
def db_session(test_db_url: str) -> Iterator:
    """
    Session SQLAlchemy para testes integration. Cada teste roda numa transação
    que é rollback ao final — zero poluição cross-test.

    Uso:
        @pytest.mark.integration
        def test_algo(db_session):
            ...
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(test_db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.begin_nested()
        yield session
    finally:
        session.rollback()
        session.close()


# ---------------------------------------------------------------------------
# Time machine
# ---------------------------------------------------------------------------


@pytest.fixture
def frozen_time():
    """
    Congela time.now() em uma data fixa determinística (referência da sessão 10).
    Uso:
        def test_x(frozen_time):
            assert datetime.now().year == 2026
    """
    from freezegun import freeze_time

    with freeze_time("2026-04-18 12:00:00", tz_offset=-3) as frozen:
        yield frozen


# ---------------------------------------------------------------------------
# Collection hooks — skip "live" por padrão
# ---------------------------------------------------------------------------


def pytest_collection_modifyitems(config, items):
    """
    Pula testes @pytest.mark.live a menos que PYTEST_LIVE=1 esteja setado.
    Auditoria de coletores roda com: PYTEST_LIVE=1 pytest -m live
    """
    if os.environ.get("PYTEST_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="live tests rodam só com PYTEST_LIVE=1")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
