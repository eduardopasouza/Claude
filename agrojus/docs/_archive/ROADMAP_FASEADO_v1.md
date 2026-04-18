# AgroJus — Roadmap Faseado v1.0

> Data: 2026-04-15
> Autor: Sessoes 1-3 (pesquisa competitiva + backend + consolidacao)
> Para: Proxima sessao de desenvolvimento

---

## VISAO DO PRODUTO

AgroJus e uma plataforma de inteligencia fundiaria, ambiental, juridica e financeira para o agronegocio brasileiro. Diferencial: **combina dados geoespaciais (10M+ registros) com analise juridica especializada** — algo que nenhum concorrente faz.

**Publico:**
1. **Advogados agraristas** — due diligence, defesa em embargos, recuperacao de credito
2. **Bancos/cooperativas** — compliance MCR 2.9, analise de risco para credito rural
3. **Produtores rurais** — regularizacao, alongamento de dividas, checklists de conformidade
4. **Investidores** — due diligence fundiaria, EUDR, ESG

---

## DIFERENCIAIS COMPETITIVOS (todos os concorrentes analisados)

### Diferenciais que concorrentes tem e devemos incorporar

| Diferencial | Quem faz | Como incorporar |
|---|---|---|
| **Consulta via WhatsApp** | Agrolend (WhatsApp-first, 3 cliques) | Bot WhatsApp → API AgroJus → resposta formatada |
| **Marketplace modular de camadas** | Agrotools (1.300+ layers, plugins) | Catalogo de camadas com on/off por plano |
| **Score visual tipo Serasa** | Serasa Agro (gauge 0-1000) | Gauge visual por eixo no dashboard |
| **Calculadora de prescricao** | AdvLabs (prescricao ambiental automatica) | Prescricao em 5 eixos (ambiental, criminal, trabalhista, civil, tributario) |
| **CRM Kanban de teses** | AdvLabs (128 teses catalogadas) | Kanban de teses aplicaveis por caso |
| **Radar de prospecao** | AdvLabs (filtro por tipo de auto+regiao) | Busca avancada: "embargos no MA com prescricao em < 1 ano" |
| **Monitoramento por satelite** | SpectraX, TerraMagna (NDVI, fogo, uso solo) | Earth Engine ja integrado (flag include_satellite) |
| **Imagens antes/depois** | MapBiomas Alerta, SpectraX | GraphQL MapBiomas ja integrado (retorna URLs das imagens) |
| **UX produtor simplicidade** | Agrolend, Traive | Fluxo simplificado para produtor (3 telas) |
| **170+ fontes integradas** | Serasa Agro | Meta: 50+ fontes ativas (temos 14 hoje) |
| **Cadeia dominial completa** | Serasa Agro, Registro Rural | Matricula + SIGEF + CAR + CNPJ + socios |

### Diferenciais UNICOS do AgroJus (ninguem faz)

| Diferencial | Por que e unico | Impacto |
|---|---|---|
| **Analise juridica integrada a dados geo** | Concorrentes sao OU tech OU juridico, nunca ambos | CRITICO — raison d'etre |
| **Score juridico 0-1000 com prescricao** | AdvLabs faz prescricao ambiental so; nos fazemos 5 eixos | ALTO |
| **Recuperacao de credito rural + alongamento** | Ninguem oferece analise de viabilidade de alongamento | ALTO — diferencial juridico |
| **Analise de embargos com defesa sugerida** | Concorrentes mostram o embargo; nos dizemos como defender | CRITICO |
| **Contratos agro com analise de risco** | Ninguem integra dados geoespaciais na redacao de contratos | ALTO |
| **Checklists regulatorios interativos** | Ninguem oferece checklists de autorizacao contextualizados | MEDIO-ALTO |
| **Raciocinio IA auditavel (cite-to-source)** | Concorrentes dao score; nos mostramos o raciocinio | ALTO — confianca |
| **5 scores independentes + score geral** | Serasa faz 1 score; nos fazemos 5 + geral | ALTO |

---

## NOVAS FUNCIONALIDADES SOLICITADAS

### 1. Recuperacao de Credito e Alongamento de Dividas
O produtor insere dados da operacao de credito (banco, valor, safra, modalidade, data vencimento) e o sistema:
- Verifica elegibilidade para alongamento (Lei 9.138/95, MPs, Res. CMN)
- Calcula saldo devedor com juros legais vs juros cobrados
- Identifica abusos (capitalizacao, taxa acima do permitido, cobranças indevidas)
- Sugere via processual (acao revisional, renegociacao, alongamento)
- Gera minuta de notificacao extrajudicial

**Backend necessario:**
- POST /api/v1/credito/analisar-alongamento
- POST /api/v1/credito/calcular-saldo-devedor
- GET /api/v1/credito/legislacao-aplicavel
- Tabela de taxas historicas BCB (Selic, TR, TJLP)
- Regras de alongamento por programa (PESA, PRONAF, PRONAMP, etc.)

### 2. Analise de Embargos e Autuacoes
Dado um embargo/autuacao IBAMA ou ICMBio, o sistema:
- Classifica o tipo (desmatamento, APP, RL, fauna, pesca, poluicao)
- Verifica prescricao (administrativa 5 anos, criminal 12-20 anos)
- Identifica nulidades formais (prazo notificacao, competencia, motivacao)
- Sugere linhas de defesa (com jurisprudencia aplicavel)
- Calcula multa esperada e possibilidade de conversao (Dec. 6.514/08)

**Backend necessario:**
- POST /api/v1/embargos/analisar
- GET /api/v1/embargos/prescricao/{auto_id}
- GET /api/v1/embargos/nulidades/{auto_id}
- GET /api/v1/embargos/defesa-sugerida/{auto_id}
- Base de jurisprudencia ambiental (STJ, TRFs)

### 3. Contratos Agro e Comunicacoes
Templates e analise de contratos comuns no agro:
- Arrendamento rural
- Parceria agricola/pecuaria
- Compra e venda de imovel rural
- CPR (Cedula de Produto Rural)
- Contrato de integrao (aves, suinos)
- Contrato de fornecimento de cana/soja/milho
- Notificacoes extrajudiciais
- Comunicacoes a orgaos (IBAMA, SEMA, INCRA)

**Backend necessario:**
- GET /api/v1/contratos/templates
- POST /api/v1/contratos/gerar (com dados do caso + dados geoespaciais do imovel)
- POST /api/v1/contratos/analisar-risco (upload de contrato existente)
- POST /api/v1/comunicacoes/gerar (notificacao, requerimento, defesa)

### 4. Checklists e Requisitos de Autorizacoes
Checklists interativos para procedimentos regulatorios:
- Licenciamento ambiental (LP, LI, LO) por estado
- Autorizacao de desmate (ASV)
- Registro de reserva legal (CAR)
- Outorga de uso de agua (ANA/estadual)
- Certificacao de imovel (SIGEF/INCRA)
- Regularizacao fundiaria (Programa Terra Legal)
- Registro no SIF (frigorificos)
- Certificacao organica
- Compliance MCR 2.9 (passo a passo)
- Compliance EUDR (passo a passo)

**Backend necessario:**
- GET /api/v1/checklists (lista todas)
- GET /api/v1/checklists/{tipo}?uf=MA (checklist contextualizado por estado)
- POST /api/v1/checklists/{tipo}/verificar (verifica status do imovel contra checklist)
- Banco de requisitos por estado/tipo de autorizacao

### 5. Bot WhatsApp
- Consulta rapida por CAR code → score + resumo
- Alerta de novos embargos/autuacoes no imovel monitorado
- Status de processo judicial
- Lembrete de prazo de defesa

**Backend necessario:**
- Webhook WhatsApp Business API (Twilio ou Meta Cloud API)
- POST /api/v1/whatsapp/webhook (recebe mensagens)
- Formatador de respostas para WhatsApp (texto + imagem do mapa)

---

## ESTADO ATUAL DO BACKEND (2026-04-15)

### O que funciona
- 42+ endpoints FastAPI
- PostGIS com 59 tabelas, 10.7M+ registros
- SICAR 79.3M CARs via BigQuery (script pronto, MA em download)
- SIGEF 493k parcelas certificadas (6 estados carregados)
- Motor de relatorio: 13 camadas PostGIS cruzadas em ~250ms
- Compliance MCR 2.9 + EUDR (checklist basico)
- Earth Engine integrado (flag include_satellite)
- MapBiomas GraphQL integrado (flag include_realtime_alerts)
- Dashboard com materialized view (5ms)
- PDF com tabelas de compliance
- Busca de imoveis, GeoJSON para mapa, overlaps

### O que NAO funciona
- Frontend nao renderiza mapa (problema de integracao, nao de backend)
- Compliance e simplista (checklist binario, sem raciocinio IA)
- Nao ha diferenca util entre "compliance" e "deep search" para o usuario
- Scoring e basico (sem 5 eixos independentes)
- Sem analise juridica (prescricao, teses, defesa)
- Sem recuperacao de credito
- Sem contratos/comunicacoes
- Sem checklists regulatorios
- Sem bot WhatsApp
- DataJud sem backup local
- DETER/PRODES com dados parciais (50k cada, nao e dataset completo)

---

## ROADMAP FASEADO

### FASE 0 — FUNDACAO (pre-requisito, 2-3 dias)

**Objetivo:** Garantir que o basico funciona antes de construir features novas.

| # | Tarefa | Tipo | Prioridade |
|---|---|---|---|
| 0.1 | **Consertar mapa no frontend** — diagnosticar porque nao renderiza | Frontend | CRITICA |
| 0.2 | Unificar compliance e search num unico fluxo (busca → relatorio → score) | Backend+UX | CRITICA |
| 0.3 | Completar download SICAR todos os estados via BigQuery | ETL | ALTA |
| 0.4 | Completar download SIGEF todos os estados | ETL | ALTA |
| 0.5 | Baixar DETER/PRODES completos (shapefiles, nao WFS) | ETL | ALTA |
| 0.6 | Cadastros Eduardo: MapBiomas conta, Embrapa AgroAPI, Portal Transparencia | Config | MEDIA |

### FASE 1 — MOTOR JURIDICO (5-7 dias)

**Objetivo:** O diferencial unico. Transformar dados em inteligencia juridica.

| # | Tarefa | Tipo | Prioridade |
|---|---|---|---|
| 1.1 | **Scoring 5 eixos** (fundiario, ambiental, trabalhista, juridico, financeiro) 0-1000 cada | Backend | CRITICA |
| 1.2 | **Prescricao automatica** — calcular prescricao para cada embargo/auto/processo | Backend | CRITICA |
| 1.3 | **Analise de embargos/autuacoes** — classificacao, nulidades, defesa sugerida | Backend | CRITICA |
| 1.4 | **Recuperacao de credito** — input dados operacao → analise de alongamento | Backend | ALTA |
| 1.5 | Base de jurisprudencia ambiental (STJ, TRFs) — tabela com precedentes-chave | Dados | ALTA |
| 1.6 | Regras de alongamento por programa (PESA, PRONAF, PRONAMP) | Dados | ALTA |

### FASE 2 — CONTRATOS E CHECKLISTS (3-5 dias)

**Objetivo:** Ferramentas praticas para o dia a dia do advogado/produtor.

| # | Tarefa | Tipo | Prioridade |
|---|---|---|---|
| 2.1 | **Templates de contratos agro** (arrendamento, parceria, CPR, compra/venda) | Backend | ALTA |
| 2.2 | **Gerador de contratos** com dados do imovel (area, CAR, municipio) | Backend | ALTA |
| 2.3 | **Analise de risco de contrato** (upload + verificacao contra dados geo) | Backend | MEDIA |
| 2.4 | **Checklists regulatorios** interativos (licenciamento, CAR, outorga, SIGEF) | Backend | ALTA |
| 2.5 | **Gerador de comunicacoes** (notificacao, requerimento, defesa) | Backend | ALTA |
| 2.6 | Banco de requisitos por estado/tipo (licenciamento ambiental varia por UF) | Dados | MEDIA |

### FASE 3 — FRONTEND COMPLETO (7-10 dias)

**Objetivo:** Interface profissional, dark mode, mapa interativo.

| # | Tarefa | Tipo | Prioridade |
|---|---|---|---|
| 3.1 | **Next.js 14 + Tailwind + shadcn/ui** — setup e esqueleto | Frontend | CRITICA |
| 3.2 | **Mapa interativo** — react-leaflet + 13 camadas + opacity + inspector | Frontend | CRITICA |
| 3.3 | **Dashboard** — KPI cards com scores 0-1000, gauge visual, sparklines | Frontend | ALTA |
| 3.4 | **Ficha do imovel** — relatorio completo com todas as secoes | Frontend | ALTA |
| 3.5 | **Busca inteligente** — Command Palette (Cmd+K) + autocomplete | Frontend | ALTA |
| 3.6 | **Upload de geometria** — drag-drop shapefile/GeoJSON/CSV/KML | Frontend | MEDIA |
| 3.7 | **Time slider** — evolucao DETER/PRODES ao longo dos anos | Frontend | MEDIA |
| 3.8 | **Split view antes/depois** — comparacao de imagens satelite | Frontend | MEDIA |
| 3.9 | **PDF viewer + export** | Frontend | ALTA |
| 3.10 | **Tela de embargos** — lista, analise, prescricao, defesa | Frontend | ALTA |
| 3.11 | **Tela de credito** — calculadora de alongamento | Frontend | ALTA |
| 3.12 | **Tela de contratos** — templates, gerador, analise | Frontend | MEDIA |
| 3.13 | **Tela de checklists** — interativo com progresso | Frontend | MEDIA |

### FASE 4 — CANAIS E INTEGRACAO (3-5 dias)

**Objetivo:** Chegar no usuario onde ele esta.

| # | Tarefa | Tipo | Prioridade |
|---|---|---|---|
| 4.1 | **Bot WhatsApp** — consulta por CAR, alerta de embargos, status processo | Backend+Infra | ALTA |
| 4.2 | **Alertas por email** — novos embargos, vencimento de prazo, mudanca de status | Backend | MEDIA |
| 4.3 | **Monitoramento continuo** — webhook quando novo embargo/autuacao detectado | Backend | MEDIA |
| 4.4 | **API publica documentada** — para integracao com sistemas de clientes | Backend | MEDIA |

### FASE 5 — IA AVANCADA (5-7 dias)

**Objetivo:** Raciocinio auditavel e prospecao automatica.

| # | Tarefa | Tipo | Prioridade |
|---|---|---|---|
| 5.1 | **Raciocinio cite-to-source** — cada score explica seu raciocinio com fontes | Backend+IA | ALTA |
| 5.2 | **Teses aplicaveis automaticas** — dado um caso, listar teses com % exito | Backend+IA | ALTA |
| 5.3 | **Radar de prospecao** — buscar casos por tipo, regiao, prescricao proxima | Backend | MEDIA |
| 5.4 | **CRM Kanban** — gerenciar casos/teses em quadro visual | Frontend | MEDIA |
| 5.5 | **Analise preditiva** — risco de novo embargo baseado em historico da regiao | Backend+IA | MEDIA |

---

## ESTIMATIVA TOTAL

| Fase | Dias | Acumulado |
|---|---|---|
| Fase 0 — Fundacao | 2-3 | 2-3 |
| Fase 1 — Motor Juridico | 5-7 | 7-10 |
| Fase 2 — Contratos e Checklists | 3-5 | 10-15 |
| Fase 3 — Frontend Completo | 7-10 | 17-25 |
| Fase 4 — Canais | 3-5 | 20-30 |
| Fase 5 — IA Avancada | 5-7 | 25-37 |

**MVP competitivo (Fases 0-2):** ~15 dias
**Produto completo (Fases 0-5):** ~37 dias

---

## HANDOFF PARA PROXIMA SESSAO

### Arquivos criticos para ler primeiro
1. Este documento: `docs/ROADMAP_FASEADO_v1.md`
2. Contrato API: `docs/API_FRONTEND_CONTRACT.md`
3. Analise competitiva: `docs/ANALISE_COMPETITIVA_COMPLETA.md`
4. Inventario features: `docs/INVENTARIO_FEATURES.md`

### Onde estao os dados
- PostGIS: `postgresql://agrojus:agrojus@db:5432/agrojus` (59 tabelas)
- BigQuery: `basedosdados.br_sfb_sicar` (79.3M CARs)
- SIGEF downloads: `https://certificacao.incra.gov.br/csv_shp/zip/Sigef%20Brasil_{UF}.zip`

### Servicos rodando
```bash
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d
# Backend: http://localhost:8000
# Swagger: http://localhost:8000/docs
# PostGIS: localhost:5432
```

### ETLs pendentes
```bash
# SIGEF todos os estados (~1h)
docker exec agrojus-backend-1 python scripts/etl_sigef_download.py ALL

# SICAR BigQuery todos os estados (~4h)
docker exec agrojus-backend-1 python scripts/etl_sicar_bigquery.py ALL

# DETER/PRODES completos (precisa script novo — download shapefile TerraBrasilis)
```

### Decisoes pendentes do Eduardo
1. Criar conta MapBiomas Alerta (se nao for a mesma ja configurada)
2. Cadastro Embrapa AgroAPI (ZARC, ClimAPI) — gratuito
3. Cadastro Portal Transparencia API (CEIS, CNEP) — gratuito
4. Decisao: WhatsApp Business API via Twilio ou Meta Cloud API?
5. Decisao: IA para teses/scoring — usar Claude API ou OpenAI?

### Proxima sessao deve comecar por
**Fase 0.1** — Diagnosticar e consertar o mapa no frontend. Depois seguir Fase 1 (Motor Juridico).
