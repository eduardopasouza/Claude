# AgroJus — Catálogo Exaustivo de Fontes de Dados

**Versão:** 3.0 — Pesquisa Profunda
**Data:** 12 abril 2026

> Este documento lista **TODOS** os bancos de dados, camadas de mapa, APIs e fontes disponíveis publicamente que o AgroJus pode usar. O objetivo é ser mais completo que qualquer concorrente.

---

## I. ECOSSISTEMA MAPBIOMAS (18 subprodutos)

O MapBiomas é a base de dados ambiental mais completa do hemisfério sul. **Nenhum concorrente usa todos os subprodutos.** Nós vamos usar todos.

### 1. Cobertura e Uso da Terra (Coleção 10.1)
| | |
|---|---|
| **Conteúdo** | Mapeamento anual de 1985 a 2023 — classifica cada pixel (30m) como: floresta, pastagem, soja, café, cana, silvicultura, mineração, infraestrutura, água, etc. |
| **Formato** | GeoTIFF raster (30m resolução) |
| **Asset GEE** | `projects/mapbiomas-public/assets/brazil/lulc/collection10_1/mapbiomas_brazil_collection10_1_coverage_v1` |
| **Aplicação AgroJus** | Classificar uso da terra de qualquer coordenada/propriedade. Histórico 38 anos para verificar conversão de vegetação nativa (EUDR exige pré-2020) |
| **Status** | ❌ Falta baixar GeoTIFFs por bioma |

### 2. MapBiomas 10 metros (Coleção Beta)
| | |
|---|---|
| **Conteúdo** | Mapas anuais de cobertura com **10m de resolução** desde 2016 (Sentinel-2) |
| **Aplicação** | Resolução 9× maior — detalha limites de talhão, APP ripária, cultivo vs pastagem vizinhos |
| **Status** | ❌ Não explorado — **nenhum concorrente usa publicamente** |

### 3. MapBiomas Fogo (Coleção 4)
| | |
|---|---|
| **Conteúdo** | Cicatrizes de fogo anuais e mensais de 1985 a 2024 |
| **Aplicação** | Histórico de incêndios por propriedade — risco ambiental, compliance MCR 2.9, seguro rural |
| **Status** | ❌ Não baixado |

### 4. Monitor Mensal do Fogo
| | |
|---|---|
| **Plataforma** | [plataforma.monitorfogo.mapbiomas.org](https://plataforma.monitorfogo.mapbiomas.org/) |
| **Conteúdo** | Alertas mensais de fogo em tempo quase-real |
| **Aplicação** | Monitoramento contínuo — se o cliente tem imóvel com fogo recente, alertar imediatamente |
| **Status** | ❌ Não integrado |

### 5. MapBiomas Alerta (API GraphQL)
| | |
|---|---|
| **Endpoint** | `https://plataforma.alerta.mapbiomas.org/api/v2/graphql` |
| **Conteúdo** | Alertas de desmatamento validados com laudos técnicos |
| **Queries** | `alerts` (lista), `alert` (detalhe+laudo), `alertReport` (CSV/SHP em massa) |
| **Aplicação** | **PEÇA CENTRAL EUDR** — cruzar propriedade com alertas de desmatamento. Gerar laudos automáticos |
| **Status** | ❌ Precisa criar conta e implementar collector |

### 6. Monitor do Crédito Rural
| | |
|---|---|
| **Plataforma** | [plataforma.creditorural.mapbiomas.org](https://plataforma.creditorural.mapbiomas.org) |
| **Conteúdo** | **Polígonos vetoriais** de onde o crédito rural é aplicado, cruzados com desmatamento |
| **Download** | Arquivos vetoriais organizados para download |
| **Aplicação** | **OURO ABSOLUTO** — verifica se crédito público foi usado em área desmatada. Exclusividade MapBiomas. Nenhum concorrente tem isso |
| **Status** | ❌ Não baixado — prioridade máxima |

### 7. Monitor da Recuperação
| | |
|---|---|
| **Plataforma** | [plataforma.recuperacao.mapbiomas.org](https://plataforma.recuperacao.mapbiomas.org/) |
| **Conteúdo** | Áreas em processo de regeneração/recuperação |
| **Aplicação** | Laudos de compliance florestal — prova que proprietário está recuperando área degradada (reduz risco ESG) |
| **Status** | ✅ Download parcial (132 MB, módulo recuperação Col.10) |

### 8. Monitor da Mineração
| | |
|---|---|
| **Plataforma** | [plataforma.monitormineracao.mapbiomas.org](https://plataforma.monitormineracao.mapbiomas.org/) |
| **Conteúdo** | Detecção de garimpo e mineração ilegal por satélite |
| **Aplicação** | Sobreposição com imóvel rural — risco ambiental e fundiário |
| **Status** | ❌ Não integrado |

### 9. Módulo Urbano (Coleção 10)
| | |
|---|---|
| **Conteúdo** | Mapeamento detalhado de áreas urbanizadas do Brasil |
| **Aplicação** | Delimitar perímetro urbano — imóveis na franja urbana/rural |
| **Status** | ✅ Download (59 MB zip) |

### 10. MapBiomas Água
| | |
|---|---|
| **Conteúdo** | Mapeamento anual de superfícies hídricas (rios, reservatórios, áreas alagáveis) |
| **Aplicação** | Risco de alagamento, compliance de APP ripária, outorga de água |
| **Status** | ❌ Não baixado |

### 11. MapBiomas Solo
| | |
|---|---|
| **Conteúdo** | Estoque de carbono orgânico, granulometria e textura do solo |
| **Aplicação** | Avaliação de aptidão agrícola, potencial de carbono, valor da terra |
| **Status** | ❌ Não explorado — **diferencial enorme vs concorrentes** |

### 12. MapBiomas Degradação (Beta)
| | |
|---|---|
| **Conteúdo** | Vetores de degradação da vegetação nativa |
| **Aplicação** | Compliance EUDR — degradação ≠ desmatamento mas é verificada na regulação europeia |
| **Status** | ❌ Novo, não explorado |

### 13. MapBiomas Cacau
| | |
|---|---|
| **Conteúdo** | Mapeamento específico de cacau no Sul da Bahia |
| **Aplicação** | Nicho: compliance EUDR para cacau (commodity regulada pela UE) |
| **Status** | ❌ Não explorado |

### 14. Dados de Infraestrutura
| | |
|---|---|
| **Conteúdo** | Energia, transporte, mineração, agronegócio, telecomunicações, pistas de pouso na Amazônia |
| **Aplicação** | Análise logística — distância do imóvel a estradas, portos, silos |
| **Status** | ❌ Não baixado |

### 15-18. Mosaicos Landsat, Mapas de Referência, Pontos de Validação, Camadas
| | |
|---|---|
| **Conteúdo** | Imagens brutas, validação científica, camadas auxiliares |
| **Aplicação** | Base para processamento próprio se necessário |
| **Status** | ❌ Baixar conforme demanda |

---

## II. FONTES GEOESPACIAIS (Camadas do Mapa)

### 19. INPE TerraBrasilis — DETER (Alertas em tempo real)
| | |
|---|---|
| **WFS** | `https://terrabrasilis.dpi.inpe.br/geoserver/ows` |
| **Download** | [terrabrasilis.dpi.inpe.br/downloads](https://terrabrasilis.dpi.inpe.br/downloads/) |
| **Biomas** | Amazônia, Cerrado (florestais + não-florestais), Pantanal (experimental) |
| **Aplicação** | Overlay de alertas de desmatamento no mapa — padrão ouro para MCR 2.9 |

### 20. INPE TerraBrasilis — PRODES (Desmatamento anual)
| | |
|---|---|
| **Conteúdo** | Mapeamento consolidado de corte raso — base oficial para políticas públicas |
| **Aplicação** | Histórico de desmatamento oficial |

### 21. FUNAI — Terras Indígenas
| | |
|---|---|
| **WFS** | `https://geoserver.funai.gov.br/geoserver/wfs` |
| **SHP** | [gov.br/funai/geoprocessamento](https://www.gov.br/funai/pt-br/atuacao/terras-indigenas/geoprocessamento-e-mapas) |
| **Aplicação** | **Bloqueio MCR 2.9** — sobreposição com TI bloqueia crédito automaticamente |

### 22. ICMBio — Unidades de Conservação
| | |
|---|---|
| **SHP** | [gov.br/icmbio/dados_geoespaciais](https://www.gov.br/icmbio/pt-br/assuntos/dados_geoespaciais/) |
| **Conteúdo** | Parques nacionais, APAs, reservas biológicas, reservas extrativistas |
| **Aplicação** | Sobreposição com UC pode restringir atividades |

### 23. INCRA / SIGEF — Parcelas Certificadas
| | |
|---|---|
| **WFS** | `https://acervofundiario.incra.gov.br/i3geo/ogc.php` (por UF) |
| **Autenticação** | login gov.br |
| **Aplicação** | Limites exatos de propriedades georreferenciadas |

### 24. SICAR / CAR — Cadastro Ambiental Rural
| | |
|---|---|
| **Consulta** | [consultapublica.car.gov.br](https://consultapublica.car.gov.br/publico/imoveis/index) |
| **Conteúdo** | Polígonos com APP, Reserva Legal, uso consolidado |
| **Aplicação** | Base principal para identificação do imóvel |

### 25. Parcelas de Financiamento Rural (BCB GPKG)
| | |
|---|---|
| **Arquivo local** | `parcelas_financiamento_201224.gpkg` (4.7 GB) |
| **Aplicação** | Para onde vai o crédito rural — cruzar com embargos |
| **Status** | ✅ Baixado |

### 26. IBAMA SISCOM — Áreas Embargadas (SHP)
| | |
|---|---|
| **URL** | [siscom.ibama.gov.br](https://siscom.ibama.gov.br/) — Dados Geoespaciais |
| **Conteúdo** | **Polígonos** das áreas embargadas (diferente do CSV tabular) |
| **Aplicação** | Overlay visual no mapa |

### 27. Assentamentos Rurais INCRA
| | |
|---|---|
| **Conteúdo** | Polígonos de todos os assentamentos da reforma agrária |
| **Aplicação** | Verificar se área é assentamento — implicações fundiárias distintas |

### 28. Quilombos — INCRA / Fundação Palmares
| | |
|---|---|
| **Conteúdo** | Territórios quilombolas |
| **Aplicação** | Sobreposição com quilombo = restrição fundiária |

### 29. ANM/SIGMINE — Mineração
| | |
|---|---|
| **API** | `https://geo.anm.gov.br/arcgis/rest/services` |
| **Conteúdo** | Processos minerários, direitos, lavras, requerimentos |
| **Aplicação** | Sobreposição com área de mineração |

### 30. ANA — Recursos Hídricos
| | |
|---|---|
| **Conteúdo** | Outorgas de água, bacias hidrográficas, rios |
| **Aplicação** | Risco hídrico, irrigação, conflitos de uso da água |

### 31. Embrapa GeoInfo — Solos e Aptidão
| | |
|---|---|
| **URL** | [geoinfo.embrapa.br](https://geoinfo.embrapa.br/) |
| **Conteúdo** | Tipos de solo, aptidão agrícola, zoneamentos |
| **Aplicação** | Valor da terra, potencial produtivo |

### 32. IBGE — Malhas Territoriais
| | |
|---|---|
| **API** | `servicodados.ibge.gov.br/api/v3/malhas` |
| **Conteúdo** | Limites de municípios, estados, biomas, regiões |
| **Aplicação** | Base de referência para todas as análises geográficas |

### 33. SINAFLOR — Autorizações de Supressão
| | |
|---|---|
| **Conteúdo** | Registros de autorização de desmatamento legal pelo IBAMA/órgãos estaduais |
| **Aplicação** | Verificar se desmatamento na propriedade foi autorizado (crucial para EUDR) |

---

## III. FONTES TABULARES / COMPLIANCE

### 34. IBAMA — Embargos (CSV)
| | |
|---|---|
| **URL** | `dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/` |
| **Recursos** | `termo_embargo_csv.zip`, `coordenadas.csv`, `itens.csv`, `decisao.csv`, `enquadramento.csv`, `historico.csv`, `anexo.csv` |
| **Status** | ✅ **103.668 embargos reais indexados no PostGIS** |

### 35. IBAMA — Autos de Infração (CSV)
| | |
|---|---|
| **URL** | [dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao](https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao) |
| **Conteúdo** | Multas ambientais — valor, tipo de infração, localização |
| **Aplicação** | Complementar aos embargos — mostra valor das multas |
| **Status** | ❌ Não baixado |

### 36. MTE — Lista Suja Trabalho Escravo
| | |
|---|---|
| **URL** | [gov.br/trabalho/combate-ao-trabalho-escravo](https://www.gov.br/trabalho/pt-br/assuntos/fiscalizacao/combate-ao-trabalho-escravo) |
| **Formato** | CSV/XLSX (semestral) |
| **Status** | ⚠️ ETL criado, usando backup (portal 500) |

### 37. Receita Federal — CNPJ
| | |
|---|---|
| **API** | `brasilapi.com.br/api/cnpj/v1/{cnpj}` |
| **Status** | ✅ Integrado |

### 38. BCB SICOR — Crédito Rural (API)
| | |
|---|---|
| **OData** | `olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/` |
| **Recursos** | `CusteioMunicipioProduto`, `InvestMunicipioProduto`, `ComercMunicipioProduto` |

### 39. DataJud / CNJ — Processos Judiciais
| | |
|---|---|
| **API** | `api-publica.datajud.cnj.jus.br` (Elasticsearch) |

### 40. BCB — Indicadores (SELIC, IPCA, câmbio)
| | |
|---|---|
| **API** | `api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados` |
| **Status** | ✅ Online |

### 41. NASA POWER — Clima
| | |
|---|---|
| **API** | `power.larc.nasa.gov/api/temporal/daily/point` |

### 42. CEPEA/ESALQ — Preços de Commodities
| | |
|---|---|
| **Conteúdo** | Indicadores de preço de soja, milho, boi, café, algodão |
| **Aplicação** | Painel Mercado — cotações em tempo real |

### 43. CONAB — Produção e Safras
| | |
|---|---|
| **Conteúdo** | Estimativas de safra, estoques, custos de produção |
| **Aplicação** | Inteligência de mercado por município |

### 44. IBGE SIDRA — Estatísticas Agro
| | |
|---|---|
| **API** | `apisidra.ibge.gov.br` |
| **Conteúdo** | Censo agropecuário, produção agrícola municipal, rebanho |

### 45. MAPA — Dados Abertos
| | |
|---|---|
| **URL** | [dados.agricultura.gov.br](https://dados.agricultura.gov.br) |
| **Conteúdo** | Agrofit (agrotóxicos), SIPEAGRO, ZARC (zoneamento de risco climático) |
| **Aplicação** | Zoneamento agrícola por cultura — onde plantar o quê |

### 46. CNIR / SNCR — Cadastro Nacional de Imóveis
| | |
|---|---|
| **Conteúdo** | Integração INCRA + Receita Federal — dados cadastrais unificados |
| **URL** | [gov.br/incra/cnir](https://www.gov.br/incra/pt-br) |

### 47. INDE — Infraestrutura Nacional de Dados Espaciais
| | |
|---|---|
| **URL** | [inde.gov.br](https://www.inde.gov.br/) |
| **Conteúdo** | Metaportal de dados geoespaciais de todos os órgãos federais |

### 48. Base dos Dados (basedosdados.org)
| | |
|---|---|
| **Conteúdo** | Repositório unificado de dados públicos brasileiros (BigQuery) |
| **Aplicação** | Acesso otimizado a IBAMA, INPE, IBGE, MTE via SQL |

---

## IV. ANÁLISE COMPETITIVA PROFUNDA

### Agrotools — o que eles têm:
- **1.200 camadas** de informação geoespacial (data lake proprietário 10+ anos)
- Monitoramento 100% digital por satélite
- Due Diligence automatizada de fornecedores (cadeia campo-a-varejo)
- APIs (microserviços) para integração em sistemas de clientes
- ATMarket — marketplace de produtos digitais
- App de Campo offline com GPS e fotos georreferenciadas
- Análise de crédito e seguro rural em segundos

### SpectraX — o que eles têm:
- Análise de conformidade CAR (Reserva Legal, APP, uso consolidado)
- Histórico de uso do solo 2008-2024
- PRODES + ImazonGeo para alertas de desmatamento
- SINAFLOR — verificação de autorizações de supressão
- Estoque de carbono + potencial de créditos VCU
- Blockchain para integridade de laudos
- Mapeamento de safra de soja em tempo quase-real
- Foco total em EUDR

### Registro Rural — o que eles têm:
- **16 milhões de imóveis** rurais cadastrados
- Base consolidada CAR + SIGEF + INCRA
- Consulta unificada por código CAR
- Foco em regularização fundiária

### Onde o AgroJus pode superar TODOS:

| Diferencial | Agrotools | SpectraX | Registro Rural | **AgroJus** |
|-------------|-----------|----------|----------------|-------------|
| **Jurídico + Ambiental integrado** | ⬜ | ⬜ | ⬜ | ✅ DataJud + IBAMA no mesmo laudo |
| **MapBiomas Crédito Rural** | ⬜ | ⬜ | ⬜ | ✅ cruzar financ. com desmatamento |
| **MapBiomas Solo (carbono)** | ⬜ | Parcial | ⬜ | ✅ Aptidão agrícola + valor terra |
| **MapBiomas 10m resolução** | ⬜ | ⬜ | ⬜ | ✅ Precisão de talhão |
| **MapBiomas Degradação** | ⬜ | ⬜ | ⬜ | ✅ EUDR diferenciado |
| **Todos subprodutos MapBiomas** | Parcial | Parcial | ⬜ | ✅ Todos 18 |
| **103K embargos IBAMA reais** | Interno | Interno | ✅ | ✅ Já no PostGIS |
| **Parcelas financiamento 4.7GB** | ⬜ | ⬜ | ⬜ | ✅ Baixado |
| **Auditoria MCR 2.9 automatizada** | Pago | Pago | ⬜ | ✅ Gratuito/Enterprise |

---

## V. CAMADAS RENDERIZÁVEIS NO MAPA

Todo item abaixo **pode ser renderizado como camada no mapa Leaflet**:

| # | Camada | Tipo Geo | Fonte | Acesso |
|---|--------|----------|-------|--------|
| 1 | Cobertura e Uso da Terra | Raster 30m | MapBiomas Col.10 | GEE |
| 2 | Cobertura 10m | Raster 10m | MapBiomas Beta | GEE |
| 3 | Cicatrizes de Fogo | Raster | MapBiomas Fogo | GEE |
| 4 | Alertas de Desmatamento (laudos) | Polígono | MapBiomas Alerta | GraphQL |
| 5 | Crédito Rural (polígonos) | Polígono | MapBiomas Monitor | Download |
| 6 | Recuperação de Vegetação | Polígono | MapBiomas Monitor | Download |
| 7 | Mineração/Garimpo | Polígono | MapBiomas Monitor | Download |
| 8 | Áreas Urbanizadas | Polígono | MapBiomas Urbano | ✅ Baixado |
| 9 | Superfícies Hídricas | Raster | MapBiomas Água | GEE |
| 10 | Carbono do Solo | Raster | MapBiomas Solo | GEE |
| 11 | Degradação da Vegetação | Raster | MapBiomas Degradação | GEE |
| 12 | Infraestrutura (estradas, portos) | Vetor | MapBiomas Infra | Download |
| 13 | DETER Alertas | Polígono | INPE TerraBrasilis | WFS |
| 14 | PRODES Desmatamento | Polígono | INPE TerraBrasilis | WFS |
| 15 | Terras Indígenas | Polígono | FUNAI | WFS/SHP |
| 16 | Unidades de Conservação | Polígono | ICMBio | SHP |
| 17 | Parcelas Certificadas | Polígono | INCRA/SIGEF | WFS |
| 18 | CAR (APP/RL/Uso) | Polígono | SICAR | Consulta |
| 19 | Parcelas de Financiamento | Polígono | BCB GPKG | ✅ Local |
| 20 | Embargos IBAMA (coord.) | Ponto | IBAMA CSV | ✅ PostGIS |
| 21 | Embargos IBAMA (polígono) | Polígono | IBAMA SISCOM | Download |
| 22 | Assentamentos | Polígono | INCRA | SHP |
| 23 | Quilombos | Polígono | INCRA/Palmares | SHP |
| 24 | Processos Minerários | Polígono | ANM/SIGMINE | ArcGIS REST |
| 25 | Outorgas de Água | Ponto/Polígono | ANA | API |
| 26 | Solos/Aptidão | Raster | Embrapa GeoInfo | Download |
| 27 | Biomas | Polígono | IBGE | API |
| 28 | Municípios | Polígono | IBGE | API |
| 29 | Rodovias | Linha | DNIT/IBGE | Download |
| 30 | Ferrovias | Linha | ANTT/IBGE | Download |

---

## VI. DADOS DISPONÍVEIS PARA CONSULTAS (Busca por CPF/CNPJ)

Todo item abaixo pode ser consultado por CPF ou CNPJ e apresentado no dossiê:

| # | Consulta | Fonte | Formato |
|---|----------|-------|---------|
| 1 | Razão Social, CNAE, Sócios, Capital | Receita Federal (BrasilAPI) | JSON |
| 2 | Embargos ambientais | IBAMA PostGIS | SQL |
| 3 | Autos de infração (multas) | IBAMA CSV | SQL |
| 4 | Lista Suja trabalho escravo | MTE | SQL |
| 5 | Processos judiciais | DataJud/CNJ | Elasticsearch |
| 6 | Crédito rural contratado | BCB SICOR | OData |
| 7 | Propriedades CAR | SICAR | Scraping |
| 8 | Parcelas certificadas SIGEF | INCRA | WFS |
| 9 | Certidões negativas | Receita/PGFN | Scraping |
| 10 | Débitos tributários | PGFN | Portal |
| 11 | Alertas de desmatamento | MapBiomas Alerta | GraphQL |
| 12 | CADIN (inadimplentes) | Portal Gov | Manual |
| 13 | SINAFLOR autorizações | IBAMA | Portal |

---

## VII. PRIORIDADES ESTRATÉGICAS

### Tier 0 — Fazer agora (vantagem competitiva imediata)
1. ✅ **IBAMA Embargos CSV** — 103.668 registros no PostGIS
2. 🔴 **IBAMA Autos de Infração CSV** — complementar embargos com multas
3. 🔴 **FUNAI TI shapefile** — baixar SHP e carregar no PostGIS
4. 🔴 **ICMBio UCs shapefile** — baixar SHP e carregar no PostGIS

### Tier 1 — Diferencial MapBiomas (nenhum concorrente faz tudo)
5. 🟡 **MapBiomas Alerta API** — criar conta, implementar GraphQL
6. 🟡 **MapBiomas Monitor Crédito Rural** — baixar vetoriais
7. 🟡 **MapBiomas Monitor do Fogo** — alertas mensais

### Tier 2 — Profundidade além dos concorrentes
8. 🟢 **MapBiomas Solo** — carbono, textura, aptidão
9. 🟢 **MapBiomas 10m** — resolução que ninguém usa
10. 🟢 **MapBiomas Degradação** — EUDR diferenciado
11. 🟢 **Embrapa GeoInfo** — solos e zoneamentos
12. 🟢 **CONAB safras** — inteligência de mercado

---

*Este catálogo é o mapa de guerra do AgroJus. Será atualizado conforme cada fonte for integrada ao PostGIS.*
