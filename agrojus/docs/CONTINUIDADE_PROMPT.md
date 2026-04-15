# PROMPT DE CONTINUIDADE — AgroJus Enterprise

## Contexto do Projeto

Você está assumindo o desenvolvimento do **AgroJus**, uma plataforma de inteligência agropecuária enterprise para o mercado brasileiro.

- **Repositório:** `c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus`
- **Branch Git:** `claude/continue-backend-dev-sVLGG`
- **Último commit:** `c2aae7e` — feat: login overlay UI + handoff v2 + CSS auth
- **Handoff completo:** `docs/HANDOFF_2026-04-15.md`
- **⭐ LEIA PRIMEIRO:** `docs/CONTEXTO_COMPLETO.md` — contexto de produto, concorrentes, todas as fontes de dados

---

## O Que É o AgroJus

Plataforma SaaS B2B de inteligência fundiária, ambiental e de mercado para:
- **Bancos e Cooperativas de Crédito Rural** — compliance MCR 2.9 (BCB), auditoria EUDR
- **Traders e Exportadores** — monitoramento de commodities e cadeia de fornecimento limpa
- **Escritórios Jurídicos Rurais** — dossiê consolidado de CPF/CNPJ (IBAMA, MTE, DataJud)
- **Fintechs Agro** — motor de score de risco ambiental e trabalhista

**Diferencial:** cruzamento em tempo real de 15+ bases de dados oficiais (IBAMA, FUNAI, MapBiomas, INPE DETER Amazônia **+ Cerrado**, MTE, BCB, IBGE, Yahoo Finance, NASA POWER) em uma única API REST.

---

## Stack Tecnológico

| Camada | Tecnologia |
|---|---|
| Backend API | FastAPI + SQLAlchemy + Uvicorn |
| Banco de Dados | PostgreSQL 15 + PostGIS |
| Frontend Principal | Vanilla JS + Vite + Leaflet (GIS Engine v2) |
| Infraestrutura | Docker Compose (containers: `db` + `backend`) |
| ETL / Coleta | Python scripts (pdfplumber, httpx, geopandas, ogr2ogr) |

---

## Estado Atual do Banco de Dados (2026-04-15)

```bash
docker exec agrojus-backend-1 python scripts/db_status.py
docker exec agrojus-backend-1 python scripts/db_inventory.py  # inventário completo
```

| Tabela | Registros | Source | Status |
|---|---|---|---|
| `environmental_alerts` (IBAMA) | **103.668** | dadosabertos.ibama.gov.br | ✅ |
| `environmental_alerts` (MTE) | **614** | gov.br/trabalho | ✅ |
| `mapbiomas_credito_rural` | **5.614.207** | MapBiomas GPKG | ✅ |
| `mapbiomas_agriculture_cycles` | **15.180** | MapBiomas Stats | ✅ |
| `mapbiomas_coverage_states` | **953** | MapBiomas Stats | ✅ |
| `mapbiomas_irrigation_stats` | **7.174** | MapBiomas Stats | ✅ |
| `mapbiomas_mining_stats` | **1.294** | MapBiomas Stats | ✅ |
| `mapbiomas_pasture_age` | **1.911** | MapBiomas Stats | ✅ |
| `mapbiomas_pasture_vigor` | **147** | MapBiomas Stats | ✅ |
| `geo_terras_indigenas` | **655** | FUNAI WFS | ✅ |
| `geo_deter_amazonia` | **50.000** | INPE TerraBrasilis WFS | ✅ |
| `geo_deter_cerrado` | **50.000** | INPE TerraBrasilis WFS | ✅ **NOVO** |
| `geo_armazens_silos` | **16.676** | MapBiomas | ✅ |
| `geo_frigorificos` | **207** | MapBiomas | ✅ |
| `geo_rodovias_federais` | **14.255** | MapBiomas | ✅ |
| `geo_ferrovias` | **2.244** | MapBiomas | ✅ |
| `geo_portos` | **35** | MapBiomas | ✅ |
| `market_quotes` | **24** | Yahoo Finance CBOT/CME | ✅ |
| `rural_credits` | **0** | BCB SICOR (em manutenção) | ⏳ |
| `ana_outorgas` | **0** | ANA SNIRH (ETL criado) | ⏳ |
| `properties` | **0** | SICAR (~40 GB) | ⬜ |

---

## APIs Funcionando (http://localhost:8000)

```
GET  /api/v1/dashboard/metrics              → KPIs reais: 8 indicadores + geo_summary
GET  /api/v1/market/quotes                  → 10 cotações CBOT/CME em BRL
GET  /api/v1/compliance/dossier/{cpf_cnpj}  → Dossiê CPF/CNPJ (IBAMA + MTE)
GET  /api/v1/geo/layers/{id}/geojson        → GeoJSON PostGIS para mapa Leaflet
GET  /api/v1/geo/layers/desmatamento_cerrado/geojson → DETER Cerrado (50k polígonos locais)
GET  /api/v1/geo/analyze-point              → Análise coordenada (risco, FUNAI, DETER, clima)
GET  /api/v1/geo/catalogo                   → Catálogo completo de 20+ camadas (status real)
GET  /api/v1/geo/municipios/{cod}/producao  → PAM SIDRA (soja, milho, café...)
GET  /api/v1/geo/clima                      → NASA POWER (any coordinate)
GET  /docs                                  → Swagger UI completo
```

---

## Frontend GIS Engine v2 (http://localhost:5173)

- **Basemap Switcher:** Satélite / Terreno / OSM
- **Multi-layer Overlay:** Embargos + TI + DETER + Cerrado + Crédito Rural
- **Right-click → Análise de Ponto:** risco, município, FUNAI, DETER, clima, jurisdição
- **Bounding Box Search:** Shift+drag → alertas na região
- **Coord Picker:** click esquerdo copia lat,lon
- **Legenda Dinâmica** com botão ✕ por camada

**Camadas disponíveis no select do mapa:**
- `desmatamento` → DETER Amazônia (WFS em tempo real)
- `desmatamento_cerrado` → DETER Cerrado (50k polígonos PostGIS local ✅)
- `embargos` → 103k IBAMA polígonos
- `terras_indigenas` → FUNAI WFS
- `parcelas_financiamento` → 5.6M MapBiomas
- `municipios` → Malha IBGE

---

## Diagnóstico de Fontes de Dados

### O que funciona sem credenciais ✅
| Fonte | Endpoint | Dados |
|---|---|---|
| IBAMA Embargos | dadosabertos.ibama.gov.br | 103k polígonos |
| MTE Lista Suja | gov.br/trabalho-e-emprego | 614 CPF/CNPJ |
| INPE DETER Amazônia | terrabrasilis.dpi.inpe.br WFS | 50k polígonos |
| INPE DETER Cerrado | terrabrasilis.dpi.inpe.br WFS | 50k polígonos |
| MapBiomas (GPKG/Stats) | storage.googleapis.com | 5.6M+ registros |
| FUNAI | geoserver.funai.gov.br WFS | 655 TIs |
| Yahoo Finance | query1.finance.yahoo.com | 10 commodities CBOT/CME |
| NASA POWER | power.larc.nasa.gov | Clima em qualquer coord |
| IBGE SIDRA | apisidra.ibge.gov.br | PAM/PPM por município |
| BasedosDados GraphQL | backend.basedosdados.org | Metadados (dados precisam GCP) |

### Bloqueado / Requer credencial ⚠️
| Fonte | Bloqueador | Solução |
|---|---|---|
| dados.gov.br CKAN | Retorna 401 (migrou plataforma) | usar URLs diretas por dataset |
| BasedosDados BigQuery | Requer `GCP_PROJECT_ID` | adicionar ao .env → 1TB/mês grátis |
| BCB SICOR OData | 503 Service Unavailable (manutenção) | tentar novamente em outro horário |
| ANA SNIRH Outorgas | Endpoints de arquivo 404 | descobrir URL correta no portal |
| ICMBio UCs | DNS falha do container Docker | baixar manualmente do ICMBio |
| SICAR/CAR | ~40 GB por estado | download manual prioritário |

---

## ROADMAP — Estado e Próximas Tarefas

### ✅ FASE 7 — Base de Dados Core (CONCLUÍDA)

- [x] **7.1** ETL Lista Suja MTE — 4 → 614 registros (parser regex + pdfplumber)
- [x] **7.2** Scraper de cotações — Yahoo Finance CBOT/CME (10 commodities, câmbio HG Brasil)
- [x] **7.3** `GET /api/v1/dashboard/metrics` — 8 KPIs reais do PostgreSQL + geo_summary

### ✅ FASE 7.5 — Expansão de Dados (CONCLUÍDA NESTA SESSÃO)

- [x] **7.5.1** DETER Cerrado → tabela `geo_deter_cerrado` (50k polígonos via WFS)
- [x] **7.5.2** Layer `/layers/desmatamento_cerrado/geojson` via PostGIS com bbox filter
- [x] **7.5.3** Catálogo de camadas expandido (`camadas.py`) com 20+ fontes catalogadas
- [x] **7.5.4** Dashboard metrics expandido: DETER Amazônia+Cerrado, TIs, armazéns, frigoríficos
- [x] **7.5.5** ETLs criados: `etl_deter_cerrado.py`, `etl_ana_outorgas.py`, `etl_sicor_bcb.py`
- [x] **7.5.6** Catalogadores: `bd_catalog.py` (BasedosDados GraphQL), `catalog_data_sources.py`
- [x] **7.5.7** `db_inventory.py` — inventário completo de todas as tabelas com contagens

### 🔴 FASE 8 — Integração Dados Externos (PRÓXIMA PRIORIDADE)

**8.1 — BasedosDados / BigQuery** ← **MÁXIMA PRIORIDADE**
- Requer: `GCP_PROJECT_ID` no `.env` (criar projeto gratuito em console.cloud.google.com)
- Tabelas de alto valor:
  - `basedosdados.cnpj.Empresas` (2.7 bilhões de linhas) — enrichment CNPJ completo
  - `basedosdados.cnpj.Estabelecimentos` (2.8 bilhões) — razão social, CNAE, endereço
  - `basedosdados.censo_agropecuario.Municipio` (20k linhas) — PAM por município
  - `basedosdados.trabalho_escravo` — complementar ao MTE
- Arquivo: `backend/scripts/etl_basedosdados.py` (já existe, precisa GCP)

**8.2 — BCB SICOR Crédito Rural** ← Alta prioridade
- O OData retornou 503 (manutenção) — tentar novamente
- Arquivo: `backend/scripts/etl_sicor_bcb.py`
- Alternativa: bulk download em `dadosabertos.bcb.gov.br`

**8.3 — ANA Outorgas de Água**
- ETL escrito em `etl_ana_outorgas.py` — precisar descobrir URL correta do arquivo ZIP
- Portal: https://metadados.snirh.gov.br

**8.4 — IBAMA Autos de Infração (~300k multas)**
- CSV de `dadosabertos.ibama.gov.br` retorna apenas 4 linhas (bug do portal)
- Alternativa: buscar URL de download completo via Transparência.gov.br

### 🟡 FASE 9 — Login e Controle de Acesso
- 9.1 Tela de Login → `POST /api/v1/auth/login` (JWT)
- 9.2 Rate Limiting por API Key (`slowapi`)
- 9.3 Hardening `JWT_SECRET` via `.env`

### 🟡 FASE 10 — Relatórios e Export
- 10.1 Export PDF do Dossiê (`WeasyPrint`)
- 10.2 Export PNG do mapa (`leaflet-image`)

### 🟢 FASE 11 — Features Enterprise
- 11.1 Motor de Score de Risco (0-100) combinando IBAMA + MTE + DataJud + sobreposição TI
- 11.2 Alertas em Tempo Real via WebSocket (novos embargos sem refresh)
- 11.3 Next.js Frontend Enterprise (migração gradual)

---

## Como Iniciar o Ambiente

```bash
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"

# 1. Subir containers (PostgreSQL + FastAPI)
docker compose up -d

# 2. Verificar saúde e inventário do banco
docker exec agrojus-backend-1 python scripts/db_status.py
docker exec agrojus-backend-1 python scripts/db_inventory.py

# 3. Iniciar frontend Vite
cd frontend && npm run dev

# 4. Acessar
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000
# Swagger:   http://localhost:8000/docs
# Dashboard: http://localhost:8000/api/v1/dashboard/metrics
```

---

## Scripts ETL Disponíveis

| Script | Função | Status |
|---|---|---|
| `etl_mte_escravo.py` | Lista Suja MTE (PDF → 614 registros) | ✅ Funcional |
| `fetch_market_prices.py` | Cotações CBOT/CME via Yahoo Finance | ✅ Funcional |
| `etl_geo_sources.py` | Geo layers (DETER, TI, infraestrutura) | ✅ Funcional |
| `etl_deter_cerrado.py` | DETER Cerrado via WFS → PostGIS | ✅ Funcional |
| `etl_mapbiomas_credito.py` | 5.6M parcelas crédito rural | ✅ Funcional |
| `etl_basedosdados.py` | BigQuery (PAM, CNPJ) | ⚠️ Precisa GCP_PROJECT_ID |
| `etl_sicor_bcb.py` | Crédito Rural BCB OData | ⚠️ BCB em manutenção |
| `etl_ana_outorgas.py` | Outorgas ANA SNIRH | ⚠️ URL de download pendente |
| `etl_ibama_infracoes.py` | Autos de Infração IBAMA | ⚠️ CSV do portal tem 4 linhas (bug) |
| `db_inventory.py` | Inventário completo do banco | ✅ Funcional |
| `bd_catalog.py` | Catálogo tabelas BasedosDados.org | ✅ Funcional |

---

## Credenciais e Variáveis de Ambiente

| Serviço | Detalhes |
|---|---|
| PostgreSQL | host: `localhost:5432` · db: `agrojus` · user: `agrojus` · pass: `agrojus` |
| Backend API | `http://localhost:8000` |
| Frontend | `http://localhost:5173` |
| GCP / BigQuery | ❌ **Não configurado** — adicionar `GCP_PROJECT_ID` ao `.env` |

---

## Instruções para o Agente de IA

1. **Leia primeiro** `docs/HANDOFF_2026-04-15.md` + este arquivo
2. **Verifique o estado** com `docker exec agrojus-backend-1 python scripts/db_inventory.py`
3. **Prioridade 1:** Obter `GCP_PROJECT_ID` do usuário e rodar `etl_basedosdados.py` (CNPJ + PAM)
4. **Prioridade 2:** Tentar BCB SICOR novamente (`etl_sicor_bcb.py`) — pode ter saído da manutenção
5. **Prioridade 3:** Implementar Fase 9 (Login/JWT) para tornar a plataforma multi-tenant
6. **Nunca usar mock data** — toda informação vem do PostgreSQL ou APIs reais
7. **Commits atômicos** com mensagens descritivas em português
8. **Ao finalizar:** atualizar este arquivo + `docs/HANDOFF_2026-04-15.md`

---

*AgroJus Enterprise — Prompt de Continuidade v2.0 — 2026-04-15 (atualizado às 02:50 BRT)*
