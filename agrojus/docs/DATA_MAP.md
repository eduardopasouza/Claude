# Mapa Completo de Dados Públicos Acessíveis — AgroJus

Este documento mapeia **exaustivamente** todas as fontes de dados públicos
que podemos acessar, quais campos servem como chave de busca, o que retorna,
como acessar, e como tudo se conecta.

---

## COMO TUDO SE CONECTA (Grafo de Identificadores)

O cliente pode entrar com QUALQUER dado. Cada dado puxa outros:

```
NOME DO PROPRIETÁRIO
  └→ busca textual em CNPJ (BrasilAPI), IBAMA (CSV), Lista Suja (CSV)

CPF/CNPJ
  ├→ Receita Federal → razão social, sócios, CNAE, endereço
  ├→ IBAMA embargos → autos de infração vinculados
  ├→ Lista Suja → registros de trabalho escravo
  ├→ DataJud/CNJ → processos judiciais
  ├→ Portal Transparência → sanções (CEIS, CEPIM, CNEP)
  ├→ PGFN → dívida ativa da União (dados abertos CSV)
  ├→ CENPROT → protestos em cartório (nacional)
  ├→ TST → CNDT (certidão trabalhista)
  ├→ ANM → processos minerários do titular
  └→ SICOR/BCB → crédito rural (agregado por município)

CÓDIGO CAR
  ├→ SICAR → perímetro, área, APP, RL, status, município, UF
  ├→ SICAR WFS → geometria (polígono) do imóvel
  ├→ Com geometria → sobreposição com TI, UC, embargo, desmatamento
  └→ MapBiomas Alerta → alertas de desmatamento no CAR

CÓDIGO SIGEF / PARCELA
  ├→ SIGEF/INCRA → parcela certificada, área, RT, data certificação
  └→ Acervo Fundiário WFS → geometria da parcela

COORDENADAS (LAT/LON)
  ├→ SIGEF WFS → parcelas próximas (bounding box)
  ├→ SICAR WFS → imóveis na área
  ├→ ANM/SIGMINE → processos minerários na área
  ├→ ANA → outorgas de água na área
  ├→ SPU → imóveis da União na área
  └→ PostGIS → sobreposição com todas as camadas importadas

MATRÍCULA (nº do cartório)
  └→ ❌ Sem API pública. Precisa: ONR/cartório (convênio ou scraping)

SNCR / NIRF / CCIR
  └→ ❌ Sem API pública aberta. CNIR requer Gov.br Prata+.
      CAFIR tem dados abertos agregados mas não por imóvel.

Nº AUTO DE INFRAÇÃO IBAMA
  └→ IBAMA API → detalhes do embargo (geometria WKT inclusa!)
      URL: corpgateway-api.ibama.gov.br/sicafiservicecorp/api/v1/public/
           termo/consultar/embargos/wkt?seqTad={numero}

PROCESSO MINERÁRIO (ANM)
  └→ ANM/Cadastro Mineiro → titular, substância, fase, área, município
      Consulta: sistemas.anm.gov.br/SCM/Extra/site/admin/pesquisarProcessos.aspx
      Dados abertos: shapefiles SIGMINE (polígonos dos processos)

OUTORGA DE ÁGUA (ANA)
  └→ ANA dados abertos → titular, finalidade, vazão, coordenadas
      GeoServer: dadosabertos.ana.gov.br

MUNICÍPIO (nome ou código IBGE)
  ├→ IBGE/SIDRA → produção agrícola, censo agro, população
  ├→ SICOR/BCB → crédito rural na região
  ├→ IBAMA → embargos no município
  ├→ SICAR → imóveis cadastrados
  ├→ ZARC/MAPA → zoneamento de risco climático, cultivares indicadas
  ├→ ANM → processos minerários no município
  ├→ PGFN → devedores no município
  └→ CEPEA regional → preços locais (quando disponível)
```

---

## INVENTÁRIO COMPLETO DE FONTES DE DADOS

### GRUPO 1 — DADOS DO IMÓVEL RURAL

| # | Fonte | Chave de busca | O que retorna | Acesso | Custo |
|---|-------|---------------|---------------|--------|-------|
| 1 | **SICAR/CAR** | Código CAR, município+UF | Perímetro, área total, APP, RL, uso consolidado, remanescente, status | WFS público + consulta web | Grátis |
| 2 | **SICAR WFS** | Código CAR, bbox, município | **Geometria (polígono GeoJSON)** do imóvel | GeoServer WFS (OGC) | Grátis |
| 3 | **SIGEF/INCRA** | Código parcela, bbox, coordenadas | Parcela certificada, área, data cert., RT | WFS Acervo Fundiário | Grátis |
| 4 | **SIGEF Provedor de Coordenadas** | Código parcela | Coordenadas do perímetro para download (XLS, CSV, XML) | Portal SIGEF | Grátis |
| 5 | **CNIR/SNCR** | NIRF, CPF/CNPJ (Gov.br Prata+) | Cadastro completo, CCIR, classificação, módulos fiscais | Portal Gov.br | Grátis (restrito) |
| 6 | **CAFIR/Receita** | Dados agregados por município | Estatísticas de imóveis rurais, ITR | Dados abertos CSV | Grátis |
| 7 | **Cartório/ONR** | Nº matrícula + comarca | Proprietário, ônus, averbações, histórico | Convênio ONR ou scraping | Pago |
| 8 | **SPU** | Coordenadas, município | Imóveis da União (terrenos de marinha, etc.) | Dados abertos + SPUGeo | Grátis |

### GRUPO 2 — DADOS AMBIENTAIS

| # | Fonte | Chave de busca | O que retorna | Acesso | Custo |
|---|-------|---------------|---------------|--------|-------|
| 9 | **IBAMA Embargos** | CPF/CNPJ, município, nº TAD | Auto de infração, área embargada, data, status, **geometria WKT** | CSV dados abertos + API REST | Grátis |
| 10 | **IBAMA Autuações** | CPF/CNPJ, município | Autos de infração (desde 2000), valor da multa, status | CSV dados abertos | Grátis |
| 11 | **IBAMA API de Embargo** | Nº seq TAD | Geometria WKT do embargo individual | REST API pública | Grátis |
| 12 | **FUNAI (TI)** | Sobreposição geoespacial | Terras indígenas: nome, etnia, fase | Download shapefile | Grátis |
| 13 | **ICMBio (UC)** | Sobreposição geoespacial | Unidades de conservação: nome, categoria, esfera | Download shapefile | Grátis |
| 14 | **INPE/PRODES** | Sobreposição geoespacial | Desmatamento acumulado por ano | Download shapefile / WMS | Grátis |
| 15 | **INPE/DETER** | Sobreposição geoespacial | Alertas de desmatamento recentes | Geoserviços TerraBrasilis | Grátis |
| 16 | **MapBiomas** | Coordenadas, CAR | Uso do solo série histórica (1985-2023), cobertura vegetal | Download / geoserviços | Grátis |
| 17 | **MapBiomas Alerta** | CAR, coordenadas | Alertas de desmatamento validados, cruzados com CAR/SIGEF | Plataforma web pública | Grátis |
| 18 | **ANA Outorgas** | Coordenadas, município, titular | Outorgas de uso de água: titular, finalidade, vazão | Dados abertos + GeoServer | Grátis |

### GRUPO 3 — DADOS MINERÁRIOS

| # | Fonte | Chave de busca | O que retorna | Acesso | Custo |
|---|-------|---------------|---------------|--------|-------|
| 19 | **ANM/Cadastro Mineiro** | Nº processo, CPF/CNPJ, município | Titular, substância, fase, área requerida | Consulta web pública | Grátis |
| 20 | **ANM/SIGMINE** | Sobreposição geoespacial | **Polígonos dos processos minerários** (ativos e inativos) | Download shapefile | Grátis |
| 21 | **ANM Dados Abertos** | Downloads periódicos | Produção mineral, RAL, barragens (SIGBM) | CSV/JSON dados abertos | Grátis |

### GRUPO 4 — DADOS DO PROPRIETÁRIO (PESSOA)

| # | Fonte | Chave de busca | O que retorna | Acesso | Custo |
|---|-------|---------------|---------------|--------|-------|
| 22 | **Receita Federal (CNPJ)** | CNPJ | Razão social, fantasia, CNAE, sócios, capital, endereço, situação | BrasilAPI (REST JSON) | Grátis |
| 23 | **Receita Federal (CPF)** | CPF | Nome, situação cadastral | ❌ Sem API pública. Infosimples ~R$0.20 | Pago |
| 24 | **Portal Transparência - Sanções** | CPF/CNPJ, nome | CEIS (empresas inidôneas), CEPIM, CNEP, CEAF | API REST pública | Grátis |
| 25 | **Portal Transparência - Trab. Escravo** | Download periódico | Nome, CPF/CNPJ, município, trabalhadores resgatados | Download CSV | Grátis |
| 26 | **DataJud/CNJ** | CPF/CNPJ, assunto, tribunal | Processos judiciais: nº, assunto, tribunal, data, status | API REST (chave gratuita) | Grátis |
| 27 | **TST/CNDT** | CPF/CNPJ | Certidão negativa de débitos trabalhistas | Consulta web (scraping) | Grátis |
| 28 | **CND Federal** | CPF/CNPJ | Certidão negativa de débitos federais | Consulta web (scraping) | Grátis |
| 29 | **FGTS/CRF** | CNPJ | Certificado de regularidade do FGTS | Consulta web (scraping) | Grátis |
| 30 | **PGFN Lista de Devedores** | CPF/CNPJ, nome | Inscrições em dívida ativa da União e FGTS, valor, situação | CSV dados abertos (trimestral) | Grátis |
| 31 | **CENPROT (Protestos)** | CPF/CNPJ | Títulos protestados em cartório (nacional) | Consulta web pública | Grátis |

### GRUPO 5 — DADOS DE MERCADO, FINANCEIROS E SEGUROS

| # | Fonte | Chave de busca | O que retorna | Acesso | Custo |
|---|-------|---------------|---------------|--------|-------|
| 32 | **SICOR/BCB** | Município, ano, programa | Crédito rural: valor, banco, linha, finalidade, cultura | API OData pública | Grátis |
| 33 | **CEPEA/ESALQ** | Commodity | Preço indicador diário (soja, milho, boi, café, etc.) | Scraping do site | Grátis |
| 34 | **IBGE/SIDRA (PAM)** | Município (cód. IBGE) | Produção agrícola: área, produção, rendimento por cultura | API REST pública | Grátis |
| 35 | **CONAB** | Estado, cultura | Safra: área plantada, produtividade, produção | Download portal | Grátis |
| 36 | **CVM (FIAGRO)** | Nome do fundo | Patrimônio, rendimento, ativos | Dados abertos CVM | Grátis |
| 37 | **ZARC/MAPA** | Município, cultura, safra | Zoneamento de risco climático: cultivares indicadas, períodos de plantio | Dados abertos MAPA | Grátis |
| 38 | **Proagro/MAPA** | Município | Dados de seguro rural e Proagro | Dados abertos MAPA | Grátis |

### GRUPO 6 — NOTÍCIAS E CONTEÚDO

| # | Fonte | Chave de busca | O que retorna | Acesso | Custo |
|---|-------|---------------|---------------|--------|-------|
| 35 | **RSS Agrolink** | - | Notícias agro | RSS feed | Grátis |
| 36 | **RSS Canal Rural** | - | Notícias agro | RSS feed | Grátis |
| 37 | **RSS Notícias Agrícolas** | - | Notícias agro + cotações | RSS feed | Grátis |
| 38 | **RSS Embrapa** | - | Notícias agro + pesquisa | RSS feed | Grátis |

---

## CAMPOS DE BUSCA ACEITOS (O que o cliente pode digitar)

| Campo de entrada | Tipo | Exemplo | Fontes que dispara |
|-----------------|------|---------|-------------------|
| Código CAR | Texto | MT-5107925-ABC123 | SICAR, MapBiomas Alerta |
| Código parcela SIGEF | UUID | a1b2c3d4-... | SIGEF, Acervo Fundiário |
| CNPJ | 14 dígitos | 12.345.678/0001-90 | Receita, IBAMA, Lista Suja, DataJud, PGFN, CENPROT, Sanções, CNDT |
| CPF | 11 dígitos | 123.456.789-00 | IBAMA, Lista Suja, DataJud, PGFN, CENPROT, CNDT |
| Nome do proprietário | Texto livre | "Fazenda XYZ Ltda" | Receita (CNPJ), Lista Suja, IBAMA, ANM |
| Coordenadas GPS | Lat, Lon | -15.7801, -47.9292 | SIGEF, SICAR, ANM, ANA, SPU, todas camadas PostGIS |
| Município + UF | Texto | "Sorriso/MT" | SICAR, IBAMA, IBGE/SIDRA, SICOR/BCB, ANM, ZARC |
| Nº matrícula | Texto | 12345 | Cartório/ONR (❌ requer convênio) |
| NIRF | Número | 1234567 | CNIR (❌ requer Gov.br Prata+) |
| CCIR | Número | 1234567890 | SNCR (❌ requer Gov.br Prata+) |
| Nº auto infração IBAMA | Número | 9876543 | **IBAMA API → retorna geometria WKT!** |
| Nº termo embargo IBAMA | Número | 1234567 | **IBAMA API → retorna geometria WKT!** |
| Nº processo minerário ANM | Texto | 830.123/2020 | ANM Cadastro Mineiro |
| Nº processo judicial | CNJ | 0001234-56.2024.8.10.0001 | DataJud/CNJ |
| Nº outorga ANA | Texto | 12345/2020 | ANA dados abertos |
| Commodity | Texto | "soja", "milho" | CEPEA, CONAB, ZARC |

---

## BENCHMARK: O QUE O REGISTRO RURAL OFERECE

Plano Gratuito: R$ 0/mês (buscas simples)
Plano Pro: R$ 149,90/mês (consultas completas e ilimitadas)
Plano Premium: R$ 850/mês (empresas, alta demanda de relatórios)

Funcionalidades:
- Busca por nome do imóvel ou titular
- Busca por coordenadas
- Busca por CPF/CNPJ
- Relatório PDF completo do CAR (dados, titulares, matrícula, área, mapa satélite)
- Relatório PDF completo do INCRA/SNCR
- Busca CAR por CPF/CNPJ
- Busca SNCR por CPF/CNPJ
- Mapas interativos com satélite
- Download KML/KMZ
- Documentos oficiais: Demonstrativo CAR, Comprovante CAFIR, CCIR
- API para empresas (integração com sistemas de terceiros)

**Nosso diferencial sobre o Registro Rural:**
- Camada jurídica (processos DataJud, PGFN, protestos, sanções, lista suja)
- Camada minerária (ANM/SIGMINE)
- Camada hídrica (outorgas ANA)
- Cotações de mercado e crédito rural
- Portal de notícias com curadoria jurídica
- Monitoramento e alertas de mudanças
- Score de risco automatizado

---

## O QUE PODEMOS OFERECER DE FATO HOJE (Realista)

### Consulta por CAR (Muito viável)
- Perímetro e área do imóvel (SICAR WFS)
- Mapa com polígono + camadas de sobreposição
- Alerta se sobrepõe TI, UC, embargo, desmatamento
- Score de risco ambiental
**Valor: R$ 15-50 por consulta**

### Consulta por CNPJ (Muito viável)
- Dados cadastrais completos (BrasilAPI)
- Embargos IBAMA vinculados
- Lista Suja do trabalho escravo
- Sanções (CEIS/CEPIM)
- Processos judiciais (DataJud)
- CNDT trabalhista
**Valor: R$ 20-80 por consulta**

### Consulta por Coordenadas (Viável)
- Parcelas SIGEF próximas
- Imóveis CAR na área
- Processos minerários (SIGMINE)
- Outorgas de água (ANA)
- Imóveis da União (SPU)
- Sobreposição com todas as camadas
**Valor: R$ 30-100 por consulta**

### Relatório Due Diligence Completo (CAR + CNPJ + Geo)
Combina tudo acima + PDF profissional + score de risco em 6 áreas
**Valor: R$ 150-500 por relatório**

### Monitoramento (Assinatura)
Verifica periodicamente embargos, processos, CAR status
**Valor: R$ 49-199/mês**

### Portal (Cotações + Notícias)
Atrai tráfego, converte em clientes pagos
**Valor: Gratuito (monetiza com anúncios + conversão)**

---

## FONTES QUE NÃO CONSEGUIMOS ACESSAR (Limitações)

| Dado | Por que não | Alternativa |
|------|------------|-------------|
| Matrícula de imóvel | Cartórios não têm API pública | Convênio ONR, ou cliente faz upload |
| SNCR/NIRF/CCIR | CNIR requer Gov.br Prata+ | Scraping com auth, ou input manual |
| CPF (nome por CPF) | Receita não disponibiliza | Infosimples (~R$0.20) ou input manual |
| ITR por imóvel | Dados não são públicos | Dados agregados do CAFIR |
| Preço de terra | FNP/ESALQ não é público | Importação manual de relatórios |
| Certidões (CND, CRF) | Sites sem API, com captcha | Scraping avançado (Playwright) |

---

## IMPLEMENTAÇÃO: O QUE FALTA CODAR

| Fonte | Status | O que falta |
|-------|--------|------------|
| SICAR/CAR (WFS) | ✅ Pronto | - |
| SIGEF (WFS) | ✅ Pronto | - |
| BrasilAPI (CNPJ) | ✅ Pronto | - |
| IBAMA embargos (CSV) | ✅ Pronto | Importar dados via CLI |
| IBAMA API embargo (geometria) | 🔲 Novo | Implementar coletor para API REST individual |
| Lista Suja | ✅ Pronto | Importar CSV via CLI |
| DataJud/CNJ | ✅ Pronto | Obter chave API (cadastro) |
| CEPEA cotações | ✅ Pronto | Testar com dados reais |
| IBGE/SIDRA | ✅ Pronto | - |
| SICOR/BCB | ✅ Pronto | - |
| RSS notícias | ✅ Pronto | - |
| Portal Transparência (sanções) | 🔲 Novo | Implementar consulta CEIS/CEPIM |
| ANM processos minerários | 🔲 Novo | Implementar scraper do Cadastro Mineiro |
| ANM/SIGMINE (shapefiles) | 🔲 Novo | Download + importação PostGIS |
| ANA outorgas | 🔲 Novo | Consumir GeoServer da ANA |
| SPU imóveis da União | 🔲 Novo | Consumir dados abertos SPU |
| MapBiomas Alerta | 🔲 Novo | Integrar plataforma de alertas |
| TST/CNDT | 🔲 Novo | Scraping do site do TST |
| Importação shapefiles (FUNAI, ICMBio) | ✅ CLI pronto | Baixar arquivos e rodar |
| Sobreposição PostGIS | ✅ Pronto | Popular banco com camadas |
