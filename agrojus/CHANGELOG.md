# Changelog — AgroJus

Todas as mudanças notáveis do projeto, por sessão de trabalho.
Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [0.10.0] — 2026-04-17 · Sessão 9 · Sprint 3

### Added — MCR 2.9 Expandido (32 critérios em 5 eixos)

**Backend — `app/services/mcr29_expanded.py` + endpoints em `compliance.py`:**
- 32 critérios em 5 eixos: Fundiário (8) · Ambiental (8) · Trabalhista (6) · Jurídico (5) · Financeiro (5)
- Status por critério: `passed` / `failed` / `pending` / `not_applicable`
- Peso por critério reflete impacto no indeferimento (bloqueantes com `weight >= 2.5`)
- Score 0-1000 ponderado + risk level (LOW/MEDIUM/HIGH/CRITICAL)
- 13/32 critérios com **dados reais integrados** (41%); 19 `pending` aguardam Sprint 4 (dados.gov.br) e fontes pagas (CCIR, ITR, CNDT, CEIS/CNEP via Portal Transparência, etc.)

**Novos endpoints:**
- `GET /api/v1/compliance/mcr29/criteria` → metadados dos 32 critérios agrupados por eixo
- `POST /api/v1/compliance/mcr29/full` → executa avaliação, retorna `axis_scores`, `criteria[]`, `sources_consulted`, `pending_sources`, `recommendation`
- `POST /api/v1/compliance/mcr29/full/pdf` → laudo PDF A4 (4 páginas) com tabela por eixo, destaque em falhas/pendentes, lista de fontes

**Frontend `/compliance` — reescrito do zero (antes: mock 3 rows):**
- Form CAR + CPF/CNPJ com query string auto-run (`?car=...`)
- Banner geral APTO / RESTRITO / BLOQUEADO / INDETERMINADO + score + recomendação
- 5 cards de score por eixo com ícones distintos
- Accordion por eixo (auto-expande se há falhas) mostrando cada critério com evidência JSON expansível
- Botão "Exportar laudo PDF"
- Tela inicial com overview dos 5 eixos

**`ComplianceTab` da ficha** ganhou card de destaque com link para `/compliance?car={CAR}&auto=true`, preservando o toggle básico MCR 2.9 / EUDR.

### Commits
| Hash | Descrição |
|---|---|
| `b9182bd` | feat(compliance): service expandido + 3 endpoints + PDF |
| `ca26f3f` | feat(frontend): /compliance standalone + link do ComplianceTab |

---

## [0.9.0] — 2026-04-17 · Sessão 9 · Sprint 2e

### Added — Sistema de Webhooks (tempo real)

**Backend**
- Modelos `Webhook` e `WebhookDelivery` em Postgres (novos) com filtros por `car_code` e `cpf_cnpj`, 9 event types e secret HMAC-SHA256 opcional.
- Service `webhook_dispatcher` com dispatch async paralelizado (asyncio.gather) e assinatura `X-AgroJus-Signature`.
- Router `/api/v1/webhooks` com CRUD completo + `POST {id}/test` (dispara payload sintético) + `GET {id}/deliveries` (logs paginados).
- `MonitoringService._record_alert()` integra dispatch automático em background task — cada novo alerta (MapBiomas/DETER/IBAMA/DJEN/CAR status) dispara webhooks aplicáveis.

**Frontend — aba Monitoramento da ficha**
- Form de cadastro com seletor multi-select de 9 event types.
- Lista de webhooks com toggle ativo/pausado, botão de teste, logs expansíveis (20 entregas, auto-refresh 15s).
- Drawer de entrega detalha status code, duration, payload JSON e response body.

### Added — Aba Ações da ficha (fecha 12/12)

**Backend — 5 novos endpoints em `/api/v1/property`**
- `GET /{car}/laudo.pdf` — laudo consolidado A4 via reportlab: identificação, sobreposições (TI/UC/embargos/PRODES/DETER/autos IBAMA), crédito rural vinculado, avisos legais.
- `GET /{car}/export.geojson` — GeoJSON FeatureCollection (CAR + overlaps) em EPSG:4326 com metadados embarcados.
- `GET /{car}/export.gpkg` — GeoPackage OGC SQLite com 1 layer por tipo (via geopandas, sem ogr2ogr).
- `GET /{car}/export.shp.zip` — Shapefile ESRI zipado (1 .shp por layer).
- `POST /{car}/minuta` — gera minuta jurídica via Claude API (anthropic SDK). Tipos: notificação extrajudicial, ação anulatória de auto, defesa administrativa, contrarrazões, livre. 501 com mensagem amigável se `ANTHROPIC_API_KEY` não configurada.

**Frontend — aba Ações**
- 4 cards de download (PDF, GeoJSON, GPKG, Shapefile) com loading state.
- Painel de minuta com selector de tipo, destinatário, lista de processos relacionados, observações do advogado.
- Resultado em markdown renderizado com contador de tokens, copiar para clipboard, download .md.
- Aviso explícito de revisão humana obrigatória; lacunas marcadas como `[buscar precedente]`.

### Added — dependências

- `anthropic>=0.45.0` no `requirements.txt` (para geração de minutas via Claude).
- Settings novas: `anthropic_api_key`, `anthropic_model` (default `claude-opus-4-7`), `webhook_timeout_seconds` (10s), `webhook_max_retries` (3).

### Fixed

- Query `_fetch_property_base` fazia `UNION` entre `sicar_completo.cod_municipio_ibge` (integer) e `geo_car.cod_municipio_ibge` (text) — `UNION types text and integer cannot be matched`. Corrigido castando ambos para `text`.

### Milestone — Ficha do imóvel 100% completa

Após Sprint 2e, a ficha `/imoveis/[car]` tem as **12 abas** finais:
Visão Geral · Compliance · Dossiê · Histórico · Agronomia · Clima · Jurídico · Valuation · Logística · Crédito · **Monitoramento** · **Ações**

### Commits

| Hash | Descrição |
|---|---|
| `77142b2` | feat(webhooks): sistema completo com dispatch + CRUD + logs |
| `a34cf24` | feat(property): laudo PDF + exports GeoJSON/GPKG/SHP + minuta Claude |
| `1630150` | feat(ficha): MonitoramentoTab + AcoesTab — ficha 12/12 |

---

## [0.8.0] — 2026-04-18 · Sessão 8

### Added — Cotações & Mercado (Agrolink + UX "minha região")

**Backend**
- Collector `agrolink.py` — scrape das páginas `/cotacoes/historico/{uf}/{slug}` (HTML puro, até **265 meses** de histórico mensal por UF).
- **13 commodities cobertas**: Grãos (soja, milho, sorgo, trigo, arroz, feijão), Permanentes/Industriais (café, algodão, cana-de-açúcar, açúcar), Proteínas (boi gordo, frango, leite).
- Cobertura: 5–26 UFs por commodity (milho cobre quase Brasil inteiro; soja 20 UFs; leite 18 UFs; boi 20 UFs).
- Endpoints:
  - `GET /api/v1/market/quotes/agrolink/{commodity}` → histórico + uf_stats
  - `GET /api/v1/market/quotes/agrolink` → lista commodities
  - `GET /api/v1/geo/ibge/choropleth/uf/preco/{commodity}` → GeoJSON BR UF com preço atual estadual
- Tesseract OCR instalado no container (fallback anti-scraping futuro; não usado no fluxo atual).

**Frontend `/mercado` — UX centrada na UF do usuário**
- `UFPicker` grande (default MA, persistido em localStorage).
- Hero "**Preço de hoje em {Estado}**" com 13 commodity cards (preço estadual + seta colorida % vs Brasil).
- Gráfico histórico Recharts ao clicar num card: estadual + nacional, range 1/2/5/10 anos + "tudo".
- Indicadores BCB (SELIC, dólar, IPCA, IGP-M, CDI) compactos.
- 6 notícias de mercado embed (link pra `/noticias`).
- **Removidos**: CBOT/Yahoo Finance, cards CEPEA duplicados, labels "fonte: X".

**Frontend `/mapa`**
- `PriceChoroplethWidget` — botão "Colorir por preço" no topo-esquerdo do mapa com dropdown agrupado (Grãos / Industriais / Proteínas) — 10 commodities. Toggle exclusivo.
- 10 novas camadas no catálogo (`preco_*_uf`) com endpoint `ibge_choropleth_uf`.
- `ZoomControl` no MapPreview (mini-mapa da ficha) + scroll-wheel zoom + drag habilitados.

### Added — Ficha do Imóvel `/imoveis/[car]` (10/12 abas)

- **Sprint 2a** (sessão 7): Visão Geral, Dossiê, Histórico MapBiomas, Agronomia (Agritec).
- **Sprint 2b** (sessão 7): Compliance (MCR 2.9 + EUDR), Clima (NASA POWER), Jurídico (DataJud).
- **Sprint 2c** (sessão 7): Valuation (NBR 14.653-3 nível expedito), Logística (KNN PostGIS), Crédito (SICOR 5.6M contratos).
- **MapPreview** no header da ficha com polígono CAR em Leaflet.

### Added — Ferramentas do mapa (sessão 7)

- **Point analysis** — click em qualquer ponto → popup com município, TI próxima, DETER, clima, jurisdição.
- **Draw polygon** — desenhar AOI → analisa overlaps em 9 camadas + score 0-100.
- **Upload GeoJSON/KML/GML** — parser built-in para memorial descritivo, CAR não oficial.
- **Backend**: novo endpoint `POST /geo/aoi/analyze` com ST_Area + overlaps.

### Changed — Visualização

- **Choropleth IBGE**: escala linear → **quintis** (5 buckets uniformes). Datasets log-normais agora têm diferenciação visual real.
- **OmniSearch (TopBar)**: regex detecta código CAR e roteia para `/imoveis/[car]`.
- **Catálogo `layers-catalog.ts`**: 42 camadas ativas (antes 18) + 10 de preço por UF (Agrolink).

### Added — Dados Sessão 7

- **Embrapa AgroAPI** — 7/9 APIs funcionais (27 endpoints REST)
- **IBGE Choropleth** — 16 métricas (PAM 10 culturas + PPM 4 rebanhos + POP/PIB)
- **MapBiomas Alerta GraphQL** — auth JWT via mutation signIn
- **IBAMA SIFISC** — 16.121 autos de infração georreferenciados em `geo_autos_ibama`
- **Notícias RSS** — nova rota `/noticias` (Canal Rural, Agrolink, Notícias Agrícolas, etc.)

### Housekeeping (sessão 8)

- 7 handoffs antigos movidos para `docs/_archive/handoffs_antigos/`.
- 6 docs superseded (CONTEXTO_COMPLETO, CONTINUIDADE_PROMPT, FRONTEND_SPEC, INVENTARIO_FEATURES, ROADMAP_FASEADO_v1, STATUS_FONTES_DADOS) movidos para `docs/_archive/`.
- `docs/` agora tem 9 arquivos ativos (antes: 22+).
- README reescrito com estrutura real do projeto e índice de documentação.

### Commits

| Hash | Descrição |
|---|---|
| `324b3f6` | Sprint 1 — Embrapa + IBGE choropleth + MapBiomas + IBAMA script |
| `2d6bd06` | Sprint 2a — ficha 4 abas + IBAMA 16k |
| `df70f47` | Sprint 2b — Compliance + Clima + Jurídico (7 abas) |
| `2732e38` | OmniSearch CAR routing |
| `bd0815f` | Fix render choropleth + docs consolidadas |
| `d3f2dcf` | Sprint 2c — Valuation + Logística + Crédito (10 abas) |
| `3f9de00` | Sprint 2d — toolbar mapa (point/draw/upload) + quintis |
| `613e4b7` | Housekeeping docs |
| `88223c0` | /mercado com gráficos + /noticias + choropleth UF SIDRA |
| `17fe965` | Cotações regionais Notícias Agrícolas |
| `d6d551d` | Agrolink histórico UF 22 anos + preço no mapa |
| `8a976fe` | Fix slugs Agrolink — 7 commodities × até 26 UFs |
| `506ba60` | +6 commodities (total 13) + 10 camadas choropleth preço |
| `426a6b4` | UX /mercado centrada na região + widget preço mapa + zoom MapPreview |

---

## [0.7.0-unreleased-consolidation] — 2026-04-17 · Sessão 7

### Added — Cotações regionalizadas (Agrolink)
- **Collector Agrolink UF** (`app/collectors/agrolink.py`) — scrape das páginas `/cotacoes/historico/{uf}/{slug}` que têm **texto puro** (tabela HTML com mês/ano, preço estadual, preço nacional) desde 2003. Até **265 meses** de histórico por UF.
- **7 commodities cobertas**: soja, milho, café, trigo, arroz, feijão, boi gordo.
- **Endpoints:**
  - `GET /api/v1/market/quotes/agrolink/{commodity}` — histórico por UF + uf_stats
  - `GET /api/v1/market/quotes/agrolink` — lista commodities
  - `GET /api/v1/geo/ibge/choropleth/uf/preco/{commodity}` — GeoJSON choropleth com preço atual estadual por UF (para o mapa)
- **Tesseract OCR** instalado no backend (Dockerfile + `pytesseract`) como fallback para decodar preços em imagens PNG anti-scraping (não foi necessário — o histórico está em texto).
- **Dependências:** `inmetpy>=0.1.1`, `pytesseract==0.3.13`, `Pillow>=10.0.0`.

### Frontend `/mercado` — nova seção "Preço médio por UF (Agrolink)"
- Tabela ordenada por preço com 20+ UFs.
- Select de commodity (Soja, Milho, Café, Boi, Trigo, Arroz, Feijão).
- Comparação vs preço nacional (% diff, colorizado).
- Click em UF abre **gráfico de série histórica** Recharts com linha estadual + nacional (últimos 60 meses).
- Link para fonte original.

### Novas camadas no catálogo (4)
- `preco_soja_uf`, `preco_milho_uf`, `preco_cafe_uf`, `preco_boi_uf`
- Endpoint: `ibge_choropleth_uf` com prefixo `preco_` redireciona pro endpoint Agrolink.
- Mapa do Brasil colorido pelo preço **atual** do produto em cada estado.

### Housekeeping
- **docs/** reorganizado: 7 handoffs antigos (sessões 1-5 + HANDOFF inicial) movidos para `docs/_archive/handoffs_antigos/`.
- **docs/** superseded: `CONTEXTO_COMPLETO.md`, `CONTINUIDADE_PROMPT.md`, `FRONTEND_SPEC.md`, `INVENTARIO_FEATURES.md`, `ROADMAP_FASEADO_v1.md`, `STATUS_FONTES_DADOS.md` movidos para `docs/_archive/` (substituídos por README/ROADMAP/CHANGELOG na raiz + HANDOFF sessão 7).
- **README.md** atualizado com estrutura de arquivos real e índice de documentação.
- Pasta `downloads/` está vazia (dados foram limpos); arquivos grandes em `data/` estão gitignored.
- Pasta `frontend/` (versão vanilla JS legada) marcada como descontinuada no README.

## [0.7.0] — 2026-04-17 · Sessão 7

### Added — Dados & Backend
- **Embrapa AgroAPI** — 7/9 APIs assinadas ativas (Agritec ZARC, AGROFIT defensivos, Bioinsumos, AgroTermos, BovTrace, RespondeAgro, SmartSolosExpert). 27 endpoints REST em `/api/v1/embrapa/*`. Paths descobertos via Swagger + validados por curl com OAuth2 real.
- **IBGE Choropleth** — novo módulo `/api/v1/geo/ibge/choropleth/{metric}/{ano}?uf=` com 16 métricas (PAM 10 culturas + PPM 4 rebanhos + POP/PIB/PIB-PC). 14 camadas stub do catálogo saíram de "em breve".
- **MapBiomas Alerta GraphQL** — autenticação via mutation `signIn` + JWT Bearer. Endpoints: `status`, `alerts`, `alert/{code}`, `property/{car}`, `territories`. Retorna alertas tempo real (SAD, DETER, GLAD, SIRAD-X).
- **IBAMA SIFISC** — 16.121 autos de infração georreferenciados carregados em `geo_autos_ibama` (18ª camada PostGIS). URL nova descoberta: era SICAFI, virou SIFISC + ZIP.
- **Property endpoints** (para ficha): `/property/{car}/neighbors` (KNN armazéns/frigos/portos), `/property/{car}/credit` (SICOR via MapBiomas 5.6M), `/property/{car}/valuation` (NBR 14.653-3 nível expedito).
- **AOI Analyze** — `POST /api/v1/geo/aoi/analyze` recebe GeoJSON de polígono custom e retorna área, centróide, overlaps em 9 camadas, score de compliance, risk level.

### Added — Frontend
- **Ficha do Imóvel** `/imoveis/[car]` com **10/12 abas**:
  1. Visão Geral (score 0-100 + 8 KPIs + alertas MapBiomas tempo real)
  2. Compliance (MCR 2.9 ↔ EUDR toggle, banner APTO/RESTRITO/BLOQUEADO)
  3. Dossiê (8 camadas agrupadas)
  4. Histórico (timeline MapBiomas mensal)
  5. Agronomia (Agritec ZARC + culturas do município)
  6. Clima (NASA POWER 30 dias)
  7. Jurídico (DataJud CNJ via CPF/CNPJ)
  8. Valuation (NBR 14.653-3 com descontos por overlap)
  9. Logística (KNN armazéns/frigos/portos + rodovia/ferrovia)
  10. Crédito (contratos SICOR por ano)
- **MapPreview** no header da ficha (mini-mapa leaflet dynamic import)
- **MapTools** (toolbar canto superior direito do mapa):
  - 🎯 Analisar ponto (click → popup lateral com risco + município + TI + DETER)
  - ✏️ Desenhar polígono (vértices + fechar → análise AOI)
  - 📤 Upload GeoJSON/KML (parser built-in, plota + analisa)
- **OmniSearch** (TopBar) agora detecta regex `^[A-Z]{2}-\d{7}-[A-F0-9]{32}$` e roteia para `/imoveis/[car]`.

### Changed
- **Choropleth IBGE** — escala linear → **quintis** (quantile breaks). Datasets agrícolas são log-normais; linear pintava 99% igual. Quintis dividem uniformemente: top 20% escuro → bottom 20% claro.
- **Catálogo de camadas** — 14 novas ativas (endpoint `ibge_choropleth`) + 1 nova postgis (`autos_ibama`) = 32/119 ativas (27%).
- **LayerConfig type** — novos campos `defaultYear` e `colorScheme` + novo endpoint type `"ibge_choropleth"`.

### Fixed
- **Render choropleth no mapa** — switch em `ActiveLayer` não tratava `"ibge_choropleth"`, caía no default e não fetchava. Adicionado case.
- **SIDRA URL** — usava `/f/n` (só nomes) que não retornava código IBGE `D1C`. Trocado para `/f/u` (unified).
- **SmartSolos base path** — era `/smartsolos/v1` (404), correto é `/smartsolos/expert/v1`.
- **MapBiomas auth** — endpoint REST `/auth/login` retorna 500 (deprecated). Correto é mutation GraphQL `signIn`.

### Infra
- 8 commits sequenciais na branch `claude/continue-backend-dev-sVLGG`.
- 42 arquivos novos (backend collectors/routers/scripts, frontend tabs/components, docs).
- Build frontend limpo (Next.js 16.2.3 Turbopack, 10 rotas + 1 dinâmica `/imoveis/[car]`).

---

## [0.6.0] — 2026-04-17 · Sessão 6

### Added
- **DJEN/Comunica.PJe** integrado — 42 publicações reais da OAB/MA 12147 (Eduardo) persistidas em `publicacoes_djen`. Frontend `/publicacoes` com filtros + drawer de detalhe.
- **DataJud CNJ** — `/processos` rewrite, busca real por CPF/CNPJ em 13 tribunais.
- **MapComponent v2** — LayerTreePanel (árvore temática esquerda) + BasemapSwitcher (4 mapas base) + LayerInspector (drawer on-click) + StatsDashboard (painel inferior).
- **Catálogo 119 camadas** em 23 temas (17 ativas + 102 stubs) em `layers-catalog.ts`.
- **48 auditorias visuais** de plataformas concorrentes em `docs/research/visual-audit/*` + SYNTHESIS.md com 25 padrões prioritários e 7 killer gaps.
- **Blueprints** — `analise-agronomica-integrada.md` (15 perguntas-chave da ficha) + `cadeia-dominial-acesso-real.md` + `dados-gov-guia.md` (32 datasets priorizados).

### Changed
- **Projeto movido** de OneDrive para `C:\dev\agrojus-workspace\agrojus\` (resolveu loop Turbopack + sync OneDrive).
- **Docker compose** com `mem_limit` ajustado (backend 2g, db 1g) + Postgres tuning conservador.
- **`.wslconfig`** limita WSL2 a 8GB RAM.

### Fixed
- **OmniSearch TopBar** — handler real (era placeholder).
- **`next.config.ts`** — path absoluto (remove warning Turbopack).
- **ENV var `NEXT_PUBLIC_API_URL`** — finalmente documentada.

---

## [0.5.0] — 2026-04-16 · Sessão 5

### Added
- **DJEN collector base** (sem persistência, só API).
- **MapBiomas credito_rural** — 5.614.207 contratos carregados via GPKG.
- **SIGEF parcelas** — 1.717.474 parcelas INCRA certificadas.

---

## [0.4.0] — 2026-04-15 · Sessão 4

### Added
- **PostGIS layer registry** com 10 camadas iniciais (TI, UC, embargos, PRODES, DETER, SICAR, SIGEF, rodovias, ferrovias, portos).
- **Property search + overlaps** endpoint.
- **NASA POWER collector** (clima).

---

## [0.3.0] — 2026-04-15 · Sessões 2-3

### Added
- **Dashboard** com materialized view.
- **Market** — 11 endpoints CEPEA/BCB + Yahoo Finance CBOT.
- **Compliance MCR 2.9 + EUDR** (6 checks cada).
- **Jurisdicao** service com 27 UFs.

---

## [0.2.0] — 2026-04-15 · Sessão 1

### Added
- **FastAPI scaffold** com auth JWT (PyJWT + bcrypt).
- **SQLAlchemy 2.0** + modelos base (Property, EnvironmentalAlert, LegalRecord, RuralCredit, LandPrice, MarketData, MonitoringAlert).
- **Docker Compose** — 2 containers (db postgis/postgis:16-3.4 + backend Python 3.12).
- **Frontend Next.js 16** scaffold com `(dashboard)` group + login.

---

## [0.1.0] — 2026-04-14 · Kickoff

- Conceito validado: plataforma SaaS B2B de inteligência agrojurídica.
- Stack definida: FastAPI + PostGIS + Next.js + shadcn/ui.
- Credenciais obtidas: GCP, MapBiomas Alerta, Embrapa AgroAPI (9 APIs), dados.gov.br, Portal Transparência, DataJud.
