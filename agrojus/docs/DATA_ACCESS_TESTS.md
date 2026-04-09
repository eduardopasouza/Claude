# Teste Real de Acesso às Fontes de Dados — AgroJus

Data do teste: 2026-04-09
Ambiente: servidor Linux, acesso direto à internet

---

## RESULTADOS DOS TESTES

### ✅ FUNCIONA — Testado e confirmado

| # | Fonte | Teste | Resultado | Notas |
|---|-------|-------|-----------|-------|
| 1 | **BrasilAPI (CNPJ)** | GET /api/cnpj/v1/00000000000191 | HTTP 200, 20KB, 0.19s | Retorna dados completos: sócios, CNAE, endereço, capital social |
| 2 | **IBGE/SIDRA (PAM)** | GET /values/t/5457/n6/5107925/v/216/... | HTTP 200 | Retorna produção agrícola de Sorriso-MT. Variável v/35 NÃO existe (erro 400); usar v/214, v/215, v/216 |
| 3 | **SICOR/BCB (Crédito Rural)** | OData CusteioMunicipioProduto | HTTP 200 | Funciona! Campo correto: `codIbge` (não `codMunic`). Retorna milho, bovinos, soja em Sorriso-MT com valores reais (R$602K milho, R$7.5M bovinos) |
| 4 | **IBAMA Embargos (ZIP)** | Download termo_embargo_csv.zip | HTTP 206 (partial content OK) | **URL mudou!** Antiga: /SICAFI/embargo/Embargo.csv. Nova: /SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip |
| 5 | **IBAMA Coordenadas** | Download coordenadas.csv | HTTP 200 | CSV com LAT, LON, WKT de cada embargo. Atualizado em 2026-04-08! Contém POINT geometry |
| 6 | **IBAMA Auto Infração** | Download auto_infracao_csv.zip | HTTP 206 | Disponível para download |
| 7 | **SIGEF Portal** | GET sigef.incra.gov.br | HTTP 200, 2.7s | Portal acessível |
| 8 | **TST CNDT** | GET cndt-certidao.tst.jus.br | HTTP 200, 1.2s | Portal acessível para scraping |
| 9 | **MapBiomas Alerta** | GET plataforma.alerta.mapbiomas.org | HTTP 200, 0.9s | Plataforma acessível |

### ⚠️ PARCIAL — Funciona com ressalvas

| # | Fonte | Teste | Resultado | Problema |
|---|-------|-------|-----------|---------|
| 10 | **SICAR/CAR WFS** | GetCapabilities | HTTP 503 | WFS estava fora no momento do teste. Pode ser instabilidade temporária — o SICAR é conhecido por ficar fora periodicamente |
| 11 | **SIGEF/INCRA WFS** | GetCapabilities | HTTP 404 | URL pode ter mudado. O Acervo Fundiário pode ter migrado endpoint |
| 12 | **DataJud/CNJ** | GET base URL | HTTP 401 | API funciona mas **requer chave API** (cadastro gratuito). Sem chave = 401 |
| 13 | **IBAMA API Embargo Individual** | GET /wkt?seqTad=1 | HTTP 404 | API corpgateway-api.ibama.gov.br não respondeu. Pode ter sido descontinuada ou mudado URL |

### ❌ NÃO ACESSÍVEL — Bloqueado ou indisponível neste ambiente

| # | Fonte | Teste | Resultado | Motivo |
|---|-------|-------|-----------|--------|
| 14 | **Portal Transparência API** | GET CEIS | HTTP 000 (timeout/block) | Provavelmente bloqueio de IP de datacenter ou requer chave API |
| 15 | **PGFN Lista Devedores** | GET listadevedores.pgfn.gov.br | HTTP 000 (connection reset) | Bloqueio de IP ou proteção contra bots |
| 16 | **CENPROT Nacional** | GET pesquisaprotesto.com.br | HTTP 403 | Bloqueio explícito (proteção anti-bot) |
| 17 | **ANA Dados Abertos** | GET dadosabertos.ana.gov.br | Não testado (timeout anterior) | Precisa testar de outro ambiente |
| 18 | **ANM Geo Portal** | GET geo.anm.gov.br | Não testado | Precisa testar |

### 📋 NÃO TESTADO — Requer ação manual

| # | Fonte | O que precisa |
|---|-------|--------------|
| 19 | **FUNAI (Shapefiles TI)** | Download manual do portal Gov.br |
| 20 | **ICMBio (Shapefiles UC)** | Download manual do portal Gov.br |
| 21 | **CEPEA (Cotações)** | Scraping do site — funcional mas depende do layout HTML |
| 22 | **CONAB** | Download manual de relatórios |
| 23 | **CVM (FIAGRO)** | Download de dados abertos |
| 24 | **ZARC/MAPA** | Download de dados abertos |
| 25 | **PGFN (CSV devedores)** | Download manual do portal dados abertos |
| 26 | **CND Federal** | Scraping com captcha |
| 27 | **FGTS/CRF** | Scraping com captcha |

---

## CORREÇÕES NECESSÁRIAS NO CÓDIGO

### 1. IBAMA — URLs erradas
```
ERRADO: https://dadosabertos.ibama.gov.br/dados/SICAFI/embargo/Embargo.csv
CERTO:  https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip

NOVO CSV de coordenadas (com geometria!):
        https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/coordenadas/coordenadas.csv

CSV de Autos de Infração:
        https://dadosabertos.ibama.gov.br/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip
```

### 2. IBGE/SIDRA — Variáveis erradas
```
ERRADO: v/35 (não existe na tabela 5457)
CERTO:  v/214 (área colhida), v/215 (área plantada), v/216 (quantidade produzida)
```

### 3. SICOR/BCB — Endpoint e campo errados
```
ERRADO: endpoint "RecursosMunicipios", campo "cdMunicipio"
CERTO:  endpoint "CusteioMunicipioProduto", campo "codIbge"

Endpoints disponíveis: CusteioMunicipioProduto, InvestMunicipioProduto,
ComercRegiaoUFProduto, ProgramaSubprogramaRegiaoUF, etc.
```

### 4. SICAR WFS — Pode estar instável
O WFS do SICAR retornou 503. Precisa de retry com backoff e fallback.

### 5. SIGEF WFS — URL pode ter mudado
O Acervo Fundiário retornou 404 no WFS. Verificar se migrou.

---

## CAMADAS DO MAPA ONR (referência para replicarmos)

Com base na pesquisa do manual e do site, o ONR tinha/tem as seguintes categorias de camadas:

### Registro de Imóveis
- Código Nacional de Matrícula
- Competência registral (qual cartório atende cada região)
- Imóveis rurais georreferenciados (SIGEF/SNCI)
- Lotes e quadras (parcelamento do solo)

### Ambiental
- APP (Áreas de Preservação Permanente)
- Biomas
- CAR (Cadastro Ambiental Rural)
- Desmatamento (PRODES/DETER)
- Incêndios florestais
- Exploração florestal
- Uso restrito

### Fundiário
- Terras indígenas (FUNAI)
- Quilombos (INCRA)
- Unidades de conservação (ICMBio)
- Assentamentos (INCRA)
- Imóveis públicos (SPU)
- MATOPIBA (aptidão)

### Infraestrutura
- Energia
- Transporte
- Logística

### Mineração
- Processos minerários (SIGMINE/ANM)

### Agronegócio
- Crédito rural
- Potencial agrícola
- Características do solo

### Outros
- Limites territoriais (estados, municípios)
- Google Street View integrado

**Nota**: O ONR declarava ter 184 camadas. Muitas podem ter sido removidas
por questões de manutenção dos dados ou acordos com as fontes.
Precisamos confirmar quais existem hoje acessando o mapa diretamente.
