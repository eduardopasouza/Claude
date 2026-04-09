"""Fixtures compartilhadas para testes."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """TestClient reutilizável."""
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    """Registra um usuário de teste e retorna o token JWT."""
    response = client.post("/api/v1/auth/register", json={
        "email": "fixture@agrojus.com",
        "password": "fixture_senha_123",
        "name": "Fixture User",
        "plan": "pro",
    })
    if response.status_code == 409:
        # Already registered, login instead
        response = client.post("/api/v1/auth/login", json={
            "email": "fixture@agrojus.com",
            "password": "fixture_senha_123",
        })
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Headers com Bearer token para rotas autenticadas."""
    return {"Authorization": f"Bearer {auth_token}"}
