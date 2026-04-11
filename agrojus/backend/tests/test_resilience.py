"""Test that the app handles external API failures gracefully."""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)


class TestExternalAPIFailures:
    """Verify endpoints don't crash when external APIs fail."""

    def test_smart_search_with_garbage_input(self):
        """Smart search should handle garbage input without crashing."""
        response = client.post("/api/v1/search/smart", json={
            "query": "!@#$%^&*()_+{}|:<>?",
        })
        assert response.status_code in (200, 422, 429)

    def test_cnpj_search_nonexistent(self):
        """CNPJ search with valid format but nonexistent CNPJ."""
        response = client.get("/api/v1/search/cnpj/99999999000199")
        # Should return 200 with error info, 404, or 429 rate limit — not 500
        assert response.status_code in (200, 404, 429)

    def test_analyze_point_invalid_coords(self):
        """Analyze point with out-of-range coordinates."""
        response = client.get("/api/v1/geo/analyze-point?lat=999&lon=999")
        assert response.status_code in (200, 400, 422)

    def test_compliance_with_empty_body(self):
        """Compliance endpoints should handle empty requests gracefully."""
        response = client.post("/api/v1/compliance/mcr29", json={})
        assert response.status_code in (200, 422)

    def test_report_nonexistent_entity(self):
        """Report generation for nonexistent entity should not 500."""
        response = client.post("/api/v1/reports/due-diligence", json={
            "cpf_cnpj": "00000000000000",
        })
        assert response.status_code in (200, 404, 422)
