# AgroJus — Prompt de Continuidade para Nova Sessão

> **Leia este arquivo primeiro.** É o ponto de entrada para qualquer nova sessão de desenvolvimento.
> Atualizado: 2026-04-15 (03:27 BRT)

---

## 🚀 Como retomar o trabalho

```bash
# 1. Subir infraestrutura
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# 2. Verificar banco de dados
docker exec agrojus-backend-1 python scripts/db_inventory.py

# 3. Subir frontend
cd frontend && npm run dev   # → http://localhost:5173

# 4. Verificar backend
curl http://localhost:8000/api/v1/dashboard/metrics
```

---

## 📁 Mapa de Documentação

| Documento | O que contém | Quando ler |
|---|---|---|
| `docs/CONTEXTO_COMPLETO.md` | **Briefing primário** — produto, 5 módulos, concorrentes, fontes, padrões de código | **Sempre, em primeiro lugar** |
| `docs/PESQUISA_FONTES.md` | Guia técnico profundo de CADA fonte de dados — dados.gov, basedosdados, MapBiomas 18 produtos, IBAMA, ANA, BCB, ONR | Antes de qualquer ETL |
| `docs/coordination/ROADMAP.md` | Status dos 5 módulos + 30 pendências de dados + 14 pendências de código | Para decidir o que fazer |
| `docs/HANDOFF_2026-04-15.md` | Estado técnico atual do sistema — tabelas, APIs, commits | Para entender onde parou |
| `docs/ARCHITECTURE.md` | Arquitetura técnica da plataforma | Antes de mudanças estruturais |
| `docs/FRONTEND_SPEC.md` | Especificação detalhada do frontend | Antes de trabalho no frontend |
| `docs/coordination/API_CONTRACT.md` | Contrato de API backend↔frontend | Antes de criar/modificar endpoints |
| `docs/coordination/BACKLOG.md` | Backlog de tarefas de curto prazo | Para micro-tarefas do dia |
| `docs/coordination/DECISIONS.md` | Decisões técnicas tomadas e justificativas | Para entender por que as coisas são como são |

---

## 🔑 Informações de Acesso

| Serviço | Valor |
|---|---|
| PostgreSQL | `localhost:5432` / db: `agrojus` / user: `agrojus` / pass: `agrojus` |
| Backend API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |
| Frontend | `http://localhost:5173` |
| Branch Git | `claude/continue-backend-dev-sVLGG` |

---

## ⚡ Estado Atual da Plataforma (2026-04-15)

### Backend — Operacional ✅
- FastAPI + PostGIS rodando em Docker
- 19 tabelas com dados reais (103k IBAMA, 614 MTE, 50k DETER Amazônia, 50k DETER Cerrado, 5.6M crédito rural, 655 TIs, 16k armazéns...)
- Auth JWT completo (login, registro, rate limiting)
- Dashboard metrics com 8 KPIs reais
- Layer GIS serving do PostGIS local (20+ camadas)

### Frontend — Funcional ✅ (login em progresso)
- GIS Map Engine v2 com Leaflet — multi-layer, análise de ponto, bbox search
- Login overlay UI adicionado (needs browser test)
- KPI cards, market feed, news feed, compliance view

### Dados — Parcialmente bloqueados ⏳
- BCB SICOR: 503 manutenção
- BasedosDados BigQuery: requer GCP_PROJECT_ID do usuário
- ANA Outorgas: URL de download pendente
- ICMBio UCs: download manual pendente

---

## 🎯 Próximos Passos Recomendados

### IMEDIATO — 1 sessão
1. **Testar login no browser** `http://localhost:5173` → fluxo completo (register → badge → logout)
2. **BasedosDados**: usuário criar projeto GCP grátis em `console.cloud.google.com`
3. **Motor Score MCR 2.9**: implementar checklist IBAMA + DETER + CAR + TI

### CURTO PRAZO — 2-3 sessões
4. `POST /api/v1/imovel/relatorio` — motor central do Módulo 1
5. **PRODES** — carregar desmatamento anual consolidado (WFS TerraBrasilis)
6. **MapBiomas Alerta** — criar conta + implementar GraphQL collector
7. **Export PDF** — WeasyPrint para relatório de conformidade

### MÉDIO PRAZO — 1-2 semanas
8. **Valuation R$/ha** — modelo preditivo por município
9. **DataJud/CNJ** — processos judiciais por CPF/CNPJ
10. **APScheduler** — cotações automáticas 09h e 18h BRT

---

## ⚠️ Avisos Críticos

> **JWT_SECRET** ainda é o valor padrão de dev — adicionar ao `.env` antes de deploy

> **GCP_PROJECT_ID** não configurado — bloqueia BasedosDados BigQuery

> **MapBiomas Alerta** — conta não criada — bloqueia laudos técnicos de desmatamento

> **DETER**: temos apenas 50k alertas (limite do WFS). Total real: 800k Amazônia + 200k Cerrado.
> Baixar arquivo completo em `terrabrasilis.dpi.inpe.br/downloads/`

---

## 🧹 Estrutura de Arquivos (após limpeza 15/04/2026)

```
docs/
├── CONTEXTO_COMPLETO.md     ← LEIA PRIMEIRO (briefing de produto)
├── PESQUISA_FONTES.md       ← Guia técnico de cada fonte de dados
├── CONTINUIDADE_PROMPT.md   ← Este arquivo
├── HANDOFF_2026-04-15.md    ← Estado técnico atual
├── ARCHITECTURE.md          ← Arquitetura de sistema
├── FRONTEND_SPEC.md         ← Spec do frontend
├── API.md                   ← Documentação de API
├── _archive/                ← Docs obsoletos (não apagar)
├── coordination/
│   ├── ROADMAP.md           ← Status dos módulos e pendências
│   ├── API_CONTRACT.md      ← Contrato backend↔frontend
│   ├── BACKLOG.md           ← Tarefas de curto prazo
│   ├── DECISIONS.md         ← Decisões técnicas
│   ├── BRIEFING_ANTIGRAVITY.md ← Briefing para o agente IA
│   └── agents/              ← Instruções por agente
└── plans/
    ├── 2026-04-11-fase1-consolidacao.md
    ├── 2026-04-11-frontend-nextjs14-design.md
    └── 2026-04-11-frontend-phase1-scaffold-core.md

backend/
├── app/
│   ├── api/         ← Rotas FastAPI (geo, compliance, market, dashboard, auth)
│   ├── collectors/  ← Coletores de dados externos
│   └── models/      ← SQLAlchemy models
└── scripts/         ← ETLs e scripts de manutenção

frontend/
├── index.html       ← App principal + login overlay
├── main.js          ← Lógica principal + GIS Engine
├── style.css        ← Design system completo
└── src/components/  ← Componentes JS (GisMap, etc.)
```

---

*AgroJus Enterprise — Continuidade Prompt v3.0 — 2026-04-15*
