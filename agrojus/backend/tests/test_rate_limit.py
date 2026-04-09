"""Testes do middleware de rate limiting por plano."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth import create_token


client = TestClient(app)


class TestRateLimitHeaders:
    def test_search_includes_remaining_header(self):
        response = client.get("/api/v1/search/validate/11222333000181")
        assert response.status_code == 200
        assert "X-RateLimit-Remaining-Searches" in response.headers

    def test_non_search_no_header(self):
        response = client.get("/health")
        assert "X-RateLimit-Remaining-Searches" not in response.headers

    def test_remaining_decreases(self):
        """Pro user's remaining count should decrease with each request."""
        token = create_token(996, "decrement-test@agrojus.com", "pro")
        headers = {"Authorization": f"Bearer {token}"}

        r1 = client.get("/api/v1/search/validate/52998224725", headers=headers)
        r2 = client.get("/api/v1/search/validate/52998224725", headers=headers)

        rem1 = int(r1.headers.get("X-RateLimit-Remaining-Searches", 0))
        rem2 = int(r2.headers.get("X-RateLimit-Remaining-Searches", 0))
        assert rem2 < rem1


class TestRateLimitByPlan:
    def test_enterprise_unlimited(self):
        """Enterprise plan should have unlimited searches."""
        token = create_token(999, "enterprise@test.com", "enterprise")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/v1/search/validate/11222333000181",
            headers=headers,
        )
        assert response.status_code == 200
        # Enterprise has -1 (unlimited), no remaining header
        remaining = response.headers.get("X-RateLimit-Remaining-Searches")
        assert remaining is None  # unlimited doesn't set header

    def test_authenticated_pro_has_higher_limit(self):
        """Pro plan should have 500 searches/day."""
        token = create_token(998, "pro@test.com", "pro")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/v1/search/validate/11222333000181",
            headers=headers,
        )
        assert response.status_code == 200
        remaining = int(response.headers.get("X-RateLimit-Remaining-Searches", 0))
        assert remaining > 50  # Pro has 500, should have plenty left


class TestRateLimitResponse:
    def test_429_includes_details(self):
        """When limit exceeded, response should include plan info."""
        from app.middleware.rate_limit import _search_bucket

        # Manually fill the bucket to trigger 429
        test_key = "search:ratelimit-test@example.com"
        import time
        for _ in range(15):
            _search_bucket._counts[test_key].append(time.time())

        token = create_token(997, "ratelimit-test@example.com", "free")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/api/v1/search/validate/11222333000181",
            headers=headers,
        )
        assert response.status_code == 429
        data = response.json()
        assert "plan" in data
        assert data["plan"] == "free"
        assert "upgrade_hint" in data
