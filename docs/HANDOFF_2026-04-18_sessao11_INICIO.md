# AgroJus — Handoff Sessão 11 (2026-04-18)

> **Substitui todos os handoffs anteriores como mestre.**
> Sessão 10 fechou prioridade A (frontend `/juridico`). Esta sessão muda o
> foco para **resolver pendências, dívida técnica e garantir acesso aos dados**.

---

## 0. REGRAS DE OURO PARA ESTA SESSÃO

1. **Repositório principal é local:** `C:\dev\agrojus-workspace`
   - Toda leitura/escrita acontece aqui
   - `git` é usado como **backup** (push ao GitHub após commits lógicos)
   - Não confundir com `/c/dev/advia` nem qualquer pasta do OneDrive
2. **AgroJus ≠ advIA.** Nada de `iara_*` / `advia_*` / FIRAC / Bloco 11 / cadernos.
   Se stop-hook disparar com esse vocabulário, é ruído de config — ignorar.
   Salvamento do estado se faz com git commit + push + `docs/HANDOFF_*.md`.
3. **Autonomia total** (`memory/feedback_autonomy.md`) — executar o que claude puder.
4. **Sem mocks** — código real com dados reais.
5. **Não rotular como "feito"** o que está parcial.
6. **Não expor fonte dos dados** ao usuário final no frontend
   (decisão sessão 8; vale inclusive para dossiê e juridico).
7. **PT-BR** UI + dark mode Forest/Onyx.
8. **Commits pequenos** e push frequente.
9. **CHANGELOG atualizado** a cada commit lógico.
10. **Branch atual:** `claude/continue-backend-dev-sVLGG`
    (último commit: `c6ee0f7`).

---

## 1. CONTEXTO RÁPIDO DO PRODUTO

**AgroJus** é plataforma SaaS B2B de **inteligência agrojurídica integrada**
para imóveis rurais brasileiros. Não é "ferramenta para advogado" — é **hub
multi-persona**: comprador de imóvel, trading, banco/cooperativa, consultor
ambiental, produtor rural, advogado agrário.

**Eduardo** (OAB/MA 12.147, Guerreiro Advogados, São Luís/MA) quer o produto
"mostrável em qualquer reunião" cruzando dados oficiais com análise automática.

**Stack consolidada (não questionar sem motivo plausível):**
- Backend: FastAPI monolítico modular · SQLAlchemy 2.0 sync · PostGIS 3.4 ·
  Docker Compose 2 containers · JWT · cache SHA256 24h
- Frontend: Next 16.2.3 canary + React 19.2 · Tailwind v4 · react-leaflet 5
  (CARTO Dark) · SWR 2.4 · Zustand 5 · App Router com grupo `(dashboard)`

---

## 2. ESTADO ATUAL (pós-sessão 10)

### Números consolidados
- **~120 endpoints** em 26 routers
- **~40 tabelas PostgreSQL** (18 PostGIS originais + 12 Sprint 4 + 5 jurídico-agro
  + webhooks + logs + market_prices)
- **~8,5M registros** (7,7M originais + 822k Sprint 4 + 75 seeds jurídicos)
- **28 coletores** (10 ativos em Sprint 4, outros originais)
- **14 rotas frontend** (12 implementadas + `/consulta` e `/alertas` ainda mock)

### Frontend — o que funciona
| Rota | Status |
|---|---|
| `/` dashboard | ✅ KPIs |
| `/login` | ✅ JWT |
| `/mapa` | ✅ v2.1 (painel colapsa, inspector copy/KML, stats MapBiomas-style, CTA dossiê) |
| `/imoveis/[car]` | ✅ 12/12 abas |
| `/mercado` | ✅ UFPicker + 13 commodities + gráfico |
| `/noticias` | ✅ RSS agro |
| `/publicacoes` | ✅ DJEN |
| `/processos` | ✅ DataJud |
| `/compliance` | ✅ 32 critérios standalone + laudo PDF |
| `/dados-gov` | ✅ admin ETL |
| `/dossie` | ✅ multi-input + 6 personas + PDF 20-45pg |
| **`/juridico`** | ✅ **NOVO (sessão 10)** — 5 abas: Processos · Contratos · Teses · Legislação · Monitoramento |
| `/alertas` | ⚠ mock |
| `/consulta` | ⚠ mock |

### MCR 2.9 cobertura
- **15/32 critérios** com dados reais (47%)
- 17 pending aguardam fontes pagas (CCIR/ITR/CNDT) ou ETLs novos

---

## 3. FOCO DA SESSÃO 11 — 3 TRILHAS

Eduardo definiu a direção: **pendências + dívida técnica + garantir acesso
aos dados**. Execução sugerida em 3 trilhas encadeadas (começar pela Trilha 1).

### 🔵 Trilha 1 — Acesso aos dados (prioridade máxima)

**Sprint A · Auditoria e reparo de coletores (1-2 dias)**
- Varrer os 28 coletores: frescor (última execução), taxa de sucesso,
  contagem real vs esperada
- Re-testar token `dados.gov.br` (bug CloudFront 401 pode ter sido corrigido)
- Re-testar SIGMINE ANM (estava em 502 externo)
- Re-testar ANA Outorgas, ANA BHO (sem URL estável até sessão 9)
- Re-testar Garantia-Safra (token CGU sem permissão)
- Entregável: `docs/AUDITORIA_COLETORES_2026-04-18.md` com ranking de
  urgência de reparo

**Sprint B · Cobertura nacional dos grandes (3-5 dias)**
- **SICAR nacional** (hoje só MA — faltam ~79M registros das outras UFs;
  dados abertos por UF em https://www.car.gov.br/publico/imoveis/index)
- **DETER/PRODES completo** (hoje 50k, deveria ser 800k+)
- **IBAMA embargos** — confirmar atualização mensal (snapshot atual: 88k)
- **ETL incremental** em todos (delta vs full reload) — infra já tem
  `ingestion_log`

**Sprint C · Novos coletores alto impacto (5-7 dias)**
- **Scheduler** (APScheduler in-container OU cron docker) para refresh
  automático
- **Observability dos ETLs** — dashboard admin `/dados-gov` expandido com
  gráficos (sucesso/falha ao longo do tempo, contagem por dataset)
- **Receita Federal QSA** (Casa dos Dados tem API grátis)
- **Histórico MapBiomas 1985-atual** (dados públicos)

### 🟢 Trilha 2 — Dívida técnica crítica (em paralelo)

**Sprint D · Fundação (2-3 dias)**
- **Alembic migrations** — substituir `Base.metadata.create_all()` ad-hoc
  por migrations versionadas. Bootstrap: `alembic init` + primeira migration
  snapshotando o schema atual. Fundação para qualquer mudança futura sem
  risco de perder dados.
- **JWT httpOnly cookie** — hoje em localStorage (risco XSS). Alteração em
  `/auth` endpoints + `fetchWithAuth`.
- **Middleware auth frontend** — no Next 16 o arquivo é `proxy.ts`, não
  `middleware.ts` (breaking change v16). Redirect pra `/login` se sem
  cookie.
- **Error boundaries** — `app/error.tsx` + `app/global-error.tsx`.

**Sprint E · Testes mínimos (3-5 dias)**
- **pytest + FastAPI TestClient** para os 4 endpoints mais críticos:
  - `/property/search` (busca CAR + CPF)
  - `/juridico/processos/{cpf}/dossie`
  - `/dossie` (POST)
  - `/compliance/mcr29/full` (POST)
- **Vitest + React Testing Library** para 3 componentes críticos:
  - `ProcessosTab` (hub jurídico)
  - `ContratosTab` (modal + template fill)
  - `MapComponent` (render + layer toggle)
- **CI simples GitHub Actions** (só lint + tsc + pytest)

### 🟠 Trilha 3 — Pendências frontend

**Sprint F · Sprint 5 mapa (3-5 dias)** — fecha o iniciado na sessão 9
- Integrar Zustand store já criado ao `MapComponent`
- Slider temporal duplo (YYYY-MM) para DETER/PRODES/MapBiomas
- Drill-down UF → Município (breadcrumb + fly-to)
- Opacidade individual por camada
- Export CSV/Shapefile da view atual

**Sprint G · Substituir mocks**
- `/consulta` → usar search real (endpoint `/property/search` já existe)
- `/alertas` → usar tabela `environmental_alerts` já populada

---

## 4. PENDÊNCIAS COMPLETAS — INVENTÁRIO

### 🔴 Alta prioridade (próximos sprints)

**Trilhas 1-3 acima.** Priorização:
1. Auditoria de coletores (Sprint A) — descobre estado real antes de gastar esforço
2. Alembic (Sprint D primeira tarefa) — segurança de schema é fundação
3. Sprint 5 mapa (Sprint F) — fecha pendência já iniciada

**Hub Jurídico-Agro — itens ainda pendentes:**
- Calculadora de prescrição administrativa (Lei 9.873/99) — pedido explícito
- Editor guiado de contratos (wizard)
- Expansão da base: +30 normativos estaduais · +20 teses · +15 contratos
- Upload documento + OCR + análise automática
- IA sugere tese conforme caso
- Cron de monitoramento ativo de CPFs cadastrados

**Motor jurídico (Sprint 6):**
- STJ dados abertos + TCU webservice → tabela `jurisprudencia`
- Embedding bge-m3 (já no mia-project)
- Busca híbrida vetorial+textual
- Enriquecer teses com precedentes reais verificáveis

### 🟠 Média prioridade

**Sprint 7 — Gerador de minutas**
- Claude API + anti-alucinação + `/minutas` + export DOCX

**Sprint 8 — Leilões agro**
- Scrapers (Caixa, Spy, Portal Leilão, TJs)
- Dedup + classificação rural + parser LLM edital
- Cruzar com dossiê geo + timeline 1ª→2ª→3ª praça

**Sprint 9 — Dossiê Proativo**
- Dashboard `/proprietarios/[cpf_cnpj]`
- Webhook por evento novo, Export Excel, Comparação A vs B

**Sprint 11 — Calculadoras**
- Multas IBAMA, ITR, Crédito rural (PRONAF/PRONAMP), RL por bioma, CRA,
  conversor unidades rurais

**Compliance — 17 critérios pending MCR 2.9**
- CCIR, ITR, CNDT, protestos CENPROT, SPU, SIGMINE, NR-31, CIPATR, CAGED,
  eSocial, etc.

### 🟡 Backlog

- Sprint 10 (ESG + Basel IV)
- Sprint 12 (Receita QSA, ONR, SERPRO, SICAR oficial API, LexML, Câmaras)
- Sprint 13 (mercado avançado: basis, oferta×demanda, arbitragem)
- Sprint 14 (API Pública + SDKs + parcerias)
- Sprint 15 (Mobile/PWA)
- Dossiê: INMET 10 anos, ZARC, SmartSolos, NDVI, benchmark vizinhos, ESG
- UX: tour guiado, favoritos, histórico, compartilhamento, dashboard KPIs
- Negócio: planos, billing, multi-tenant, whitelabel, marketplace de laudos

### 🧩 Dívida técnica detalhada

- **Alembic migrations** (crítico — schema ad-hoc)
- JWT httpOnly cookie (localStorage → XSS)
- Middleware/proxy auth frontend (Next 16 usa `proxy.ts`)
- Error boundaries
- Testes Vitest + pytest + Playwright
- Storybook para design system
- OpenAPI codegen → types TypeScript
- Redis (rate_limiter, monitoring persistido)
- Sentry/Axiom + PostHog
- Celery para ETLs/monitoramento/webhooks
- i18n (pt_BR / en_US / es_AR)
- ETL incremental (delta vs full)
- Observability ETLs (Grafana)
- Data lake S3
- Versionamento datasets (snapshot mensal)

### Coletores ainda ausentes
- SIGMINE (ANM 502 externo — reverificar)
- ANA Outorgas, ANA BHO (scrape SNIRH GeoNetwork)
- Garantia-Safra (API Portal Transparência com upgrade)
- IBAMA CTF (dataset específico a identificar)
- NDVI SATVeg, ONR matrículas (InfoSimples pago), SNCI, SPU, ZEE por estado

---

## 5. COMANDOS RÁPIDOS

```bash
cd C:\dev\agrojus-workspace
docker compose up -d
curl http://localhost:8000/health

# Auditoria inicial sugerida — status dos ETLs
curl http://localhost:8000/api/v1/dados-gov/status | jq

# Listar coletores
curl http://localhost:8000/api/v1/dados-gov/loaders | jq

# Roda um ETL específico
curl -X POST http://localhost:8000/api/v1/dados-gov/run?loader=ceis

# Seed jurídico (reset completo)
curl -X POST "http://localhost:8000/api/v1/juridico/seed?force=true"

# Dossiê por CAR
curl -X POST http://localhost:8000/api/v1/dossie \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2100055-0013026E975B48D9B4F045D7352A1CB9","persona":"investidor"}'

# Consulta jurídica por CPF (exemplo conhecido com 2 sanções CEIS)
curl http://localhost:8000/api/v1/juridico/processos/00818544000165/dossie | jq

# Frontend
cd frontend_v2 && npm run dev
# Type-check
npx tsc --noEmit
# Lint
npx eslint src/app/\(dashboard\)/juridico src/components/juridico

# Git — backup
git status
git add -A && git commit -m "..."
git push origin claude/continue-backend-dev-sVLGG
```

---

## 6. ESTRUTURA DE ARQUIVOS (atual)

```
C:\dev\agrojus-workspace\                   ← repo principal (este HD)
├── CHANGELOG.md                            ← v0.13.0 última entrada
├── README.md
├── ROADMAP.md                              ← 15 sprints + ideias cross-cutting
├── docker-compose.yml
├── .claude/
│   └── settings.json                       ← AgroJus config, hooks advIA zerados
│
├── backend/
│   ├── app/
│   │   ├── api/              # 26 routers
│   │   │   ├── juridico.py           # 12 endpoints Hub
│   │   │   ├── dossie.py
│   │   │   ├── dados_gov.py          # admin ETL — alvo Sprint A
│   │   │   ├── webhooks.py
│   │   │   ├── property_actions.py
│   │   │   └── ... (21 outros)
│   │   ├── services/
│   │   │   ├── dossie_generator.py
│   │   │   ├── dossie_pdf.py
│   │   │   ├── juridico_seeds.py
│   │   │   ├── mcr29_expanded.py
│   │   │   ├── webhook_dispatcher.py
│   │   │   ├── minuta_generator.py
│   │   │   └── ... (15 outros)
│   │   ├── collectors/     # 28 coletores — alvo Sprint A
│   │   │   ├── dados_gov.py                # CKAN client + KNOWN_RESOURCES
│   │   │   ├── dados_gov_loaders.py        # 11 loaders
│   │   │   ├── portal_transparencia.py
│   │   │   ├── sicar_collector.py          # SICAR MA (expandir para nacional)
│   │   │   ├── inpe_collector.py           # DETER/PRODES (expandir)
│   │   │   └── ... (23 outros)
│   │   ├── models/database.py              # ~40 models
│   │   └── main.py
│   ├── scripts/
│   │   └── run_dados_gov_etl.py
│   └── .env                               ← credenciais (nunca commitar)
│
├── frontend_v2/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── juridico/page.tsx            ← NOVO sessão 10
│   │   │   │   ├── dossie/page.tsx
│   │   │   │   ├── compliance/page.tsx
│   │   │   │   ├── imoveis/[car]/page.tsx
│   │   │   │   ├── mapa/page.tsx                ← alvo Sprint F
│   │   │   │   ├── mercado/, noticias/, processos/, publicacoes/, dados-gov/
│   │   │   │   ├── alertas/page.tsx             ← mock (alvo Sprint G)
│   │   │   │   └── consulta/page.tsx            ← mock (alvo Sprint G)
│   │   │   ├── login/page.tsx
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── juridico/          # 5 tabs do Hub
│   │   │   ├── mapa/              # v2.1 (alvo integração Zustand)
│   │   │   ├── imovel/tabs/       # 12 tabs
│   │   │   └── layout/            # Sidebar, TopBar, CommandPalette
│   │   ├── lib/
│   │   │   ├── api.ts             # fetchWithAuth + swrFetcher (alvo JWT cookie)
│   │   │   ├── stores/map-store.ts ← scaffold Zustand (alvo Sprint F)
│   │   │   └── layers-catalog.ts
│   │   └── AGENTS.md              ← Next 16 notes
│   ├── package.json               # next@16.2.3, react@19.2.4, tailwind@4
│   └── tsconfig.json
│
└── docs/
    ├── HANDOFF_2026-04-18_sessao11_INICIO.md   ← ESTE (mestre)
    ├── HANDOFF_2026-04-18_sessao10_FECHAMENTO.md
    ├── HANDOFF_2026-04-18_sessao10_INICIO.md
    ├── HANDOFF_2026-04-17_sessao9.md
    ├── HANDOFF_2026-04-18_sessao8.md
    ├── HANDOFF_2026-04-17_sessao7.md
    ├── ARCHITECTURE.md · API.md · API_FRONTEND_CONTRACT.md
    ├── ANALISE_COMPETITIVA_COMPLETA.md · ANALISE_COMPETITIVA_v2_COMPLETA.md
    ├── PESQUISA_FONTES.md · PESQUISA_MERCADO_v3_EXECUTIVO.md
    └── _archive/
```

---

## 7. CREDENCIAIS (em `backend/.env`)

```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
DADOS_GOV_TOKEN=eyJhbGc...       # bug CloudFront 401 — reverificar em Sprint A
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a  # OK
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
# ANTHROPIC_API_KEY=sk-ant-...    # adicionar para Sprint 7 (minutas)
```

---

## 8. O QUE FOI FEITO NA SESSÃO 10

### Prioridade A fechada — Frontend `/juridico`
**Commit `e9b1f26` · 2.710 linhas · 0 dependências novas**

Arquivos criados:
| Arquivo | Função |
|---|---|
| `frontend_v2/src/app/(dashboard)/juridico/page.tsx` | Shell com 5 tabs + query string `?tab=` + Suspense |
| `components/juridico/ProcessosTab.tsx` | Dossiê por CPF/CNPJ (6 bases + risco colorido) |
| `components/juridico/ContratosTab.tsx` | Grid + modal preview markdown + exports .doc/.md/clipboard |
| `components/juridico/TesesTab.tsx` | 7 áreas com chips + accordion lazy |
| `components/juridico/LegislacaoTab.tsx` | Filtros UF/IBGE/tema/esfera + agrupamento |
| `components/juridico/MonitoramentoTab.tsx` | CRUD monitoramentos + form inline |

**Validações:**
- `tsc --noEmit`: 0 erros · ESLint: 0 warnings
- 4 endpoints validados via curl com seeds reais

### Limpeza de hooks advIA em config
**Commit `c6ee0f7`** — sobrescreve `Stop/SubagentStop/PreCompact` com arrays
vazios em `.claude/settings.json` do projeto. Também zerado no plugin advIA
(marketplace local + cache) para evitar disparo em cache de runtime.

Memória registrada em `memory/project_agrojus_vs_advia.md`:
- AgroJus ≠ advIA
- Como reverter se Eduardo quiser Stop behavior no advIA operacional
- Efeito pleno só no próximo restart do Claude Code

---

## 9. COMMITS DA SESSÃO 10 (já pushados)

```
c6ee0f7  chore(claude): neutraliza hooks advIA no settings do AgroJus
1f763e4  docs: handoff fechamento sessao 10
e9b1f26  feat(juridico): frontend Hub Juridico-Agro — 5 abas consumindo backend
0ddfed6  chore: flatten — move agrojus/* to repo root
```

---

## 10. ARMADILHAS CONHECIDAS

- **PowerShell não aceita `&&`** — usar `;` ou linhas separadas
- **Next 16 breaking:** `middleware.ts` virou `proxy.ts`; `params`/`searchParams`
  agora são `Promise<...>` (usar `await` + PageProps helper do typegen)
- **Docker network quebra** → `docker compose down && up -d`
- **Token dados.gov.br** retorna 401 mesmo renovado (bug CloudFront do portal).
  **Alvo primeiro de Sprint A** — reverificar em 2026-04-18+
- **SIGMINE/ANM** servidor em 502 externo — reverificar em Sprint A
- **sicar_completo.cod_municipio_ibge** é integer; `geo_car.cod_municipio_ibge`
  é text — castar em UNION
- **TeseDefesaAgro.situacao** deve ser Text (não String(200)) — descrições longas
- **ANEEL CSV** usa Latin-1/ISO-8859-1 (não UTF-8) e separador `;`
- **pandas NaN** não serializa para JSON Postgres — usar `_clean_for_json`
- **Dossiê PDF grande** (>20 págs) leva ~3-5s para gerar
- **Hooks advIA** podem continuar disparando até Claude Code reiniciar
  (cache de runtime). Se aparecer, ignorar — config já está neutra em disco

---

## 11. MENSAGEM PARA A PRÓXIMA SESSÃO

Olá Claude. Essa é a sessão 11 do AgroJus. Você tem **autonomia total**
(`memory/feedback_autonomy.md`). Eduardo quer começar pela **Trilha 1 ·
Sprint A — Auditoria de coletores** porque sem saber o estado real dos
dados, qualquer sprint B/C/F pode estar investindo em lugar errado.

**Primeiro passo sugerido:**
1. Ler `backend/app/collectors/dados_gov.py` + `dados_gov_loaders.py` +
   `sicar_collector.py` + `inpe_collector.py` + outros para mapear os 28
2. Query `SELECT source, MAX(last_run_at), COUNT(*) FROM ingestion_log
   GROUP BY source` para ver frescor e taxa
3. Query `SELECT COUNT(*) FROM {tabela}` para cada tabela de destino para
   ver volume real
4. Tentar rodar os 4 loaders atualmente quebrados (SIGMINE, ANA Outorgas,
   ANA BHO, Garantia-Safra, IBAMA CTF) e capturar erro
5. Entregar `docs/AUDITORIA_COLETORES_2026-04-18.md` com:
   - Tabela de todos os 28 coletores: endpoint, tabela, última run, volume,
     status, fonte upstream
   - Top 5 coletores que dão mais ROI reparar agora
   - Plano detalhado para Sprint B (cobertura nacional)

Se quiser atalho, usar o endpoint já existente
`GET /api/v1/dados-gov/status` como ponto de partida. Backend deve estar
rodando via `docker compose up -d`.

---

*AgroJus — Handoff Sessão 11 — 2026-04-18 BRT*
*Versão 0.13.0 · 4 commits pushados na sessão 10 · 40 tabelas · 8,5M registros · ~120 endpoints · 14 rotas frontend*
*Repositório principal: `C:\dev\agrojus-workspace` · Git como backup · Branch `claude/continue-backend-dev-sVLGG`*
