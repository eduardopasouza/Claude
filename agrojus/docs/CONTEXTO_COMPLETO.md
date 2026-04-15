# AGROJUS ENTERPRISE — CONTEXTO COMPLETO PARA IA

> **Este documento é o briefing primário.** Leia ANTES de qualquer código.
> Consolida: produto, concorrentes, fontes de dados, APIs, pendências e padrões de acesso.
> Versão: 1.0 — 2026-04-15

---

## 1. O QUE É O AGROJUS E POR QUE EXISTE

AgroJus é uma plataforma SaaS B2B de inteligência fundiária, ambiental e de mercado para o agronegócio brasileiro. Nasceu da **brecha regulatória criada pelas Resoluções CMN 5.267/5.268 de 2025** (MCR 2.9), que exigem que **todo banco do Brasil** verifique automaticamente conformidade ambiental antes de liberar crédito rural — desde 01/04/2026 para imóveis grandes, a partir de 04/01/2027 para os demais.

**O BCB já bloqueou mais de R$6 bilhões em operações com irregularidades.**

### Público-alvo principal:
- **Bancos e cooperativas de crédito rural** → compliance MCR 2.9, auditoria EUDR
- **Traders e exportadores** → rastreabilidade da cadeia (UE vai multar produtos com desmatamento)
- **Escritórios de advocacia rural** → dossiê CPF/CNPJ consolidado (IBAMA + MTE + DataJud)
- **Fintechs agro** → score de risco ambiental/trabalhista via API
- **Produtores rurais** → auto-diagnóstico do imóvel

### Stack atual:
```
Backend:    FastAPI + SQLAlchemy + PostGIS (PostgreSQL 15)
Frontend:   Vanilla JS + Vite + Leaflet (GIS Engine v2)
Infra:      Docker Compose (containers db + backend)
ETL:        Python scripts (pdfplumber, httpx, geopandas, ogr2ogr)
Branch:     claude/continue-backend-dev-sVLGG
```

---

## 2. MAPA COMPETITIVO COMPLETO

### 2.1 Concorrentes Diretos

**Registro Rural** (`registrorural.com.br`)
- Maior banco de dados de imóveis rurais do Brasil: 16 milhões cadastrados
- Preço: Gratuito / R$149,90 / R$850/mês (créditos por consulta)
- O que faz: CAR + SIGEF + INCRA unificados. Consulta por código CAR
- **Nosso gap sobre eles:** dados brutos sem análise. Sem score de risco. Sem jurídico.
  AgroJus transforma dados em **RISCO e AÇÃO**

**SpectraX** (`spectrax.com.br`) — Sinop/MT
- Compliance MCR 2.9 / EUDR via satélite + IA
- O que faz: CAR × PRODES × DETER, SINAFLOR (autorizações), histórico 2008-2024
- Estoque de carbono + potencial créditos VCU. Blockchain para laudos
- **Nosso gap:** não têm jurídico (DataJud), não têm MTE, não têm MapBiomas completo

**Agrotools** (`agrotools.com.br`) — cliente Itaú, JBS, McDonald's, Cargill, Sicredi
- 1.200 camadas geoespaciais. Data lake proprietário de +10 anos
- Preço: R$5k–50k+/mês (enterprise inacessível para bancos regionais)
- **Nosso gap:** é o "mercado do meio" que Agrotools não atende

**AdvLabs** (`advlabs.com.br`)
- IA para defesa ambiental (IBAMA/ICMBio). Teses e petições judiciais
- **Gap:** só ambiental. AgroJus tem ambiental + fundiário + trabalhista

**Docket** (`docket.com.br`)
- OCR de certidões com IA (50+ tipos). Parceira da Agrotools
- **Gap:** genérico. AgroJus fará OCR especializado para documentos rurais

**DadosFazenda** (`dadosfazenda.com.br`)
- "Consulta de imóvel rural em segundos" — simplicidade extrema
- Referência de UX de busca rápida

**Serasa Agro** (`serasaexperian.com.br/agronegocio`)
- Agro Score, compliance MCR, monitoramento via satélite
- Score visual (gauge), alertas, semáforo — referência de UX

**Traive / Agrolend**
- Motor de risco para fintechs agro (Traive: USD 20M série B)
- **Oportunidade:** ser o fornecedor de dados que essas fintechs compram via API

### 2.2 Referências de UX/Produto (não concorrentes)

| Site | Por que estudar |
|---|---|
| **ONR/SIG-RI** (`onr.org.br`) | 184 camadas geoespaciais, matrícula, Street View integrado — **interface que inspirou o mapa AgroJus** |
| **MapBiomas** (`mapbiomas.org`) | Melhor UX de mapa interativo com camadas ambientais do Brasil |
| **TerraBrasilis** (`terrabrasilis.dpi.inpe.br`) | Dashboard DETER/PRODES — fonte real dos dados de desmatamento |
| **SICAR** (`car.gov.br`) | Busca por código CAR, visualização de polígono |
| **Chãozão** (`chaozao.com.br`) | Marketplace de terras — R$500bi anunciados |
| **Canal Rural** (`canalrural.com.br`) | Portal de notícias agro + RSS feeds |
| **Agrolink** (`agrolink.com.br`) | Notícias agro + cotações + feed RSS |

### 2.3 O que ninguém tem e o AgroJus pode ter primeiro

| Feature | Todos os concorrentes | AgroJus |
|---|---|---|
| MapBiomas **Crédito Rural** (cruzar financiamento c/ desmatamento) | ❌ | ✅ (5.6M parcelas no PostGIS) |
| MapBiomas **Solo** (carbono, textura, aptidão) | Parcial | ✅ Pendente |
| MapBiomas **10m resolução** (Sentinel-2) | ❌ | ✅ Pendente |
| MapBiomas **Degradação** (EUDR diferenciado) | ❌ | ✅ Pendente |
| DataJud (processos judiciais) + IBAMA + MTE no mesmo laudo | ❌ | ✅ Pendente |
| Score MCR 2.9 automatizado (checklist auditável) | Pago/manual | ✅ Pendente |
| 103k embargos IBAMA no PostGIS acessíveis por API | Interno | ✅ Já está |
| 50k alertas DETER Cerrado no PostGIS local | ❌ | ✅ Já está |

---

## 3. FONTES DE DADOS — GUIA COMPLETO

### 3.1 MapBiomas — 18 Subprodutos (O mais importante de tudo)

MapBiomas é nossa maior vantagem competitiva. Nenhum concorrente usa todos os 18 subprodutos. Todos os downloads em `storage.googleapis.com/mapbiomas-public/...`

| # | Subproduto | Acesso | Status |
|---|---|---|---|
| 1 | **Cobertura e Uso da Terra** (Col.10.1, 1985-2023) | GEE Asset + Download GeoTIFF | ✅ Parcial (stats) |
| 2 | **MapBiomas 10m** (Sentinel-2, Beta, 2016+) | GEE Asset | ❌ Pendente |
| 3 | **Fogo** (Col.4 — cicatrizes mensais 1985-2024) | Download + GEE | ❌ Pendente |
| 4 | **Monitor do Fogo** (alertas mensais) | `plataforma.monitorfogo.mapbiomas.org` | ❌ Pendente |
| 5 | **Alerta** (desmatamento validado c/ laudo) | GraphQL `https://plataforma.alerta.mapbiomas.org/api/v2/graphql` | ❌ Precisa conta |
| 6 | **Monitor Crédito Rural** (polígonos) | `plataforma.creditorural.mapbiomas.org` | ✅ 5.6M parcelas PostGIS |
| 7 | **Recuperação** (áreas em regeneração) | Download | ✅ Parcial |
| 8 | **Mineração** (garimpo ilegal) | `plataforma.monitormineracao.mapbiomas.org` | ✅ Stats PostGIS |
| 9 | **Módulo Urbano** (Col.10) | Download SHP | ✅ Baixado |
| 10 | **Água** (superfícies hídricas anuais) | GEE Asset | ❌ Pendente |
| 11 | **Solo** (carbono orgânico, textura) | GEE Asset | ❌ Pendente — **maior diferencial** |
| 12 | **Degradação** (Beta) | GEE Asset | ❌ Pendente — **essencial para EUDR** |
| 13 | **Cacau** (nicho EUDR Sul Bahia) | Download | ❌ Pendente |
| 14 | **Infraestrutura** (estradas, portos, silos, pistas) | Download | ✅ No PostGIS |
| 15-18 | Mosaicos, Referências, Pontos, Camadas | GEE | Conforme demanda |

**Como acessar MapBiomas:**
- **Download direto:** `https://storage.googleapis.com/mapbiomas-public/brasil/...`
- **Google Earth Engine:** conta GEE + Python SDK `earthengine-api`
- **API Alerta GraphQL:** requer conta em `plataforma.alerta.mapbiomas.org` (gratuita)
- **Parcelas Crédito Rural:** GPKG de 4.7GB — já baixado e no PostGIS

### 3.2 Bases de Dados Públicas — Downloads Diretos

#### IBAMA
```
# Embargos (103k no PostGIS — ✅ ATIVO)
https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo_csv.zip

# Autos de Infração (multas — ❌ PENDENTE)
https://dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/Autuacao.csv
https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao

# SISCOM — polígonos embargados (shapefile)
https://siscom.ibama.gov.br/  → Dados Geoespaciais
```

#### MTE — Lista Suja Trabalho Escravo
```
# Download CSV (614 registros no PostGIS — ✅ ATIVO)
https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo
# Backup PDF: data/mte_trabalho_escravo.pdf
# ETL: backend/scripts/etl_mte_escravo.py (regex parser)
```

#### INPE TerraBrasilis — DETER e PRODES
```
# WFS Amazônia (50k alertas no PostGIS — ✅)
https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/wfs?service=WFS

# WFS Cerrado (50k alertas no PostGIS — ✅)
https://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/wfs?service=WFS

# Downloads completos
https://terrabrasilis.dpi.inpe.br/downloads/
```

#### FUNAI — Terras Indígenas
```
# WFS (655 TIs no PostGIS — ✅)
https://geoserver.funai.gov.br/geoserver/Funai/ows?service=WFS

# Download SHP
https://www.gov.br/funai/pt-br/atuacao/terras-indigenas/geoprocessamento-e-mapas
```

#### INCRA — SIGEF e Assentamentos
```
# WFS Parcelas Certificadas (bloqueado por proxy no container)
https://acervofundiario.incra.gov.br/geoserver/wfs
# Alternativa: i3geo por UF
https://acervofundiario.incra.gov.br/i3geo/ogc.php?uf=MT

# Assentamentos
https://acervofundiario.incra.gov.br/i3geo/ogc.php?layer=assentamentos
```

#### ICMBio — Unidades de Conservação
```
# Download SHP (download manual necessário — DNS falha no container)
https://www.gov.br/icmbio/pt-br/assuntos/monitoramento/geoprocessamento
https://www.gov.br/icmbio/pt-br/assuntos/dados_geoespaciais/
# CNUC (catalogo nacional de UCs)
https://www.gov.br/mma/pt-br/assuntos/areas-protegidas/unidades-de-conservacao
```

#### ANA — Recursos Hídricos
```
# Portal CKAN (200 retorna 200 mas CKAN retorna 404)
https://dadosabertos.ana.gov.br/

# CSW Metadados SNIRH (FUNCIONA — 218 datasets)
https://metadados.snirh.gov.br/geonetwork/srv/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetRecords

# WFS (bloqueado por proxy Docker)
https://metadados.snirh.gov.br/geoserver/wfs

# ETL escrito, URL de download pendente:
backend/scripts/etl_ana_outorgas.py
```

#### ANM — Mineração SIGMINE
```
# ArcGIS REST (FUNCIONA ✅)
https://geo.anm.gov.br/arcgis/rest/services
```

#### IBGE — Malhas e Estatísticas
```
# Malhas territoriais (municípios, estados, biomas)
https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json

# SIDRA — PAM (Produção Agrícola Municipal)
https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/all/p/2023/c782/allxt/d/v214%201,v216%201,v217%201,v218%201

# Censo agropecuário
https://apisidra.ibge.gov.br/values/t/6786/...
```

#### BCB — Indicadores e SICOR
```
# SICOR Crédito Rural OData (em manutenção 503 em 15/04/2026)
https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata
# ETL: backend/scripts/etl_sicor_bcb.py

# SELIC, IPCA, câmbio (FUNCIONA ✅)
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json
# Códigos: 432=SELIC, 433=IPCA, 1=câmbio USD
```

#### MAPA — Agricultura
```
# Dados abertos
https://dados.agricultura.gov.br/
# Agrofit (agrotóxicos registrados)
https://agrofit.agricultura.gov.br/agrofit_cons/principal_agrofit_cons
# ZARC (zoneamento de risco climático)
https://www.embrapa.br/zarc
```

### 3.3 BasedosDados.org — O maior agregador de dados públicos brasileiros

BasedosDados.org hospeda centenas de bases públicas normalizadas no **Google BigQuery**, com SQL direto. **Gratuito até 1TB/mês de queries.**

**Como acessar:**
```python
# Requer GCP_PROJECT_ID no .env
import basedosdados as bd
df = bd.read_sql("SELECT * FROM `basedosdados.br_me_cnpj.estabelecimentos` LIMIT 100", billing_project_id="meu-projeto")

# GraphQL (metadados sem credencial — FUNCIONA ✅)
https://backend.basedosdados.org/api/v1/graphql
```

**Tabelas de alto valor:**
| Tabela BigQuery | Conteúdo | Linhas |
|---|---|---|
| `basedosdados.br_me_cnpj.empresas` | Razão social, natureza jurídica, capital | 22M |
| `basedosdados.br_me_cnpj.estabelecimentos` | CNAE, endereço, sócios, abertura | 57M |
| `basedosdados.br_me_cnpj.socios` | Sócios de todas as empresas | 30M |
| `basedosdados.br_ibge_censo_agropecuario.municipio` | Censo agro 2017 por município | 5.5k |
| `basedosdados.br_ibge_pam.municipio` | Produção agrícola 2003-2022 | 250k |
| `basedosdados.br_me_rais.microdados_vinculos` | Vínculos empregatícios formais | 300M+ |
| `basedosdados.br_mte_trabalho_escravo.microdados` | Trabalho escravo + localização | 5k |

**Para desbloquear:**
1. Criar projeto Google Cloud grátis em `console.cloud.google.com`
2. Adicionar `GCP_PROJECT_ID=meu-projeto` ao `.env`
3. `pip install basedosdados google-cloud-bigquery`
4. Rodar `backend/scripts/etl_basedosdados.py`

### 3.4 dados.gov.br — Portal Nacional de Dados Abertos

O portal passou por migração de plataforma e muitas URLs antigas retornam 401/404.

**Como navegar:**
```
# Portal principal
https://dados.gov.br/dados/conjuntos-dados

# Busca de datasets
https://dados.gov.br/dados/conjuntos-dados?q=embargo+ambiental

# API CKAN (status instável — usar URLs diretas por dataset)
https://dados.gov.br/api/3/action/package_search?q=ibama
```

**Datasets confirmados por URL direta (sem CKAN):**
- IBAMA embargos: `dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/`
- IBAMA autuações: `dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/`
- ANEEL infraestrutura: `dadosabertos.aneel.gov.br/api`
- ANM mineração: `geo.anm.gov.br/arcgis/rest/services`

### 3.5 Fontes de Cotações de Mercado

```
# Yahoo Finance CBOT/CME (FUNCIONA ✅ — nossa fonte principal)
https://query1.finance.yahoo.com/v8/finance/chart/ZS=F  # Soja
https://query1.finance.yahoo.com/v8/finance/chart/ZC=F  # Milho
https://query1.finance.yahoo.com/v8/finance/chart/ZW=F  # Trigo
# ETL: backend/scripts/fetch_market_prices.py

# NASA POWER — clima em qualquer coordenada (FUNCIONA ✅)
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR&...

# CEPEA/ESALQ (bloqueia container — 403)
https://www.cepea.esalq.usp.br/br/indicador/
# Alternativa: dados históricos via PDF/Excel no site

# CONAB safras (download manual)
https://portaldeinformacoes.conab.gov.br/
```

### 3.6 Fontes Jurídicas

```
# DataJud / CNJ — Processos judiciais (API Elasticsearch)
https://api-publica.datajud.cnj.jus.br/_search
POST com JSON body: {"query": {"match": {"dadosBasicos.partes.nome": "EMPRESA LTDA"}}}

# BrasilAPI — CNPJ (FUNCIONA ✅)
https://brasilapi.com.br/api/cnpj/v1/{cnpj}

# ONR — Registro de Imóveis (via convênio ou consulta pública)
https://mapa.onr.org.br/
# Interface antiga: cartórios individuais por UF
# Desafio: cada cartório tem sistema próprio

# PGFN / CND — Certidão de débitos federais
https://cnd.pgfn.gov.br/

# TST / CNDT — Certidão trabalhista
https://www.tst.jus.br/certidao

# SINAFLOR — Autorizações de supressão de vegetação
https://servicos.ibama.gov.br/sinaflor/
```

---

## 4. ONR E A INTERFACE ANTIGA — CONTEXTO HISTÓRICO

**ONR (Operador Nacional do Registro de Imóveis)** é a entidade que unifica cartórios de registro de imóveis.

**O que o ONR tem:**
- `mapa.onr.org.br` — Mapa Nacional de Imóveis com 184 camadas geoespaciais
- Busca por matrícula, endereço, coordenada
- Google Street View integrado
- Integração com cartórios de todos os estados
- **Dados que o AgroJus não tem ainda:** matrícula real, histórico de titularidade, ônus registrados

**A "interface antiga" que o usuário menciona:**
Antes do mapa.onr.org.br, cada cartório tinha sistema próprio (ARISP em SP, ARIEMS no MS, etc.). A consulta era feita estado a estado, sem API unificada. O AgroJus deve aspirar a algo similar ao `mapa.onr.org.br` — um mapa central que carrega camadas sob demanda.

**Como integrar:**
- Acesso via convênio formal com ONR (modelo B2B)
- Alternativa: scraping das interfaces públicas dos TJs (busca processual)
- Para matrículas: usuário faz upload do PDF do cartório → OCR especializado

---

## 5. CONCORRENTES COM FOCO ESPECÍFICO — APROFUNDAMENTO

### Canal Rural (`canalrural.com.br`)
- **O que é:** Principal TV e portal de notícias do agronegócio brasileiro
- **RSS:** `https://www.canalrural.com.br/feed/`
- **Seções relevantes:** cotações, legislação, tecnologia no campo
- **Integração AgroJus:** já consumimos o RSS para a aba de notícias
- **Não é concorrente direto** — é fonte de conteúdo e referência de cobertura do setor

### Agrolink (`agrolink.com.br`)
- **O que é:** Portal integrado — notícias, cotações, clima, defensivos, eventos
- **RSS:** `https://www.agrolink.com.br/rss/noticias.xml`
- **Diferencial deles:** cotações diárias de commodities (CEPEA parceiro)
- **Integração AgroJus:** RSS já consumido para notícias
- **Modelo:** assinatura para acesso premium a cotações históricas

### SpectraX (`spectrax.com.br`) — Concorrente mais técnico
- **Checklist MCR 2.9:** CAR ativo? → PRODES limpo? → SIGEF certificado? → Embargo?
- **EUDR:** demonstram conformidade para exportadores
- **Diferencial deles:** blockchain para laudos (imutabilidade jurídica)
- **O que não têm:** jurídico (DataJud), trabalhista (MTE), crédito rural MapBiomas

### DadosFazenda (`dadosfazenda.com.br`)
- **O que é:** Consulta simplificada de imóvel rural — "resultados em segundos"
- **Como funciona:** consulta CAR + dados básicos do imóvel
- **Modelo:** créditos por consulta (similar a Registro Rural)
- **Diferencial AgroJus:** profundidade de análise vs simplicidade deles

### Registro Rural (`registrorural.com.br`) — Concorrente mais próximo
- **URL:** `https://registrorural.com.br`
- **Preços:** Free / R$149,90 (Individual) / R$850/mês (Profissional)
- **O que têm:** 16M imóveis, CAR+SIGEF+INCRA unificados, relatório em PDF
- **Modelo:** créditos pré-pagos — cada consulta consome créditos
- **Gap deles:** dados brutos sem inteligência. Sem score, sem jurídico, sem mapa

---

## 6. ESTADO ATUAL DO SISTEMA — DATABASE

### Tabelas no PostGIS

```bash
# Para listar todas com contagens:
docker exec agrojus-backend-1 python scripts/db_inventory.py
```

| Tabela | Registros | Fonte | Observação |
|---|---|---|---|
| `environmental_alerts` (IBAMA) | 103.668 | Embargos CSV | ✅ |
| `environmental_alerts` (MTE) | 614 | Lista Suja PDF | ✅ |
| `mapbiomas_credito_rural` | 5.614.207 | GPKG 4.7GB | ✅ |
| `mapbiomas_agriculture_cycles` | 15.180 | Stats | ✅ |
| `mapbiomas_irrigation_stats` | 7.174 | Stats (anos 2000-2023) | ✅ |
| `mapbiomas_mining_stats` | 1.294 | Stats | ✅ |
| `mapbiomas_pasture_age` | 1.911 | Stats | ✅ |
| `mapbiomas_pasture_vigor` | 147 | Stats | ✅ |
| `geo_terras_indigenas` | 655 | FUNAI WFS | ✅ |
| `geo_deter_amazonia` | 50.000 | INPE WFS | ✅ |
| `geo_deter_cerrado` | 50.000 | INPE WFS | ✅ NOVO |
| `geo_armazens_silos` | 16.676 | MapBiomas Infra | ✅ |
| `geo_frigorificos` | 207 | MapBiomas Infra | ✅ |
| `geo_rodovias_federais` | 14.255 | MapBiomas Infra | ✅ |
| `geo_ferrovias` | 2.244 | MapBiomas Infra | ✅ |
| `geo_portos` | 35 | MapBiomas Infra | ✅ |
| `market_quotes` | 24 | Yahoo Finance | ✅ |
| `rural_credits` | 0 | BCB SICOR | ⏳ BCB em manutenção |
| `ana_outorgas` | 0 | ANA SNIRH | ⏳ URL pendente |
| `users` | 0 | Auth local | ✅ Tabela criada |

---

## 7. FEATURES PENDENTES — PRIORIDADE

### P1 — BasedosDados (BigQuery) ← MÁXIMA PRIORIDADE
**Por que:** enriquecimento de CNPJ (razão social, CNAE, sócios) é essencial para o dossiê
**Como:** usuário deve criar projeto GCP gratuito + adicionar `GCP_PROJECT_ID` ao `.env`
**Script:** `backend/scripts/etl_basedosdados.py`

### P2 — BCB SICOR (Crédito Rural)
**Por que:** saber quanto crédito rural foi liberado para quem, onde e para qual cultura
**Como:** `etl_sicor_bcb.py` já escrito — tentar quando BCB voltar do 503
**Alternativa:** bulk download em `dadosabertos.bcb.gov.br`

### P3 — ANA Outorgas de Água
**Por que:** imóveis sem outorga em área de irrigação = risco regulatório alto
**Como:** `etl_ana_outorgas.py` escrito — descobrir URL correta do ZIP no SNIRH
**Portal:** `https://dadosabertos.ana.gov.br/`

### P4 — IBAMA Autos de Infração (multas ~300k)
**Por que:** embargos sem multas = informação incompleta
**Como:** `https://dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/Autuacao.csv`
**Problema:** portal retorna CSV vazio (bug) — monitorar

### P5 — ICMBio Unidades de Conservação
**Por que:** sobreposição com UC = atividade proibida/restrita
**Como:** download manual do shapefile + `ogr2ogr` para PostGIS
**DNS:** falha dentro do container — baixar manualmente

### P6 — DataJud/CNJ (Processos Judiciais)
**Por que:** fechar o ciclo do dossiê jurídico
**API:** `api-publica.datajud.cnj.jus.br` (Elasticsearch, gratuita)
**Script:** cruzar CPF/CNPJ com processos de todas as justiças

### P7 — Login UI Completo (em progresso)
**O que falta:** testar fluxo no browser, verificar CORS, adicionar JWT ao cabeçalho das requisições
**Arquivo:** `frontend/index.html` (overlay adicionado em 15/04/2026)

### P8 — APScheduler para Cotações Automáticas
**O que faz:** rodar `fetch_market_prices.py` às 09h e 18h BRT sem intervenção manual
**Como:** `from apscheduler.schedulers.background import BackgroundScheduler` no FastAPI startup

### P9 — Score de Risco MCR 2.9 (0-100)
**Algoritmo:** (IBAMA embargos × 40) + (MTE lista suja × 30) + (DataJud processos × 20) + (sobreposição TI × 10)
**Output:** Baixo / Médio / Alto / Crítico com justificativa auditável

### P10 — Export PDF Dossiê (WeasyPrint)
**Endpoint:** `GET /api/v1/compliance/dossier/{cpf_cnpj}/export?format=pdf`
**Template:** HTML com logo AgroJus, tabela de alertas, score, mapa miniatura

---

## 8. PADRÕES DE IMPLEMENTAÇÃO

### Como funciona `get_session()` no AgroJus
```python
# CORRETO — get_session() retorna Session direta, não context manager
db = get_session()
try:
    result = db.execute(text("SELECT..."), params).scalar()
finally:
    db.close()

# ERRADO — isso causa AttributeError silencioso
with get_session() as db:  # ← NÃO USAR
    ...
```

### Rota de camadas GIS
```
GET /api/v1/geo/layers/{layer_id}/geojson?bbox=west,south,east,north&uf=SP&max_features=500
```
Layer IDs disponíveis: `desmatamento`, `desmatamento_cerrado`, `terras_indigenas`, `embargos`, `embargos_mte`, `parcelas_financiamento`, `municipios`

### Catálogo de camadas
```python
# camadas.py — status possíveis:
"active"           → servida pelo backend (PostGIS ou WFS)
"blocked_proxy"    → WFS existe mas falha dentro do Docker
"available_etl"    → ETL escrito, dados não carregados
"available_download" → download manual necessário
"offline_404"      → endpoint off
```

### Padrão de ETL
```python
# Todo ETL deve:
1. Definir a tabela SQLAlchemy (declarative_base)
2. Chamar Base.metadata.create_all() para criar a tabela
3. Limpar dados antigos (DELETE + commit)
4. Fazer bulk_save_objects em lotes de 500
5. Logar progress a cada 500 registros
6. Terminar com ✅ e total de registros
```

---

## 9. URLS DE REFERÊNCIA RÁPIDA

```
Frontend:   http://localhost:5173
Backend:    http://localhost:8000
Swagger:    http://localhost:8000/docs
Dashboard:  http://localhost:8000/api/v1/dashboard/metrics

# Testes rápidos:
curl "http://localhost:8000/api/v1/geo/layers/desmatamento_cerrado/geojson?max_features=2"
curl "http://localhost:8000/api/v1/geo/catalogo" | python -m json.tool
curl "http://localhost:8000/api/v1/dashboard/metrics" | python -m json.tool
curl "http://localhost:8000/api/v1/compliance/dossier/99514230434"
```

---

*AgroJus Enterprise — Contexto Completo para IA v1.0 — 2026-04-15*
*Mantenha este arquivo atualizado a cada sessão de desenvolvimento*
