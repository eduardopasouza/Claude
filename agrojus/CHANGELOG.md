# Changelog — AgroJus

Todas as mudanças notáveis do projeto, por sessão de trabalho.
Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), versionamento [SemVer](https://semver.org/lang/pt-BR/).

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
