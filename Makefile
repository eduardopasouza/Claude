# AgroJus — Makefile
#
# Alvos principais:
#   make up              sobe dev stack (db + backend)
#   make down            para tudo
#   make logs            tail dos containers
#
#   make test            loop de dev rápido (unit + integration sem live/slow)
#   make test-all        suite completa com cobertura
#   make test-unit       só unit (mais rápido)
#   make test-live       auditoria de coletores (bate upstream)
#   make test-coverage   gera htmlcov/ abrir em navegador
#
#   make test-up         sobe db_test isolado (porta 5433)
#   make test-down       derruba db_test e limpa volume
#
#   make lint            ruff check no backend
#   make typecheck       tsc --noEmit no frontend
#   make audit-coletores gera docs/AUDITORIA_COLETORES_YYYYMMDD.md do live run
#
# Convenção Anti-Vibe Coding: cada PR/commit deve sair com `make test`
# passando antes de push. CI replica o mesmo comando.

.PHONY: help up down logs rebuild \
        test test-all test-unit test-live test-coverage test-up test-down \
        lint typecheck audit-coletores \
        frontend-dev frontend-build frontend-test

help:
	@echo "AgroJus — veja comentários no topo do Makefile"

# ---- Dev stack ----

up:
	docker compose up -d
	@echo "Backend em http://localhost:8000  ·  DB em localhost:5432"

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

rebuild:
	docker compose build --no-cache backend

# ---- Testes ----

test-up:
	docker compose -f docker-compose.test.yml up -d
	@sleep 2
	@echo "db_test pronto em localhost:5433"

test-down:
	docker compose -f docker-compose.test.yml down -v

test: test-up
	cd backend && pytest -m "not live and not slow" -q

test-unit:
	cd backend && pytest -m unit -q

test-all: test-up
	cd backend && pytest --cov=app --cov-report=term-missing --cov-report=html

test-live:
	@echo ">>> Rodando suite LIVE (bate upstream real). Requer internet."
	cd backend && PYTEST_LIVE=1 pytest -m live --durations=0

test-coverage: test-all
	@echo "Relatório em backend/htmlcov/index.html"

# ---- Qualidade ----

lint:
	cd backend && ruff check app/

typecheck:
	cd frontend_v2 && npx tsc --noEmit

# ---- Auditoria ----

audit-coletores:
	@echo ">>> Auditoria de coletores via pytest --json-report"
	cd backend && PYTEST_LIVE=1 pytest tests/collectors/ -m live --json-report \
		--json-report-file=../docs/_generated/audit-latest.json || true
	@echo "Saída em docs/_generated/audit-latest.json"
	python scripts/audit_report_from_pytest.py

# ---- Frontend ----

frontend-dev:
	cd frontend_v2 && npm run dev

frontend-build:
	cd frontend_v2 && npm run build

frontend-test:
	cd frontend_v2 && npm run test
