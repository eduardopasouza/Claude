# Arquitetura Técnica — AgroJus

## Visão Geral

AgroJus é uma plataforma que agrega dados públicos de múltiplas fontes governamentais e de mercado, cruza essas informações geoespacialmente e juridicamente, e entrega relatórios de due diligence para diferentes perfis de usuário.

## Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                         │
│                                                                │
│  ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Portal     │ │   Mapa     │ │Relatórios│ │  Dashboard   │  │
│  │  Notícias   │ │ Interativo │ │   PDF    │ │  do Usuário  │  │
│  │  Cotações   │ │  Camadas   │ │   DD     │ │  Alertas     │  │
│  └────────────┘ └────────────┘ └──────────┘ └──────────────┘  │
│                                                                │
└────────────────────────┬───────────────────────────────────────┘
                         │ REST API (JSON)
┌────────────────────────▼───────────────────────────────────────┐
│                     BACKEND (FastAPI)                           │
│                                                                │
│  Camada API (/api/v1/)                                         │
│  ├── search.py     → Busca universal de imóveis/pessoas        │
│  ├── report.py     → Geração de relatórios (DD, dossiê, região)│
│  ├── map_data.py   → Dados geoespaciais (GeoJSON, camadas)     │
│  ├── market.py     → Cotações, crédito rural, preços de terra  │
│  └── news.py       → Notícias curadas do agronegócio           │
│                                                                │
│  Camada de Serviços                                            │
│  ├── due_diligence.py      → Orquestração de DD (7 etapas)     │
│  ├── person_intelligence.py → Dossiê CPF/CNPJ                 │
│  ├── region_intelligence.py → Inteligência regional            │
│  └── pdf_report.py         → Geração de PDF profissional       │
│                                                                │
│  Camada de Coletores (Data Pipeline)                           │
│  ├── sicar.py          → CAR (WFS + consulta pública)          │
│  ├── sigef.py          → SIGEF/INCRA (WFS)                     │
│  ├── receita_federal.py → CNPJ (BrasilAPI)                     │
│  ├── ibama.py          → Embargos (dados abertos CSV)          │
│  ├── slave_labour.py   → Lista Suja (Portal Transparência)     │
│  ├── financial.py      → Crédito rural (SICOR/BCB)             │
│  ├── market_data.py    → Cotações CEPEA, IBGE/SIDRA, CONAB     │
│  └── news_aggregator.py → RSS (Agrolink, Canal Rural, etc)     │
│                                                                │
│  Camada de Processamento                                       │
│  └── geospatial.py → Cruzamento de camadas (sobreposição)      │
│                                                                │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│              DATABASE (PostgreSQL 16 + PostGIS 3.4)            │
│                                                                │
│  Tabelas principais:                                           │
│  ├── properties        → Imóveis rurais (11 identificadores)   │
│  ├── persons           → Pessoas monitoradas (CPF/CNPJ)        │
│  ├── environmental_alerts → Embargos, desmatamento, sobreposição│
│  ├── legal_records     → Processos, protestos, certidões       │
│  ├── rural_credits     → Crédito rural (SICOR)                 │
│  ├── land_prices       → Preços de terra por região            │
│  ├── market_data       → Cotações de commodities               │
│  ├── monitoring_alerts → Alertas de monitoramento              │
│  └── cached_queries    → Cache de consultas externas           │
│                                                                │
└────────────────────────────────────────────────────────────────┘

Fontes externas:
  SICAR ←→ WFS/Download        Tribunais ←→ Scrapers
  SIGEF ←→ WFS/Acervo          CEPEA ←→ Scraping/RSS
  Receita ←→ API CNPJ          CONAB ←→ Downloads/API
  IBAMA ←→ Dados Abertos       IBGE ←→ API SIDRA
  MapBiomas ←→ Geoserviços     Portais Agro ←→ RSS feeds
  INPE ←→ Geoserviços          BCB/SICOR ←→ OData API
```

## Fluxo de uma Consulta de Due Diligence

```
Usuário informa: CAR ou matrícula ou CNPJ ou coordenadas
         │
         ▼
    ┌─────────────┐
    │  Resolução   │  → Identifica o imóvel a partir de qualquer identificador
    │  do Imóvel   │
    └──────┬──────┘
           │
     ┌─────┼──────┬──────────┬──────────┬──────────┐
     ▼     ▼      ▼          ▼          ▼          ▼
  SICAR  SIGEF  Receita   IBAMA    Lista Suja  Financeiro
  (CAR)  (geo)  (CNPJ)   (embargo)  (MTE)     (SICOR)
     │     │      │          │          │          │
     └─────┼──────┴──────────┴──────────┴──────────┘
           │
           ▼
    ┌─────────────┐
    │  Cruzamento  │  → Sobreposição com TI, UC, embargos, desmatamento
    │  Geoespacial │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   Score de   │  → Fundiário + Ambiental + Jurídico + Trabalhista + Financeiro
    │    Risco     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  Relatório   │  → JSON + PDF profissional com semáforo de riscos
    │    Final     │
    └─────────────┘
```

## Estratégia de Coleta de Dados

### Prioridade 1 — APIs oficiais e dados abertos
- SICAR/CAR: WFS (geoserviço padrão OGC)
- SIGEF/INCRA: WFS do Acervo Fundiário
- Receita Federal: BrasilAPI (gratuita, sem autenticação)
- IBAMA: CSV de dados abertos
- IBGE: API SIDRA
- BCB: API SICOR (OData)

### Prioridade 2 — Geoserviços padrão OGC
- MapBiomas: WMS/WFS
- INPE (DETER/PRODES): Geoserviços
- ANA: Geoserviços

### Prioridade 3 — Scraping ético
- Tribunais estaduais/federais (PJe)
- CEPEA/ESALQ (cotações)
- SNCR/CNIR (consulta pública)

### Prioridade 4 — Downloads periódicos + importação
- FUNAI (shapefiles de terras indígenas)
- ICMBio (shapefiles de UCs)
- Lista Suja (CSV do Portal da Transparência)
- CONAB (relatórios de safra)

## Cache

Todas as consultas externas são cacheadas em arquivo JSON com TTL configurável (padrão: 24h). O cache usa hash SHA-256 da query como chave.

Em produção, o cache migraria para Redis ou para a tabela `cached_queries` do PostgreSQL.

## Estrutura de Diretórios

```
agrojus/
├── README.md
├── docker-compose.yml
├── docs/
│   ├── ARCHITECTURE.md        ← Este arquivo
│   ├── API.md                 ← Documentação da API
│   ├── DATA_SOURCES.md        ← Referência de fontes de dados
│   └── FRONTEND_SPEC.md       ← Especificação para o frontend
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── main.py            ← App FastAPI
│       ├── config.py          ← Configurações
│       ├── api/               ← Rotas REST
│       ├── collectors/        ← Coletores de dados externos
│       ├── processors/        ← Processamento geoespacial
│       ├── services/          ← Lógica de negócio
│       ├── models/            ← Schemas Pydantic + SQLAlchemy
│       └── utils/             ← Utilitários
├── frontend/                  ← Next.js (ver FRONTEND_SPEC.md)
└── data/
    ├── shapefiles/            ← Shapefiles de referência (FUNAI, ICMBio)
    └── cache/                 ← Cache de consultas externas
```
