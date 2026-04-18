# AgroJus — Handoff Sessao 3 (15/04/2026)

> Leia este arquivo primeiro na proxima sessao.
> Sessao de ~3 horas. Resultado: motor de relatorio funcional + SIGEF baixado + roadmap completo.

---

## RESUMO PARA QUEM NAO LEU NADA

AgroJus e uma plataforma de inteligencia fundiaria, juridica, ambiental e financeira para o agronegocio brasileiro. Combina 10.7M+ registros geoespaciais com analise juridica especializada — nenhum concorrente faz isso.

O backend tem 59 tabelas PostGIS, 42+ endpoints FastAPI, motor de relatorio que cruza 13 camadas espaciais em ~250ms, compliance MCR 2.9/EUDR basico, Earth Engine e MapBiomas GraphQL integrados. O frontend nao renderiza mapa ainda. Nao tem motor juridico (prescricao, teses, defesa). Nao tem recuperacao de credito, contratos, checklists.

O roadmap tem 5 fases. A proxima sessao deve comecar pela Fase 0 (consertar mapa) e Fase 1 (motor juridico).

---

## O QUE FOI FEITO NESTA SESSAO

### 1. Motor de Relatorio (Fase 2 — CONCLUIDO)

Pipeline: CAR code → PostGIS (13 camadas) → Compliance → JSON/PDF

**Arquivos criados:**
- `backend/app/services/postgis_analyzer.py` — cruza geometria CAR com 13 camadas (~250ms)
- `backend/app/services/compliance.py` — MCR 2.9 (6 itens), EUDR (4 itens), score 0-1000
- `backend/app/services/earth_engine.py` — LULC, fogo, solo, agua (flag include_satellite)
- `backend/app/services/mapbiomas_alerta.py` — alertas tempo real por CAR (flag include_realtime_alerts)
- `backend/app/api/property.py` — busca, GeoJSON, overlaps para mapa
- `backend/scripts/etl_sicar_bigquery.py` — ETL SICAR 79.3M CARs via BigQuery
- `backend/scripts/etl_sigef_download.py` — ETL SIGEF parcelas certificadas por estado

**Arquivos modificados:**
- `backend/app/services/due_diligence.py` — reescrito: PostGIS-first, APIs enriquecimento
- `backend/app/services/pdf_report.py` — +secao compliance MCR/EUDR com tabelas
- `backend/app/models/schemas.py` — +compliance, +spatial_analysis, +satellite_data, +mapbiomas_realtime, +include_satellite, +include_realtime_alerts
- `backend/app/api/dashboard.py` — reescrito: materialized view (1700ms → 5ms)
- `backend/app/main.py` — +property router

### 2. Dados Novos

| Tabela | Registros | Fonte | Novidade |
|---|---|---|---|
| sigef_parcelas | 493.913 | Download INCRA direto | 6 UFs (MA, MT, PA, GO, TO, MS) |
| sicar_completo | ~72k (MA parcial, rodando) | BigQuery BasedosDados | 79.3M disponiveis |
| + indices GiST e B-tree | — | — | 11 novos indices |
| mv_dashboard_kpis | 1 row | Materialized view | Dashboard instantaneo |

### 3. Documentacao

| Documento | O que contem |
|---|---|
| `docs/ROADMAP_FASEADO_v1.md` | Roadmap 5 fases com todas as features + diferenciais + estimativas |
| `docs/API_FRONTEND_CONTRACT.md` | Contrato completo API para dev frontend (endpoints, exemplos, fluxo) |
| `docs/ANALISE_COMPETITIVA_COMPLETA.md` | 53 sites, 7 concorrentes (sessao anterior) |
| `docs/INVENTARIO_FEATURES.md` | 336 features catalogadas (sessao anterior) |

---

## BANCO DE DADOS — ESTADO ATUAL

**59 tabelas | ~10.7M+ registros no PostGIS**

Tabelas-chave para o motor de relatorio:
- `geo_car`: 135.000 CARs (WFS, 27 UFs, 5k cada)
- `sicar_completo`: em carga via BigQuery (79.3M disponiveis no br_sfb_sicar)
- `sigef_parcelas`: 493.913 parcelas certificadas SIGEF (6 UFs prioritarias)
- `geo_mapbiomas_alertas`: 515.823 alertas de desmatamento
- `mapbiomas_credito_rural`: 5.614.207 parcelas de credito
- `environmental_alerts`: 104.284 (IBAMA + MTE)
- `geo_deter_amazonia` + `geo_deter_cerrado`: 100.000 alertas DETER
- `geo_prodes`: 50.000 registros de desmatamento anual
- `geo_terras_indigenas`: 655 | `geo_unidades_conservacao`: 346
- `geo_embargos_icmbio`: 5.000 | `geo_autos_icmbio`: 10.000
- Infraestrutura: armazens 16.676, frigorificos 207, rodovias 14.255, portos 35
- BigQuery stats: PAM, PPM, SICOR, CNPJ, censo

APIs conectadas:
- Earth Engine (LULC, fogo, solo, agua) — integrado no endpoint via flag
- MapBiomas Alerta GraphQL — integrado no endpoint via flag
- BigQuery BasedosDados — ETL scripts prontos
- DataJud/CNJ — API key publica
- BrasilAPI — CNPJ em tempo real

---

## ENDPOINTS FUNCIONAIS

| Endpoint | Metodo | Tempo | O que faz |
|---|---|---|---|
| `/api/v1/report/due-diligence` | POST | ~250ms | Relatorio completo: 13 camadas + compliance |
| `/api/v1/report/due-diligence/pdf` | POST | ~1s | Export PDF com MCR/EUDR |
| `/api/v1/report/buyer` | POST | ~400ms | Relatorio persona comprador |
| `/api/v1/report/lawyer` | POST | ~400ms | Relatorio persona advogado |
| `/api/v1/report/investor` | POST | ~400ms | Relatorio persona investidor |
| `/api/v1/property/search` | GET | <100ms | Busca paginada de CARs |
| `/api/v1/property/ufs` | GET | <50ms | UFs com contagem |
| `/api/v1/property/municipios?uf=MA` | GET | <50ms | Municipios de uma UF |
| `/api/v1/property/{car}/geojson` | GET | <50ms | GeoJSON para Leaflet |
| `/api/v1/property/{car}/overlaps/geojson` | GET | ~300ms | Camadas sobrepostas para mapa |
| `/api/v1/dashboard/metrics` | GET | **5ms** | KPIs via materialized view |
| `/api/v1/dashboard/refresh` | POST | ~2s | Atualizar materialized view |
| `/api/v1/consulta/completa` | POST | ~5s | Dossie CPF/CNPJ (7 fontes paralelas) |
| `/api/v1/geo/analyze-point` | GET | ~3s | Analise de ponto no mapa |
| `/api/v1/geo/layers/{id}/geojson` | GET | varies | Camadas WFS para mapa |

Swagger completo: http://localhost:8000/docs

---

## O QUE NAO FUNCIONA / PROBLEMAS CONHECIDOS

| Problema | Impacto | Acao |
|---|---|---|
| **Frontend nao renderiza mapa** | CRITICO — produto nao demonstravel | Diagnosticar e consertar (Fase 0.1) |
| **Compliance e checklist binario, sem IA** | ALTO — nao e diferencial | Fase 1: scoring IA com raciocinio |
| **Sem motor juridico** | CRITICO — diferencial principal nao existe | Fase 1: prescricao, teses, defesa |
| **Sem recuperacao de credito** | ALTO — feature solicitada | Fase 1: alongamento de dividas |
| **Sem contratos/checklists** | MEDIO — feature solicitada | Fase 2 |
| **Sem WhatsApp bot** | MEDIO — diferencial copiavel | Fase 4 |
| **DETER/PRODES parciais** | MEDIO — 50k cada (dataset incompleto) | Fase 0: baixar shapefiles completos |
| **DataJud sem backup local** | BAIXO — depende de uptime CNJ | Sem solucao offline |
| **SICAR download lento** | BAIXO — script funciona, leva tempo | Rodar `etl_sicar_bigquery.py ALL` |

---

## ROADMAP FASEADO (docs/ROADMAP_FASEADO_v1.md)

### FASE 0 — FUNDACAO (2-3 dias)
- Consertar mapa no frontend
- Unificar compliance e search num fluxo unico
- Completar download SICAR e SIGEF (todos estados)
- Baixar DETER/PRODES completos (shapefiles, nao WFS)

### FASE 1 — MOTOR JURIDICO (5-7 dias) ← DIFERENCIAL UNICO
- Scoring 5 eixos 0-1000 cada (fundiario, ambiental, trabalhista, juridico, financeiro)
- Prescricao automatica (administrativa 5a, criminal 12-20a, trabalhista 2a)
- Analise de embargos/autuacoes (classificacao, nulidades, defesa sugerida)
- Recuperacao de credito rural (alongamento, saldo devedor, taxas abusivas)
- Base de jurisprudencia ambiental

### FASE 2 — CONTRATOS E CHECKLISTS (3-5 dias)
- Templates de contratos agro (arrendamento, parceria, CPR, compra/venda)
- Gerador de contratos com dados do imovel
- Checklists regulatorios interativos por estado (licenciamento, CAR, outorga, SIGEF)
- Gerador de comunicacoes (notificacao, requerimento, defesa)

### FASE 3 — FRONTEND COMPLETO (7-10 dias)
- Next.js 14 + Tailwind + shadcn/ui + react-leaflet
- Mapa interativo (13 camadas, opacity, inspector, upload, time slider)
- Dashboard com gauges 0-1000
- Telas: ficha imovel, embargos, credito, contratos, checklists

### FASE 4 — CANAIS (3-5 dias)
- Bot WhatsApp (consulta CAR, alerta embargos, status processo)
- Alertas por email
- Monitoramento continuo

### FASE 5 — IA AVANCADA (5-7 dias)
- Raciocinio auditavel cite-to-source
- Teses aplicaveis automaticas com % exito
- Radar de prospecao
- CRM Kanban de teses

**MVP: Fases 0-2 (~15 dias) | Completo: Fases 0-5 (~37 dias)**

---

## DIFERENCIAIS COMPETITIVOS

### O que copiar dos concorrentes
| De quem | O que | Como |
|---|---|---|
| Agrolend | Bot WhatsApp | Fase 4 — WhatsApp Business API |
| Serasa Agro | Gauge visual 0-1000 | Fase 3 — shadcn/ui gauge component |
| AdvLabs | Prescricao, CRM teses | Fase 1 — motor juridico |
| SpectraX | EUDR automatico, split view | Fase 1 (EUDR) + Fase 3 (split view) |
| Agrotools | Marketplace modular | Fase futura — catalogo de camadas |

### Diferenciais UNICOS (nenhum concorrente faz)
1. Juridico + geoespacial integrado
2. Score juridico com prescricao em 5 eixos
3. Recuperacao de credito rural + alongamento
4. Analise de embargos com defesa sugerida
5. Contratos agro com dados do imovel
6. Checklists regulatorios por estado
7. Raciocinio IA auditavel

---

## DECISOES PENDENTES DO EDUARDO

1. WhatsApp: Twilio ou Meta Cloud API?
2. IA para teses/scoring: Claude API ou OpenAI?
3. Cadastros gratuitos (~20 min total):
   - Embrapa AgroAPI (ZARC, ClimAPI)
   - Portal Transparencia API (CEIS, CNEP)
4. ONR (matriculas): contratar InfoSimples (~R$0.50/consulta)?

---

## COMANDOS RAPIDOS

```bash
# Subir ambiente
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# Verificar status
curl -s http://localhost:8000/health | python -m json.tool

# Testar relatorio
curl -s -X POST http://localhost:8000/api/v1/report/due-diligence \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21"}' | python -m json.tool

# Testar com satelite (~20s extra)
curl -s -X POST http://localhost:8000/api/v1/report/due-diligence \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21","include_satellite":true,"include_realtime_alerts":true}'

# Dashboard (5ms)
curl -s http://localhost:8000/api/v1/dashboard/metrics | python -m json.tool

# Buscar imoveis MA
curl -s "http://localhost:8000/api/v1/property/search?uf=MA&page_size=5" | python -m json.tool

# GeoJSON para mapa
curl -s "http://localhost:8000/api/v1/property/MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21/geojson"

# Swagger UI
# http://localhost:8000/docs

# Completar download SIGEF (todos os estados, ~1h)
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python scripts/etl_sigef_download.py ALL

# Completar download SICAR BigQuery (todos os estados, ~4h)
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python scripts/etl_sicar_bigquery.py ALL

# Atualizar dashboard materialized view
curl -s -X POST http://localhost:8000/api/v1/dashboard/refresh
```

---

## CREDENCIAIS (nao commitar .env!)

| Servico | Localizacao |
|---|---|
| PostgreSQL | localhost:5432, agrojus/agrojus |
| GCP Project | agrojus |
| GCP Credentials | ${APPDATA}/gcloud/application_default_credentials.json |
| MapBiomas | eduardo@guerreiro.adv.br (em .env) |
| DataJud | API key publica em config.py |
| JWT Secret | Valor default dev |

---

## ESTRUTURA DE ARQUIVOS RELEVANTE

```
backend/
  app/
    api/
      property.py          ← NOVO: busca, GeoJSON, overlaps
      report.py             ← due-diligence, buyer, lawyer, investor, PDF
      dashboard.py          ← REESCRITO: materialized view
      geo.py                ← analyze-point, layers GeoJSON, catalogo
      consulta.py           ← dossie CPF/CNPJ unificado
      compliance.py         ← endpoints compliance (basico)
    services/
      postgis_analyzer.py   ← NOVO: 13 camadas espaciais
      compliance.py         ← NOVO: MCR 2.9, EUDR, score 0-1000
      earth_engine.py       ← NOVO: LULC, fogo, solo, agua
      mapbiomas_alerta.py   ← NOVO: GraphQL alertas tempo real
      due_diligence.py      ← REESCRITO: PostGIS-first
      pdf_report.py         ← ATUALIZADO: +compliance tables
    models/
      schemas.py            ← ATUALIZADO: +compliance, +spatial, +satellite
      database.py           ← SQLAlchemy engine, sessions
    config.py               ← Settings (API keys, URLs)
  scripts/
    etl_sicar_bigquery.py   ← NOVO: download SICAR via BigQuery
    etl_sigef_download.py   ← NOVO: download SIGEF via INCRA
    etl_earth_engine.py     ← funcoes EE por propriedade
docs/
  ROADMAP_FASEADO_v1.md     ← NOVO: roadmap 5 fases completo
  API_FRONTEND_CONTRACT.md  ← NOVO: contrato API para frontend
  ANALISE_COMPETITIVA_COMPLETA.md
  INVENTARIO_FEATURES.md
  STATUS_FONTES_DADOS.md
```

---

*AgroJus v0.9.2 — Handoff Sessao 3 — 2026-04-15 12:30 BRT*
