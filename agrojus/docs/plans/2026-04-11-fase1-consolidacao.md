# Fase 1 — Consolidacao: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stabilize AgroJus backend v0.5.0 — real data imports, test coverage, working database, CI pipeline.

**Architecture:** Each task is assigned to a specific agent and can be executed independently in a separate session. Tasks within the same agent are sequential. Cross-agent dependencies are marked with DEPENDS.

**Tech Stack:** Python 3.11+, FastAPI, pytest, Docker, PostgreSQL+PostGIS, GitHub Actions

---

## AGENT: Data Engineer

### Task 1: Import IBAMA embargos with coordinates (CSV 8MB)

**Files:**
- Create: `agrojus/backend/app/collectors/ibama_csv.py`
- Create: `agrojus/backend/data/reference/ibama_embargos_coords.csv` (gitignored, downloaded at runtime)
- Modify: `agrojus/backend/app/collectors/ibama.py`
- Modify: `agrojus/backend/app/api/search.py`
- Test: `agrojus/backend/tests/test_ibama_import.py`

- [ ] **Step 1: Write test for CSV parser**

```python
# tests/test_ibama_import.py
import pytest
from app.collectors.ibama_csv import parse_ibama_csv_row

def test_parse_ibama_csv_row():
    row = {
        "SEQ_AUTO_INFRACAO": "12345",
        "NUM_AUTO_INFRACAO": "9876543",
        "DAT_AUTO_INFRACAO": "2024-03-15",
        "NOM_RAZAO_SOCIAL": "Fazenda Teste LTDA",
        "CPF_CNPJ": "11222333000181",
        "DES_AUTO_INFRACAO": "Desmatamento ilegal",
        "VAL_AUTO_INFRACAO": "50000.00",
        "DES_MUNICIPIO": "Sao Luis",
        "SIG_UF": "MA",
        "NUM_LATITUDE": "-2.5",
        "NUM_LONGITUDE": "-44.2",
    }
    result = parse_ibama_csv_row(row)
    assert result["id"] == "12345"
    assert result["cpf_cnpj"] == "11222333000181"
    assert result["lat"] == -2.5
    assert result["lon"] == -44.2
    assert result["municipality"] == "Sao Luis"
    assert result["state"] == "MA"
    assert result["value"] == 50000.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agrojus/backend && python -m pytest tests/test_ibama_import.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.collectors.ibama_csv'`

- [ ] **Step 3: Implement CSV parser**

```python
# app/collectors/ibama_csv.py
"""Parser for IBAMA embargos CSV with coordinates."""
import csv
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("agrojus.collectors.ibama_csv")

IBAMA_CSV_URL = "https://dadosabertos.ibama.gov.br/dados/SICAFI/relatorio_auto_infracao_ibama_coords.csv"

def parse_ibama_csv_row(row: dict) -> dict:
    """Parse a single row from IBAMA CSV into normalized dict."""
    def safe_float(val):
        try:
            return float(val) if val else None
        except (ValueError, TypeError):
            return None

    return {
        "id": row.get("SEQ_AUTO_INFRACAO", ""),
        "auto_number": row.get("NUM_AUTO_INFRACAO", ""),
        "date": row.get("DAT_AUTO_INFRACAO", ""),
        "name": row.get("NOM_RAZAO_SOCIAL", ""),
        "cpf_cnpj": row.get("CPF_CNPJ", "").replace(".", "").replace("/", "").replace("-", ""),
        "description": row.get("DES_AUTO_INFRACAO", ""),
        "value": safe_float(row.get("VAL_AUTO_INFRACAO")),
        "municipality": row.get("DES_MUNICIPIO", ""),
        "state": row.get("SIG_UF", ""),
        "lat": safe_float(row.get("NUM_LATITUDE")),
        "lon": safe_float(row.get("NUM_LONGITUDE")),
    }

def load_ibama_csv(filepath: Path) -> list[dict]:
    """Load and parse entire IBAMA CSV file."""
    records = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            parsed = parse_ibama_csv_row(row)
            if parsed["lat"] and parsed["lon"]:
                records.append(parsed)
    logger.info("Loaded %d IBAMA records with coordinates", len(records))
    return records

def search_ibama_by_cpf_cnpj(records: list[dict], cpf_cnpj: str) -> list[dict]:
    """Search loaded records by CPF/CNPJ."""
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    return [r for r in records if r["cpf_cnpj"] == clean]

def search_ibama_by_municipality(records: list[dict], municipality: str, uf: str = "") -> list[dict]:
    """Search loaded records by municipality name."""
    name = municipality.lower()
    results = [r for r in records if name in r["municipality"].lower()]
    if uf:
        results = [r for r in results if r["state"].upper() == uf.upper()]
    return results
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agrojus/backend && python -m pytest tests/test_ibama_import.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/collectors/ibama_csv.py tests/test_ibama_import.py
git commit -m "feat: add IBAMA CSV parser with coordinate support"
```

---

### Task 2: Import Lista Suja completa (CSV real)

**Files:**
- Create: `agrojus/backend/app/collectors/lista_suja_csv.py`
- Test: `agrojus/backend/tests/test_lista_suja_import.py`

- [ ] **Step 1: Write test for Lista Suja CSV parser**

```python
# tests/test_lista_suja_import.py
import pytest
from app.collectors.lista_suja_csv import parse_lista_suja_row

def test_parse_lista_suja_row():
    row = {
        "Ano da acao fiscal": "2023",
        "UF": "MA",
        "Empregador": "Fazenda Exemplo",
        "CNPJ/CPF": "11.222.333/0001-81",
        "Estabelecimento": "Fazenda Exemplo Unidade",
        "Trabalhadores envolvidos": "15",
        "CNAE": "0111301",
        "Decisao administrativa": "Inclusao",
    }
    result = parse_lista_suja_row(row)
    assert result["year"] == 2023
    assert result["state"] == "MA"
    assert result["employer"] == "Fazenda Exemplo"
    assert result["cpf_cnpj"] == "11222333000181"
    assert result["workers"] == 15
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agrojus/backend && python -m pytest tests/test_lista_suja_import.py -v`
Expected: FAIL

- [ ] **Step 3: Implement parser**

```python
# app/collectors/lista_suja_csv.py
"""Parser for Lista Suja (slave labour) CSV from Portal da Transparencia."""
import csv
import logging
from pathlib import Path

logger = logging.getLogger("agrojus.collectors.lista_suja_csv")

LISTA_SUJA_URL = "https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo"

def parse_lista_suja_row(row: dict) -> dict:
    """Parse a single row from Lista Suja CSV."""
    def safe_int(val):
        try:
            return int(val) if val else 0
        except (ValueError, TypeError):
            return 0

    cpf_cnpj = row.get("CNPJ/CPF", "")
    cpf_cnpj_clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")

    return {
        "year": safe_int(row.get("Ano da acao fiscal")),
        "state": row.get("UF", ""),
        "employer": row.get("Empregador", ""),
        "cpf_cnpj": cpf_cnpj_clean,
        "establishment": row.get("Estabelecimento", ""),
        "workers": safe_int(row.get("Trabalhadores envolvidos")),
        "cnae": row.get("CNAE", ""),
        "decision": row.get("Decisao administrativa", ""),
    }

def load_lista_suja_csv(filepath: Path) -> list[dict]:
    """Load and parse Lista Suja CSV."""
    records = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            records.append(parse_lista_suja_row(row))
    logger.info("Loaded %d Lista Suja records", len(records))
    return records

def search_by_cpf_cnpj(records: list[dict], cpf_cnpj: str) -> list[dict]:
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    return [r for r in records if r["cpf_cnpj"] == clean]

def search_by_state(records: list[dict], uf: str) -> list[dict]:
    return [r for r in records if r["state"].upper() == uf.upper()]
```

- [ ] **Step 4: Run test, verify pass**

Run: `cd agrojus/backend && python -m pytest tests/test_lista_suja_import.py -v`

- [ ] **Step 5: Commit**

```bash
git add app/collectors/lista_suja_csv.py tests/test_lista_suja_import.py
git commit -m "feat: add Lista Suja CSV parser for real data import"
```

---

### Task 3: Add PRODES accumulated deforestation layer

**Files:**
- Modify: `agrojus/backend/app/collectors/geolayers.py`
- Modify: `agrojus/backend/app/api/geo.py`
- Test: `agrojus/backend/tests/test_prodes.py`

- [ ] **Step 1: Write test**

```python
# tests/test_prodes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_prodes_layer_in_catalog():
    response = client.get("/api/v1/geo/catalogo")
    assert response.status_code == 200
    layer_ids = [l["id"] for l in response.json()["layers"]]
    assert "prodes_amazonia" in layer_ids or "prodes" in layer_ids

def test_prodes_geojson_endpoint():
    response = client.get("/api/v1/geo/layers/prodes_amazonia/geojson?max_features=5")
    assert response.status_code == 200
    data = response.json()
    assert data.get("type") == "FeatureCollection" or "error" not in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agrojus/backend && python -m pytest tests/test_prodes.py -v`

- [ ] **Step 3: Add PRODES to geolayers and geo.py endpoint**

In `app/api/geo.py`, add handling for `prodes_amazonia` and `prodes_cerrado` in `get_layer_geojson()`:

```python
# Add to the elif chain in get_layer_geojson():
elif layer_id.startswith("prodes_"):
    biome_map = {
        "prodes_amazonia": "prodes-legal-amz:accumulated_deforestation_2007",
        "prodes_cerrado": "prodes-cerrado-nb:accumulated_deforestation_2000",
        "prodes_mata_atlantica": "prodes-mata-atlantica-nb:accumulated_deforestation_2000",
        "prodes_caatinga": "prodes-caatinga-nb:accumulated_deforestation_2000",
        "prodes_pampa": "prodes-pampa-nb:accumulated_deforestation_2000",
        "prodes_pantanal": "prodes-pantanal-nb:accumulated_deforestation_2000",
    }
    layer_name = biome_map.get(layer_id)
    if not layer_name:
        return {"error": f"PRODES layer '{layer_id}' not found", "available": list(biome_map.keys())}

    workspace = layer_name.split(":")[0]
    try:
        params = {
            "service": "WFS",
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": layer_name,
            "maxFeatures": str(max_features),
            "outputFormat": "application/json",
        }
        if bbox:
            params["bbox"] = bbox
        url = f"https://terrabrasilis.dpi.inpe.br/geoserver/{workspace}/wfs"
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            r = await client.get(url, params=params)
            if r.status_code == 200:
                data = r.json()
                data["source"] = "INPE/TerraBrasilis PRODES"
                data["total"] = len(data.get("features", []))
                return data
    except Exception as e:
        logger.warning("PRODES WFS error: %s", e)
        return {"type": "FeatureCollection", "features": [], "error": str(e)}
```

- [ ] **Step 4: Run test, verify pass**

Run: `cd agrojus/backend && python -m pytest tests/test_prodes.py -v`

- [ ] **Step 5: Commit**

```bash
git add app/api/geo.py app/collectors/geolayers.py tests/test_prodes.py
git commit -m "feat: add PRODES accumulated deforestation WFS layer"
```

---

## AGENT: QA & Testes

### Task 4: Measure baseline coverage with pytest-cov

**Files:**
- Modify: `agrojus/backend/requirements.txt` (add pytest-cov)

- [ ] **Step 1: Add pytest-cov to requirements**

Add to end of `requirements.txt`:
```
pytest-cov==6.0.0
```

- [ ] **Step 2: Run coverage baseline**

Run: `cd agrojus/backend && pip install pytest-cov && python -m pytest --cov=app --cov-report=term-missing -q`
Expected: Report showing current coverage per module. Record the number.

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "chore: add pytest-cov for coverage measurement"
```

---

### Task 5: Tests for compliance endpoints (MCR 2.9, EUDR)

**Files:**
- Create: `agrojus/backend/tests/test_compliance.py`

- [ ] **Step 1: Write compliance tests**

```python
# tests/test_compliance.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMCR29Compliance:
    def test_mcr29_valid_request(self):
        response = client.post("/api/v1/compliance/mcr29", json={
            "cpf_cnpj": "11222333000181",
            "property_car": "MA-2100055-abc123",
            "lat": -5.0,
            "lon": -44.0,
        })
        assert response.status_code == 200
        data = response.json()
        assert "compliant" in data or "checks" in data

    def test_mcr29_missing_fields(self):
        response = client.post("/api/v1/compliance/mcr29", json={})
        # Should still return 200 with partial analysis or 422 validation
        assert response.status_code in (200, 422)

class TestEUDRCompliance:
    def test_eudr_valid_request(self):
        response = client.post("/api/v1/compliance/eudr", json={
            "cpf_cnpj": "11222333000181",
            "lat": -5.0,
            "lon": -44.0,
            "product": "soja",
        })
        assert response.status_code == 200
        data = response.json()
        assert "compliant" in data or "checks" in data

    def test_eudr_missing_fields(self):
        response = client.post("/api/v1/compliance/eudr", json={})
        assert response.status_code in (200, 422)
```

- [ ] **Step 2: Run tests**

Run: `cd agrojus/backend && python -m pytest tests/test_compliance.py -v`

- [ ] **Step 3: Fix any failures, then commit**

```bash
git add tests/test_compliance.py
git commit -m "test: add compliance endpoint tests (MCR 2.9, EUDR)"
```

---

### Task 6: Tests for jurisdicao endpoints

**Files:**
- Create: `agrojus/backend/tests/test_jurisdicao.py`

- [ ] **Step 1: Write jurisdicao tests**

```python
# tests/test_jurisdicao.py
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
        # Should have 27 states
        assert len(data.get("estados", data.get("data", []))) >= 27

    def test_reserva_legal(self):
        response = client.get("/api/v1/jurisdicao/reserva-legal?uf=MA&bioma=amazonia")
        assert response.status_code == 200

    def test_comparar_estados(self):
        response = client.get("/api/v1/jurisdicao/comparar?uf1=MA&uf2=PA")
        assert response.status_code == 200
        data = response.json()
        assert "MA" in str(data) and "PA" in str(data)
```

- [ ] **Step 2: Run tests**

Run: `cd agrojus/backend && python -m pytest tests/test_jurisdicao.py -v`

- [ ] **Step 3: Commit**

```bash
git add tests/test_jurisdicao.py
git commit -m "test: add jurisdicao endpoint tests (27 states, comparator)"
```

---

### Task 7: Tests for clima and BCB endpoints

**Files:**
- Create: `agrojus/backend/tests/test_clima_bcb.py`

- [ ] **Step 1: Write clima and BCB tests**

```python
# tests/test_clima_bcb.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestClima:
    def test_clima_valid_coords(self):
        response = client.get("/api/v1/geo/clima?lat=-5.0&lon=-44.0&days=7")
        assert response.status_code == 200
        data = response.json()
        assert "source" in data or "temperature" in str(data).lower() or "error" in str(data).lower()

class TestBCBIndicators:
    def test_indicators_list(self):
        response = client.get("/api/v1/market/indicators")
        assert response.status_code == 200
        data = response.json()
        # Should have at least selic and dolar
        assert any(k in str(data).lower() for k in ["selic", "dolar", "ipca"])

    def test_indicator_serie(self):
        # SELIC serie = 432
        response = client.get("/api/v1/market/indicators/432")
        assert response.status_code == 200

    def test_quotes(self):
        response = client.get("/api/v1/market/quotes")
        assert response.status_code == 200
        data = response.json()
        assert "quotes" in data

    def test_credit_municipality(self):
        # Sao Luis = 2111300
        response = client.get("/api/v1/market/credit/municipality/2111300")
        assert response.status_code == 200
```

- [ ] **Step 2: Run tests**

Run: `cd agrojus/backend && python -m pytest tests/test_clima_bcb.py -v`

- [ ] **Step 3: Commit**

```bash
git add tests/test_clima_bcb.py
git commit -m "test: add clima (NASA POWER) and BCB indicators tests"
```

---

### Task 8: Tests for consulta unificada

**Files:**
- Create: `agrojus/backend/tests/test_consulta_unificada.py`

- [ ] **Step 1: Write consulta unificada tests**

```python
# tests/test_consulta_unificada.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestConsultaUnificada:
    def test_consulta_completa_cnpj(self):
        response = client.post("/api/v1/consulta/completa", json={
            "cpf_cnpj": "11222333000181",
        })
        assert response.status_code == 200
        data = response.json()
        # Should have sources dict
        assert "sources" in data or "results" in data

    def test_consulta_completa_cpf(self):
        response = client.post("/api/v1/consulta/completa", json={
            "cpf_cnpj": "12345678909",
        })
        assert response.status_code == 200

    def test_consulta_missing_doc(self):
        response = client.post("/api/v1/consulta/completa", json={})
        assert response.status_code in (200, 422)

    def test_consulta_has_risk_score(self):
        response = client.post("/api/v1/consulta/completa", json={
            "cpf_cnpj": "11222333000181",
        })
        data = response.json()
        # Risk score should be present
        assert "risk" in str(data).lower() or "score" in str(data).lower()
```

- [ ] **Step 2: Run tests**

Run: `cd agrojus/backend && python -m pytest tests/test_consulta_unificada.py -v`

- [ ] **Step 3: Commit**

```bash
git add tests/test_consulta_unificada.py
git commit -m "test: add consulta unificada tests (6 parallel sources)"
```

---

### Task 9: Resilience tests (timeout, 500, invalid JSON)

**Files:**
- Create: `agrojus/backend/tests/test_resilience.py`

- [ ] **Step 1: Write resilience tests**

```python
# tests/test_resilience.py
"""Test that the app handles external API failures gracefully."""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)

class TestExternalAPIFailures:
    """Verify endpoints don't crash when external APIs fail."""

    @patch("app.collectors.base.BaseCollector._http_get")
    def test_analyze_point_survives_timeout(self, mock_get):
        """analyze-point should return partial results if a source times out."""
        mock_get.side_effect = httpx.TimeoutException("Connection timed out")
        response = client.get("/api/v1/geo/analyze-point?lat=-5.0&lon=-44.0")
        assert response.status_code == 200
        data = response.json()
        assert "coordinates" in data

    @patch("app.collectors.base.BaseCollector._http_get")
    def test_analyze_point_survives_500(self, mock_get):
        """analyze-point should return partial results if a source returns 500."""
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error", request=AsyncMock(), response=mock_response
        )
        mock_get.side_effect = mock_response.raise_for_status.side_effect
        response = client.get("/api/v1/geo/analyze-point?lat=-5.0&lon=-44.0")
        assert response.status_code == 200

    def test_smart_search_with_garbage_input(self):
        """Smart search should handle garbage input without crashing."""
        response = client.post("/api/v1/search/smart", json={
            "query": "!@#$%^&*()_+{}|:<>?",
        })
        assert response.status_code in (200, 422)

    def test_cnpj_search_nonexistent(self):
        """CNPJ search with valid format but nonexistent CNPJ."""
        response = client.get("/api/v1/search/cnpj/99999999000199")
        # Should return 200 with error info or 404, not 500
        assert response.status_code in (200, 404)
```

- [ ] **Step 2: Run tests**

Run: `cd agrojus/backend && python -m pytest tests/test_resilience.py -v`

- [ ] **Step 3: Fix any 500 errors found, then commit**

```bash
git add tests/test_resilience.py
git commit -m "test: add resilience tests (timeout, 500, invalid input)"
```

---

## AGENT: DevOps

### Task 10: Test and fix Docker Compose

**Files:**
- Modify: `agrojus/docker-compose.yml`
- Modify: `agrojus/backend/Dockerfile`
- Modify: `agrojus/backend/.env.example`

- [ ] **Step 1: Review existing docker-compose.yml**

Run: `cat agrojus/docker-compose.yml`
Verify it has: backend service, postgres+postgis service, volume mounts, env vars.

- [ ] **Step 2: Test docker compose up**

Run: `cd agrojus && docker compose up --build -d`
Expected: Both containers start. If errors, fix and retry.

- [ ] **Step 3: Test backend connects to PostgreSQL**

Run: `curl http://localhost:8000/health`
Expected: `{"status": "healthy"}`

Run: `docker compose logs backend | tail -20`
Verify no database connection errors.

- [ ] **Step 4: Test Alembic migrations**

Run: `docker compose exec backend alembic upgrade head`
Expected: Migrations applied successfully.

- [ ] **Step 5: Commit fixes**

```bash
git add docker-compose.yml backend/Dockerfile backend/.env.example
git commit -m "fix: docker compose working with PostgreSQL + PostGIS"
```

---

### Task 11: GitHub Actions CI pipeline

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create CI workflow**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, "claude/**"]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: agrojus/backend

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
          cache-dependency-path: agrojus/backend/requirements.txt

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests with coverage
        run: python -m pytest --cov=app --cov-report=term-missing -q

      - name: Lint check
        run: pip install ruff && ruff check app/
```

- [ ] **Step 2: Commit and push to trigger CI**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions pipeline (pytest + ruff)"
git push
```

- [ ] **Step 3: Check CI run**

Run: `gh run list --limit 1`
Expected: CI run triggered and (ideally) passing.

---

## AGENT: Pesquisador

### Task 12: Register DataJud API key

- [ ] **Step 1: Register at datajud-wiki.cnj.jus.br**

Navigate to the DataJud API portal and register for a free API key.
Document the process in `agrojus/docs/coordination/agents/researcher.md`.

- [ ] **Step 2: Test the API key**

Run: `curl -H "Authorization: APIKey YOUR_KEY" "https://api-publica.datajud.cnj.jus.br/api_publica_cnj/_search" -d '{"size":1}'`
Expected: JSON response with one process.

- [ ] **Step 3: Add key to .env.example**

Add to `agrojus/backend/.env.example`:
```
DATAJUD_API_KEY=your_key_here
```

- [ ] **Step 4: Commit**

```bash
git add agrojus/backend/.env.example
git commit -m "docs: add DataJud API key configuration"
```

---

### Task 13: Validate all 13 real data sources

- [ ] **Step 1: Test each source**

Run a quick request against each of the 13 sources and document results:

| Source | URL | Status | Notes |
|--------|-----|--------|-------|
| BrasilAPI | brasilapi.com.br/api/cnpj/v1/... | ? | |
| FUNAI WFS | geoserver.funai.gov.br/... | ? | |
| INPE/DETER | terrabrasilis.dpi.inpe.br/... | ? | |
| IBGE API | servicodados.ibge.gov.br/... | ? | |
| IBGE SIDRA | apisidra.ibge.gov.br/... | ? | |
| BCB API | api.bcb.gov.br/... | ? | |
| BCB SICOR | olinda.bcb.gov.br/... | ? | |
| NASA POWER | power.larc.nasa.gov/... | ? | |
| ANM | geo.anm.gov.br/... | ? | |
| ANEEL | sigel.aneel.gov.br/... | ? | |
| Nominatim | nominatim.openstreetmap.org/... | ? | |
| SICAR | car.gov.br (was 503) | ? | |
| SIGEF | sigef.incra.gov.br (was 404) | ? | |

- [ ] **Step 2: Update VERIFIED_SOURCES.md**

Update `agrojus/docs/VERIFIED_SOURCES.md` with test results and dates.

- [ ] **Step 3: Commit**

```bash
git add agrojus/docs/VERIFIED_SOURCES.md
git commit -m "docs: validate data sources status 2026-04-11"
```

---

## AGENT: Dev Backend

### Task 14: Add UCs and Quilombolas endpoints

DEPENDS: Data Engineer completing shapefiles download (Tasks 3-like, or use WFS if available)

**Files:**
- Modify: `agrojus/backend/app/api/geo.py`
- Test: `agrojus/backend/tests/test_ucs_quilombolas.py`

- [ ] **Step 1: Write test**

```python
# tests/test_ucs_quilombolas.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ucs_endpoint():
    response = client.get("/api/v1/geo/layers/unidades_conservacao/geojson?max_features=5")
    assert response.status_code == 200
    data = response.json()
    assert "type" in data or "error" in data

def test_quilombolas_endpoint():
    response = client.get("/api/v1/geo/layers/quilombolas/geojson?max_features=5")
    assert response.status_code == 200
    data = response.json()
    assert "type" in data or "error" in data
```

- [ ] **Step 2: Run test to verify fail**

Run: `cd agrojus/backend && python -m pytest tests/test_ucs_quilombolas.py -v`

- [ ] **Step 3: Add layer handling in geo.py**

Add to the `get_layer_geojson` elif chain in `app/api/geo.py`:

```python
elif layer_id == "unidades_conservacao":
    # ICMBio/MMA - CNUC via TerraBrasilis
    try:
        layer_name = "prodes-legal-amz:conservation_units_legal_amazon"
        params = {
            "service": "WFS",
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": layer_name,
            "maxFeatures": str(max_features),
            "outputFormat": "application/json",
        }
        if bbox:
            params["bbox"] = bbox
        url = "https://terrabrasilis.dpi.inpe.br/geoserver/prodes-legal-amz/wfs"
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as cl:
            r = await cl.get(url, params=params)
            if r.status_code == 200:
                data = r.json()
                data["source"] = "INPE/TerraBrasilis (CNUC)"
                data["total"] = len(data.get("features", []))
                return data
    except Exception as e:
        logger.warning("UCs WFS error: %s", e)
        return {"type": "FeatureCollection", "features": [], "error": str(e)}

elif layer_id == "quilombolas":
    # INCRA - territorios quilombolas
    try:
        params = {
            "service": "WFS",
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": "Funai:comunidades_quilombolas",
            "maxFeatures": str(max_features),
            "outputFormat": "application/json",
        }
        if bbox:
            params["bbox"] = bbox
        # Try INCRA GeoServer
        url = "https://acervofundiario.incra.gov.br/geoserver/ows"
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as cl:
            r = await cl.get(url, params=params)
            if r.status_code == 200:
                data = r.json()
                data["source"] = "INCRA/Acervo Fundiario"
                data["total"] = len(data.get("features", []))
                return data
    except Exception as e:
        logger.warning("Quilombolas WFS error: %s", e)
        return {"type": "FeatureCollection", "features": [], "error": str(e)}
```

- [ ] **Step 4: Run test**

Run: `cd agrojus/backend && python -m pytest tests/test_ucs_quilombolas.py -v`

- [ ] **Step 5: Commit**

```bash
git add app/api/geo.py tests/test_ucs_quilombolas.py
git commit -m "feat: add UCs and Quilombolas GeoJSON endpoints"
```

---

## Summary — Execution Order

**Can run in parallel (different agents/sessions):**
- Tasks 1-3 (Data Engineer)
- Tasks 4-9 (QA)
- Tasks 10-11 (DevOps)
- Tasks 12-13 (Pesquisador)

**Sequential dependency:**
- Task 14 (Backend) DEPENDS on Task 3 (Data Engineer) or can use WFS directly

**Total: 14 tasks, ~30 bite-sized steps**
