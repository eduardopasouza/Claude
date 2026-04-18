# AgroJus — Handoff Sessão 12 (2026-04-18)

> **Substitui todos os handoffs anteriores como mestre.**
> Sessão 11 entregou **416 testes verdes** (fundação Anti-Vibe Coding).
> Agora voltamos às 3 trilhas originais com TDD em cima da fundação.

---

## 0. REGRAS DE OURO

1. **Repositório principal é local**: `C:\dev\agrojus-workspace`
   - Leitura/escrita aqui · `git push` é backup
   - Branch atual: `claude/continue-backend-dev-sVLGG`
   - Último commit: `8635783` (14 component tests)
2. **AgroJus ≠ advIA.** Zero `iara_*` / FIRAC / Bloco 11. Stop-hooks advIA
   foram neutralizados em `.claude/settings.json` (efeito pleno após
   próximo restart do Claude Code).
3. **Anti-Vibe Coding** (Fabio Akita 2026): cada feature/fix nova tem
   teste. TDD red → green → refactor. Vocabulário de commit: `feat:`,
   `fix:`, `test:`, `harden:`, `extract:`, `refactor:`.
4. **Autonomia total** — ver `memory/feedback_autonomy.md`.
5. **Sem mocks** no código de produção — código real com dados reais.
6. **`make test` passa** antes de push. Senão, volta.
7. **Não rotular como "feito"** o que não passa em teste.

---

## 1. ESTADO ATUAL (pós-sessão 11)

### Números
- **~120 endpoints** em 26 routers
- **~40 tabelas** PostgreSQL · 8,5M registros · 822k Sprint 4 · 75 seeds
- **14 rotas frontend** (12 implementadas + `/consulta` e `/alertas` mock)
- **416 testes passing** em ~53s · 21 xfailed documentados · 2 skipped
  live opt-in

### Frontend — o que funciona
`/login` · `/` · `/mapa` v2.1 · `/imoveis/[car]` 12/12 abas ·
`/mercado` · `/noticias` · `/publicacoes` · `/processos` ·
`/compliance` 32 critérios · `/dados-gov` admin · `/dossie` multi-input ·
`/juridico` 5 abas (Processos · Contratos · Teses · Legislação · Monitoramento)

Mocks ainda ativos: `/consulta`, `/alertas` (alvo sessão 12).

### Suite de testes (a nossa fundação)
```
Backend:  327 passed, 2 skipped, 21 xfailed em ~51s
  tests/unit/              162 testes  (<3s offline)
  tests/integration/        27 testes  (Hub Juridico completo)
  tests/contract/           10 testes  (Portal Transparencia + VCR)
  tests/collectors/         22 testes  (normalizer CEIS/CNEP)
  (legados)               ~106 testes  + 21 xfails

Frontend:  89 passed em 2.2s
  src/lib/                  72 testes  (markdown 31, map-store 24,
                                         utils 9, basemaps 8)
  src/components/juridico/  14 testes  (ProcessosTab 5, ContratosTab 5,
                                          TesesTab 4)
```

---

## 2. PLANO SESSÃO 12 — 3 TRILHAS

### 🔵 Trilha 1 — Acesso aos dados (prioridade seu pedido explícito)

**Sprint A · Auditoria automatizada dos 28 coletores** (1-2 dias)
- Escrever `tests/collectors/test_*_live.py` para cada um dos 28 coletores
  no padrão de `test_portal_transparencia.py::TestPortalTransparenciaLive`
  (opt-in via `PYTEST_LIVE=1`)
- Rodar `make test-live` gera output JSON com status real de cada coletor
- Script `scripts/audit_report_from_pytest.py` converte → `docs/AUDITORIA_COLETORES_2026-04-18.md`
- Ranking: o que está ok, o que quebrou, ROI de reparo

**Sprint B · Cobertura nacional dos grandes** (3-5 dias, com TDD)
- **SICAR nacional** — hoje só MA (faltam ~79M de outras UFs). Test
  primeiro: `test_sicar_loader_processa_ma_sp_mt` com pequeno fixture
- **DETER/PRODES completo** — hoje 50k, alvo 800k+
- **IBAMA embargos** — confirmar atualização mensal (snapshot atual 88k)
- **ETL incremental** em todos (delta vs full reload)

**Sprint C · Novos coletores** (5-7 dias)
- **Scheduler** (APScheduler in-container ou cron docker)
- **Observability ETLs** — dashboard `/dados-gov` com gráficos
- **Receita Federal QSA** (Casa dos Dados grátis) — contract test com VCR
- **Histórico MapBiomas 1985-atual**

### 🟢 Trilha 2 — Dívida técnica documentada

**Primeira prioridade: os 21 xfails.**
Lista em `backend/tests/conftest.py` `LEGACY_XFAILS`. Cada um tem motivo
na entrada. Trabalho:

1. `test_risk_score.py` (9 testes) — API interna renomeada
   `_calculate_risk_score` → `_calculate_risk_score_fallback`. Atualizar
   chamadas ou decidir se o teste ainda é válido.
2. `test_person_dossier.py` (5 testes) — shape de rota mudou. Recalibrar.
3. `test_lista_suja.py` (4 testes) — coletor mudou endpoint.
4. `test_compliance.py` (2 testes) — rota mudou para MCR 2.9 expandido.
5. `test_api.py::test_register_and_login` (1 teste) — sem isolação de DB.
   Fix: usar faker por run ou limpar user na fixture.

**Depois:**
- Alembic — primeira migration versionada (`alembic revision --autogenerate`
  com schema atual como base)
- JWT em httpOnly cookie (remove do localStorage)
- Middleware auth frontend (`proxy.ts` Next 16 — NÃO `middleware.ts`)
- Error boundaries (`app/error.tsx` + `app/global-error.tsx`)

### 🟠 Trilha 3 — Features novas com TDD

- **Calculadora de prescrição administrativa** (Lei 9.873/99) — pedido
  explícito. TDD primeiro, depois implementação
- **Cron monitoramento ativo** de CPFs em `monitoramento_partes`
- **Sprint 5 mapa v3** — integrar Zustand ao `MapComponent`, slider
  temporal, drill-down UF→Município, opacidade
- **Substituir mocks** `/consulta` (usa `/property/search` real) e
  `/alertas` (usa tabela `environmental_alerts` populada)

---

## 3. COMANDOS RÁPIDOS

```bash
cd C:\dev\agrojus-workspace

# Dev stack
docker compose up -d
curl http://localhost:8000/health

# Testes (rápido, loop de dev)
make test              # unit + integration + contract (sem live/slow)
make test-unit         # só unit (<1s)
make test-coverage     # gera htmlcov/index.html

# Auditoria de upstream
make test-live         # bate API real dos coletores (PYTEST_LIVE=1)
make audit-coletores   # gera docs/AUDITORIA_COLETORES_YYYY-MM-DD.md

# Frontend
cd frontend_v2
npm test               # vitest run
npm run test:watch     # watch mode
npm run test:coverage  # relatório HTML
npm run typecheck
npx eslint src/

# Gravar/regravar cassette VCR de um contract test
rm backend/tests/contract/cassettes/TestX.yaml
VCR_RECORD_MODE=once pytest backend/tests/contract/test_x.py

# Git (backup)
git add -A && git commit -m "..."
git push origin claude/continue-backend-dev-sVLGG
```

---

## 4. ESTRUTURA DE ARQUIVOS

```
C:\dev\agrojus-workspace\
├── CHANGELOG.md                        ← v0.14.0 última entrada
├── README.md
├── ROADMAP.md                          ← 3 trilhas sessão 12
├── Makefile                            ← test, test-up, test-live, audit-coletores
├── docker-compose.yml
├── docker-compose.test.yml             ← db_test porta 5433
├── .github/workflows/ci.yml            ← backend + frontend (fix path feito)
├── .claude/settings.json               ← advIA zerado
│
├── backend/
│   ├── app/                            ← código (26 routers, 28 coletores)
│   ├── alembic/                        ← instalado, 1 migration placeholder
│   ├── tests/
│   │   ├── README.md                   ← playbook
│   │   ├── conftest.py                 ← fixtures + LEGACY_XFAILS
│   │   ├── unit/                       ← 162 testes
│   │   ├── integration/                ← 27 (Hub Jurídico)
│   │   ├── contract/                   ← 10 + 7 cassettes VCR
│   │   ├── collectors/                 ← 22 (normalizer CEIS/CNEP)
│   │   ├── e2e/                        ← (futuro Playwright)
│   │   └── test_*.py                   ← 17 arquivos legados
│   ├── pytest.ini                      ← 5 markers + timeout 30s
│   └── requirements.txt                ← +deps test (pytest-cov/vcr/freezegun/faker)
│
├── frontend_v2/
│   ├── vitest.config.ts                ← jsdom + coverage v8
│   ├── tests/setup.ts                  ← jest-dom + mocks matchMedia/IO/RO
│   ├── package.json                    ← scripts test, test:watch, test:coverage
│   └── src/
│       ├── app/(dashboard)/juridico/   ← 5 tabs · sessão 10
│       ├── components/juridico/        ← +tests sessão 11 (14 testes)
│       └── lib/
│           ├── markdown.ts/test        ← 31 testes
│           ├── utils.ts/test           ← 9 testes
│           ├── basemaps.ts/test        ← 8 testes
│           └── stores/
│               └── map-store.ts/test   ← 24 testes
│
└── docs/
    ├── HANDOFF_2026-04-18_sessao12_INICIO.md   ← ESTE (mestre)
    ├── HANDOFF_2026-04-18_sessao11_INICIO.md   ← plano original da sessão 11
    ├── ANALISE_COMPETITIVA.md                   ← era v2, agora canônico
    ├── ARCHITECTURE.md
    ├── API.md · API_FRONTEND_CONTRACT.md
    ├── PESQUISA_FONTES.md · PESQUISA_MERCADO.md
    ├── research/                               ← material de base
    └── _archive/                               ← handoffs 1-10 + docs obsoletas
```

---

## 5. CREDENCIAIS (em `backend/.env`)

```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
DADOS_GOV_TOKEN=eyJhbGc...                # bug CloudFront 401 — validar Sprint A
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a  # OK em 2026-04-18
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
# ANTHROPIC_API_KEY=sk-ant-...             # adicionar para Sprint 7 (minutas)
```

**Token PORTAL_TRANSPARENCIA passa em teste live (confirmado sessão 11).**

---

## 6. COMMITS DA SESSÃO 11 (14 commits, todos pushados)

```
8635783 test(frontend): +14 component render smoke tests das tabs do juridico
f0d9005 test(frontend): +44 testes — map-store Zustand + utils + basemaps
c3d2c7c test(unit): +24 testes MCR 2.9 — dataclasses + WEIGHTS + metadata
450296e test(integration): +27 testes Hub Juridico via TestClient
8d93a68 test(unit): +50 testes — DadosGovClient + DataJud parser + Agrolink
3b65192 test(unit): +49 testes — CPF/CNPJ + jurisdicao + webhook
0a33573 test(collectors): fix normalizer Portal Transparencia + 22 testes
5bc5eea test(contract): Portal da Transparencia CEIS+CNEP com VCR
3e997a5 test(frontend): vitest + testing-library + markdown utils + 31 testes
7a245f8 chore(tests): scaffold profissional — 5 categorias + VCR + Makefile
ed472a3 docs: consolida sessao 10 → 11 — handoff + roadmap + changelog
c6ee0f7 chore(claude): neutraliza hooks advIA no settings
1f763e4 docs: handoff fechamento sessao 10
e9b1f26 feat(juridico): frontend Hub Juridico-Agro — 5 abas (sessão 10)
```

---

## 7. ARMADILHAS CONHECIDAS

- **PowerShell** não aceita `&&` — usar `;` ou linhas separadas
- **Next 16 breaking:** `middleware.ts` virou `proxy.ts`; `params` e
  `searchParams` agora são `Promise<...>`
- **Docker network quebra** → `docker compose down && up -d`
- **Token `dados.gov.br`** retorna 401 mesmo renovado (bug CloudFront).
  Alvo do Sprint A — reverificar
- **SIGMINE/ANM** servidor em 502 externo — reverificar
- **Portal Transparência mudou contrato:** `orgaoSancionador` →
  `fonteSancao`. Fix já no loader (sessão 11). Contract test trava
  regressões futuras.
- **`sicar_completo.cod_municipio_ibge`** é integer; `geo_car.cod_municipio_ibge`
  é text — castar em UNION
- **ANEEL CSV** usa Latin-1 e separador `;`
- **pandas NaN** não serializa para JSON Postgres — usar `_clean_for_json`
- **Hooks advIA** podem continuar disparando até Claude Code reiniciar
  (cache de runtime) — ignorar, config em disco já está neutra

---

## 8. MENSAGEM PARA A PRÓXIMA SESSÃO

Olá Claude. Essa é a sessão 12 do AgroJus. Você tem **autonomia total**.

**Contexto crucial:** na sessão 11 montamos a **fundação de testes
completa** (416 testes, ~53s). Agora cada mudança é segura: se você
quebrar algo, um teste falha. Se descobrir um bug, vira um teste novo.
TDD red→green→refactor.

**Primeiro passo sugerido:** arrumar a casa — os **21 xfails legados**
em `LEGACY_XFAILS` no `backend/tests/conftest.py`. Começar por
`test_risk_score.py` porque são 9 testes e todos quebram pelo mesmo
motivo (método renomeado de `_calculate_risk_score` para
`_calculate_risk_score_fallback`). Uma correção simples destrava 9 xfails.

Depois disso, avançar para Sprint A da Trilha 1: escrever
`test_*_live.py` para cada um dos 28 coletores e gerar o relatório
automático de auditoria.

Bom código.

---

*AgroJus — Handoff Sessão 12 — 2026-04-18 BRT*
*Versão 0.14.0 · 14 commits na sessão 11 · 40 tabelas · 8,5M registros*
*~120 endpoints · 14 rotas frontend · **416 testes verdes***
*Repositório principal: `C:\dev\agrojus-workspace` · Git como backup*
*Branch: `claude/continue-backend-dev-sVLGG`*
