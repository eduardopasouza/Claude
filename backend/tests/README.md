# AgroJus — Testes

Disciplina de teste inspirada no Anti-Vibe Coding (Fabio Akita, 2026).
Não é cobertura por cobertura — é **controle sobre o que funciona e o que
não funciona em cada camada do sistema**.

## Categorias

| Marker | Pasta | Toca rede? | Toca banco? | Roda no CI? |
|---|---|---|---|---|
| `unit` | `tests/unit/` | ❌ | ❌ | ✅ |
| `integration` | `tests/integration/` | ❌ | ✅ (pg_test container) | ✅ |
| `contract` | `tests/contract/` | VCR cassette | ❌ | ✅ |
| `collectors` | `tests/collectors/` | VCR cassette | ✅ | ✅ |
| `live` | qualquer | ✅ upstream real | depende | ❌ (opt-in) |
| `e2e` | `tests/e2e/` | ✅ local | ✅ | ✅ (slow job) |
| `slow` | qualquer | — | — | pulado em fast-run |

## Como rodar

```bash
# Dev loop rápido (só unit)
pytest -m unit

# Dev loop padrão (tudo exceto live e slow)
pytest -m "not live and not slow"

# Auditoria semanal de coletores (bate upstream real)
PYTEST_LIVE=1 pytest -m live --durations=0

# Tudo
pytest

# Com cobertura
pytest --cov=app --cov-report=term-missing

# Paralelo (pytest-xdist)
pytest -n auto -m "not live"

# Só um arquivo
pytest tests/collectors/test_ceis.py -v
```

Targets `make` disponíveis no root do repo:

```bash
make test           # rápido, sem live/slow
make test-all       # tudo com cobertura
make test-live      # auditoria upstream (CI não roda)
make test-coverage  # gera htmlcov/
```

## Como adicionar teste novo

**Unit** (lógica pura, sem I/O):
```python
# tests/unit/test_risk_classifier.py
import pytest
from app.services.juridico import classificar_risco

@pytest.mark.unit
class TestClassificarRisco:
    def test_sem_sancoes_retorna_baixo(self):
        sumario = {"processos_datajud": 0, "autos_ibama": 0, "ceis": 0, "cnep": 0, "lista_suja_mte": 0}
        assert classificar_risco(sumario) == "BAIXO"
```

**Integration** (endpoint + banco):
```python
# tests/integration/test_juridico_api.py
import pytest

@pytest.mark.integration
class TestJuridicoContratos:
    def test_list_contratos_retorna_seeds(self, client, db_session):
        response = client.get("/api/v1/juridico/contratos?limit=3")
        assert response.status_code == 200
        assert response.json()["total"] >= 3
```

**Contract** (API externa via VCR):
```python
# tests/contract/test_datajud.py
import pytest

@pytest.mark.contract
@pytest.mark.vcr
class TestDataJudContract:
    def test_search_cnpj_retorna_processos(self):
        from app.collectors.datajud import buscar_por_cnpj
        result = buscar_por_cnpj("00818544000165")
        assert "records" in result
        assert isinstance(result["records"], list)
```

**Collector** (combina unit + contract + schema):
```python
# tests/collectors/test_ceis.py
import pytest

@pytest.mark.collectors
class TestCeisCollector:
    @pytest.mark.vcr
    def test_download_retorna_schema_esperado(self):
        ...

    @pytest.mark.live
    def test_upstream_ainda_acessivel(self):
        """Opt-in: roda na auditoria semanal."""
        ...
```

## Cassettes VCR

Ficam em `tests/contract/cassettes/<test_module>/<test_name>.yaml`.

Gravar pela primeira vez:
```bash
VCR_RECORD_MODE=once pytest tests/contract/test_datajud.py -v
```

Atualizar quando upstream mudar contrato (com intenção):
```bash
rm tests/contract/cassettes/test_datajud/test_search_cnpj.yaml
VCR_RECORD_MODE=once pytest tests/contract/test_datajud.py::TestDataJud::test_search_cnpj
```

Cassettes **NÃO** devem conter tokens, cookies, CPFs reais — o `vcr_config`
em `conftest.py` filtra `authorization`, `x-api-key`, `cookie` e params
`token`/`api_key`/`access_token`. Se um cassette tiver dado pessoal,
apagar e regravar com um CPF fictício (`faker`).

## Princípios

1. **Determinismo.** Testes que falham "às vezes" são bugs de teste, não do
   código. Usar `freezegun`, cassettes VCR, `faker` com seed fixo.
2. **Um conceito por teste.** Nome descritivo: `test_dossie_retorna_risco_alto_quando_ha_sancao_ceis` > `test_dossie_1`.
3. **Arrange-Act-Assert** em blocos separados por linha em branco.
4. **Fixtures sobre mocks.** `conftest.py` > `unittest.mock` em todo lugar.
5. **Teste o contrato, não a implementação.** Endpoint retorna o JSON
   documentado → ok. Quantas vezes chama `session.query()` internamente →
   irrelevante.
6. **Coleção `live` existe para auditoria**, não para CI. Rodar semanalmente
   ou antes de release para saber se upstream mudou.
