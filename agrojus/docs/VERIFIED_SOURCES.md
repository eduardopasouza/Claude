# Fontes de Dados VERIFICADAS e TESTADAS — AgroJus

Todas as fontes abaixo foram testadas com requisições reais em 2026-04-09.
Somente fontes que REALMENTE funcionam estão listadas aqui.

---

## ✅ APIs EM TEMPO REAL (sem auth, resposta imediata)

### Dados de Pessoa/Empresa
| Fonte | URL testada | Dados | Tempo |
|-------|-----------|-------|-------|
| **BrasilAPI CNPJ** | `brasilapi.com.br/api/cnpj/v1/{cnpj}` | Razão social, CNAE, sócios, capital, endereço | 0.2s |
| **CNPJa** | `open.cnpja.com/office/{cnpj}` | Alternativa CNPJ | 0.5s |

### Dados Econômicos e Financeiros
| Fonte | URL testada | Dados | Tempo |
|-------|-----------|-------|-------|
| **BCB Dólar PTAX** | `olinda.bcb.gov.br/.../PTAX/.../CotacaoDolarDia` | Cotação compra/venda (R$5,08) | <1s |
| **BCB Selic** | `api.bcb.gov.br/dados/serie/bcdata.sgs.432/...` | Taxa Selic (14,75%) | <1s |
| **BCB IPCA** | `api.bcb.gov.br/dados/serie/bcdata.sgs.433/...` | Inflação mensal | <1s |
| **BCB CDI** | `api.bcb.gov.br/dados/serie/bcdata.sgs.4391/...` | CDI (0,27% abr) | <1s |
| **BCB Crédito Rural Total** | `api.bcb.gov.br/dados/serie/bcdata.sgs.22037/...` | R$240,7 bi (fev/2026) | <1s |
| **BCB Endividamento Rural** | `api.bcb.gov.br/dados/serie/bcdata.sgs.28763/...` | R$48,8 bi (fev/2026) | <1s |
| **SICOR/BCB Custeio** | `olinda.bcb.gov.br/.../SICOR/.../CusteioMunicipioProduto` | Crédito por município/produto/ano | 1-2s |
| **B3 Boi Gordo** | `cotacao.b3.com.br/mds/api/v1/DerivativeQuotation/BGI` | R$342,65/@ (1437 contratos) | 4s |
| **B3 Milho** | `.../DerivativeQuotation/CCM` | R$72,53/sc (983 contratos) | 4s |
| **B3 Café Arábica** | `.../DerivativeQuotation/ICF` | R$390,00/sc (462 contratos) | 4s |
| **B3 Soja CME** | `.../DerivativeQuotation/SJC` | R$25,47 (592 contratos) | 4s |
| **B3 Etanol** | `.../DerivativeQuotation/ETH` | R$2.640 (36 contratos) | 4s |

### Dados Geoespaciais
| Fonte | URL testada | Dados | Tempo |
|-------|-----------|-------|-------|
| **FUNAI GeoServer WFS** | `geoserver.funai.gov.br/geoserver/Funai/ows` | 655 TIs com geometria, etnia, fase, área | 2.4s |
| **TerraBrasilis DETER WFS** | `terrabrasilis.dpi.inpe.br/geoserver/deter-amz/wfs` | 445.960 alertas desmatamento (Amazônia) | 2.6s |
| **TerraBrasilis Biomas WFS** | `.../prodes-brasil-nb/wfs` | Limites dos 6 biomas | ~3s |

### Dados de Produção Agrícola
| Fonte | URL testada | Dados | Tempo |
|-------|-----------|-------|-------|
| **IBGE/SIDRA PAM** | `apisidra.ibge.gov.br/values/t/5457/...` | Área, produção, rendimento por município/cultura | 1s |
| **IBGE Localidades** | `servicodados.ibge.gov.br/api/v1/localidades/.../municipios` | Nomes e códigos de todos os municípios | <1s |

### Previsão do Tempo
| Fonte | URL testada | Dados | Tempo |
|-------|-----------|-------|-------|
| **BrasilAPI/CPTEC** | `brasilapi.com.br/api/cptec/v1/clima/previsao/{id}/6` | Previsão 6 dias: temp min/max, condição, UV | 1s |

---

## ✅ DOWNLOADS DISPONÍVEIS (CSVs, ZIPs, Shapefiles)

| Fonte | URL | Formato | Atualização |
|-------|-----|---------|-------------|
| **IBAMA Embargos** | `.../SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip` | ZIP/CSV | Semanal |
| **IBAMA Coordenadas** | `.../SIFISC/termo_embargo/coordenadas/coordenadas.csv` | CSV com WKT | 2026-04-08 |
| **IBAMA Autos Infração** | `.../SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip` | ZIP/CSV | Semanal |
| **MMA UCs (CNUC)** | `dados.mma.gov.br/.../shp_cnuc_2025_08.zip` | Shapefile | Mar 2025 |
| **IBGE Biomas** | `geoftp.ibge.gov.br/.../Biomas_250mil.zip` | Shapefile | 2025 |
| **IBGE Solos** | `geoftp.ibge.gov.br/.../pedologia/vetores/...` | Shapefile | Disponível |
| **IBGE Vegetação** | `geoftp.ibge.gov.br/.../vegetacao/vetores/...` | Shapefile | Disponível |
| **IBGE Geomorfologia** | `geoftp.ibge.gov.br/.../geomorfologia/vetores/...` | Shapefile | Disponível |
| **CONAB Séries Históricas** | `portaldeinformacoes.conab.gov.br/.../SerieHistoricaGraos.txt` | TXT/CSV | Desde 1976 |
| **ANM Cadastro Mineiro** | `dados.gov.br/.../sistema-de-cadastro-mineiro` | CSV | Periódico |
| **ANM SIGMINE** | `dados.gov.br/.../sistema-de-informacoes-geograficas-da-mineracao-sigmine` | Shapefile | Periódico |

---

## ✅ RSS FEEDS FUNCIONANDO

| Portal | URL | HTTP |
|--------|-----|------|
| **Agrolink** | `agrolink.com.br/rss/noticias.xml` | 200 |
| **Canal Rural** | `canalrural.com.br/feed/` | 200 |
| **Portal do Agronegócio** | `portaldoagronegocio.com.br/feed` | 200 |
| **AgFeed** | `agfeed.com.br/feed/` | 200 |
| **Agrofy News** | `news.agrofy.com.br/feed` | 200 |
| **Beef Point** | `beefpoint.com.br/feed/` | 200 (redir) |
| **InfoMoney** | `infomoney.com.br/feed/` | 200 |
| **G1 Agro** | `g1.globo.com/rss/g1/economia/agronegocios/` | 200 |

---

## ⚠️ REQUER CADASTRO/TOKEN (gratuito)

| Fonte | O que precisa | Dados disponíveis |
|-------|--------------|-------------------|
| **DataJud/CNJ** | Chave API (cadastro gratuito) | Processos judiciais por CPF/CNPJ, assunto, tribunal |
| **MapBiomas Alerta** | Token (solicitar) | Alertas desmatamento com cruzamento CAR/SIGEF/TI/UC/embargo |
| **Portal Transparência** | Chave API (cadastro) | Sanções CEIS/CEPIM, dados de contratos, gastos |

---

## ⚠️ INSTÁVEL / MIGROU

| Fonte | Problema | Solução |
|-------|---------|---------|
| **SICAR/CAR** | 503 em todos endpoints | Cache agressivo (7d) + retry |
| **SIGEF/INCRA WFS** | 404 (/geoserver removido) | Investigar novo endpoint |
| **CEPEA** | Cloudflare (403) | Playwright (browser headless) |
| **INMET** | 503 | Usar BrasilAPI/CPTEC como fallback |

---

## RESUMO QUANTITATIVO

- **APIs em tempo real sem auth**: 17 endpoints confirmados
- **Downloads disponíveis**: 11 datasets (CSV, shapefile, TXT)
- **RSS feeds funcionando**: 8 portais de notícias
- **Requer cadastro gratuito**: 3 fontes (DataJud, MapBiomas, Portal Transparência)
- **Instável/migrou**: 4 fontes (SICAR, SIGEF WFS, CEPEA, INMET)
- **Total de fontes utilizáveis**: ~39 fontes confirmadas
