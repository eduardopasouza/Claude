# Fontes de Dados — AgroJus

Referência completa de todas as fontes de dados públicos utilizadas pela plataforma, com URLs, métodos de acesso e status de implementação.

---

## 1. Dados Fundiários

### SICAR / CAR (Cadastro Ambiental Rural)
- **O que é**: Registro público eletrônico nacional obrigatório para imóveis rurais
- **Dados**: Perímetro do imóvel, APP, Reserva Legal, uso consolidado, remanescente
- **Acesso**: WFS (geoserviço) + consulta pública web
- **URLs**:
  - Consulta pública: `https://consultapublica.car.gov.br/publico/imoveis/index`
  - GeoServer WFS: `https://car.gov.br/geoserver/wfs`
  - Download por município: disponível no SICAR
- **Formato**: GeoJSON (via WFS), Shapefile (download)
- **Status no AgroJus**: ✅ Implementado (`collectors/sicar.py`)

### SIGEF / INCRA (Sistema de Gestão Fundiária)
- **O que é**: Sistema de certificação de imóveis rurais do INCRA
- **Dados**: Parcelas certificadas, coordenadas georreferenciadas, responsável técnico
- **Acesso**: WFS do Acervo Fundiário
- **URLs**:
  - Acervo Fundiário: `https://acervofundiario.incra.gov.br/`
  - WFS: `https://acervofundiario.incra.gov.br/geoserver/wfs`
  - API: `https://sigef.incra.gov.br/api/v1/`
- **Formato**: GeoJSON, WMS/WFS (padrão OGC)
- **Status no AgroJus**: ✅ Implementado (`collectors/sigef.py`)

### SNCR / INCRA (Sistema Nacional de Cadastro Rural)
- **O que é**: Cadastro de imóveis rurais do INCRA
- **Dados**: Código SNCR, NIRF, classificação do imóvel, módulos fiscais, CCIR
- **Acesso**: Portal Gov.br (requer conta nível Prata+)
- **URLs**:
  - CNIR: `https://cnir.serpro.gov.br/`
  - SNCR/DCR: `https://sncr.serpro.gov.br/dcr/`
- **Status no AgroJus**: 🔲 Placeholder (requer autenticação Gov.br)

### CAFIR / Receita Federal
- **O que é**: Cadastro de imóveis rurais da Receita Federal
- **Dados**: NIRF, dados fiscais do imóvel, ITR
- **Acesso**: Dados abertos + consulta via Gov.br
- **URLs**:
  - Dados abertos: `https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/portal-cnir/estatisticas-e-dados-abertos`
- **Status no AgroJus**: 🔲 Placeholder

### Cartórios de Registro de Imóveis / ONR
- **O que é**: Registro oficial de propriedade imobiliária
- **Dados**: Matrícula, proprietário, ônus/gravames, averbações
- **Acesso**: Via ONR (convênio) ou scraping de sistemas de cartórios
- **URLs**:
  - Mapa ONR: `https://mapa.onr.org.br/`
  - RI Digital: `https://ridigital.org.br/`
- **Status no AgroJus**: 🔲 Em desenvolvimento (requer convênio ou scraping)

---

## 2. Dados Ambientais

### IBAMA (Embargos e Autuações)
- **O que é**: Áreas embargadas e autos de infração ambiental
- **Dados**: CPF/CNPJ autuado, município, área embargada, tipo de infração
- **Acesso**: Dados abertos CSV
- **URLs**:
  - Embargos: `https://dadosabertos.ibama.gov.br/dados/SICAFI/embargo/Embargo.csv`
  - Autuações: `https://dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/Autuacao.csv`
- **Formato**: CSV (delimitador `;`)
- **Status no AgroJus**: ✅ Implementado (`collectors/ibama.py`)

### FUNAI (Terras Indígenas)
- **O que é**: Limites de terras indígenas demarcadas
- **Dados**: Polígonos, nome da TI, etnia, fase de demarcação
- **Acesso**: Download de shapefile
- **URLs**:
  - Download: `https://www.gov.br/funai/pt-br/atuacao/terras-indigenas/geoprocessamento-e-mapas`
- **Formato**: Shapefile
- **Status no AgroJus**: ✅ Suportado (importação manual de shapefile)

### ICMBio (Unidades de Conservação)
- **O que é**: Limites de UCs federais e estaduais
- **Dados**: Polígonos, nome, categoria (PI, US), esfera
- **Acesso**: Download de shapefile
- **URLs**:
  - CNUC: `https://www.gov.br/icmbio/pt-br/servicos/geoprocessamento/mapa-tematico-e-dados-geoestatisticos-das-unidades-de-conservacao`
- **Formato**: Shapefile
- **Status no AgroJus**: ✅ Suportado (importação manual de shapefile)

### INPE / PRODES (Desmatamento)
- **O que é**: Monitoramento de desmatamento na Amazônia Legal e Cerrado
- **Dados**: Polígonos de desmatamento, ano, área
- **Acesso**: Download + geoserviços
- **URLs**:
  - TerraBrasilis: `http://terrabrasilis.dpi.inpe.br/`
- **Formato**: Shapefile, GeoJSON, WMS
- **Status no AgroJus**: 🔲 Pendente

### INPE / DETER (Alertas de Desmatamento)
- **O que é**: Alertas de desmatamento em tempo quase-real
- **Dados**: Polígonos de alertas recentes
- **Acesso**: Geoserviços
- **URLs**:
  - TerraBrasilis: `http://terrabrasilis.dpi.inpe.br/`
- **Status no AgroJus**: 🔲 Pendente

### MapBiomas
- **O que é**: Mapeamento anual de uso e cobertura do solo do Brasil
- **Dados**: Série histórica de uso do solo (1985-presente)
- **Acesso**: Downloads + geoserviços
- **URLs**:
  - Plataforma: `https://plataforma.brasil.mapbiomas.org/`
- **Status no AgroJus**: 🔲 Pendente

---

## 3. Dados Jurídicos

### Receita Federal (CNPJ)
- **O que é**: Cadastro nacional de pessoas jurídicas
- **Dados**: Razão social, situação cadastral, CNAE, sócios, endereço, capital social
- **Acesso**: API pública gratuita (BrasilAPI)
- **URLs**:
  - BrasilAPI: `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`
  - ReceitaWS: `https://www.receitaws.com.br/v1/cnpj/{cnpj}` (alternativa)
- **Formato**: JSON
- **Status no AgroJus**: ✅ Implementado (`collectors/receita_federal.py`)

### Lista Suja do Trabalho Escravo (MTE)
- **O que é**: Cadastro de empregadores que submeteram trabalhadores a condições análogas à escravidão
- **Dados**: Nome, CPF/CNPJ, município, trabalhadores resgatados, data
- **Acesso**: Download do Portal da Transparência
- **URLs**:
  - Portal: `https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo`
- **Formato**: CSV
- **Status no AgroJus**: ✅ Implementado (`collectors/slave_labour.py`)

### Tribunais Estaduais (TJ)
- **O que é**: Processos cíveis estaduais
- **Dados**: Número do processo, partes, tipo, valor, status
- **Acesso**: Consulta pública web (scraping por UF)
- **Status no AgroJus**: 🔲 Em desenvolvimento

### Justiça Federal (TRFs)
- **O que é**: Processos federais (execuções fiscais, ações ambientais)
- **Acesso**: PJe (consulta pública)
- **Status no AgroJus**: 🔲 Em desenvolvimento

### TST / CNDT
- **O que é**: Certidão Negativa de Débitos Trabalhistas
- **Acesso**: Consulta pública web
- **URLs**: `https://www.tst.jus.br/certidao`
- **Status no AgroJus**: 🔲 Em desenvolvimento

### CND Federal
- **O que é**: Certidão de Débitos relativos a Créditos Tributários Federais
- **Acesso**: Consulta pública web
- **Status no AgroJus**: 🔲 Em desenvolvimento

---

## 4. Dados de Mercado e Financeiros

### SICOR / BCB (Crédito Rural)
- **O que é**: Sistema de Operações do Crédito Rural do Banco Central
- **Dados**: Volume de crédito por município, banco, programa, finalidade, cultura
- **Acesso**: API OData pública
- **URLs**:
  - API: `https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata`
- **Formato**: JSON (OData)
- **Status no AgroJus**: ✅ Implementado (`collectors/financial.py`)

### IBGE / SIDRA (Produção Agrícola Municipal)
- **O que é**: Dados do PAM (Produção Agrícola Municipal)
- **Dados**: Produção, área plantada, rendimento por cultura e município
- **Acesso**: API SIDRA pública
- **URLs**:
  - API: `https://apisidra.ibge.gov.br/values/`
  - Tabela 5457: produção, área, rendimento
- **Formato**: JSON
- **Status no AgroJus**: ✅ Implementado (`collectors/market_data.py`)

### CEPEA / ESALQ (Cotações)
- **O que é**: Indicadores de preços agropecuários
- **Dados**: Preços diários de soja, milho, boi gordo, café, algodão, etc.
- **Acesso**: Scraping do site (sem API pública oficial)
- **URLs**: `https://www.cepea.esalq.usp.br/br/indicador/`
- **Status no AgroJus**: 🔲 Placeholder (requer scraping)

### CONAB (Safras)
- **O que é**: Acompanhamento de safras brasileiras
- **Dados**: Área plantada, produtividade, produção por estado e cultura
- **Acesso**: Downloads do portal de informações
- **URLs**:
  - Portal: `https://portaldeinformacoes.conab.gov.br/`
  - Dados abertos: `https://dados.agricultura.gov.br/`
- **Status no AgroJus**: 🔲 Placeholder

### CVM (FIAGRO)
- **O que é**: Fundos de investimento nas cadeias produtivas agroindustriais
- **Dados**: Fundos, patrimônio, rendimento
- **Acesso**: Dados abertos CVM
- **URLs**: `https://dados.cvm.gov.br/`
- **Status no AgroJus**: 🔲 Placeholder

---

## 5. Notícias do Agronegócio (RSS)

| Portal | Feed RSS | Status |
|--------|----------|--------|
| Agrolink | `https://www.agrolink.com.br/rss/noticias.xml` | ✅ |
| Canal Rural | `https://www.canalrural.com.br/feed/` | ✅ |
| Notícias Agrícolas | `https://www.noticiasagricolas.com.br/rss/noticias.xml` | ✅ |
| Embrapa | `https://www.embrapa.br/rss/ultimas-noticias.xml` | ✅ |
| Portal do Agronegócio | `https://www.portaldoagronegocio.com.br/feed` | ✅ |

Classificação automática em categorias: `jurídico`, `mercado`, `geral`.

---

## Considerações Legais (LGPD)

1. **Dados de imóveis** (coordenadas, áreas, matrículas): não são dados pessoais
2. **Dados de proprietários** (CPF/CNPJ): são dados pessoais — requer base legal
3. **Base legal recomendada**: Legítimo interesse (LGPD art. 7, IX)
4. **Scraping de sites governamentais**: permitido se respeitar termos de uso e rate limiting
5. **Priorizar sempre**: APIs oficiais e dados abertos antes de scraping
