# ANALISE COMPETITIVA COMPLETA — AgroJus

> **53 sites analisados em profundidade.** Concorrentes, fintechs, portais, fontes governamentais, APIs, referencias de UX.
> Pesquisa realizada: 2026-04-15 | 7 lotes em paralelo | Fontes: Tavily crawl/extract/search/research

---

## PARTE I — CONCORRENTES DIRETOS (7)

---

### 1. Registro Rural (registrorural.com.br)

**O que faz:** Maior banco de dados de imoveis rurais do Brasil (16M+ cadastros). Agrega CAR + INCRA/SNCR + SIGEF + Cartorios + Receita Federal.

**Features:** Busca por nome/CPF/CNPJ/coordenadas, mapas com satelite, download KML/KMZ, relatorios PDF (CAR completo, INCRA completo, busca por CPF), analise de sobreposicao, API corporativa.

**Precos:** PRO R$149,90/mes (buscas ilimitadas + 5 relatorios/mes). Creditos adicionais por relatorio. API empresarial com faixas de credito.

**API:** docs.registrorural.com.br — Postman Collection publica, auth X-API-Key, dashboard empresarial em dashboard.registrorural.com.br.

**Design:** Light mode, busca central, resultados em lista, mapa satelite integrado. Funcional, nao premium.

**Copiar:** API documentada com Postman, modelo de creditos, busca por coordenadas, download KML/KMZ.

**Gaps:** Sem analise juridica, sem monitoramento, sem IA, sem score de risco, sem dashboard analitico, sem alertas.

---

### 2. SpectraX (spectrax.com.br)

**O que faz:** Compliance MCR 2.9/EUDR via satelite + IA. Equipe de 3 pos-doutores em sensoriamento remoto (UNEMAT, Sinop/MT).

**Produtos:** City (monitoramento territorial), ESG (relatorios geoespaciais), FarmGuide (clima), FarmGuide-API (produtividade), Report (compliance), Expansao Territorial, API Soja/Carbono/Clima (em breve).

**Satelites:** Landsat-9, Sentinel-2, GEDI, MODIS, GOES, ALOS/PALSAR, Suomi NPP.

**Diferenciais:** Equipe cientifica, data center proprio, validador de relatorio por codigo unico, LGPD compliance, 213 documentos cientificos, 13 ODS mapeados.

**Copiar:** Validador de relatorio por codigo unico, formulario de finalidade na emissao (LGPD).

**Gaps:** Sem juridico (DataJud/processos), sem MTE, sem credito rural BCB, sem cotacoes, sem noticias.

---

### 3. Agrotools (agrotools.com.br)

**O que faz:** Maior agtech da America Latina. 1.300+ camadas de dados, 200M+ hectares, 200k+ analises/dia. Receita R$200M+. Clientes: Itau, JBS, Cargill, McDonald's, Rabobank, Carrefour. B Corp + GPTW.

**Solucoes (6):** Brand Protection (ESG), Rural Financing, Rural Insurance, ESG Compliance, Sales Efficiency, Supply Chain.

**ATMarket (marketplace):** Pixels (ferramentas prontas — R$257-283/req): Analise Socioambiental, NDVI, Produtividade, Uso do Solo, Meteorologia. Functions (APIs): CAR, IBAMA, divida trabalhista, bioma, UC, quilombola.

**ScoreCAR:** IA/ML que avalia confiabilidade do CAR. 10 criterios, 5 niveis, timeline historica.

**Precos:** Enterprise sob consulta. ATMarket: pay-per-use R$257-283/req.

**API:** Sem docs publicos. Integracoes enterprise customizadas.

**Copiar:** ATMarket (marketplace modular), ScoreCAR (scoring de confiabilidade), calculadora de ROI publica, 45+ criterios socioambientais.

**Gaps:** Zero juridico, sem advogados como publico, preco inacessivel, sem self-service.

---

### 4. Docket (docket.com.br)

**O que faz:** OCR de documentos com IA. Leitura e analise de certidoes "em segundos". Parceira Agrotools.

**Produtos:** Freemium (teste gratis), Docket IA (leitor de docs), Hub (solicitacao de docs), Controle (gestao integrada).

**Segmentos:** Agronegocio (pagina dedicada!), Real Estate, Industria, Financeiro, Energia, Varejo.

**Copiar:** Freemium como modelo de conversao, programa de parcerias, IA para OCR de documentos rurais.

**Gaps:** Sem GIS/mapa, sem dados ambientais, sem compliance MCR/EUDR, sem cotacoes.

---

### 5. Serasa Agro (serasaexperian.com.br/agronegocio)

**O que faz:** Bureau de credito agro global (Experian plc). 4,5M produtores, 370M hectares, 170+ fontes integradas.

**Produtos:**
- **Farm Check:** Relatorio consolidado multi-modulo (Produtor + Propriedade + Agro Check + Credit Check + Agro Score)
- **Agro Score:** 0-1000 exclusivo agro, 80+ clientes (Raizen, Cargill, Allianz)
- **Agro Consulta:** Self-service pay-per-use
- **Smart ESG:** Monitoramento diario, protocolos personalizaveis, alertas email, EUDR/RenovaBio
- **Agro Report:** Sensoriamento remoto, ZARC, compliance BACEN
- **MCR Compliance:** ZARC + PRODES + CAR automatizado
- **Consulta CPR:** Cedulas registradas CERC/B3/CRDC
- **SCR:** Endividamento BCB

**Precos:** Agro Consulta pay-per-use. Farm Check/Smart ESG enterprise sob consulta.

**API:** Developer Portal em developer.serasaexperian.com.br — Postman Collection publica. JWT auth (10h expiry). REST JSON/GeoJSON.

**Design:** Light mode, gauge visual Score 0-1000, mapa interativo no Smart ESG (CAR/embargos/DETER). Sem dark mode.

**Copiar:** Gauge visual 0-1000, 170+ fontes em relatorio unico, Smart ESG com protocolos configuráveis, pay-per-use + enterprise, API com Postman docs, Boletim Agro periodico.

**Gaps:** Sem analise juridica/fundiaria, sem cadeia dominial, sem dark mode, sem self-service signup rapido.

---

### 6. DadosFazenda (dadosfazenda.com.br)

**O que faz:** "Consulta de imovel rural em segundos." Stack: Vite + React SPA.

**Features:** Mapa KML, dados CAR, dados GEO, alertas ambientais, embargos. Consulta via WhatsApp!

**Modelo:** Creditos por consulta.

**Copiar:** WhatsApp como canal, velocidade percebida ("em segundos"), simplicidade extrema da interface.

**Gaps:** Poucos layers, sem score, sem juridico, sem mercado, sem MapBiomas profundo.

---

### 7. AdvLabs (advlabs.com.br)

**O que faz:** IA para defesa ambiental IBAMA/ICMBio. Desenvolvida por Farenzena & Franco Advocacia Ambiental.

**Features:**
- **128 teses catalogadas** (127 admin + 1 civel) com diagnostico por IA
- **Calculadora de prescricao** administrativa e criminal ambiental
- **900+ modelos de peticoes** editaveis (Word)
- **Radar de prospeccao:** Detecta autuados num raio (50-200km) e converte em leads
- **Radar de autos de infracao:** Monitoramento IBAMA/ICMBio
- **Monitoramento SEI/IBAMA/ICMBio** em tempo real
- **Monitoramento judicial** de processos
- **CRM "Meu Escritorio"** com Kanban, prazos, clientes ilimitados
- **Consultas inteligentes** via IA (5/25/100 por plano)
- **Rede social interna** para networking
- **Cursos exclusivos** (basico/intermediario/avancado)

**Precos:** Comunidade R$39/mes. Plano completo R$4.997/ano (Basico/Intermediario/Avancado). Trial 7 dias. Sistema de creditos (Coinback).

**Design:** Light mode, roxo (#19074a) + turquesa (#0bc9ab) + verde (#aaf051). Cards com bordas 30px, sombras. Stack WordPress + Cloudflare.

**Copiar:** Diagnostico de teses por IA, calculadora de prescricao, radar de prospeccao (genial!), modelos editaveis, trial 7 dias, monetizacao hibrida (assinatura + creditos), CRM Kanban integrado, ecossistema plataforma + comunidade + conteudo + eventos.

**Gaps:** ZERO inteligencia fundiaria, zero GIS/mapas, SO ambiental (nao agrario/possessorio/tributario), sem API, stack WordPress (escalabilidade?), apenas 1 tese civel (vs 127 admin).

---

## PARTE II — FINTECHS AGRO (2)

---

### 8. Traive (traive.com)

**O que faz:** Motor de risco agro para fintechs. B2B2C. 2.500+ data points por avaliacao, 15 segundos por analise.

**Funding:** USD 41.1M total (Banco do Brasil, Tiger Global, Syngenta, BASF VC, Serasa VC). FIDC R$800M com Syngenta.

**Features:** 5 tipos de credit scores, LLMs + GANs, database enrichment em 3 tiers (Basico/Intermediario/Avancado), securitizacao digital, monitoramento de portfolio.

**Copiar:** 3 tiers de enrichment, velocidade como selling point (15s), validacao academica (ACM).

**Gaps:** Zero juridico, sem interface para produtor, sem API publica, sem compliance ambiental proprio.

---

### 9. Agrolend (agrolend.agr.br)

**O que faz:** Fintech de credito rural digital. Autorizada pelo BC como financeira (SCFI).

**Funding:** ~USD 100M total. Moody's BBB+. Investidores: Valor Capital, Lightrock, Creation, Syngenta, Norinchukin (Japao).

**Features:** Motor de credito proprietario (Score 0-1000 via Serasa), CPR-F digital com assinatura via link WhatsApp, 3 cliques / <5 minutos, 150+ revendas parceiras, R$600M em carteira, LCAs via XP/BTG/Itau.

**Stack:** AWS, MySQL, WordPress (site), WhatsApp Business API.

**Copiar:** WhatsApp-first (toda jornada via celular), 3 cliques como benchmark UX, CPR-F digital, rede de parceiros como canal de distribuicao.

**Gaps:** Zero juridico, sem due diligence de propriedades (100% Serasa), sem GIS, sem API aberta.

---

## PARTE III — PORTAIS DE CONTEUDO (8)

---

### 10-11. Agrolink + Noticias Agricolas
(Analisados em sessao anterior — 30+ categorias de cotacoes cada, RSS ativos)

### 12. Canal Rural (canalrural.com.br)
RSS ativo (`/feed/`). Cotacoes via Safras & Mercado + Agrosapiens IA. Pracas regionais. TV 24h. Previsao do tempo por municipio com 7 meses de antecedencia. Modelo: gratuito + ads.

### 13. Embrapa (embrapa.br)
**AgroAPI Store** com 11 APIs gratuitas (1K req/mes): Agritec (ZARC), ClimAPI (clima 6h), SATVeg (NDVI/EVI), AGROFIT (agrotoxicos), Bioinsumos, BovTrace, SmartSolos.
**GeoInfo** (geoinfo.dados.embrapa.br): WMS/WFS/WCS/WMTS abertos, sem auth. Dados de solos.

### 14. Portal do Agronegocio (portaldoagronegocio.com.br)
RSS ativo (`/feed`). Taxonomia granular. Secao "Assuntos Juridicos" dentro de Politica Rural. Gratuito + ads.

### 15. AgFeed (agfeed.com.br)
RSS ativo (`/feed/`). Cobertura de FIAGROs, fintechs, M&A agro. Jornalismo de negocios. Gratuito.

### 16. Chaozao (chaozao.com.br)
Marketplace de terras (R$500bi anunciados). Dados reais de R$/ha por regiao. WhatsApp direto para anunciante.

### 17. Valor Agro (valor.globo.com/agronegocios)
Paywall hard. +20 colunistas agro. Nao viavel para scraping.

### 18. DOU (in.gov.br)
INLABS: XMLs completos gratuitos (cadastro). **Ro-DOU** (GitHub): ferramenta open source de clipping. **dou-api**: API REST self-hosted. Essencial para monitorar portarias ZARC, INs IBAMA, resolucoes CONAMA.

---

## PARTE IV — FONTES GOVERNAMENTAIS (18)

---

### 19. MapBiomas (mapbiomas.org)
**GraphQL v2** em plataforma.alerta.mapbiomas.org/api/v2/graphql. Bearer token (cadastro gratis). 17 queries incluindo `ruralProperty` (busca por CAR). Exporta CSV/Shapefile. Collection 9 LULC (1985-2023). Earth Engine assets. GCS downloads publicos.

### 20. INPE TerraBrasilis (terrabrasilis.dpi.inpe.br)
WFS/WMS/WCS aberto. Sem auth. DETER (diario), PRODES (anual). GeoJSON, Shapefile, KML. EPSG:4674.

### 21. IBGE (servicodados.ibge.gov.br + apisidra.ibge.gov.br)
REST completo sem auth. Localidades, malhas (GeoJSON/TopoJSON), SIDRA (PAM/PPM). Tabelas 1612/5457 (lavouras), 3939 (rebanhos). Max 100k valores/req.

### 22. ANA (dadosabertos.ana.gov.br)
ArcGIS FeatureServer. Outorgas, rede hidrometeorologica (17k+ estacoes), pivos irrigacao, bacias. HidroWeb REST para series temporais. Sem auth.

### 23. CONAB (portaldeinformacoes.conab.gov.br)
**SEM API PUBLICA.** Dashboards Pentaho. Dados via download manual XLS ou scraping. Series desde 1976/77. Alternativa: IBGE/SIDRA cobre parcialmente.

### 24. DataJud/CNJ (api-publica.datajud.cnj.jus.br)
**API key PUBLICA** (sem cadastro): `cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==`. Elasticsearch POST. 88 tribunais. 10k registros/pagina. Busca por numero, classe, orgao.

### 25. ONR (mapa.onr.org.br)
**SEM API PUBLICA.** 184 camadas GIS (visual). Acesso programatico via InfoSimples (pago) ou parceria institucional. Maior plataforma registral do Brasil.

### 26. SICAR/CAR (car.gov.br)
GeoServer WFS aberto. 6.5M+ imoveis. Sem auth. 27 camadas por estado. Download Shapefile/GeoJSON por UF.

### 27. INCRA (acervofundiario.incra.gov.br)
WMS + downloads de shapefiles. **Agora requer login gov.br** para muitos servicos. SIGEF particular/publico, assentamentos, quilombolas. EPSG:4674. Atualizacao quinzenal.

### 28. MAPA (dados.agricultura.gov.br)
CKAN API funcional. 13 datasets. ZARC Tabua de Risco (CSV semanal). Agrofit (CSV diario). AgroAPI Embrapa (AGROFIT v1 com Swagger, 100k req/mes gratis).

### 29. BasedosDados (basedosdados.org)
GraphQL (metadados publicos) + BigQuery (dados reais, requer GCP Project). CNPJ 2.7B linhas, censo agropecuario, trabalho escravo, SICOR. Free tier: 1TB/mes BigQuery.

### 30. dados.gov.br
API CKAN instavel (401). Requer token. Estrategia: usar downloads diretos por URL ou portais ministeriais separados.

### 31. IBAMA (dadosabertos.ibama.gov.br)
Embargos ja integrados (103k). Autos de infracao retornam CSV vazio (bug portal). Monitorar.

### 32. FUNAI (geoserver.funai.gov.br)
WFS aberto, sem auth. Camadas: tis_poligonais (655 TIs), aldeias_pontos, coordenacoes regionais. Ja integrado.

### 33. ICMBio (geoservicos.inde.gov.br/geoserver/ICMBio)
WFS via INDE GeoServer. Sem auth. ~340+ UCs federais (Protecao Integral + Uso Sustentavel). Download Shapefile/KMZ.

### 34. MTE (gov.br/trabalho-e-emprego)
Lista Suja: download direto XLSX/CSV (sem API dedicada). 614 empregadores ativos. Atualizacao semestral. Portal da Transparencia API para CEIS/CNEP (cadastro email gratis).

### 35. ANM/SIGMINE (geo.anm.gov.br)
ArcGIS FeatureServer. Sem auth. Processos minerarios ativos (poligonos). Query espacial por coordenada/poligono. Max 5k/req. Download KMZ por estado.

---

## PARTE V — CLIMA / COTACOES / INTERNACIONAIS (6)

---

### 36. NASA POWER (power.larc.nasa.gov)
API REST sem auth. Dados desde 1981. Temp, chuva, radiacao, umidade solo, evapotranspiracao. Community=AG para agricultura. JSON/CSV/NetCDF.

### 37. INMET (apitempo.inmet.gov.br)
API REST sem auth. ~600 estacoes automaticas. Dados horarios/diarios. Biblioteca Python `inmetpy`. BDMEP historico desde 1910.

### 38. CEPEA/ESALQ (cepea.esalq.usp.br)
API oficial paga (OneToOne). **Alternativa gratuita: `agrobr`** (20 indicadores). Boi, soja, milho, cafe, algodao, trigo, arroz, acucar, etanol, frango, suino, leite.

### 39. USDA FAS (apps.fas.usda.gov)
API REST. API key gratis via api.data.gov. PSD (Production/Supply/Distribution): 200+ paises, 300+ commodities. WASDE mensal. Dados desde 1960.

### 40. Yahoo Finance / CME
API unofficial via `yfinance`. Futuros CBOT: ZC=F (milho), ZS=F (soja), ZW=F (trigo), LE=F (boi), KC=F (cafe). Instavel, pode bloquear.

### 41. B3
Futuros agro: BGI (boi), CCM (milho), ICF (cafe), SFI (soja), ETH (etanol). Via `agrobr` (gratuito, MIT). Alternativa oficial: Up2Data (enterprise).

---

## PARTE VI — APIs COMPLEMENTARES (5)

---

### 42. BrasilAPI (brasilapi.com.br)
100% gratuita, sem auth. CNPJ, CEP v2 (com geo), cambio, taxas (SELIC/CDI/IPCA), CPTEC (tempo), CVM fundos, municipios IBGE, NCM, tickers B3, bancos, feriados.

### 43. InfoSimples (infosimples.com)
900+ APIs gov. Pay-per-query. IBAMA embargos R$0.04, INCRA/SIGEF R$0.10, CAR shapefile, CAFIR, protestos CENPROT R$0.06, CPF, CNPJ, PGFN, CEPEA. REST JSON.

### 44. SERPRO (serpro.gov.br)
OAuth2. CPF, CNPJ (3 niveis), **CCIR** (Certificado Imovel Rural), CND, Divida Ativa, NFe, Datavalid. Teste: 30 dias ou 3k consultas gratis. Producao: R$0.35-0.66/consulta. Requer e-CNPJ.

### 45. CENPROT
Sem API publica direta. Via InfoSimples (R$0.06/consulta) ou pesquisaprotesto.com.br (manual, requer Gov.br).

### 46. CVM (dados.cvm.gov.br)
API CKAN funcional, sem auth. FIAGRO informe mensal (CSV), fundos cadastro/diario. Download direto de ZIPs. ODbL license.

---

## PARTE VII — REFERENCIAS DE UX/DESIGN (7)

---

### 47. Stripe Dashboard
KPI metric strip (4-6 cards com sparklines). Sidebar colapsavel com links recentes. 8-point grid (4/8/16/24/32/48px). Principio: "cada numero informa uma decisao."

### 48. Linear
LCH color space (perceptualmente uniforme). Command Palette (Cmd+K). Sidebar dimmed. Inter + Inter Display. Gray morno neutro. Keyboard-first.

### 49. Vercel
Favicon status (cor muda com deployment). SWR real-time. Mobile bottom bar flutuante. Screenshot cards com preview visual.

### 50. Notion
Slash commands (/). Breadcrumbs. Database views (table/board/calendar/gallery). Dark mode: #2F3438 bg, #373C3F sidebar, #3F4448 hover.

### 51. Google Earth Engine
Layer Manager com slider de opacidade. Inspector on-click (crosshair + pixel values). Geometry drawing tools. Search contextual.

### 52. Kepler.gl
GPU-accelerated (deck.gl). Hexbin aggregation. Time slider. Split map view. Dark default. Vector Tiles para datasets enormes.

### 53. Felt
Upload Anything (drag-drop shapefile/GeoJSON/CSV 5GB). Auto-detect espacial. Legend auto-gerada. Popup Table/List views. Basemap switcher.

---

## PARTE VIII — DESCOBERTAS ESTRATEGICAS

---

### A. Top 10 Descobertas Mais Impactantes

| # | Descoberta | Impacto |
|---|---|---|
| 1 | **`agrobr`** (pip install) — 38 fontes agro unificadas (CEPEA, B3, CONAB, IBGE, NASA, MapBiomas) | Substitui 10+ collectors |
| 2 | **DataJud API key publica** — 88 tribunais, sem cadastro | Processos judiciais HOJE |
| 3 | **Embrapa AgroAPI** — ZARC, clima, NDVI, agrotoxicos (gratis 1K/mes) | 4 APIs novas |
| 4 | **AdvLabs** — 128 teses + prescricao + radar prospeccao | Modelo de features juridicas |
| 5 | **Serasa Developer Portal** com Postman | Referencia de API docs |
| 6 | **Agrotools ATMarket** — marketplace modular (Pixels) | Modelo de monetizacao |
| 7 | **DOU Ro-DOU** — monitoramento open source do Diario Oficial | Alertas de normas agro |
| 8 | **BCB SICOR OData** com Swagger — credito rural municipal | Complementa 5.6M parcelas |
| 9 | **SICAR GeoServer WFS** — 6.5M imoveis sem auth | CAR direto da fonte |
| 10 | **ICMBio WFS via INDE** — UCs federais abertas | Completar layer ambiental |

### B. Features Para Copiar dos Concorrentes (Top 20)

| # | Feature | De quem | Prioridade |
|---|---|---|---|
| 1 | Score Fundiario 0-1000 com gauge visual | Serasa | CRITICA |
| 2 | Diagnostico de teses por IA | AdvLabs | ALTA |
| 3 | API documentada com Postman Collection | Registro Rural/Serasa | ALTA |
| 4 | Calculadora de prescricao | AdvLabs | ALTA |
| 5 | Radar de prospeccao (detectar autuados) | AdvLabs | ALTA |
| 6 | WhatsApp como canal principal | Agrolend/DadosFazenda | ALTA |
| 7 | MCR Compliance automatizado | Serasa | CRITICA |
| 8 | Validador de relatorio por codigo unico | SpectraX | MEDIA |
| 9 | ScoreCAR (confiabilidade do CAR) | Agrotools | MEDIA |
| 10 | Marketplace modular (ATMarket/Pixels) | Agrotools | MEDIA |
| 11 | Smart ESG com protocolos configuraveis | Serasa | MEDIA |
| 12 | Trial 7 dias | AdvLabs | ALTA |
| 13 | 900+ modelos de peticoes editaveis | AdvLabs | MEDIA |
| 14 | Monitoramento SEI/IBAMA/ICMBio | AdvLabs | ALTA |
| 15 | Database enrichment em 3 tiers | Traive | MEDIA |
| 16 | CRM Kanban integrado | AdvLabs | BAIXA |
| 17 | Calculadora de ROI publica | Agrotools | MEDIA |
| 18 | Monitoramento DOU automatizado | Ro-DOU | ALTA |
| 19 | Boletim/Newsletter periodico | Serasa | MEDIA |
| 20 | Freemium com IA para conversao | Docket | ALTA |

### C. Posicionamento Unico do AgroJus

Nenhum concorrente cobre a intersecao completa:

| Capacidade | Registro Rural | Agrotools | AdvLabs | Serasa | Traive | Agrolend | **AgroJus** |
|---|---|---|---|---|---|---|---|
| Dados fundiarios (CAR/SIGEF) | SIM | SIM | NAO | PARCIAL | NAO | NAO | **SIM** |
| GIS/Mapa interativo | Basico | Fechado | NAO | Parcial | NAO | NAO | **SIM** |
| Analise juridica/teses | NAO | NAO | SIM (ambiental) | NAO | NAO | NAO | **SIM (agro completo)** |
| Monitoramento processos | NAO | NAO | SIM (admin) | NAO | NAO | NAO | **SIM** |
| Score MCR 2.9 | NAO | SIM | NAO | SIM | NAO | NAO | **A construir** |
| API REST aberta | SIM | Parcial | NAO | SIM | NAO | NAO | **SIM** |
| MapBiomas completo (18 prod) | NAO | Parcial | NAO | NAO | NAO | NAO | **SIM** |
| Credito rural BCB (5.6M) | NAO | NAO | NAO | NAO | NAO | NAO | **SIM (unico!)** |
| Preco acessivel | SIM | NAO | SIM | NAO | NAO | NAO | **SIM** |
| Dark mode premium | NAO | NAO | NAO | NAO | NAO | NAO | **SIM** |

### D. Matriz de Integracao Priorizada

**HOJE (0 custo, 0 auth):**
- `pip install agrobr` (38 fontes: CEPEA, B3, CONAB, IBGE, NASA, MapBiomas, ZARC)
- DataJud/CNJ (API key publica, 88 tribunais)
- BCB SICOR OData (credito rural municipal, Swagger)
- SICAR WFS (6.5M imoveis, sem auth)
- BrasilAPI (CNPJ, cambio, taxas, tempo)
- ICMBio WFS via INDE (UCs federais)
- ANM/SIGMINE (processos minerarios, query espacial)
- INPE TerraBrasilis WFS (PRODES anual)

**SEMANA (cadastro gratis):**
- Embrapa AgroAPI (ZARC, clima, NDVI, agrotoxicos — 1K/mes)
- MapBiomas Alerta GraphQL (alertas por CAR)
- INMET (estacoes proximas — `inmetpy`)
- CVM FIAGRO (CKAN aberto)
- USDA PSD (producao/exportacao global)
- DOU via Ro-DOU (monitoramento de normas)
- MTE: migrar de PDF para download CSV/XLSX direto

**MES (custo baixo):**
- InfoSimples (INCRA/SIGEF R$0.10, CAR shapefile, IBAMA R$0.04, protestos R$0.06)
- SERPRO (CCIR, CPF/CNPJ oficial — teste 30 dias gratis)
- BasedosDados BigQuery (CNPJ 2.7B linhas — requer GCP Project gratis)

**TRIMESTRE (complexo/bloqueado):**
- ONR (parceria institucional ou InfoSimples)
- CONAB (scraping Pentaho ou download XLS)
- INCRA (login gov.br obrigatorio)
- DataJud API key publica pode mudar — monitorar

### E. Design System Recomendado (Dark Mode Forest/Onyx)

**Tokens:**

| Token | Valor |
|---|---|
| `--bg-base` | `#0D1117` |
| `--bg-surface` | `#161B22` |
| `--bg-sidebar` | `#1C2128` |
| `--bg-hover` | `#2D333B` |
| `--border` | `#30363D` |
| `--text-primary` | `#E6EDF3` |
| `--text-secondary` | `#8B949E` |
| `--accent-green` | `#3FB950` |
| `--danger` | `#F85149` |
| `--warning` | `#D29922` |
| `--info` | `#58A6FF` |

**Componentes obrigatorios:**

| Componente | Referencia | Uso |
|---|---|---|
| KPI Card + sparkline | Stripe | Score, alertas, metricas |
| Command Palette (Cmd+K) | Linear | Busca global |
| Sidebar colapsavel | Stripe/Vercel | Nav principal |
| Layer Manager + opacity | GEE | Camadas do mapa |
| Inspector on-click | GEE | Dados do ponto |
| Upload Anything | Felt | Import shapefile |
| Breadcrumbs | Notion | Hierarquia |
| Data Table linkada | Felt/Kepler | Lista de imoveis |
| Drawing Tools | GEE/Felt | Area customizada |
| Badge status | Stripe/Vercel | LOW/MEDIUM/HIGH/CRITICAL |
| Time Slider | Kepler | DETER historico |
| Split Map View | Kepler | Antes/depois |
| Hexbin aggregation | Kepler | Densidade de risco |
| Slash commands | Notion | /analise /camadas /risco |

**Layout:**
```
Top Bar: Logo + Search (Cmd+K) + Notifications + User
+--------+--------------------------------------------+
| Sidebar |              MAPA (protagonista)            |
| 240px   |  [Layer Manager]       [Inspector]          |
| colapsa |  [Drawing Tools]       [Legend]              |
| vel     |  [Time Slider]         [Basemap]             |
|         |+------------+-----------------------------+ |
| - Dash  || KPI Strip  | Charts + Table              | |
| - Mapa  |+------------+-----------------------------+ |
+---------+----------------------------------------------+
```

**Tipografia:** Inter + Inter Display (headings). Geist Mono (dados tecnicos). KPIs: 28-32px, weight 600-700.

---

*AgroJus — Analise Competitiva Completa v1.0 — 53 sites — 2026-04-15*
