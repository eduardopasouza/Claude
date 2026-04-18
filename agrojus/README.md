# AgroJus Enterprise

**Plataforma SaaS B2B de Inteligência Fundiária, Jurídica, Ambiental e de Mercado para o Agronegócio Brasileiro**

AgroJus cruza 20+ fontes públicas (IBAMA, INPE, FUNAI, MapBiomas, MapBiomas Alerta, BCB, IBGE/SIDRA, MTE, DataJud, DJEN, SIGEF/INCRA, Embrapa AgroAPI, ANA, ANM...) para oferecer **due diligence rural automatizada**, **compliance ambiental (MCR 2.9 / EUDR)**, **ficha completa por imóvel (CAR)**, **feed de publicações processuais (DJEN)** e **monitoramento em tempo real de alertas** — tudo com score de risco jurídico auditável.

> **Briefing completo:** `docs/HANDOFF_2026-04-17_sessao7.md` (documento mestre atual).
> **Pesquisa visual concorrencial:** `docs/research/visual-audit/SYNTHESIS.md` (48 plataformas auditadas).

---

## Estado atual (abr/2026)

**Backend** — FastAPI + PostGIS com **~90 endpoints** e **18 camadas PostGIS ativas**:

- ✅ CAR search + overlaps em 8 camadas (TI, UC, embargo ICMBio, PRODES, DETER Amazônia/Cerrado, MapBiomas, SIGEF)
- ✅ **MapBiomas Alerta** (GraphQL) — alertas em tempo real por CAR, JWT
- ✅ **Embrapa AgroAPI** — 7/9 APIs funcionais (Agritec ZARC, AGROFIT, Bioinsumos, AgroTermos, BovTrace, RespondeAgro, SmartSolos)
- ✅ **IBGE SIDRA choropleth** — 16 métricas (PAM 10 culturas + PPM 4 rebanhos + POP/PIB/PIB-PC)
- ✅ **DJEN/Comunica.PJe** — feed real de publicações por OAB (42 publicações do Eduardo OAB/MA 12147)
- ✅ **DataJud CNJ** — busca em 13 tribunais por CPF/CNPJ ou assunto
- ✅ **IBAMA SIFISC** — 16.121 autos de infração georreferenciados
- ✅ **Compliance MCR 2.9 + EUDR** — 5 fontes cruzadas (FUNAI, ICMBio, IBAMA, INPE, MTE)
- ✅ Mercado (CEPEA, BCB, Yahoo Finance CBOT)
- ⚠ Portal Transparência, dados.gov.br (tokens configurados, coletores pendentes)

**Frontend** — Next.js 16.2.3 + Turbopack + Tailwind v4 + shadcn/ui + react-leaflet:

| Rota | Status |
|---|---|
| `/login` | ✅ JWT real |
| `/` (dashboard) | ✅ KPIs |
| `/mapa` | ✅ 18 camadas PostGIS + 16 choropleth IBGE + 4 basemaps + inspector |
| `/imoveis/[car]` | ✅ **7/12 abas** (Visão · Compliance · Dossiê · Histórico · Agronomia · Clima · Jurídico) |
| `/publicacoes` | ✅ Feed DJEN real |
| `/processos` | ✅ DataJud real |
| `/mercado` | ✅ Cotações live |
| `/consulta` | ⚠ DeepSearch mock |
| `/compliance`, `/alertas` | ⚠ mocks standalone (ficha usa endpoints reais) |

---

## Stack

```
Backend:    Python 3.12 · FastAPI · SQLAlchemy 2.0 · PostGIS 3.4 (Postgres 16)
Frontend:   Next.js 16 · React 19 · TypeScript strict · Tailwind v4 · shadcn/ui
            react-leaflet 5 · SWR 2.4 · Recharts · Lucide
Infra:      Docker Compose 2 (db + backend) · WSL2 8GB · volume named agrojus_pgdata
Auth:       JWT PyJWT + bcrypt
Cache:      SHA256 em disco, TTL 24h padrão (1h DJEN)
ETL:        httpx streaming · geopandas · ogr2ogr · CSV COPY
```

---

## Início Rápido

```bash
# 1) Backend + Postgres
cd C:\dev\agrojus-workspace\agrojus
docker compose up -d
curl http://localhost:8000/health  # {"status":"healthy"}

# 2) Frontend
cd frontend_v2
npm install
npm run dev
# Abrir http://localhost:3000
```

> **PowerShell 5.1 não aceita `&&`.** Use `;` ou execute em linhas separadas. Git Bash / WSL funcionam normalmente.

**Teste rápido da ficha do imóvel:**
```
http://localhost:3000/imoveis/MA-2100055-0013026E975B48D9B4F045D7352A1CB9
```

---

## Dados carregados no PostGIS (~7.7M registros)

| Tabela | Registros | Fonte |
|---|---|---|
| `mapbiomas_credito_rural` | 5.614.207 | MapBiomas GPKG × SICOR |
| `sigef_parcelas` | 1.717.474 | INCRA SIGEF |
| `geo_mapbiomas_alertas` | 515.823 | MapBiomas Alerta × CAR |
| `mapbiomas_legality` | 493.032 | MapBiomas legalidade |
| `sicar_completo` (MA) | 352.215 | SICAR BigQuery |
| `geo_car` | 135.000 | SICAR WFS nacional |
| `environmental_alerts` | 104.284 | IBAMA + MTE |
| `geo_deter_amazonia` / `cerrado` | 50.000 cada | INPE TerraBrasilis |
| `geo_prodes` | 50.000 | INPE PRODES |
| `geo_autos_ibama` | **16.121** | IBAMA SIFISC (abr/2026) |
| `geo_armazens_silos` | 16.676 | CONAB SICARM |
| `geo_rodovias_federais` | 14.255 | DNIT |
| `geo_autos_icmbio` / `embargos_icmbio` | 10k / 5k | ICMBio |
| `geo_ferrovias` | 2.244 | ANTT |
| `geo_terras_indigenas` | 655 | FUNAI |
| `geo_unidades_conservacao` | 346 | ICMBio |
| `geo_frigorificos` | 207 | MAPA SIF |
| `geo_portos` | 35 | ANTAQ |
| `publicacoes_djen` | 42 | CNJ DJEN (Eduardo OAB/MA) |

---

## API — Endpoints Principais

| Rota | Descrição |
|---|---|
| `GET /health` | Healthcheck |
| `GET /api/v1/geo/postgis/catalog` | Lista 18 camadas PostGIS disponíveis |
| `GET /api/v1/geo/postgis/{layer_id}/geojson?bbox=&max_features=` | GeoJSON genérico por camada |
| `GET /api/v1/geo/ibge/choropleth/metrics` | Lista 16 métricas choropleth |
| `GET /api/v1/geo/ibge/choropleth/{metric}/{ano}?uf=MA` | Choropleth municipal SIDRA |
| `GET /api/v1/property/search?q=&uf=&municipio=` | Busca CAR |
| `GET /api/v1/property/{car}/geojson` | Polígono do imóvel |
| `GET /api/v1/property/{car}/overlaps/geojson` | 8 camadas sobrepostas |
| `GET /api/v1/embrapa/status` | OAuth Embrapa válido? |
| `GET /api/v1/embrapa/agritec/zoneamento?idCultura=&codigoIBGE=&risco=20` | ZARC |
| `GET /api/v1/embrapa/agrofit/produtos?cultura=&praga=` | Defensivos MAPA |
| `GET /api/v1/mapbiomas/alerts?start=&end=&limit=` | Alertas tempo real |
| `GET /api/v1/mapbiomas/property/{car}` | Alertas do imóvel |
| `GET /api/v1/publicacoes/stats/oab/{uf}/{numero}` | KPIs DJEN |
| `GET /api/v1/publicacoes/sync/oab/{uf}/{numero}` | Sync DJEN |
| `GET /api/v1/lawsuits/search/{cpf_cnpj}` | DataJud (13 tribunais) |
| `POST /api/v1/compliance/mcr29` | MCR 2.9 (CAR + lat/lon + cpf) |
| `POST /api/v1/compliance/eudr` | EUDR (cutoff 31/12/2020) |
| `GET /api/v1/market/*` | 11 endpoints CEPEA/BCB |

Swagger completo: `http://localhost:8000/docs`

---

## Ficha do Imóvel `/imoveis/[car]` — 10/12 abas

1. **Visão Geral** — score de compliance (0-100) + 8 KPI cards + alertas MapBiomas tempo real + MapPreview (mini-mapa)
2. **Compliance** — MCR 2.9 ↔ EUDR toggle, POST automatizado, banner APTO/RESTRITO/BLOQUEADO
3. **Dossiê** — 8 camadas cruzadas (TI, UC, embargo, PRODES, DETER, MapBiomas, SIGEF)
4. **Histórico** — timeline MapBiomas Alerta mensal + % do imóvel afetado
5. **Agronomia** — Agritec zoneamento ZARC + culturas do município
6. **Clima** — NASA POWER (temperatura, chuva, gráfico 30d)
7. **Jurídico** — DataJud CNJ (lookup por CPF/CNPJ do proprietário)
8. **Valuation** — NBR 14.653-3 nível expedito (preço UF × área − descontos por overlap)
9. **Logística** — KNN armazéns CONAB / frigoríficos SIF / portos ANTAQ + rodovia DNIT + ferrovia ANTT
10. **Crédito** — contratos SICOR via MapBiomas (5.6M) intersectando CAR, com chart por ano
11. ⏳ **Monitoramento** — webhooks (próximo sprint)
12. ⏳ **Ações** — laudo PDF, minuta DOCX, export GeoPackage

## Mapa `/mapa` — toolbar interativa

Canto superior direito do mapa tem 3 ferramentas:

| Ferramenta | Função |
|---|---|
| 🎯 **Analisar ponto** | Click em qualquer ponto → popup com município, TI próxima, DETER, clima, risco |
| ✏️ **Desenhar polígono** | Vértices + fechar → análise AOI (área, overlaps em 9 camadas, score) |
| 📤 **Upload** | Aceita `.geojson`, `.json`, `.kml`, `.gml` (memorial descritivo, polígonos de clientes) |

**Choropleth IBGE** usa **quintis** (quantile breaks): top 20% dos municípios = cor mais escura, cinco buckets uniformes. Evita o problema de distribuição log-normal (soja, bovinos, PIB) que pinta 99% igual com escala linear.

---

## Estrutura do Projeto

```
agrojus/
├── backend/
│   ├── app/
│   │   ├── api/              # 20 routers FastAPI
│   │   │   ├── embrapa.py         # 27 endpoints (NEW sessão 7)
│   │   │   ├── ibge_choropleth.py # 16 métricas (NEW sessão 7)
│   │   │   ├── mapbiomas.py       # GraphQL wrapper (NEW sessão 7)
│   │   │   ├── publicacoes.py     # DJEN
│   │   │   ├── geo_layers.py      # 18 camadas PostGIS
│   │   │   ├── property.py        # search + geojson + overlaps
│   │   │   └── compliance.py      # MCR 2.9 + EUDR
│   │   ├── collectors/       # 23 coletores de dados
│   │   │   ├── embrapa.py         # OAuth2 + 9 APIs
│   │   │   ├── mapbiomas_alerta.py # GraphQL JWT (NEW)
│   │   │   ├── djen.py            # CNJ Comunica.PJe
│   │   │   ├── datajud.py, ibge.py, ibama.py, nasa_power.py, ...
│   │   ├── models/database.py # SQLAlchemy + PostGIS + geometry
│   │   ├── services/
│   │   ├── middleware/
│   │   └── main.py
│   ├── scripts/              # 29 ETLs (download_ibama_autos, sicar_bigquery, ...)
│   └── Dockerfile
├── frontend_v2/
│   ├── src/
│   │   ├── app/(dashboard)/
│   │   │   ├── imoveis/[car]/page.tsx  # ficha do imóvel (NEW sessão 7)
│   │   │   ├── mapa/, mercado/, publicacoes/, processos/, ...
│   │   ├── components/
│   │   │   ├── imovel/     # PropertyHeader, TabNav, 7 Tabs
│   │   │   ├── mapa/       # MapComponent v2, LayerTreePanel, Inspector, Stats
│   │   │   └── layout/
│   │   └── lib/
│   │       ├── layers-catalog.ts   # 119 camadas (32 ativas, 87 em roadmap)
│   │       ├── basemaps.ts         # 4 basemaps
│   │       └── api.ts
│   └── next.config.ts
├── docs/
│   ├── HANDOFF_2026-04-17_sessao7.md   # ← mestre atual
│   ├── ROADMAP.md                      # 8 sprints
│   └── research/                       # auditoria 48 sites + blueprints
└── docker-compose.yml
```

---

## Credenciais (em `backend/.env` — gitignored)

```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=***
EMBRAPA_CONSUMER_KEY=***
EMBRAPA_CONSUMER_SECRET=***
DADOS_GOV_TOKEN=***
PORTAL_TRANSPARENCIA_TOKEN=***
DATAJUD_API_KEY=***  # pública CNJ
```

---

## Licença

Projeto proprietário. Todos os direitos reservados.
Titular: **Eduardo Pinho Alves de Souza** — OAB/MA 12.147 — Guerreiro Advogados Associados — São Luís/MA.
