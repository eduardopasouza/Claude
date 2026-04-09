"""Testes do sistema de autenticação."""

import pytest
from app.services.auth import (
    hash_password, verify_password, create_token, decode_token,
    get_plan_limits, check_plan_permission,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        password = "minha_senha_forte_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("correta")
        assert verify_password("errada", hashed) is False

    def test_different_hashes(self):
        h1 = hash_password("mesma_senha")
        h2 = hash_password("mesma_senha")
        # Different salts = different hashes
        assert h1 != h2


class TestJWT:
    def test_create_and_decode(self):
        token = create_token(1, "test@email.com", "pro")
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["email"] == "test@email.com"
        assert payload["plan"] == "pro"

    def test_invalid_token(self):
        payload = decode_token("invalid.token.here")
        assert payload is None


class TestPlanLimits:
    def test_free_plan(self):
        limits = get_plan_limits("free")
        assert limits["reports_per_month"] == 3
        assert limits["pdf"] is False
        assert limits["monitoring"] is False

    def test_pro_plan(self):
        limits = get_plan_limits("pro")
        assert limits["reports_per_month"] == 100
        assert limits["pdf"] is True
        assert limits["monitoring"] is True

    def test_enterprise_unlimited(self):
        limits = get_plan_limits("enterprise")
        assert limits["reports_per_month"] == -1  # unlimited
        assert limits["api"] is True

    def test_check_permission(self):
        assert check_plan_permission("free", "pdf") is False
        assert check_plan_permission("pro", "pdf") is True
        assert check_plan_permission("enterprise", "api") is True
