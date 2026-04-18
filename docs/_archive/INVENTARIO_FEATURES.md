# INVENTARIO COMPLETO DE FEATURES — AgroJus

> Lista exaustiva de todas as funcionalidades possiveis.
> Fontes: 53 sites analisados + capacidades proprias.
> Legenda: [QUEM JA FAZ] | [FONTE DE DADOS] | API + WEB = disponivel em ambos
> 2026-04-15

---

## 1. CONSULTA E IDENTIFICACAO DE IMOVEIS RURAIS

### 1.1 Busca por identificador
| # | Feature | Quem faz | Fonte | API | WEB |
|---|---|---|---|---|---|
| 1 | Busca por codigo CAR (ex: MT-5101100-XXXXX) | Registro Rural, Serasa, Agrotools, DadosFazenda | SICAR WFS | SIM | SIM |
| 2 | Busca por CPF do proprietario (retorna todos os imoveis vinculados) | Registro Rural, Serasa | SICAR + InfoSimples | SIM | SIM |
| 3 | Busca por CNPJ da empresa (retorna todos os imoveis) | Registro Rural, Serasa | SICAR + InfoSimples | SIM | SIM |
| 4 | Busca por nome do proprietario/empresa | Registro Rural | SICAR + CNPJ | SIM | SIM |
| 5 | Busca por codigo NIRF (Receita Federal) | Registro Rural | CAFIR/InfoSimples | SIM | SIM |
| 6 | Busca por codigo SNCR (INCRA) | Registro Rural | INCRA | SIM | SIM |
| 7 | Busca por codigo SIGEF (parcela certificada) | Registro Rural | INCRA/SIGEF | SIM | SIM |
| 8 | Busca por codigo CCIR | Ninguem | SERPRO | SIM | SIM |
| 9 | Busca por numero de matricula (cartorio) | Ninguem (ONR visual) | ONR/InfoSimples | SIM | SIM |
| 10 | Busca por coordenada geografica (lat/lon) | Registro Rural | PostGIS spatial | SIM | SIM |
| 11 | Busca por endereco/municipio/localidade | DadosFazenda | Nominatim + IBGE | SIM | SIM |
| 12 | Busca por numero de processo judicial vinculado | Ninguem | DataJud | SIM | SIM |
| 13 | Busca por numero de auto de infracao IBAMA | Ninguem | IBAMA | SIM | SIM |

### 1.2 Input de geometria
| # | Feature | Quem faz | Fonte | API | WEB |
|---|---|---|---|---|---|
| 14 | Upload de shapefile (.shp/.shx/.dbf/.prj) | Felt, ONR | ogr2ogr | SIM | SIM |
| 15 | Upload de GeoJSON | GEE | PostGIS | SIM | SIM |
| 16 | Upload de KML/KMZ | Registro Rural | ogr2ogr | SIM | SIM |
| 17 | Upload de CSV com lat/lon (auto-detect colunas) | Felt | pandas + PostGIS | SIM | SIM |
| 18 | Desenho de poligono livre no mapa | GEE, Felt, Kepler | Leaflet Draw | NAO | SIM |
| 19 | Desenho de retangulo (bbox) no mapa | GEE | Leaflet | NAO | SIM |
| 20 | Desenho de circulo (ponto + raio) no mapa | Felt | PostGIS ST_Buffer | NAO | SIM |
| 21 | Paste de coordenadas WKT | GEE | PostGIS | SIM | SIM |
| 22 | Captura de poligono do CAR pela busca (sem upload manual) | Agrotools, Serasa | SICAR WFS | SIM | SIM |

---

## 2. RELATORIO DE CONFORMIDADE (DUE DILIGENCE)

### 2.1 Identificacao do imovel
| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 23 | Ficha cadastral do imovel (nome, area, modulos fiscais, bioma, municipio, UF) | Registro Rural, Serasa | CAR + INCRA |
| 24 | Identificacao do proprietario/posseiro (CPF/CNPJ, nome, situacao cadastral) | Serasa, Registro Rural | Receita Federal/BrasilAPI/SERPRO |
| 25 | Quadro societario completo do CNPJ (socios, participacao, data entrada) | Serasa | BrasilAPI/SERPRO/BasedosDados |
| 26 | CNAEs da empresa (atividade economica) | Serasa | BrasilAPI |
| 27 | Situacao do CAR (ativo/pendente/cancelado/suspenso) | Serasa, Agrotools | SICAR |
| 28 | Historico de alteracoes do CAR (timeline de perimetro) | Serasa | SICAR + MapBiomas |
| 29 | Validacao de confiabilidade do CAR (ScoreCAR) | Agrotools (IA) | Motor proprio |
| 30 | Dados do CCIR (Certificado de Cadastro de Imovel Rural) | Ninguem via API | SERPRO |
| 31 | Dados do SNCR/CAFIR (cadastro Receita Federal) | Registro Rural | InfoSimples/SERPRO |
| 32 | Cadeia dominial resumida (titulares anteriores) | Ninguem | ONR/cartorios (futuro) |
| 33 | Matricula(s) vinculada(s) ao imovel | Ninguem via API | ONR/InfoSimples |

### 2.2 Conformidade ambiental
| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 34 | Verificacao de embargos IBAMA ativos no imovel | Serasa, Agrotools, DadosFazenda | PostGIS (103k registros) |
| 35 | Historico completo de embargos IBAMA (ativos + inativos) | Serasa | IBAMA |
| 36 | Autos de infracao IBAMA vinculados ao CPF/CNPJ | Serasa | IBAMA/InfoSimples |
| 37 | Autos de infracao IBAMA por sobreposicao espacial | Agrotools | PostGIS |
| 38 | Verificacao de alertas DETER (desmatamento recente) no imovel | Serasa, Agrotools | PostGIS (100k alertas) |
| 39 | Verificacao PRODES (desmatamento anual consolidado) | Serasa, SpectraX | INPE WFS |
| 40 | Desmatamento pos-31/07/2019 (corte MCR 2.9) | Serasa, SpectraX | PRODES + motor |
| 41 | Desmatamento pos-31/12/2020 (corte EUDR) | SpectraX | PRODES + motor |
| 42 | Alertas MapBiomas validados com laudo tecnico | Ninguem via API | MapBiomas Alerta GraphQL |
| 43 | Area de APP preservada vs suprimida | Serasa | SICAR + MapBiomas |
| 44 | Reserva Legal adequada vs deficit | Serasa | SICAR + MapBiomas |
| 45 | Passivo ambiental calculado (hectares a restaurar) | Agrotools | SICAR + motor |
| 46 | Sobreposicao com Terras Indigenas | Serasa, Agrotools | PostGIS (655 TIs) |
| 47 | Sobreposicao com Unidades de Conservacao federais | Serasa, Agrotools | ICMBio WFS (~340 UCs) |
| 48 | Sobreposicao com UCs estaduais | Agrotools | Download manual |
| 49 | Sobreposicao com assentamentos INCRA | Agrotools | INCRA WMS |
| 50 | Sobreposicao com comunidades quilombolas | Agrotools | INCRA WMS |
| 51 | Sobreposicao com areas de mineracao (ANM/SIGMINE) | Ninguem | ANM FeatureServer |
| 52 | Sobreposicao com faixa de fronteira | Ninguem | ANM estrutura_territorial |
| 53 | Sobreposicao com areas militares | Ninguem | ANM informacao_militar |
| 54 | Sobreposicao com cavernas/patrimonio espeleologico | Ninguem | ANM geociencias |
| 55 | Sobreposicao com sitios paleontologicos | Ninguem | ANM geociencias |
| 56 | Sobreposicao com areas de protecao de manancial | Ninguem | ANA FeatureServer |
| 57 | Sobreposicao entre CAR e SIGEF (conflito fundiario) | Registro Rural, Agrotools | PostGIS |
| 58 | Sobreposicao entre imoveis vizinhos (conflito de limites) | Agrotools | PostGIS |
| 59 | Verificacao de queimadas/incendios no imovel | SpectraX | MapBiomas Fogo |
| 60 | Verificacao de degradacao florestal (EUDR) | SpectraX | MapBiomas Degradacao |
| 61 | Verificacao de autorizacao de supressao (SINAFLOR) | SpectraX | Nao disponivel via API |
| 62 | Bioma do imovel (Amazonia, Cerrado, Mata Atlantica, etc.) | Agrotools | IBGE/MapBiomas |
| 63 | Fitofisionomia/tipo de vegetacao original | Ninguem | MapBiomas LULC |
| 64 | Risco hidrico (outorgas de agua, bacia, escassez) | Ninguem | ANA FeatureServer + HidroWeb |
| 65 | Pivos de irrigacao no imovel ou arredores | Ninguem | ANA Pivos Mapeados |

### 2.3 Conformidade trabalhista
| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 66 | CPF/CNPJ na Lista Suja de trabalho escravo (MTE) | Serasa, Agrotools | PostGIS (614 registros) |
| 67 | Historico na Lista Suja (inclusao/exclusao) | Ninguem | MTE download semestral |
| 68 | CEIS — Cadastro de Empresas Inidoneas e Suspensas | Ninguem | Portal Transparencia API |
| 69 | CNEP — Cadastro de Empresas Punidas | Ninguem | Portal Transparencia API |
| 70 | Divida trabalhista ativa | Agrotools | InfoSimples |

### 2.4 Conformidade juridica
| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 71 | Processos judiciais por CPF/CNPJ (todos os tribunais) | Serasa (parcial) | DataJud (88 tribunais) |
| 72 | Processos ambientais (filtro por classe/assunto) | Ninguem | DataJud + filtro |
| 73 | Processos possessorios/fundiarios | Ninguem | DataJud + filtro |
| 74 | Processos trabalhistas rurais | Ninguem | DataJud TRTs |
| 75 | Processos tributarios (IPTR, ITR, execucoes fiscais) | Ninguem | DataJud + filtro |
| 76 | Protestos cartoriais contra CPF/CNPJ | Serasa | InfoSimples/CENPROT (R$0.06) |
| 77 | Divida ativa federal (PGFN) | Serasa | InfoSimples/SERPRO |
| 78 | Certidao negativa de debitos federais | Serasa | SERPRO CND |
| 79 | Certidao negativa estadual (SEFAZ) | Ninguem | InfoSimples por UF |
| 80 | Processos administrativos IBAMA/ICMBio (via SEI) | AdvLabs | Scraping SEI |
| 81 | Prescricao administrativa calculada | AdvLabs | Motor proprio |
| 82 | Prescricao criminal ambiental calculada | AdvLabs | Motor proprio |

### 2.5 Conformidade financeira
| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 83 | Historico de credito rural (financiamentos BCB/SICOR) | Serasa | BCB SICOR OData |
| 84 | Credito rural por municipio/cultura/programa | Ninguem (como feature publica) | BCB SICOR |
| 85 | CPR registradas (Cedulas de Produto Rural) | Serasa | CERC/B3/CRDC |
| 86 | SCR — endividamento no BCB | Serasa | BCB (acesso restrito) |
| 87 | Financiamentos BNDES ativos/liquidados | Serasa | Portal Transparencia |
| 88 | FIAGROs vinculados ao imovel/regiao | Ninguem | CVM dados abertos |

---

## 3. SCORES E CLASSIFICACOES

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 89 | **Score MCR 2.9** — APTO / INAPTO / PENDENTE com checklist auditavel | Serasa, SpectraX, Agrotools | Checklist: CAR ativo + sem PRODES pos-2019 + sem embargo + sem TI/UC + sem Lista Suja |
| 90 | **Score EUDR** — Conformado / Critico / Verificacao necessaria | SpectraX | Checklist: sem desmatamento pos-2020 + sem degradacao + rastreabilidade |
| 91 | **Score Fundiario** — 0-1000 com gauge visual | Ninguem (Serasa faz credito, nao fundiario) | Titulacao + litigiosidade + regularidade + sobreposicoes |
| 92 | **Score Ambiental** — 0-1000 | Serasa (parcial) | Embargos + DETER + PRODES + APP/RL + queimadas |
| 93 | **Score Trabalhista** — 0-1000 | Ninguem | Lista Suja + processos trabalhistas + CEIS |
| 94 | **Score Juridico** — 0-1000 | Ninguem | Volume de processos + tipos + gravidade + prescricao |
| 95 | **Score Financeiro** — 0-1000 | Serasa (Agro Score) | Protestos + divida ativa + credito rural + CPR |
| 96 | **Score Geral (Overall)** — semaforo visual | Serasa, Agrotools | Pior score entre os 5 eixos |
| 97 | **ScoreCAR** — confiabilidade do cadastro ambiental rural | Agrotools | IA: 10 criterios, 5 niveis |
| 98 | **Classificacao de urgencia** — CRITICO / URGENTE / PENDENTE / EM DIA / PARADO | Ninguem | Motor de prazos |
| 99 | **Semaforo visual** — verde/amarelo/vermelho por eixo de risco | Serasa, Agrotools | Thresholds configuraveis |
| 100 | **Tendencia do score** — melhorando/piorando nos ultimos 6 meses | Ninguem | Historico de scores |

---

## 4. MAPA INTERATIVO GIS

### 4.1 Camadas de dados
| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 101 | Embargos IBAMA (103k poligonos) | Serasa (mapa ESG) | PostGIS |
| 102 | DETER Amazonia (50k alertas) | Serasa, SpectraX | PostGIS |
| 103 | DETER Cerrado (50k alertas) | Ninguem como camada publica | PostGIS |
| 104 | PRODES desmatamento anual (todos os biomas) | SpectraX | INPE WFS |
| 105 | MapBiomas Cobertura e Uso da Terra 1985-2023 | Ninguem completo | GEE/GCS |
| 106 | MapBiomas Fogo (cicatrizes mensais) | Ninguem | GEE/download |
| 107 | MapBiomas Degradacao | Ninguem | GEE |
| 108 | MapBiomas Solo (carbono, textura) | Ninguem | GEE |
| 109 | MapBiomas Agua (superficies hidricas) | Ninguem | GEE |
| 110 | MapBiomas Credito Rural (5.6M parcelas) | Ninguem | PostGIS |
| 111 | Terras Indigenas FUNAI (655 poligonos) | Serasa, Agrotools | PostGIS |
| 112 | Unidades de Conservacao ICMBio (~340 UCs) | Agrotools | ICMBio WFS |
| 113 | Assentamentos INCRA | Agrotools | INCRA WMS |
| 114 | Comunidades quilombolas | Agrotools | INCRA WMS |
| 115 | Processos minerarios ANM/SIGMINE | Ninguem como camada | ANM FeatureServer |
| 116 | Armazens e silos (16k) | Ninguem como camada publica | PostGIS |
| 117 | Frigorificos (207) | Ninguem | PostGIS |
| 118 | Rodovias federais (14k trechos) | Ninguem | PostGIS |
| 119 | Ferrovias (2.2k trechos) | Ninguem | PostGIS |
| 120 | Portos (35) | Ninguem | PostGIS |
| 121 | Outorgas de agua ANA | Ninguem | ANA FeatureServer |
| 122 | Pivos de irrigacao mapeados | Ninguem | ANA FeatureServer |
| 123 | Estacoes meteorologicas INMET | Ninguem | INMET API |
| 124 | Poligonos do CAR por estado | Agrotools, Serasa | SICAR WFS |
| 125 | Parcelas SIGEF certificadas | Registro Rural | INCRA |
| 126 | Limites municipais/estaduais | Todos os GIS | IBGE malhas |
| 127 | Biomas brasileiros | Agrotools | IBGE/MapBiomas |
| 128 | Bacias hidrograficas | Ninguem | ANA |
| 129 | Zoneamento ecologico-economico | Ninguem | Estadual |
| 130 | Heatmap de risco por regiao (hexbin) | Ninguem | Motor proprio + Kepler pattern |
| 131 | Heatmap de valor da terra (R$/ha) | Ninguem | Motor proprio |
| 132 | Limites de cartorios de RI | ONR (visual) | ONR |

### 4.2 Funcoes do mapa
| # | Feature | Quem faz | Referencia |
|---|---|---|---|
| 133 | Click esquerdo — copiar coordenada | Todos os GIS | Leaflet |
| 134 | Click direito — analise de ponto completa | Ninguem | GEE Inspector |
| 135 | Shift+drag — bbox search (alertas na area) | Ninguem | Leaflet |
| 136 | Desenho de poligono — dispara relatorio M1 | Felt, GEE | Leaflet Draw |
| 137 | Pesquisa global (municipio, CAR, CPF, endereco) | DadosFazenda | Nominatim + SICAR |
| 138 | Timeline deslizante 1985-2023 (evolucao uso do solo) | GEE (code) | Kepler time slider |
| 139 | Comparacao antes/depois (split view) | Ninguem | Kepler split map |
| 140 | Toggle de camadas com checkbox | GEE, Kepler | Layer Manager |
| 141 | Slider de opacidade por camada | GEE, Kepler | Layer Manager |
| 142 | Legenda auto-gerada | Felt | Sync com zoom |
| 143 | Basemap switcher (satelite, topo, dark, light, OSM) | Todos | Leaflet tiles |
| 144 | Export PNG do mapa com legenda | GEE | html2canvas |
| 145 | Export KML/SHP das camadas ativas | GEE, Registro Rural | ogr2ogr |
| 146 | Medicao de area (ha) por poligono | GEE | Leaflet measure |
| 147 | Medicao de distancia (km) entre pontos | GEE | Leaflet measure |
| 148 | Popup com dados do elemento clicado (tabela/lista) | Felt | Leaflet popup |
| 149 | Data table linkada ao mapa (selecionar na tabela destaca no mapa) | Felt, Kepler | React state |
| 150 | Zoom to feature (centralizar mapa num imovel) | Todos | Leaflet flyTo |
| 151 | Street View integrado | ONR | Google Street View embed |
| 152 | Imagem de satelite de alta resolucao do imovel | Serasa, SpectraX | Esri/Google tiles |
| 153 | Buffer visual (raio ao redor de ponto/imovel) | ANM query | PostGIS ST_Buffer |
| 154 | Clusterizacao de pontos em zoom baixo | Kepler | Leaflet MarkerCluster |

---

## 5. MONITORAMENTO E ALERTAS

| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 155 | Alerta de novo embargo IBAMA no imovel monitorado | Serasa Smart ESG | Cron + PostGIS |
| 156 | Alerta de novo alerta DETER no imovel | Serasa Smart ESG | Cron + INPE WFS |
| 157 | Alerta de PRODES anual (desmatamento consolidado) | SpectraX | Cron + INPE |
| 158 | Alerta de queimada/foco de calor no imovel | Ninguem | MapBiomas Fogo / INPE BDQueimadas |
| 159 | Alerta de proprietario incluido na Lista Suja MTE | Serasa Smart ESG | Cron + MTE CSV |
| 160 | Alerta de novo processo judicial contra proprietario | Ninguem | Cron + DataJud |
| 161 | Alerta de movimentacao em processo existente | AdvLabs | Cron + DataJud |
| 162 | Alerta de novo auto de infracao IBAMA | AdvLabs | Cron + IBAMA |
| 163 | Alerta de movimentacao em processo admin IBAMA (SEI) | AdvLabs | Scraping SEI |
| 164 | Alerta de alteracao no CAR (perimetro/status) | Serasa | Cron + SICAR |
| 165 | Alerta de novo processo minerario sobrepondo imovel | Ninguem | Cron + ANM |
| 166 | Alerta de publicacao no DOU relevante (portarias, INs) | Ninguem | Ro-DOU |
| 167 | Alerta de vencimento de prazo processual | AdvLabs | Motor de prazos |
| 168 | Alerta de prescricao iminente | AdvLabs | Motor de prescricao |
| 169 | Alerta de variacao brusca de cotacao de commodity | Ninguem | agrobr + threshold |
| 170 | Alerta de novo FIAGRO afetando regiao | Ninguem | CVM + cron |
| 171 | Alerta de mudanca na taxa SELIC/CDI (impacta credito rural) | Ninguem | BCB API |
| 172 | Alerta de publicacao de novo ZARC (janela de plantio) | Ninguem | MAPA CKAN + cron |
| 173 | Monitoramento de carteira inteira (banco/cooperativa) | Serasa Smart ESG | Batch + cron |
| 174 | Protocolos de monitoramento configuraveis (regras custom) | Serasa Smart ESG | Engine de regras |
| 175 | Webhook para sistemas externos (ERP, CRM do banco) | Ninguem | FastAPI webhook |
| 176 | Notificacao via email | Serasa, AdvLabs | SMTP |
| 177 | Notificacao via push (mobile/browser) | Ninguem | Web Push API |
| 178 | Notificacao via WhatsApp | Ninguem (Agrolend para credito) | WhatsApp Business API |
| 179 | Dashboard de alertas com timeline | AdvLabs | React + chart |
| 180 | Filtro de alertas por tipo/gravidade/periodo | Ninguem | UI filter |

---

## 6. INTELIGENCIA DE MERCADO E DADOS ECONOMICOS

| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 181 | Cotacoes de commodities Brasil (CEPEA/ESALQ) — boi, soja, milho, cafe, etc. | Agrolink, Noticias Agricolas | agrobr (20 indicadores) |
| 182 | Cotacoes internacionais (CBOT/CME) — futuros soja, milho, trigo, boi | Noticias Agricolas | agrobr + yfinance |
| 183 | Futuros B3 — boi gordo, milho, cafe, etanol, acucar | Ninguem como SaaS | agrobr |
| 184 | Cotacao do dolar (PTAX) em tempo real | Noticias Agricolas | BCB API / BrasilAPI |
| 185 | Taxa SELIC, CDI, IPCA atualizados | Ninguem no contexto agro | BCB API / BrasilAPI |
| 186 | Graficos historicos de precos (1 ano, 5 anos, max) | Agrolink, Noticias Agricolas | agrobr + chart |
| 187 | Comparacao de precos entre pracas regionais | Canal Rural | agrobr CEPEA |
| 188 | Custo de producao por cultura/regiao | Ninguem | CONAB (scraping) |
| 189 | Producao agricola municipal (PAM) — area, producao, rendimento | Ninguem como feature | IBGE SIDRA |
| 190 | Producao pecuaria municipal (PPM) — rebanhos por tipo | Ninguem como feature | IBGE SIDRA |
| 191 | Estimativas de safra (CONAB) | Ninguem como API | CONAB + agrobr |
| 192 | Volume de credito rural por municipio/cultura | Ninguem | BCB SICOR OData |
| 193 | FIAGROs listados — patrimonio, rentabilidade, carteira | Ninguem | CVM dados abertos |
| 194 | Producao/demanda global (USDA PSD) — Brasil vs competidores | Ninguem | USDA API |
| 195 | WASDE mensal (oferta/demanda mundial) | Ninguem | USDA API |
| 196 | Exportacoes agro Brasil (ComexStat) | Ninguem | agrobr |
| 197 | Previsao de preco de commodities (modelo) | Ninguem | ML sobre historico |
| 198 | Indice de precos ao produtor (IPPA CEPEA) | Ninguem | agrobr |
| 199 | Feed de noticias agro (5+ RSS) | Ninguem consolidado | Canal Rural + AgFeed + Portal Agro |
| 200 | Feed de noticias filtrado por commodity/regiao | Ninguem | NLP sobre RSS |
| 201 | Feed de noticias juridico-agro | Ninguem | Portal Agronegocio secao juridica |

---

## 7. CLIMA E AGRONOMIA

| # | Feature | Quem faz | Fonte |
|---|---|---|---|
| 202 | Clima historico por coordenada (40+ anos) | SpectraX (FarmGuide) | NASA POWER |
| 203 | Clima atual da estacao mais proxima | Ninguem como feature | INMET API (inmetpy) |
| 204 | Previsao do tempo 5-15 dias por municipio | Canal Rural | BrasilAPI CPTEC |
| 205 | Temperatura, chuva, radiacao, umidade, vento | SpectraX | NASA POWER + INMET |
| 206 | Umidade do solo na zona da raiz | Ninguem | NASA POWER GWETROOT |
| 207 | Evapotranspiracao | Ninguem | NASA POWER EVPTRNS |
| 208 | Indice de vegetacao NDVI/EVI temporal | SpectraX | Embrapa SATVeg API |
| 209 | Zoneamento de risco climatico ZARC (por cultura/municipio/solo) | Serasa (MCR), SpectraX | Embrapa Agritec API |
| 210 | Calendario agricola por cultura e estado | Ninguem como feature | Embrapa Agritec + MAPA |
| 211 | Verificacao se plantio esta dentro da janela ZARC | Serasa (MCR compliance) | Embrapa Agritec |
| 212 | Dados de solo (carbono organico, textura, aptidao) | Ninguem | Embrapa GeoInfo WFS + MapBiomas Solo |
| 213 | Agrotoxicos registrados para cada cultura | Ninguem | Embrapa AGROFIT API |
| 214 | Bioinsumos disponiveis | Ninguem | Embrapa Bioinsumos API |
| 215 | Rastreabilidade bovina | Ninguem | Embrapa BovTrace API |
| 216 | Sugestao de cultura por solo/bioma/clima | Ninguem | Motor proprio (ZARC + Solo + PAM) |
| 217 | Risco de geada/seca/inundacao por regiao | SpectraX | NASA + INMET historico |

---

## 8. VALUATION E ANALISE ECONOMICA

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 218 | Estimativa de valor R$/ha do imovel com intervalo de confianca | Ninguem | ML: PAM + solo + bioma + infra + cotacoes + riscos |
| 219 | Comparaveis por municipio (media R$/ha) | Ninguem | IBGE SIDRA + MapBiomas |
| 220 | Comparaveis por bioma/estado | Ninguem | Idem |
| 221 | Fatores positivos (solo, irrigacao, proximidade infra) | Ninguem | Motor proprio |
| 222 | Fatores negativos (embargos, sobreposicoes, processos) | Ninguem | Motor proprio |
| 223 | Analise de distancia logistica (km ate silo, porto, rodovia, ferrovia, frigorifico) | Ninguem | PostGIS ST_Distance |
| 224 | Custo logistico estimado (frete por km) | Ninguem | Tabela ANTT + distancias |
| 225 | Potencial de credito de carbono | SpectraX (em breve) | MapBiomas Solo + vegetacao |
| 226 | Potencial de expansao agricola (area nao utilizada) | Ninguem | MapBiomas LULC |
| 227 | Simulador de viabilidade economica (custo producao vs preco venda vs area) | Ninguem | Motor proprio |
| 228 | Calculadora de ROI para investimento em terra | Agrotools (publica) | Motor proprio |

---

## 9. INTELIGENCIA JURIDICA E TESES

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 229 | Diagnostico automatico de teses de defesa por IA | AdvLabs (ambiental) | LLM + base de teses |
| 230 | Teses ambientais (APP, desmatamento, floresta, queimada, pesca, poluicao) | AdvLabs (128 teses) | Base catalogada |
| 231 | Teses agrarias (possessorias, usucapiao, desapropriacao, reforma agraria) | Ninguem | Base propria |
| 232 | Teses tributarias rurais (ITR, IPTR, imunidade, isencao) | Ninguem | Base propria |
| 233 | Teses de credito rural (nulidade, revisional, vicio de consentimento) | Ninguem | Base propria |
| 234 | Teses civis rurais (contratos agrarios, arrendamento, parceria) | Ninguem | Base propria |
| 235 | Calculadora de prescricao administrativa (IBAMA) | AdvLabs | Motor proprio |
| 236 | Calculadora de prescricao criminal ambiental | AdvLabs | Motor proprio |
| 237 | Calculadora de prescricao civil (usucapiao, possessorias) | Ninguem | Motor proprio |
| 238 | Calculadora de multa IBAMA (dosimetria) | Ninguem | Decreto 6.514/08 |
| 239 | Pesquisa de jurisprudencia por tema/tribunal | Ninguem | DataJud + NLP |
| 240 | Modelos de peticoes editaveis (Word/DOCX) | AdvLabs (900+ ambientais) | Base propria |
| 241 | Modelos de contratos agrarios (arrendamento, parceria, compra/venda) | Ninguem | Base propria |
| 242 | Gerador de parecer tecnico-juridico | Ninguem | LLM + dados do relatorio |
| 243 | Gerador de defesa administrativa IBAMA | AdvLabs | LLM + teses |
| 244 | Gerador de contestacao/recurso | Ninguem | LLM + teses |
| 245 | Sugestao de pedidos (causa de pedir + pedido) com fundamentacao | Ninguem | LLM + teses |
| 246 | Arvore de decisao por tipo de caso | Ninguem | Motor proprio |

---

## 10. GESTAO E CRM

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 247 | Cadastro de clientes (CPF/CNPJ, contato, imoveis vinculados) | AdvLabs | CRUD |
| 248 | Cadastro de casos/processos | AdvLabs | CRUD |
| 249 | Kanban de tarefas por caso | AdvLabs | Board |
| 250 | Gestao de prazos com alertas | AdvLabs | Motor de prazos |
| 251 | Calendario de audiencias/diligencias | Ninguem | Calendar |
| 252 | Timeline de atividades por caso | Ninguem | Log |
| 253 | Arquivo digital de documentos por caso | Ninguem | Storage |
| 254 | Agenda financeira (honorarios, custas, parcelas) | Ninguem | CRUD |
| 255 | Dashboard do escritorio (casos ativos, prazos, faturamento) | Ninguem | Agregacoes |
| 256 | Multi-usuario com permissoes (advogado, estagiario, cliente) | Ninguem | RBAC |
| 257 | Portal do cliente (view-only do caso) | Ninguem | Auth + views |
| 258 | Integracao com formulario do site (captura de leads) | AdvLabs | Webhook |

---

## 11. PROSPECCAO E MARKETING

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 259 | Radar de prospeccao — detectar autuados IBAMA num raio do escritorio | AdvLabs | Cron + PostGIS |
| 260 | Radar de processos — detectar novos processos rurais na comarca | Ninguem | Cron + DataJud |
| 261 | Radar de embargos — detectar novos embargos por regiao | Ninguem | Cron + PostGIS |
| 262 | Radar de oportunidades — imoveis com CAR pendente/suspenso | Ninguem | SICAR + motor |
| 263 | Lista de leads qualificados (proprietarios com problemas detectados) | AdvLabs | Motor + CNPJ |
| 264 | Newsletter automatica juridico-agro | Ninguem | RSS + curadoria |
| 265 | Boletim periodico com dados do mercado | Serasa (Boletim Agro) | agrobr + template |

---

## 12. EXPORT E RELATORIOS

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 266 | Relatorio PDF profissional (due diligence completa) | Serasa, SpectraX, Agrotools, Registro Rural | WeasyPrint |
| 267 | Relatorio PDF resumido (semaforo + highlights) | Serasa | WeasyPrint |
| 268 | Relatorio JSON (para integracao via API) | Ninguem | FastAPI |
| 269 | Relatorio Excel (tabular com abas por secao) | Ninguem | openpyxl |
| 270 | Relatorio KML/SHP (geometrias + dados) | Registro Rural | ogr2ogr |
| 271 | Validador de relatorio por codigo unico | SpectraX | UUID + assinatura digital |
| 272 | QR Code no relatorio que linka para versao digital | Ninguem | qrcode lib |
| 273 | Marca d'agua com data/hora de emissao | SpectraX | WeasyPrint |
| 274 | Relatorio com formulario de finalidade (LGPD) | SpectraX | Form pre-emissao |
| 275 | Relatorio comparativo entre 2+ imoveis | Ninguem | Motor proprio |
| 276 | Relatorio de evolucao temporal (mesmo imovel, 2 datas) | Ninguem | Motor proprio |
| 277 | Relatorio de carteira (portfolio de N imoveis) | Serasa | Batch + agregacao |
| 278 | Export de mapa em PNG com legenda e camadas | Ninguem | html2canvas/Leaflet |
| 279 | Historico de relatorios emitidos por conta | Ninguem | Log |

---

## 13. API E INTEGRACAO

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 280 | API REST documentada (OpenAPI/Swagger) | Registro Rural, Serasa | FastAPI auto-docs |
| 281 | Postman Collection publica | Registro Rural, Serasa | Postman |
| 282 | SDKs (Python, JavaScript, Java) | Ninguem agro | Codegen |
| 283 | Webhook de alertas para sistemas externos | Ninguem | FastAPI |
| 284 | Widget embarcavel para sites de terceiros | CEPEA (cotacoes) | iframe/JS |
| 285 | API de consulta batch (N imoveis por request) | Ninguem | Async batch |
| 286 | API de monitoramento (registrar e cancelar alertas) | Serasa Smart ESG | CRUD |
| 287 | API de score (retorna score MCR/EUDR/fundiario) | Serasa | Motor |
| 288 | API de mapa (tiles, WFS, WMS proprio) | Ninguem | GeoServer ou PostGIS |
| 289 | API de relatorio (gerar + download PDF/JSON) | Ninguem | Async + storage |
| 290 | Rate limiting por plano (free/pro/enterprise) | Todos os SaaS | FastAPI middleware |
| 291 | Dashboard de uso da API (requests, erros, latencia) | Serasa Developer Portal | Admin panel |
| 292 | Sandbox/ambiente de teste com dados fictícios | Ninguem agro | Fixture |

---

## 14. AUTENTICACAO, PLANOS E MONETIZACAO

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 293 | Login com email/senha | Todos | JWT |
| 294 | Login com Google/Gov.br | Ninguem agro | OAuth2 |
| 295 | Trial gratuito 7 dias (acesso completo) | AdvLabs | Flag temporal |
| 296 | Plano gratuito limitado (3 consultas/mes) | Ninguem | Rate limit |
| 297 | Plano individual (R$149-299/mes) | Registro Rural | Stripe/Asaas |
| 298 | Plano profissional (R$699-1.490/mes) | Ninguem | Stripe/Asaas |
| 299 | Plano enterprise (R$5k-50k/mes, API ilimitada) | Serasa, Agrotools | Contrato |
| 300 | Consulta avulsa (R$89-299/relatorio) | Ninguem | Creditos |
| 301 | Sistema de creditos (comprar pacote, debitar por uso) | Registro Rural, AdvLabs | Wallet |
| 302 | API B2B por imovel (R$2-15/consulta) | Ninguem | Metering |
| 303 | White-label (banco/cooperativa usa com marca propria) | Agrotools, Serasa | Multi-tenant |
| 304 | Programa de parceiros/afiliados | Docket | Referral |

---

## 15. UX E EXPERIENCIA

| # | Feature | Quem faz | Referencia |
|---|---|---|---|
| 305 | Dark mode como default (Forest/Onyx) | Ninguem agro | Linear, Kepler |
| 306 | Light mode como alternativa | Todos | Toggle |
| 307 | Command Palette (Cmd+K) — busca global | Ninguem agro | Linear |
| 308 | Slash commands (/analise, /camadas, /risco) | Ninguem | Notion |
| 309 | Keyboard shortcuts para power users | Ninguem agro | Linear |
| 310 | Sidebar colapsavel | Stripe, Vercel, Linear | Layout |
| 311 | Breadcrumbs de navegacao | Ninguem agro | Notion |
| 312 | Skeleton loading states | Best practice | UX |
| 313 | Empty states com CTA | Notion | Onboarding |
| 314 | Templates de analise predefinidos | Ninguem | Notion pattern |
| 315 | Onboarding wizard (3 passos) | Ninguem agro | UX |
| 316 | Dados de exemplo para explorar antes de subir proprios | Ninguem | UX |
| 317 | Responsivo mobile (bottom bar flutuante) | Ninguem agro | Vercel |
| 318 | PWA (Progressive Web App) — funciona offline parcial | Ninguem agro | Service Worker |
| 319 | Favicon status (cor muda com alertas criticos) | Ninguem | Vercel |
| 320 | SWR real-time (dados atualizam sem refresh) | Ninguem agro | Vercel |
| 321 | Consulta via WhatsApp (chatbot) | DadosFazenda, Agrolend | WhatsApp Business API |
| 322 | Chat em linguagem natural (consulta LLM) | Ninguem agro | LLM integration |
| 323 | Modo de apresentacao (para mostrar a cliente/juiz) | Ninguem | Fullscreen clean |
| 324 | Colaboracao multi-usuario (ver quem esta online) | Felt | Presence |
| 325 | Favoritos/salvos (imoveis, consultas, relatorios) | DadosFazenda | CRUD |
| 326 | Historico de buscas recentes | Ninguem | Local storage |

---

## 16. CONTEUDO E EDUCACAO

| # | Feature | Quem faz | Motor |
|---|---|---|---|
| 327 | Blog juridico-agro | AdvLabs, Serasa | CMS |
| 328 | Newsletter semanal com curadoria | Serasa (Boletim Agro) | Email + RSS |
| 329 | Biblioteca de modelos editaveis (peticoes, contratos) | AdvLabs (900+) | Download DOCX |
| 330 | Glossario juridico-agro interativo | AdvLabs | Embrapa AgroTermos API |
| 331 | Cursos online (basico/intermediario/avancado) | AdvLabs | Video + quiz |
| 332 | Webinars com especialistas | AdvLabs, Serasa | Calendar + live |
| 333 | Comunidade/forum de discussao | AdvLabs | Forum |
| 334 | Base de conhecimento (FAQ tecnica) | Ninguem | Docs |
| 335 | Calculadora publica de ROI agro (lead gen) | Agrotools | Motor + form |
| 336 | Mapa publico interativo (versao limitada gratuita) | Ninguem | Marketing |

---

## TOTAL: 336 FEATURES CATALOGADAS

### Resumo por categoria:

| Categoria | Qtd | Ninguem faz | AgroJus unico |
|---|---|---|---|
| 1. Consulta e identificacao | 22 | 4 | Busca por processo judicial, auto IBAMA |
| 2. Relatorio de conformidade | 60 | 22 | Sobreposicao mineracao/cavernas/manancial, prescricao, CCIR |
| 3. Scores e classificacoes | 12 | 6 | Score Fundiario, Score Trabalhista, Score Juridico, tendencia |
| 4. Mapa GIS | 54 | 28 | DETER Cerrado, MapBiomas completo, credito rural, ANM, ANA |
| 5. Monitoramento e alertas | 26 | 14 | DOU, DataJud, ANM, FIAGRO, ZARC, WhatsApp |
| 6. Mercado e dados economicos | 21 | 15 | Futuros B3, SICOR municipal, FIAGROs, USDA, ComexStat |
| 7. Clima e agronomia | 16 | 12 | Solo, agrotoxicos, bioinsumos, BovTrace, sugestao de cultura |
| 8. Valuation | 11 | 11 | Todas (ninguem faz valuation aberto) |
| 9. Inteligencia juridica | 18 | 12 | Teses agrarias/tributarias/civis, dosimetria multa, geradores |
| 10. Gestao e CRM | 12 | 8 | Portal do cliente, multi-usuario, calendario |
| 11. Prospeccao | 7 | 5 | Radar processos, radar embargos, radar CAR pendente |
| 12. Export e relatorios | 14 | 10 | Comparativo, evolucao temporal, QR code, carteira |
| 13. API e integracao | 13 | 8 | SDKs, batch, tiles proprio, sandbox |
| 14. Auth e monetizacao | 12 | 5 | Trial, creditos, B2B metering, white-label |
| 15. UX e experiencia | 22 | 18 | Dark mode agro, Cmd+K, WhatsApp, PWA, favicon status |
| 16. Conteudo e educacao | 10 | 5 | Glossario interativo, mapa publico, calculadora ROI |
| **TOTAL** | **336** | **~183** | |

> **183 features que NINGUEM faz** e que AgroJus pode fazer primeiro.

---

*AgroJus — Inventario de Features v1.0 — 336 features — 2026-04-15*
