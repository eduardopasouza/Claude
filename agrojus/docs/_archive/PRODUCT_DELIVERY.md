# Como Cada Produto é Entregue — Detalhamento Técnico

Este documento explica, produto por produto, exatamente como a informação
chega ao cliente: de onde vem, como é processada, o que funciona hoje e
o que falta.

---

## PRODUTO 1: Relatório de Imóvel Rural (Due Diligence)

### O que o cliente recebe
Um PDF de 5-10 páginas com:
- Dados cadastrais completos do imóvel (CAR, SIGEF, SNCR, matrícula, CCIR, ITR)
- Dados do proprietário (razão social, sócios, situação cadastral)
- Mapa do imóvel com sobreposições
- Semáforo de risco (verde/amarelo/vermelho) em 6 áreas
- Lista de alertas encontrados
- Fontes consultadas

### Fluxo técnico passo a passo

```
Cliente informa: qualquer dado que tenha do imóvel
         │
         ▼
ETAPA 1 — Resolução do Imóvel
         │
         ├─ Se informou CAR → consulta SICAR via WFS (geoserviço)
         │   Retorna: perímetro, área, APP, RL, município, status
         │   REAL: ✅ Funciona. WFS público do SICAR, sem autenticação.
         │   Formato: GeoJSON. Demora 2-5s.
         │
         ├─ Se informou SIGEF → consulta Acervo Fundiário via WFS
         │   Retorna: parcela certificada, área, responsável técnico
         │   REAL: ✅ Funciona. WFS público do INCRA.
         │
         ├─ Se informou coordenadas → busca SIGEF por proximidade via WFS
         │   Retorna: parcelas na área
         │   REAL: ✅ Funciona. Bounding box no WFS.
         │
         ├─ Se informou matrícula → ❌ PLACEHOLDER
         │   Precisa: scraping do sistema do cartório ou convênio com ONR
         │   Alternativa: o próprio cliente faz upload da matrícula em PDF
         │   e o sistema extrai dados via OCR (futuro)
         │
         ├─ Se informou SNCR/NIRF → ❌ PLACEHOLDER
         │   Precisa: acesso ao CNIR via Gov.br (nível Prata)
         │   O CNIR não tem API pública. Alternativa: scraping com
         │   autenticação ou convênio com INCRA/Serpro.
         │
         ├─ Se informou CCIR → ❌ PLACEHOLDER
         │   Mesmo problema: dados estão no SNCR/CNIR.
         │
         └─ Se informou ITR/NIRF → ❌ PLACEHOLDER
             Precisa: acesso ao sistema da Receita Federal.
             Dados de VTI (Valor da Terra Nua) não são públicos por imóvel.

         ▼
ETAPA 2 — Dados do Proprietário
         │
         ├─ Se CNPJ → consulta BrasilAPI (gratuita, pública)
         │   Retorna: razão social, CNAE, sócios, capital social, endereço
         │   REAL: ✅ Funciona. API REST, resposta em <1s.
         │   Limite: ~1 consulta/segundo (rate limiting da BrasilAPI)
         │
         └─ Se CPF → ❌ NÃO HÁ API PÚBLICA PARA CPF
             A Receita Federal não disponibiliza dados de CPF via API.
             Infosimples oferece isso via scraping (pago, R$0.20/consulta).
             Alternativa: o cliente informa o nome manualmente.

         ▼
ETAPA 3 — Embargos Ambientais (IBAMA)
         │
         └─ Busca por CPF/CNPJ ou município no banco local
             Dados vêm de: CSV de dados abertos do IBAMA (~500MB)
             Atualização: download periódico via CLI (python -m app.cli import-ibama)
             REAL: ✅ Funciona quando importado. Busca instantânea no banco.
             O CSV contém: auto de infração, CPF/CNPJ, município, área, data, status.
             Atualizado mensalmente pelo IBAMA.

         ▼
ETAPA 4 — Lista Suja do Trabalho Escravo
         │
         └─ Busca por CPF/CNPJ ou nome no banco local
             Dados vêm de: CSV do Portal da Transparência
             Download: manual (requer aceitar termos no portal)
             REAL: ✅ Funciona quando importado. CLI de importação pronto.
             O CSV contém: nome, CPF/CNPJ, município, trabalhadores resgatados.

         ▼
ETAPA 4B — Processos Judiciais (DataJud/CNJ)
         │
         └─ Busca por CPF/CNPJ nos TRFs e TRTs via API DataJud
             API pública do CNJ (requer cadastro para chave de API).
             Cadastro em: https://datajud-wiki.cnj.jus.br/
             REAL: ✅ API existe e funciona. Requer chave (gratuita).
             Retorna: número do processo, assunto, tribunal, data, status.
             Limitação: busca por CPF/CNPJ, não por imóvel diretamente.
             Para buscar por imóvel: precisaria cruzar CPF do proprietário.

         ▼
ETAPA 5 — Análise Geoespacial (sobreposições)
         │
         ├─ Se geometria do imóvel disponível (via WFS do CAR/SIGEF):
         │   Cruza com camadas importadas no PostGIS:
         │   - Terras Indígenas (shapefile FUNAI, ~600 TIs)
         │   - Unidades de Conservação (shapefile ICMBio, ~2.500 UCs)
         │   - Assentamentos (shapefile INCRA)
         │   - Quilombos (shapefile INCRA)
         │   Consulta PostGIS: ST_Intersects(imovel.geometry, ti.geometry)
         │   REAL: ✅ Funciona quando shapefiles importados via CLI.
         │   Shapefiles são públicos e gratuitos para download.
         │
         └─ Se geometria NÃO disponível:
             Relatório indica: "Análise geoespacial não disponível.
             Geometria do imóvel não encontrada no SICAR/SIGEF."

         ▼
ETAPA 6 — Dados Financeiros
         │
         ├─ Crédito rural por município → API SICOR do Banco Central
         │   Dados agregados (não por CPF individual).
         │   REAL: ✅ API OData pública, sem autenticação.
         │
         └─ Preço de terra na região → ❌ PLACEHOLDER
             Dados de preço de terra (FNP/ESALQ) não são públicos.
             Alternativa: IEA (SP), FAEG (GO), dados de leilões.
             Ou: importar dados manualmente de relatórios publicados.

         ▼
ETAPA 7 — Cálculo de Risco
         │
         Regras implementadas (código real):
         - CAR cancelado/suspenso → risco fundiário CRÍTICO
         - Sem SIGEF certificado → risco fundiário MÉDIO
         - Embargo IBAMA → risco ambiental CRÍTICO
         - Sobreposição com TI → risco ambiental CRÍTICO
         - Sobreposição com UC → risco ambiental ALTO
         - Lista Suja → risco trabalhista CRÍTICO
         - CNPJ inapta/baixada → risco jurídico ALTO
         - 5+ processos judiciais → risco jurídico ALTO
         - Processo ambiental → eleva risco ambiental
         - Disputa possessória → eleva risco fundiário
         - Score geral = pior score entre todas as áreas
         REAL: ✅ 100% implementado com 9 cenários testados.

         ▼
ETAPA 8 — Geração do PDF
         │
         Gera PDF com ReportLab:
         - Header com identificadores do imóvel
         - Tabela de semáforo com cores (verde/amarelo/vermelho)
         - Seções: imóvel, registral, proprietário, ambiental, trabalhista,
           sobreposições, financeiro, detalhamento, fontes, disclaimer
         REAL: ✅ Implementado. PDF funcional mas precisa de polish visual.
```

### O que funciona HOJE para entregar um relatório

Se o cliente informar **CAR + CNPJ**, o sistema consegue:
1. ✅ Buscar dados do imóvel no SICAR (área, APP, RL, status, geometria)
2. ✅ Buscar parcela certificada no SIGEF
3. ✅ Buscar dados do proprietário na Receita Federal (razão social, sócios, etc)
4. ✅ Verificar embargos IBAMA (se banco local estiver populado)
5. ✅ Verificar Lista Suja (se banco local estiver populado)
6. ✅ Buscar processos no DataJud (se chave API configurada)
7. ✅ Verificar sobreposições geoespaciais (se shapefiles importados)
8. ✅ Calcular score de risco
9. ✅ Gerar PDF

### O que NÃO funciona ainda

- **Matrícula**: requer convênio com cartório/ONR ou scraping
- **SNCR/NIRF/CCIR/ITR**: requer acesso ao CNIR (Gov.br nível Prata) ou convênio
- **CPF de pessoa física**: não há API pública (Infosimples cobra ~R$0.20/consulta)
- **Preço de terra**: dados não são públicos
- **Certidões negativas** (CND, CNDT, FGTS): requer scraping de cada site

---

## PRODUTO 2: Dossiê de Pessoa (CPF/CNPJ)

### O que o cliente recebe
Relatório sobre uma pessoa/empresa:
- Dados cadastrais (CNPJ: completo; CPF: limitado)
- Imóveis vinculados
- Embargos IBAMA
- Lista Suja
- Processos judiciais
- Crédito rural (agregado)
- Notícias públicas mencionando a pessoa

### Fluxo técnico

```
Cliente informa: CPF ou CNPJ
         │
         ▼
1. Valida documento (algoritmo local) ✅
2. Se CNPJ: busca BrasilAPI ✅
3. Se CPF: ❌ sem API pública
4. Busca embargos IBAMA no banco local ✅ (requer importação)
5. Busca Lista Suja no banco local ✅ (requer importação)
6. Busca processos no DataJud ✅ (requer chave API)
7. Busca crédito rural no SICOR ✅ (dados agregados por município)
8. Busca notícias RSS que mencionem o nome ✅ (busca textual)
9. Calcula score de risco ✅
```

### Limitação principal
- **CPF**: só funciona bem para CNPJ. Para CPF, não temos nome sem que
  o cliente informe. Solução: pedir nome + CPF como input.
- **Imóveis vinculados**: o SICAR não permite busca por CPF/CNPJ diretamente.
  Precisaria de um banco local com a relação proprietário → imóvel (construído
  gradualmente conforme relatórios são gerados).

---

## PRODUTO 3: Monitoramento e Alertas

### O que o cliente recebe
Notificações quando algo muda:
- Novo embargo IBAMA para pessoa monitorada
- Alteração no status do CAR de imóvel monitorado
- Novo processo judicial (futuro)
- Desmatamento detectado na área (futuro)

### Fluxo técnico

```
1. Cliente cadastra imóvel (CAR) ou pessoa (CPF/CNPJ) para monitorar ✅
2. Job periódico roda a cada X horas:
   - Re-consulta IBAMA para cada CPF/CNPJ monitorado ✅
   - Re-consulta CAR status para cada imóvel monitorado ✅
   - Compara com estado anterior
   - Se mudou: gera alerta
3. Cliente consulta alertas via API ou recebe por email (futuro)
```

### Estado atual
- ✅ Cadastro e remoção de monitores
- ✅ Consulta de alertas
- ✅ Ciclo de verificação manual (endpoint /run-check)
- ❌ Job periódico automático (precisa de Celery ou cron)
- ❌ Notificação por email

---

## PRODUTO 4: Portal Gratuito (Notícias + Cotações)

### Notícias
```
1. Agregação de RSS de 5 portais agro ✅
   (Agrolink, Canal Rural, Notícias Agrícolas, Embrapa, Portal do Agronegócio)
2. Classificação automática em categorias ✅
   (jurídico, mercado, geral — por keywords)
3. Endpoints: todas, jurídicas, mercado ✅
4. Cache de 24h ✅
```
FUNCIONA: sim, de ponta a ponta.

### Cotações
```
1. Scraping do CEPEA/ESALQ ✅
   (soja, milho, boi gordo, café, algodão, arroz, trigo, açúcar, etanol)
2. Parse de HTML da página de indicadores ✅
3. Cache de 24h ✅
4. API: /market/quotes e /market/quotes/{commodity} ✅
```
FUNCIONA: depende da estrutura HTML do CEPEA (pode quebrar se mudarem o layout).

---

## RESUMO: O que precisa para cada produto ser vendável

| Produto | Status | O que falta para vender |
|---------|--------|------------------------|
| Relatório de Imóvel | 70% | Popular banco com IBAMA + Lista Suja + shapefiles. Obter chave DataJud. Polish no PDF. |
| Dossiê de Pessoa | 60% | Mesmo que acima + resolver busca por CPF (pedir nome como input). |
| Monitoramento | 40% | Job periódico (Celery/cron) + notificação por email. |
| Portal (notícias) | 90% | Só precisa de frontend. Backend funciona. |
| Portal (cotações) | 80% | Funciona mas depende do HTML do CEPEA. Ter fallback. |

### Ações concretas para chegar a vendável

1. **Rodar `python -m app.cli sync-all`** → popula IBAMA e Lista Suja
2. **Baixar shapefiles** de FUNAI e ICMBio e importar via CLI
3. **Cadastrar no DataJud** → obter chave de API gratuita
4. **Configurar Celery** → monitoramento periódico
5. **Frontend** (Antigravity) → interface para o cliente usar
6. **Stripe/Mercado Pago** → cobrança por relatório ou assinatura
