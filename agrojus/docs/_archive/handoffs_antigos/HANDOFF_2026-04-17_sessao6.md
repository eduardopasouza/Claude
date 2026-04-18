# AgroJus — Handoff Sessão 6 (2026-04-17)

> **Cole este arquivo inteiro no início da próxima sessão.**
> Substitui todos os handoffs anteriores.
> Sessão 6: DJEN integrado, move do OneDrive, auditoria 48 sites, catálogo 119 camadas, Embrapa OAuth ok, coletor base pronto.
> **Prioridade de leitura:** Seções 3 (pendências) → 4 (credenciais) → 10 (próximos sprints).

---

## 1. Contexto atual

- **Projeto movido** do OneDrive para `C:\dev\agrojus-workspace\agrojus` (resolveu loop Turbopack + sync OneDrive)
- **Branch git:** `claude/continue-backend-dev-sVLGG` — commits pendentes (ver `git status`)
- **Docker:** 2 containers (`agrojus-db-1` + `agrojus-backend-1`) rodando com `.wslconfig` limitando WSL2 a 8GB
- **Volume Postgres preservado:** `agrojus_pgdata` (42 publicações DJEN + 17 camadas PostGIS sobreviveram ao move)

---

## 2. ESTADO REAL DO PRODUTO (o que funciona HOJE)

### Backend — FastAPI + PostGIS

✅ **Funcionando e validado:**
- `/health` → `{"status":"healthy"}`
- `/api/v1/geo/postgis/catalog` → lista 17 camadas
- `/api/v1/geo/postgis/{layer_id}/geojson` → 17 camadas testadas via curl:
  - ambiental: terras_indigenas, prodes, deter_amazonia, deter_cerrado, mapbiomas_alertas, unidades_conservacao, embargos_icmbio, autos_icmbio
  - fundiário: sicar_completo, geo_car, sigef_parcelas
  - infraestrutura: rodovias_federais, ferrovias, portos, armazens_silos, frigorificos
  - crédito: mapbiomas_credito_rural
- `/api/v1/publicacoes/*` → DJEN integrado, **42 publicações reais do Eduardo (OAB/MA 12147) persistidas no banco**, KPIs (11 críticas)
- `/api/v1/lawsuits/search/{cpf_cnpj}` → DataJud CNJ (API key pública)
- `/api/v1/embrapa/status` → OAuth 2.0 Embrapa **autenticado** com access_token válido
- `/api/v1/market/*` → 11 endpoints (CEPEA, BCB, Yahoo Finance com fallback)
- `/api/v1/dashboard/metrics` → materialized view
- `/api/v1/property/search`, `/api/v1/property/{car}/overlaps` etc

⚠️ **Configurado mas não testado/integrado:**
- MapBiomas Alerta GraphQL (credenciais no .env)
- Portal Transparência CKAN (token no .env)
- dados.gov.br CKAN (token no .env)
- BCB SICOR OData (URL no config)
- Earth Engine (GCP Project ID no .env, volume `application_default_credentials.json` montado)

❌ **OAuth funciona mas endpoints 404 (pendente):**
- Embrapa 9 APIs (Agritec, AGROFIT, SmartSolos, Bioinsumos, BovTrace, AgroTermos, PlantAnnot, RespondeAgro, Sting) — paths individuais no WSO2 não descobertos. Ver `docs/research/embrapa-integracao-status.md`

### Frontend — Next.js 16.2.3 + Turbopack

✅ **Funcionando (build limpo 2.8s, 10 rotas geradas):**
- `/login` — autenticação JWT real
- `/` — dashboard com SWR 60s
- `/mapa` — **MapComponent v2** com:
  - `LayerTreePanel` (árvore temática esquerda, 119 camadas em 23 temas)
  - `BasemapSwitcher` (dark/light/satélite/topo)
  - `LayerInspector` (drawer direito on-click com atributos)
  - `StatsDashboard` (painel inferior recolhível)
  - Endpoint genérico /geo/postgis para todas as camadas ativas
- `/mercado` — cotações CEPEA + indicadores BCB
- `/processos` — **DataJud real** (busca CPF/CNPJ ou assunto CNJ em 13 tribunais)
- `/publicacoes` — **feed DJEN real** (sincronização + filtros + drawer de detalhe)

⚠️ **Placeholders / mock (não conectados):**
- `/consulta` — DeepSearch elaborada visualmente, zero backend
- `/compliance` — 3 linhas hardcoded (MCR 2.9 básico)
- `/alertas` — 4 alertas hardcoded

❌ **Rotas QUE NÃO EXISTEM e foram planejadas:**
- `/imoveis/[car]` — ficha completa do imóvel (**tela mais importante do produto**, só blueprint em `docs/research/analise-agronomica-integrada.md`)
- `/valuation` — valuation NBR 14.653-3
- `/portfolio` — lista de imóveis monitorados
- `/leiloes` — agregador de leilões
- `/teses` — base jurisprudência
- `/minutas` — gerador de peças
- `/perfil`, `/plano`, `/equipe`, `/configuracoes`
- `/radar-ibama`

### Dados no PostgreSQL (verificado via SQL)

| Tabela | Registros | Status |
|---|---|---|
| mapbiomas_credito_rural | 5.614.207 | ✅ |
| sigef_parcelas | 1.717.474 | ✅ |
| geo_mapbiomas_alertas | 515.823 | ✅ |
| mapbiomas_legality | 493.032 | ✅ |
| sicar_completo | 352.215 | ✅ só MA (faltam 79M de outros UFs via BigQuery) |
| geo_car | 135.000 | ✅ |
| environmental_alerts (IBAMA+MTE) | 104.284 | ✅ |
| geo_deter_amazonia / cerrado | 50.000 cada | ❌ parcial (real: 800k+ / 200k+) |
| geo_prodes | 50.000 | ❌ parcial |
| geo_armazens_silos | 16.676 | ✅ |
| geo_rodovias_federais | 14.255 | ✅ |
| geo_autos_icmbio / embargos_icmbio | 10k / 5k | ✅ |
| geo_ferrovias | 2.244 | ✅ |
| geo_terras_indigenas | 655 | ✅ |
| geo_unidades_conservacao | 346 | ✅ |
| geo_frigorificos | 207 | ✅ |
| geo_portos | 35 | ✅ |
| publicacoes_djen | 42 | ✅ (Eduardo OAB/MA 12147) |

---

## 3. PENDÊNCIAS — TUDO QUE FOI PEDIDO E NÃO ATENDIDO

### 3.1 Pedidos do Eduardo com implementação ZERO ou INCOMPLETA

#### 🔴 CRÍTICAS — prometidas mas não feitas
1. **Endpoints Embrapa funcionais** — OAuth ok, paths individuais das 9 APIs não descobertos. Eduardo precisa navegar no portal e copiar base paths (5 min).
2. **Coletores dados.gov.br** — só escrevi guia com 32 datasets priorizados. **ZERO código de coleta.**
3. **Motor jurídico (prescrição, teses, minuta)** — só blueprint textual. Zero implementação.
4. **Base de jurisprudência STJ via bge-m3** — mencionado em plano, zero linha.
5. **Ficha do imóvel `/imoveis/[car]` com aba Agronomia** — blueprint detalhado escrito em `docs/research/analise-agronomica-integrada.md`. **Nenhuma linha de código.**
6. **Tela `/valuation` NBR 14.653-3** — idem, só documentada.
7. **Agregador de leilões** — idem, só documentado.
8. **MCR 2.9 expandido (6→30 critérios auditáveis)** — solicitado em múltiplas sessões. Ainda 6 básicos.
9. **Tela `/compliance` real** — ainda 3 linhas mock.
10. **Tela `/alertas` real** — ainda 4 mocks hardcoded.

#### 🟠 ALTAS — solicitadas mas não atendidas
11. **Slider temporal duplo no mapa** (início/fim YYYY-MM) — crítico para PRODES/DETER/MapBiomas; só está no SYNTHESIS.
12. **URL com estado serializado** — querystring para compartilhamento; não implementado.
13. **Legenda dinâmica painel direito** com "Ver só esta classe" — MapBiomas tem, AgroJus não.
14. **Tabs laterais** (Camadas/Filtros/Mapa Base/Exportar) — catálogo atual é painel único.
15. **Múltiplos identificadores no painel** (CAR + Embargo + CNPJ + CNJ simultâneos).
16. **Régua / Lat-Lon input / Histórico do ponto** — toolbar ausente.
17. **Opacidade por camada** (slider individual).
18. **Drill-down UF → Município** no filtro geográfico — universal no gov BR, ausente aqui.
19. **Dashboard inferior com série temporal + distribuição de classes** — hoje só contadores.
20. **AOI customizada** (upload GeoJSON/shapefile para calcular estatísticas sobre área própria) — estilo MapBiomas "Criar análise".

#### 🟡 MÉDIAS
21. **Lista de features visíveis** no painel direito (alternativa ao inspector — estilo MapBiomas Alerta).
22. **Export GeoJSON/CSV/Shapefile/PDF laudo** contextual por camada.
23. **Permalink versionado** com hash SHA256 para uso pericial.
24. **Webhooks** para alertas (imóvel/OAB/CPF/CNPJ).
25. **Parser LLM de edital de leilão** (Claude API).
26. **NDVI histórico SATVeg Embrapa** na ficha do imóvel.
27. **Histórico MapBiomas integrado com CAR** (endpoint + timeline visual).
28. **Tour guiado** (onboarding estilo MapBiomas Alerta).
29. **Dark/Light toggle completo** (hoje só dark).
30. **Design System Gov.br como tema opcional** para usuário institucional.

#### 🟢 BAIXAS — dívida técnica
31. **OpenAPI codegen → types TypeScript** (`openapi-typescript`) — não instalado.
32. **State global Zustand** — zero store criado.
33. **Middleware auth frontend** — não existe; só `fetchWithAuth` reativo no 401.
34. **JWT httpOnly cookie** — ainda em localStorage (XSS risk).
35. **Error boundaries** — zero.
36. **Testes (Vitest + Playwright)** — zero.
37. **Storybook** — zero.
38. **Logger estruturado** (Sentry/Axiom) — zero.
39. **Analytics** (PostHog/Plausible) — zero.

### 3.2 Sites/fontes que Eduardo mandou verificar — status real

| Fonte | Pedido | Status real |
|---|---|---|
| ONR map.onr.org.br | verificar como mapa ref | ❌ offline durante auditoria |
| 6 plataformas MapBiomas | verificar dashboards | ✅ 6/6 auditadas (`docs/research/visual-audit/mapbiomas/`) |
| 10 concorrentes | auditar | ✅ 10/10 (`concorrentes/`) |
| 6 legal techs | auditar | ✅ 6/6 (`legal-tech/`) |
| 12 fontes gov | auditar | ✅ 12/12 (`fontes-gov/`) |
| 14 valuation/mercado/leilões | auditar | ✅ 14/14 (`valuation/`, `mercado-leiloes/`, `outros/`) |
| SisDEA | pesquisar | ✅ documentado |
| Comunica.PJe/DJEN | integrar | ✅ integrado para OAB Eduardo (42 pubs) |
| SIGEF | integrar | ✅ 1.7M parcelas no banco |
| SNCI | integrar | ❌ stub no catálogo, sem código |
| ONR matrículas | integrar como camada | ❌ corrigido: não é dado público (ver `docs/research/cadeia-dominial-acesso-real.md`) — tratamento correto seria aba "Cadeia Dominial" na ficha do imóvel com upload de PDF/consulta paga InfoSimples |
| IBGE PAM/PPM choropleth | implementar | ❌ 14 camadas no catálogo como stub, endpoints SIDRA já existem mas choropleth não foi construído |
| Embrapa 9 APIs | usar as credenciais | ⚠️ OAuth ok, paths 404 |
| Portal Transparência | usar token | ❌ token salvo, zero consultas feitas |
| dados.gov.br | orientar o que baixar | ✅ guia com 32 datasets priorizados (mas zero coletor escrito) |

### 3.3 Bugs conhecidos

- Sidebar linha 17 → `DataJud` aponta para `/processos` (agora existe, ok) mas o nome "DataJud" ficou duplicado com "Processos". Consolidar.
- `OmniSearch` TopBar — **implementado com handler real** nesta sessão ✅
- `/processos` 404 — **corrigido, agora real** ✅
- `ENV var NEXT_PUBLIC_API_URL` — **implementada** ✅
- "SYSTEM ONLINE 1.2ms" na Sidebar — hardcoded (ping real nunca foi implementado)
- Avatar TopBar "Usuário VIP / Enterprise" — hardcoded, não mostra usuário real logado

### 3.4 Pendências técnicas estruturais

- **Backend sync SQLAlchemy** com endpoints async FastAPI — funciona mas não é ideal (pool_size=5)
- **Rate limiter in-memory** — não sobrevive restart, precisa Redis em produção
- **Monitoring in-memory** (`app/services/monitoring.py`) — idem
- **Cache SHA256 em disco** — ok para dev, mas 24h TTL fixo global; alguns coletores precisam TTL variável (DJEN tem 1h override manual)
- **`create_tables()` no lifespan** — idempotente, mas não faz migração. Faltam **Alembic migrations** para produção.
- **`jwt_secret` hardcoded em config.py** — MUDAR antes de produção.
- **CORS `allow_origins=["*"]`** — desenvolvimento, restringir em prod.

---

## 4. CREDENCIAIS ATIVAS (em .env do container backend)

**Arquivo:** `c:/dev/agrojus-workspace/agrojus/backend/.env` (não commitado — está no .gitignore)

```bash
DATABASE_URL=postgresql://agrojus:agrojus@db:5432/agrojus
DEBUG=true

# Google Cloud Platform
GCP_PROJECT_ID=agrojus
GCP_PROJECT_NUMBER=1064767214292
# credenciais default application: ${APPDATA}/gcloud/application_default_credentials.json
# (montado via volume Docker linha 30 do docker-compose.yml)

# MapBiomas Alerta (GraphQL)
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=1qasw23edFR$

# Embrapa AgroAPI (9 APIs assinadas, plano gratuito até 100k req/mês cada)
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
EMBRAPA_CONSUMER_SECRET=eDJph7PEE9xKDor739rgXwcUc0ca
EMBRAPA_ACCESS_TOKEN=2aef1f08-a5e9-3480-b68b-2184057e3a6d

# dados.gov.br (CKAN federal)
DADOS_GOV_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Portal da Transparência CGU
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a

# DataJud CNJ (API key pública — hardcoded em config.py, não precisa .env)
```

**APIs Embrapa assinadas:**
1. Agritec v2 (recomendação cultivo)
2. AGROFIT v1 (agrotóxicos)
3. AgroTermos v1 (glossário)
4. Bioinsumos v2 (inoculantes)
5. BovTrace v1 (rastreabilidade bovina)
6. PlantAnnot v2 (anotação plantas/pragas)
7. RespondeAgro v1 (Q&A)
8. SmartSolosExpert v1 (classificação solo)
9. Sting v1 (georreferenciamento)

---

## 5. ESTRUTURA DE ARQUIVOS

```
C:\dev\agrojus-workspace\agrojus\
├── docker-compose.yml          # 2 containers, mem_limit ajustado
├── backend\
│   ├── .env                    # credenciais (gitignored)
│   ├── app\
│   │   ├── main.py             # FastAPI + 16 routers registrados
│   │   ├── config.py           # Settings com todos .env fields
│   │   ├── api\
│   │   │   ├── publicacoes.py  # DJEN (NOVO sessão 6)
│   │   │   ├── geo_layers.py   # PostGIS genérico (NOVO sessão 6)
│   │   │   ├── embrapa.py      # 9 endpoints Embrapa (NOVO — paths 404)
│   │   │   ├── lawsuits.py     # DataJud (já existia)
│   │   │   ├── geo.py, market.py, property.py, etc.
│   │   ├── collectors\
│   │   │   ├── djen.py         # DJEN/Comunica.PJe (NOVO sessão 6)
│   │   │   ├── embrapa.py      # OAuth 2.0 client (NOVO sessão 6)
│   │   │   ├── datajud.py, ibge.py, nasa_power.py, ...
│   │   ├── models\database.py  # + modelo Publicacao (NOVO sessão 6)
│   │   └── services\
│   ├── scripts\                # 28 scripts ETL (maioria não rodados para dados completos)
│   └── data\                   # cache SHA256 + shapefiles
├── frontend_v2\                # Next.js 16
│   ├── next.config.ts          # Turbopack com path absoluto (corrigido sessão 6)
│   ├── .env.local.example      # NEXT_PUBLIC_API_URL documentado (NOVO)
│   └── src\
│       ├── app\
│       │   ├── (dashboard)\
│       │   │   ├── publicacoes\page.tsx   # NOVO — feed DJEN
│       │   │   ├── processos\page.tsx     # REESCRITO — DataJud real
│       │   │   ├── mapa\page.tsx, mercado\, consulta\, compliance\, alertas\
│       │   ├── login\page.tsx
│       ├── components\
│       │   ├── mapa\
│       │   │   ├── MapComponent.tsx       # REESCRITO v2 (LayerTreePanel+BasemapSwitcher+Inspector+Stats)
│       │   │   ├── LayerTreePanel.tsx     # NOVO — árvore temática
│       │   │   ├── BasemapSwitcher.tsx    # NOVO — 4 basemaps
│       │   │   ├── LayerInspector.tsx     # NOVO — drawer on-click
│       │   │   ├── StatsDashboard.tsx     # NOVO — painel inferior
│       │   │   └── PropertySearch.tsx
│       │   ├── layout\
│       │   │   ├── Sidebar.tsx            # REORGANIZADA em 3 grupos
│       │   │   └── TopBar.tsx             # OmniSearch com handler real (NOVO sessão 6)
│       └── lib\
│           ├── api.ts              # NEXT_PUBLIC_API_URL env (NOVO)
│           ├── layers-catalog.ts   # 119 camadas em 23 temas (EXPANDIDO sessão 6)
│           └── basemaps.ts         # 4 basemaps (NOVO)
└── docs\
    ├── HANDOFF_2026-04-17_sessao6.md   # ESTE ARQUIVO
    └── research\
        ├── visual-audit\            # 48 auditorias + README + SYNTHESIS (NOVO)
        ├── catalog-layers-complete.md  # 119 camadas documentadas (NOVO)
        ├── cadeia-dominial-acesso-real.md  # NOVO
        ├── analise-agronomica-integrada.md  # blueprint aba Agronomia (NOVO)
        ├── dados-gov-guia.md         # 32 datasets priorizados (NOVO)
        └── embrapa-integracao-status.md  # checklist pendente (NOVO)
```

**Arquivos em `docs/research/visual-audit/`** (48 subpastas .md):
- `mapbiomas/` — brasil-cobertura, alerta, credito-rural, monitor-fogo, recuperacao, mineracao
- `concorrentes/` — softfocus, advlabs, agrotools, serasa-agro, spotsat, traive, busca-terra, sette-ag, satelligence, registro-rural
- `legal-tech/` — escavador, jusbrasil, judit, intima-ai, docket, alerte
- `fontes-gov/` — sicar, sigef, portal-transparencia, ibama-consulta, sigmine, ana-snirh, stj-dados-abertos, datajud, djen, lexml, inmet, sidra-ibge
- `valuation/` — pelli-sisdea, simet-incra, ramt-incra
- `mercado-leiloes/` — caixa-leiloes, reland, spy-leiloes, portal-leilao, agroterra
- `outros/` — cepea, conab, bcb-sicor, embrapa-agroapi, dados-gov, onr

---

## 6. CATÁLOGO DE CAMADAS (119 declaradas, 17 ativas)

Ver `docs/research/catalog-layers-complete.md` para a lista exaustiva. Resumo:

| Tema | # camadas | Ativas | Stubs |
|---|---|---|---|
| Fundiário | 10 | 4 | 6 |
| Ambiental | 8 | 3 | 5 |
| Desmatamento | 5 | 4 | 1 |
| Fogo | 4 | 0 | 4 |
| Vegetação Secundária | 3 | 0 | 3 |
| Degradação | 3 | 0 | 3 |
| Agricultura | 14 | 0 | 14 |
| Pastagem | 4 | 0 | 4 |
| Água | 5 | 0 | 5 |
| Solo | 5 | 0 | 5 |
| Mineração | 3 | 0 | 3 |
| Infraestrutura | 9 | 5 | 4 |
| Energia | 3 | 0 | 3 |
| Crédito | 3 | 1 | 2 |
| Produção IBGE | 10 | 0 | 10 |
| Pecuária IBGE | 4 | 0 | 4 |
| Socioeconômico | 5 | 0 | 5 |
| Clima | 7 | 0 | 7 |
| Atmosfera | 3 | 0 | 3 |
| Risco Climático | 3 | 0 | 3 |
| Urbano | 3 | 0 | 3 |
| Jurídico | 3 | 0 | 3 |
| Fiscal | 4 | 0 | 4 |
| **Total** | **119** | **17** | **102** |

**Tema removido após correção:** "Cartório (ONR)" — matrículas não são acessíveis publicamente. Documentado em `cadeia-dominial-acesso-real.md`.

---

## 7. DOCUMENTO DE SÍNTESE (leitura obrigatória próxima sessão)

**`docs/research/visual-audit/SYNTHESIS.md`** — relatório consolidado dos 48 sites com:

- **25 padrões prioritários** ordenados por frequência + impacto (URL state, drill-down UF→Município, dashboard inferior, árvore temática, basemap switcher, inspector on-click, slider temporal, legenda dinâmica, modular por "motor", single search polimórfica, tabs laterais, webhooks premium, trial auto-serviço, resumo IA, régua, múltiplos identificadores, CRS dual, Design System Gov.br, OAuth gov.br, permalink versionado, export múltiplos formatos)

- **7 killer gaps** que nenhum dos 48 atende:
  1. Cruzamento CAR × SIGEF × SIGMINE × IBAMA × DataJud × DJEN × MapBiomas num único dossiê
  2. Webhook por imóvel/OAB/CPF/CNPJ
  3. Laudo PDF automático com rastreabilidade
  4. IA generativa de peça jurídica agro
  5. Timeline temporal MapBiomas integrada com ficha imóvel
  6. Parser LLM de edital de leilão
  7. Histórico completo do lote (1ª→2ª→3ª praça)

- **Matriz de 8 sprints** (~40 dias total) para paridade + diferenciação

---

## 8. O QUE FOI FEITO NESTA SESSÃO 6 (resumo)

**Backend novo:**
- Collector `djen.py` + modelo `Publicacao` + router `publicacoes.py` (sincroniza intimações DJEN por OAB)
- Router `geo_layers.py` genérico com registry de 17 camadas PostGIS
- Collector `embrapa.py` (OAuth 2.0 singleton + cache) + router `embrapa.py` com 9 endpoints
- Migração automática `create_tables()` no lifespan

**Frontend novo:**
- `/publicacoes` — feed DJEN com sync/filtros/drawer
- `/processos` — DataJud real substituindo placeholder 404
- MapComponent v2 refatorado (LayerTreePanel + BasemapSwitcher + LayerInspector + StatsDashboard)
- Catálogo `layers-catalog.ts` expandido para 119 camadas em 23 temas
- `basemaps.ts` com 4 opções (dark/light/satélite/topo)
- OmniSearch TopBar com handler real (CAR→DeepSearch, processo CNJ→/publicacoes)
- `NEXT_PUBLIC_API_URL` env var implementada
- Sidebar reorganizada em 3 grupos (Plataforma / Jurídico / Compliance & Mercado)
- `next.config.ts` com path absoluto (remove warning)

**Infraestrutura:**
- Projeto movido de OneDrive para `C:\dev\agrojus-workspace\` (6.6GB, 50.523 arquivos em 35s com robocopy)
- `.wslconfig` criado limitando WSL2 a 8GB RAM
- Docker compose com `mem_limit` ajustado (backend 2g, db 1g) + tuning Postgres conservador

**Documentação (nova):**
- 48 arquivos de auditoria visual em `docs/research/visual-audit/`
- `SYNTHESIS.md` — relatório consolidado
- `catalog-layers-complete.md` — 119 camadas documentadas
- `cadeia-dominial-acesso-real.md` — correção ONR
- `analise-agronomica-integrada.md` — blueprint aba Agronomia
- `dados-gov-guia.md` — 32 datasets priorizados
- `embrapa-integracao-status.md` — checklist paths pendentes

---

## 9. COMANDOS RÁPIDOS

```bash
# Subir ambiente
cd C:\dev\agrojus-workspace\agrojus
docker compose up -d

# Health check
curl http://localhost:8000/health

# Frontend dev (path fora do OneDrive = sem loop Turbopack)
cd frontend_v2
npm run dev
# Abrir http://localhost:3000

# Testar DJEN do Eduardo
curl "http://localhost:8000/api/v1/publicacoes/stats/oab/MA/12147"

# Testar camada PostGIS
curl "http://localhost:8000/api/v1/geo/postgis/terras_indigenas/geojson?max_features=5"

# Testar Embrapa OAuth
curl "http://localhost:8000/api/v1/embrapa/status"

# Swagger
# http://localhost:8000/docs

# Postgres direto
docker exec -it agrojus-db-1 psql -U agrojus -d agrojus

# Build frontend (valida tudo)
cd frontend_v2 && npm run build
```

---

## 10. ROADMAP PRÓXIMA SESSÃO — priorização honesta

### Sprint 1 (3 dias) — ATIVAÇÃO RÁPIDA
Máximo valor × mínimo esforço, destravando múltiplas camadas do catálogo:

1. **Descobrir paths Embrapa (Eduardo — 5 min):** acessar https://www.agroapi.cnptia.embrapa.br/portal/apis e copiar base paths das 9 APIs. Com isso os 9 endpoints backend que já estão escritos funcionam instantaneamente.
2. **Coletor IBGE choropleth** — endpoint `/geo/ibge/choropleth/{metrica}/{ano}` que retorna GeoJSON da malha municipal colorida por PAM/PPM/PIB. Ativa 14 camadas stub do catálogo de uma vez.
3. **Coletor IBAMA dados abertos** — download CSV de autos + embargos + CTF. Ativa 3 camadas stub.
4. **Coletor MapBiomas Alerta GraphQL** — credenciais já salvas. Ativa alertas em tempo real.

### Sprint 2 (5 dias) — FICHA DO IMÓVEL `/imoveis/[car]`
**A tela mais importante do produto, ainda não existe.** Blueprint completo em `docs/research/analise-agronomica-integrada.md` com 15 perguntas-chave e mapeamento fonte→endpoint. 12 abas planejadas (Visão Geral / Compliance / Dossiê / Histórico Ambiental / Produção / Clima / Valuation / Logística / Jurídico / Crédito / Monitoramento / Ações).

Sprint 2a: scaffold da rota + 6 abas primeiras (Visão, Compliance, Dossiê, Histórico, Produção, Clima)
Sprint 2b: 6 restantes (Valuation, Logística, Jurídico, Crédito, Monitoramento, Ações)

### Sprint 3 (5 dias) — COMPLIANCE MCR 2.9 EXPANDIDO
De 6 para 30 validações auditáveis + EUDR. Backend: expandir `compliance.py` seguindo referência Softfocus (6 fundiárias + 8 ambientais + 6 trabalhistas + 5 jurídicas + 5 financeiras). Frontend: `/compliance` real com checklist interativo + score 5 eixos + botão "Gerar PDF".

### Sprint 4 (4 dias) — 10 COLETORES dados.gov.br
Cada um ~100 linhas: download + ETL para PostGIS + ativação no LAYER_REGISTRY. Ativa: autos IBAMA pontos, embargos IBAMA polígonos, CTF, Garantia-Safra, SIGMINE, ANA outorgas, ANA BHO, assentamentos, quilombolas, ANEEL usinas+LTs.

### Sprint 5 (4 dias) — MELHORIAS CRÍTICAS DO MAPA (padrões SYNTHESIS)
- URL com estado serializado (`useSearchParams` Zustand)
- Drill-down UF → Município breadcrumb
- Slider temporal duplo (para camadas com tempo)
- Legenda dinâmica painel direito com "Ver só esta"
- Tabs laterais Camadas/Filtros/Mapa/Exportar
- Opacidade por camada

### Sprint 6 (5 dias) — MOTOR JURÍDICO (início)
- STJ dados abertos + TCU webservice → base `jurisprudencia`
- Embedding bge-m3 das ementas (Eduardo já tem o modelo em mia-project)
- Busca híbrida vetorial+textual
- Tela `/teses` com resultados verificáveis

### Sprint 7 (7 dias) — GERADOR DE MINUTAS COM VERIFICAÇÃO
- Integração Claude API
- Redação com fundamentação
- Verificação automática de citações contra `jurisprudencia` (anti-alucinação)
- Tela `/minutas` + export DOCX

### Sprint 8 (10 dias) — AGREGADOR DE LEILÕES
Scrapers Caixa + Spy + Portal Leilão + TJs → dedup + parser LLM edital + enriquecimento geo + timeline do lote + alertas WhatsApp/email/webhook.

**Total: ~43 dias de desenvolvimento focado.**

---

## 11. CONTEXTO IMPORTANTE PARA PRÓXIMA SESSÃO

### 11.1 Regras do Eduardo (invioláveis)
1. **Sem mocks** — código funcionando com dados reais, não wireframes
2. **Sem mudança de stack sem autorização** — Next.js 16 + FastAPI + PostGIS é o padrão
3. **UI em português**
4. **Dark mode** Forest/Onyx + glassmorphism
5. **Consultar antes de decidir** estratégia (R2)
6. **Não inventar** — se falhou, dizer que falhou (R3)
7. **NÃO PEDIR** coisas que consigo fazer sozinho (ex: checar RAM via powershell)
8. **NÃO ROTULAR** como "feito" o que está parcial ou mock
9. **Ser autônomo** em tudo que não depende estritamente do Eduardo
10. **Registrar tudo no disco** — não confiar na memória do contexto

### 11.2 Armadilhas que travaram sessões anteriores
- **OneDrive + Turbopack dev = loop infinito** → resolvido movendo para C:\dev
- **Paths com acento ("Escritório")** — Next 16 recente tem bugs → evitado no novo path
- **Curl longo com 60s timeout em Next compilando** → não insistir, matar processo
- **Múltiplos node.exe disparados** → sempre matar com `Stop-Process -Name node -Force`

### 11.3 Decisões técnicas já tomadas (não questionar sem motivo)
- Monolítico modular em FastAPI
- PostGIS 3.4 com GIST em todas geometrias
- SQLAlchemy 2.0 sync
- JWT stateless
- Cache SHA256 em disco com TTL 24h padrão
- Materialized view para dashboard
- Next.js App Router com grupo `(dashboard)`
- Tailwind v4 + shadcn/ui
- react-leaflet 5 + CARTO Dark default
- SWR 2.4 para data fetching
- Docker Compose 2 containers

### 11.4 Meta-regras para próxima sessão
- **Ler este handoff inteiro antes de qualquer ação**
- **Consultar `docs/research/visual-audit/SYNTHESIS.md`** antes de decidir UX
- **Consultar `docs/research/catalog-layers-complete.md`** antes de adicionar camada
- **Consultar `docs/research/analise-agronomica-integrada.md`** antes de trabalhar na ficha do imóvel
- **Não repetir auditorias** — os 48 relatórios estão no disco
- **Priorizar pendências Seção 3.1 CRÍTICAS** antes de outras ideias
- **Validar cada passo via curl/build/docker logs** antes de dizer que funciona

---

## 12. PERSONA DO USUÁRIO (lembrete)

- **Eduardo Pinho Alves de Souza** — advogado OAB/MA 12.147
- **Escritório:** Guerreiro Advogados Associados — São Luís/MA
- **Email:** eduardo@guerreiro.adv.br
- **Áreas:** agronegócio, ambiental, tributário, cível/possessório
- **Tem:** conta gov.br Prata (Portal Transparência ativo), Docker Desktop, 32GB RAM, Windows 10, WSL2
- **Tem ativo:** GCP Project, MapBiomas Alerta conta, Embrapa AgroAPI (9), dados.gov.br token, Portal Transparência token
- **Não tem/não quer:** fases de teste, retrabalho, mocks, respostas evasivas, dependência excessiva de confirmação

---

*AgroJus — Handoff Sessão 6 — 2026-04-17 BRT*
*Substitui handoffs anteriores. Use como fonte de verdade para sessão 7.*
