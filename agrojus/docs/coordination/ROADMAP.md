# AgroJus — Roadmap

Atualizado: 2026-04-11
Responsavel: Supra Gerente

## Fase 1 — Consolidacao (atual)

Objetivo: Estabilizar o backend v0.5.0, conectar banco real, cobertura de testes.

| Tarefa | Agente | Prioridade | Status |
|--------|--------|------------|--------|
| Importar IBAMA embargos coords (CSV 8MB) | Data Engineer | ALTA | Pendente |
| Importar Lista Suja completa (CSV real) | Data Engineer | ALTA | Pendente |
| Shapefiles UCs (ICMBio) | Data Engineer | ALTA | Pendente |
| Shapefiles Quilombolas (INCRA) | Data Engineer | ALTA | Pendente |
| PRODES desmatamento acumulado (WFS) | Data Engineer | MEDIA | Pendente |
| Testes: compliance, jurisdicao, clima, BCB | QA | ALTA | Pendente |
| Testes de resiliencia (timeout, 500, JSON invalido) | QA | ALTA | Pendente |
| pytest-cov — medir cobertura | QA | MEDIA | Pendente |
| Docker Compose funcional (backend + PostgreSQL) | DevOps | ALTA | Pendente |
| Alembic migrations testadas contra PostgreSQL real | DevOps | ALTA | Pendente |
| GitHub Actions CI pipeline | DevOps | MEDIA | Pendente |
| Cadastrar API key DataJud/CNJ | Pesquisador | ALTA | Pendente |
| Validar fontes que mudaram (SICAR, SIGEF) | Pesquisador | MEDIA | Pendente |

## Fase 2 — Integracao Frontend

Objetivo: Frontend consumindo backend via API_CONTRACT.md.

| Tarefa | Agente | Status |
|--------|--------|--------|
| API_CONTRACT.md completo | Supra Gerente + Backend | Pendente |
| Integrar analyze-point no right-click Leaflet | Frontend | Pendente |
| Painel de camadas toggle | Frontend | Pendente |
| Pagina compliance MCR 2.9 / EUDR | Frontend | Pendente |
| Pagina jurisdicao por estado | Frontend | Pendente |
| Graficos serie historica (producao, pecuaria) | Frontend | Pendente |
| Dashboard indicadores BCB | Frontend | Pendente |

## Fase 3 — Deploy e Producao

Objetivo: MVP rodando em cloud acessivel.

| Tarefa | Agente | Status |
|--------|--------|--------|
| Deploy em Render ou AWS | DevOps | Pendente |
| PostgreSQL + PostGIS em producao | DevOps | Pendente |
| CORS restrito ao dominio do frontend | Backend | Pendente |
| Monitoramento com cron (Celery ou APScheduler) | Backend | Pendente |
| HTTPS + dominio proprio | DevOps | Pendente |

## Fase 4 — Expansao

| Tarefa | Agente | Status |
|--------|--------|--------|
| SERPRO API (CPF completo) | Data Engineer | Pendente |
| CENPROT protestos (InfoSimples) | Data Engineer | Pendente |
| CONAB dados (safra, precos, armazens) | Data Engineer | Pendente |
| Roles/permissoes (admin/user/viewer) | Backend | Pendente |
| CAFIR/SNCR scraping Playwright | Data Engineer | Pendente |
