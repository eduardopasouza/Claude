# AgroJus — Backlog por Agente

Atualizado: 2026-04-11

## Dev Backend

1. [ ] Criar endpoint GET /api/v1/geo/unidades-conservacao (mesmo padrao terras-indigenas)
2. [ ] Criar endpoint GET /api/v1/geo/quilombolas
3. [ ] Endpoint de importacao de dados via CLI (IBAMA, Lista Suja)
4. [ ] Configurar monitoramento com APScheduler ou Celery beat
5. [ ] Restringir CORS para dominio de producao (config por env var)

## Dev Frontend (Antigravity)

1. [ ] Integrar analyze-point no right-click do mapa Leaflet
2. [ ] Painel de camadas com toggle (checkbox por camada)
3. [ ] Pagina de compliance MCR 2.9 / EUDR
4. [ ] Pagina de jurisdicao por estado
5. [ ] Graficos de serie historica (producao agricola, pecuaria)
6. [ ] Dashboard de indicadores BCB (SELIC, dolar, IPCA)

## QA & Testes

1. [ ] Testes para endpoints de compliance (MCR 2.9, EUDR)
2. [ ] Testes para endpoints de jurisdicao (27 estados, comparador)
3. [ ] Testes para endpoints de clima (NASA POWER)
4. [ ] Testes para endpoints BCB (indicadores, SICOR)
5. [ ] Testes para consulta unificada (/consulta/completa)
6. [ ] Testes de resiliencia: simular timeout, HTTP 500, JSON invalido
7. [ ] Configurar pytest-cov e medir cobertura atual
8. [ ] Meta: 90%+ de cobertura

## Data Engineer

1. [ ] IBAMA embargos com coordenadas (CSV 8MB) — novo collector ou import
2. [ ] Lista Suja completa (CSV Portal Transparencia) — import real
3. [ ] Shapefiles UCs/Unidades de Conservacao (download ICMBio)
4. [ ] Shapefiles Quilombolas (download INCRA)
5. [ ] PRODES desmatamento acumulado (TerraBrasilis WFS)
6. [ ] IBAMA embargos completo (168MB CSV → PostgreSQL)
7. [ ] CONAB: custo de producao, precos agricolas, estimativa de safra
8. [ ] Precos de terra (INCRA referencial + IEA-SP)

## DevOps

1. [ ] Docker Compose funcional (backend + PostgreSQL + PostGIS)
2. [ ] Testar Alembic migrations contra PostgreSQL real
3. [ ] GitHub Actions CI (lint + pytest em cada push)
4. [ ] Deploy em Render ou AWS (com Dockerfile existente)
5. [ ] Configurar HTTPS + dominio

## Pesquisador

1. [ ] Cadastrar API key DataJud/CNJ (gratuita)
2. [ ] Testar SICAR/CAR — ainda 503?
3. [ ] Testar SIGEF/INCRA — descobrir nova URL
4. [ ] Validar todas as 13 fontes reais — quais ainda funcionam?
5. [ ] Investigar GeoServers estaduais (SEMA-MT, SEMAS-PA, IDE-SISEMA MG)
6. [ ] Mapear fontes CONAB acessiveis (APIs, CSVs, portais)
7. [ ] Atualizar VERIFIED_SOURCES.md e DATA_MAP.md
