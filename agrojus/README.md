# AgroJus Enterprise

**Plataforma SaaS de Inteligência Fundiária, Ambiental e de Mercado para o Agronegócio Brasileiro**

AgroJus cruza dados de 15+ fontes públicas (IBAMA, INPE, FUNAI, MapBiomas, BCB, IBGE, MTE, DataJud, ANA, ANM...) para oferecer due diligence rural automatizada, compliance ambiental (MCR 2.9 / EUDR), relatórios de conformidade por imóvel e monitoramento contínuo — tudo com score de risco jurídico auditável.

> **Documentação completa:** veja `docs/CONTEXTO_COMPLETO.md` para o briefing de produto e `docs/PESQUISA_FONTES.md` para o guia técnico das fontes de dados.

---

## Stack Tecnológico

```
Backend:    FastAPI + SQLAlchemy + PostGIS (PostgreSQL 16)
Frontend:   Vanilla JS + Vite + Leaflet (GIS Engine v2)
Infra:      Docker Compose (backend + PostgreSQL/PostGIS)
ETL:        Python (pdfplumber, httpx, geopandas, ogr2ogr)
Auth:       JWT (PyJWT + bcrypt)
```

## Início Rápido

```bash
# 1. Subir infraestrutura
docker compose up -d

# 2. Verificar banco de dados
docker exec agrojus-backend-1 python scripts/db_inventory.py

# 3. Subir frontend (dev server)
cd frontend && npm install && npm run dev

# 4. Acessar
# Backend API:  http://localhost:8000
# Swagger UI:   http://localhost:8000/docs
# Frontend:     http://localhost:5173
```

## Dados no PostGIS

| Tabela | Registros | Fonte |
|--------|-----------|-------|
| Embargos IBAMA | 103.668 | dadosabertos.ibama.gov.br |
| Lista Suja MTE | 614 | Portal da Transparência |
| MapBiomas Crédito Rural | 5.614.207 | MapBiomas GPKG |
| DETER Amazônia | 50.000 | INPE TerraBrasilis WFS |
| DETER Cerrado | 50.000 | INPE TerraBrasilis WFS |
| Terras Indígenas | 655 | FUNAI WFS |
| Armazéns/Silos | 16.676 | MapBiomas Infra |
| Frigoríficos | 207 | MapBiomas Infra |
| Rodovias Federais | 14.255 | MapBiomas Infra |
| Ferrovias | 2.244 | MapBiomas Infra |
| Portos | 35 | MapBiomas Infra |
| Cotações | 24 | Yahoo Finance CBOT/CME |

## API — Endpoints Principais

| Rota | Descrição |
|------|-----------|
| `GET /api/v1/dashboard/metrics` | KPIs da plataforma |
| `GET /api/v1/geo/layers/{id}/geojson` | GeoJSON de camada para Leaflet |
| `GET /api/v1/geo/catalogo` | Catálogo de 20+ camadas |
| `GET /api/v1/geo/analyze-point` | Análise completa de ponto (right-click) |
| `GET /api/v1/compliance/dossier/{cpf_cnpj}` | Dossiê de conformidade |
| `GET /api/v1/market/quotes` | Cotações de commodities |
| `POST /api/v1/auth/login` | JWT login |
| `POST /api/v1/auth/register` | Registro de usuário |

Veja todos os endpoints em `http://localhost:8000/docs` (Swagger UI).

## Estrutura do Projeto

```
agrojus/
├── backend/
│   ├── app/
│   │   ├── api/           # Routers FastAPI (auth, geo, compliance, market, dashboard...)
│   │   ├── collectors/    # 21 coletores de dados (IBAMA, FUNAI, IBGE, BCB, NASA, etc.)
│   │   ├── models/        # SQLAlchemy models (PostGIS)
│   │   ├── services/      # Lógica de negócio (due diligence, jurisdição, PDF)
│   │   ├── middleware/     # Rate limiting
│   │   └── main.py        # FastAPI app entry point
│   ├── scripts/           # ETLs de ingestão de dados
│   ├── tests/             # 18 arquivos de teste
│   └── Dockerfile
├── frontend/
│   ├── index.html         # App principal + login overlay
│   ├── main.js            # Lógica principal + GIS Engine v2
│   ├── style.css          # Design system (glassmorphism, dark mode)
│   └── src/components/    # Componentes JS (GisMap, etc.)
├── data/
│   ├── downloads/         # Dados brutos baixados (zips, gpkg)
│   ├── mapbiomas_credito/ # GPKG 4.7GB crédito rural
│   ├── mapbiomas_stats/   # Planilhas MapBiomas (cobertura, mineração, pastagem)
│   └── mte_trabalho_escravo.pdf
├── docs/
│   ├── CONTEXTO_COMPLETO.md     # Briefing de produto (LEIA PRIMEIRO)
│   ├── PESQUISA_FONTES.md       # Guia técnico de todas as fontes
│   ├── CONTINUIDADE_PROMPT.md   # Ponto de entrada para novas sessões
│   ├── coordination/ROADMAP.md  # Status dos 5 módulos
│   └── ...
└── docker-compose.yml
```

## Módulos do Produto

| # | Módulo | Status |
|---|--------|--------|
| M1 | Relatório de Conformidade por Imóvel | 🔶 Em desenvolvimento |
| M2 | GIS Map Interativo (Leaflet multi-layer) | 🟢 Funcional |
| M3 | Assessor Agropecuário | 🔶 Parcial |
| M4 | Motor de Valuation Rural | ❌ Não iniciado |
| M5 | Dashboard Bancário (Carteira) | ❌ Não iniciado |

## Licença

Projeto proprietário. Todos os direitos reservados.
