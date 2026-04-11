# AgroJus — Arquitetura Multi-Agente

Data: 2026-04-11
Status: Aprovado

## Visao Geral

O desenvolvimento do AgroJus e distribuido entre 7 agentes autonomos que se comunicam via arquivos no repositorio. Nenhum agente fala diretamente com outro — o Supra Gerente e o hub de coordenacao.

## Agentes

| # | Agente | Modelo/Plataforma | Responsabilidade |
|---|--------|-------------------|------------------|
| 1 | **Supra Gerente** | Claude Opus 4.6 | Priorizacao, coordenacao, docs de handoff, roadmap |
| 2 | **Dev Backend** | Claude Opus 4.6 (Claude Code) | Codigo FastAPI, endpoints, services, models |
| 3 | **Dev Frontend** | Antigravity (Gemini 2.5 Pro) | Next.js 14, React, Leaflet, UI/UX |
| 4 | **QA & Testes** | Claude Opus 4.6 | Cobertura, testes de resiliencia, CI config |
| 5 | **Data Engineer** | Claude Opus 4.6 | Novos collectors, imports CSV, fontes publicas |
| 6 | **DevOps** | Claude Opus 4.6 | Docker, PostgreSQL, deploy, CI/CD pipeline |
| 7 | **Pesquisador** | Claude Opus 4.6 | APIs gov, fontes de dados, benchmarks concorrentes |
| 8 | **UX/Product Designer** | A definir | Wireframes, fluxos, UX copy, consistencia visual |
| 9 | **Tech Writer** | Claude Opus 4.6 | Documentacao tecnica, API docs, changelog, guias |
| 10 | **Security Reviewer** | Claude Opus 4.6 | Audit OWASP, JWT, input validation, dependencias |

## Estrutura de Comunicacao

```
agrojus/docs/coordination/
├── ARCHITECTURE.md         ← Este arquivo
├── ROADMAP.md              ← Supra Gerente mantem
├── BACKLOG.md              ← Tarefas priorizadas por agente
├── HANDOFF.md              ← Mensagens entre agentes
├── DECISIONS.md            ← Decisoes de arquitetura tomadas
├── API_CONTRACT.md         ← Contrato backend<->frontend
├── agents/
│   ├── backend.md          ← Estado, progresso, bloqueios
│   ├── frontend.md         ← Estado do Antigravity
│   ├── qa.md               ← Cobertura, falhas, plano
│   ├── data-engineer.md    ← Fontes integradas/pendentes
│   ├── devops.md           ← Infra, deploy, ambientes
│   ├── researcher.md       ← Fontes descobertas, APIs testadas
│   ├── ux-designer.md      ← Wireframes, fluxos, UX copy
│   ├── tech-writer.md      ← Docs tecnicas, changelog, guias
│   └── security.md         ← Audit OWASP, vulnerabilidades
```

## Fluxo de Trabalho

```
1. SUPRA GERENTE le todos os agents/*.md
2. Atualiza BACKLOG.md com prioridades
3. Escreve tarefas em HANDOFF.md para cada agente
4. Cada agente ao iniciar sessao:
   a. Le seu agents/[nome].md
   b. Le HANDOFF.md (filtra mensagens para ele)
   c. Executa tarefas
   d. Atualiza agents/[nome].md com progresso
   e. Escreve em HANDOFF.md se precisa de algo de outro agente
5. SUPRA GERENTE revisa e redistribui
```

## Regras de Coordenacao

1. **Nenhum agente muda codigo de outro** — Backend nao mexe em frontend, e vice-versa
2. **Contrato antes de codigo** — Novo endpoint? Primeiro API_CONTRACT.md, depois implementacao
3. **Bloqueio explicito** — Se um agente depende de outro, registra em HANDOFF.md
4. **Progresso atomico** — Cada agente atualiza seu `agents/*.md` ao final de cada sessao
5. **Supra Gerente nao codifica** — So coordena, prioriza, e resolve conflitos
6. **Branch por agente** — Cada agente trabalha em sua branch, merge via PR

## Contexto Inicial por Agente

### Dev Backend
- Codebase: `agrojus/backend/` (54 arquivos Python, 75 endpoints)
- Stack: FastAPI, SQLAlchemy, GeoAlchemy2, httpx async, Pydantic
- Estado: v0.5.0, 13 fontes reais funcionando, auth JWT, rate limiting

### Dev Frontend
- Codebase: repo separado ou `agrojus/frontend/` (a definir)
- Stack: Next.js 14+, TypeScript, Tailwind, shadcn/ui, react-leaflet
- Estado: layout, home, mapa, dashboard construidos (Antigravity)
- Contrato: API_CONTRACT.md

### QA & Testes
- Codebase: `agrojus/backend/tests/` (11 arquivos, 82 testes)
- Foco: cobertura dos endpoints sem teste, testes de resiliencia, pytest-cov
- Meta: 90%+ cobertura, testes para timeout/500/JSON invalido

### Data Engineer
- Codebase: `agrojus/backend/app/collectors/` (18 collectors)
- Foco imediato: IBAMA coords CSV, Lista Suja CSV real, shapefiles UCs/Quilombolas
- Foco medio prazo: CONAB, precos terra, IBAMA 168MB import

### DevOps
- Arquivos: Dockerfile, alembic/, docker-compose (existente mas nao testado)
- Foco: PostgreSQL+PostGIS funcional, docker-compose testado, CI/CD GitHub Actions
- Meta: `docker compose up` sobe tudo

### Pesquisador
- Docs: `agrojus/docs/DATA_SOURCES.md`, `PUBLIC_DATA_FULL_REPORT.md`, `VERIFIED_SOURCES.md`
- Foco: testar APIs gov que mudaram, descobrir novas fontes, validar acessibilidade
- Entregavel: atualizar VERIFIED_SOURCES.md e DATA_MAP.md
