# STATUS DE TODAS AS FONTES DE DADOS — AgroJus

> Inventario completo e honesto. Atualizado: 2026-04-15 06:10 BRT
> Cada fonte classificada: NO POSTGIS / COLLECTOR ATIVO / NAO INTEGRADO / BLOQUEADO

---

## A. NO POSTGIS (dados carregados em tabela permanente)

| # | Fonte | Tabela | Registros | Obs |
|---|---|---|---|---|
| 1 | IBAMA Embargos | `environmental_alerts` (IBAMA) | 104.284 | OK |
| 2 | MTE Lista Suja | `environmental_alerts` (MTE) | 614 | Parser PDF fragil, migracao CSV falhou (portal 500) |
| 3 | MapBiomas Credito Rural | `mapbiomas_credito_rural` | 5.614.207 | OK — 4.7GB GPKG |
| 4 | MapBiomas Stats (7 tabelas) | `mapbiomas_*` | ~26.659 | agriculture_cycles, coverage_states, irrigation, mining, pasture_age, pasture_vigor |
| 5 | FUNAI Terras Indigenas | `geo_terras_indigenas` | 655 | OK |
| 6 | DETER Amazonia | `geo_deter_amazonia` | 50.000 | Limite WFS. Total real: 800k+ |
| 7 | DETER Cerrado | `geo_deter_cerrado` | 50.000 | Limite WFS. Total real: 200k+ |
| 8 | MapBiomas Infra | `geo_armazens_silos` + 4 tabelas | ~33.417 | armazens, frigorificos, rodovias, ferrovias, portos |
| 9 | ICMBio UCs | `geo_unidades_conservacao` | 346 | **NOVO** — via INDE WFS |
| 10 | PRODES | `geo_prodes` | 50.000 | **NOVO** — desmatamento anual. Limite WFS. |
| 11 | BCB SICOR | `sicor_custeio_uf` | 50.000 | **NOVO** — custeio por UF/produto 2013-2026 |
| 12 | ICMBio Embargos | `geo_embargos_icmbio` | 5.000 | **NOVO** |
| 13 | ICMBio Autos | `geo_autos_icmbio` | 10.000 | **NOVO** |
| 14 | Yahoo Finance | `market_quotes` | 24 | Cotacoes CBOT/CME (estatico, manual) |

**Total no PostGIS: ~5.994.568 registros em 24 tabelas**

---

## B. COLLECTOR ATIVO (funciona como consulta em tempo real, sem tabela bulk)

| # | Fonte | Collector | Status | Obs |
|---|---|---|---|---|
| 15 | BrasilAPI (CNPJ) | `app/collectors/receita_federal.py` | Funciona | Consulta por CNPJ |
| 16 | NASA POWER (clima) | `app/collectors/nasa_power.py` | Funciona | Clima por coordenada |
| 17 | IBGE SIDRA (PAM) | `app/api/geo.py` | Funciona | Producao agricola por municipio |
| 18 | DataJud/CNJ | `app/collectors/datajud.py` | **NOVO — API key configurada** | 88 tribunais, testado TJMA |
| 19 | agrobr (CEPEA+B3+CONAB) | Instalado no container | **NOVO — testado** | 38 fontes, mas sem collector wrapper |
| 20 | BCB API (SELIC/IPCA/dolar) | `app/collectors/bcb.py` | Funciona | Indicadores macro |

---

## C. NAO INTEGRADO (fonte disponivel, ETL/collector nao existe)

| # | Fonte | O que falta | Dificuldade | Valor |
|---|---|---|---|---|
| 21 | **MapBiomas Alerta GraphQL** | Criar conta + collector GraphQL | Media | CRITICO — alertas por CAR |
| 22 | **Embrapa AgroAPI (ZARC)** | Cadastro gratis + collector REST | Baixa | ALTO — zoneamento agricola |
| 23 | **Embrapa ClimAPI** | Mesmo cadastro + collector | Baixa | MEDIO — clima 6h |
| 24 | **Embrapa AGROFIT** | Mesmo cadastro + collector | Baixa | MEDIO — agrotoxicos |
| 25 | **Embrapa SATVeg** | Mesmo cadastro + collector | Baixa | MEDIO — NDVI/EVI |
| 26 | **Embrapa GeoInfo WFS** | Collector WFS (sem auth) | Baixa | MEDIO — solos |
| 27 | **INMET** | Collector REST (sem auth) + `inmetpy` | Baixa | MEDIO — estacoes meteo |
| 28 | **USDA PSD** | API key gratis + collector REST | Baixa | BAIXO — oferta/demanda global |
| 29 | **CVM FIAGRO** | Collector CKAN (sem auth) | Baixa | BAIXO — fundos agro |
| 30 | **DOU (Ro-DOU)** | Self-host Ro-DOU ou INLABS | Media | ALTO — monitoramento normas |
| 31 | **SICAR/CAR WFS** | ETL WFS GeoServer (sem auth) | Media | CRITICO — poligonos do CAR |
| 32 | **ANA Outorgas** | Encontrar URL + collector ArcGIS REST | Media | MEDIO — risco hidrico |
| 33 | **ANA HidroWeb** | Collector REST (sem auth) | Media | BAIXO — series hidrologicas |
| 34 | **MAPA CKAN (Agrofit CSV)** | Download CSV direto (sem auth) | Baixa | MEDIO — agrotoxicos |
| 35 | **MAPA CKAN (ZARC CSV)** | Download CSV direto (sem auth) | Baixa | ALTO — zoneamento |
| 36 | **B3 Futuros (via agrobr)** | Wrapper sobre agrobr | Baixa | MEDIO — futuros agro |
| 37 | **CEPEA historico (via agrobr)** | Wrapper sobre agrobr | Baixa | ALTO — indicadores preco |
| 38 | **CONAB safras (via agrobr)** | Wrapper sobre agrobr | Baixa | ALTO — estimativas safra |
| 39 | **IBGE PAM/PPM bulk** | ETL SIDRA paginado | Media | MEDIO — producao por municipio |
| 40 | **ANM/SIGMINE** | Corrigir ETL ArcGIS ou baixar KMZ | Media | MEDIO — processos minerarios |
| 41 | **DETER completo (800k+)** | Download shapefile direto (nao WFS) | Media | ALTO — alertas completos |
| 42 | **IBAMA Autos de Infracao** | Bug no portal (CSV vazio) — monitorar | Bloqueado | ALTO — multas |
| 43 | **RSS feeds (5 portais)** | Collector feedparser (code existe) | Baixa | MEDIO — noticias |

---

## D. BLOQUEADO (requer acao do Eduardo ou acesso pago)

| # | Fonte | Bloqueador | Acao do Eduardo | Valor |
|---|---|---|---|---|
| 44 | **BasedosDados BigQuery** | Precisa GCP Project ID | Criar em console.cloud.google.com | CRITICO — CNPJ 2.7B linhas |
| 45 | **MapBiomas Alerta** | Precisa conta | Criar em plataforma.alerta.mapbiomas.org | CRITICO — alertas por CAR |
| 46 | **Quilombolas INCRA** | Precisa login gov.br | Baixar shapefile manualmente | MEDIO |
| 47 | **Portal Transparencia API** | Precisa cadastrar email | Cadastrar em portaldatransparencia.gov.br/api-de-dados | ALTO — CEIS/CNEP/MTE |
| 48 | **dados.gov.br CKAN** | API retorna 401 (precisa token) | Gerar token no portal | BAIXO — usamos URLs diretas |
| 49 | **INCRA SIGEF** | Precisa login gov.br | Login + download shapefiles | ALTO — parcelas certificadas |
| 50 | **ONR (matriculas)** | SEM API publica | Parceria institucional ou InfoSimples (pago) | ALTO — matriculas |
| 51 | **InfoSimples** | Pago (R$0.04-0.10/consulta) | Criar conta + depositar creditos | ALTO — INCRA, CAR, IBAMA |
| 52 | **SERPRO** | Pago (R$0.35-0.66/consulta) | Contratar com e-CNPJ | ALTO — CCIR, CPF oficial |
| 53 | **CONAB** | SEM API publica | Scraping Pentaho ou download XLS manual | MEDIO |

---

## RESUMO NUMERICO

| Status | Qtd | % |
|---|---|---|
| **No PostGIS** (tabela permanente) | 14 fontes | 26% |
| **Collector ativo** (tempo real) | 6 fontes | 11% |
| **Nao integrado** (eu resolvo) | 23 fontes | 43% |
| **Bloqueado** (depende do Eduardo ou e pago) | 10 fontes | 19% |
| **TOTAL** | **53 fontes** | 100% |

---

## PRIORIZACAO — O QUE FAZER AGORA

### Eduardo faz (5 cadastros gratuitos, ~20 min):
1. **console.cloud.google.com** — criar projeto GCP gratis
2. **plataforma.alerta.mapbiomas.org** — criar conta gratis
3. **portaldatransparencia.gov.br/api-de-dados** — cadastrar email
4. **acervofundiario.incra.gov.br** — login gov.br + baixar quilombolas
5. **agroapi.cnptia.embrapa.br** — criar conta gratis (AgroAPI Store)

### Eu faco (23 integracoes pendentes):
**Batch 1 — Wrappers agrobr (rapido, ja instalado):**
- CEPEA historico, B3 futuros, CONAB safras, IBGE PAM

**Batch 2 — APIs sem auth (rapido):**
- SICAR/CAR WFS (poligonos do CAR — CRITICO)
- ANA Outorgas ArcGIS FeatureServer
- INMET estacoes
- CVM FIAGRO
- MAPA ZARC/Agrofit CSV

**Batch 3 — Apos cadastros do Eduardo:**
- MapBiomas Alerta GraphQL
- Embrapa AgroAPI (ZARC, ClimAPI, AGROFIT, SATVeg)
- BasedosDados BigQuery (CNPJ, censo)
- Portal Transparencia (CEIS, CNEP)

**Batch 4 — Complexos:**
- DOU via Ro-DOU
- DETER completo (download shapefile 800k+)
- ANM/SIGMINE (download KMZ)
- RSS feeds (5 portais)

---

*Status de Fontes de Dados v1.0 — 2026-04-15*
