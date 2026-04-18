# AgroJus — Roadmap Consolidado (2026-04-18 · pós-Sessão 11)

> Atualizado após Sessão 11. Sincronizado com
> `docs/HANDOFF_2026-04-18_sessao11_INICIO.md` e
> `docs/HANDOFF_2026-04-18_sessao12_INICIO.md`.

## Estado atual do produto (pós-sessão 11)

| Camada | Completo | Parcial | Ausente |
|---|---|---|---|
| Backend | ~120 endpoints (26 routers) · 18 camadas PostGIS · DJEN · DataJud · Embrapa (7/9) · MapBiomas Alerta GraphQL · IBGE choropleth (16 métricas) · Webhooks CRUD + dispatch · Laudo PDF ficha · Exports GeoJSON/GPKG/SHP · Minuta Claude API · Dossiê multi-input · Hub Jurídico-Agro (12 endpoints, 75 seeds) · MCR 2.9 32 critérios · Portal Transparência + dados.gov.br (10 loaders) · **327 testes passando (Anti-Vibe Coding)** · **Alembic instalado** | MCR 2.9 (15/32 com dados reais) · SICAR MA-only (faltam 79M) · DETER/PRODES parcial (50k vs 800k+) | Motor jurídico STJ · leilões |
| Frontend | `/login`, `/`, `/mapa` v2.1, `/mercado`, `/processos`, `/publicacoes`, `/compliance` standalone, `/dados-gov`, `/dossie`, `/imoveis/[car]` 12/12 abas, `/juridico` 5 abas · **89 testes Vitest (75 lib + 14 components)** | `/consulta` e `/alertas` ainda mock | `/valuation`, `/portfolio`, `/leiloes`, `/minutas`, `/perfil`, `/plano`, `/equipe`, `/radar-ibama` |
| Dados | 40 tabelas × 8,5M registros · 822k Sprint 4 · 75 seeds jurídicos · webhooks + deliveries persistidos · **contract tests travam mudança de upstream (Portal Transparência pego)** | SICAR (só MA) · DETER/PRODES (50k vs 800k+) | Earth Engine · SIGMINE (ANM 502) · ANA Outorgas/BHO · Garantia-Safra · IBAMA CTF |
| Testes | **416 testes passing** · 162 unit + 27 integration + 10 contract + 89 frontend + 155 legacy · VCR cassettes · db_test isolado · Makefile · CI corrigido | 21 xfails legados documentados (sessão 12) | pytest integration schema snapshot · Playwright e2e · Storybook |
| Docs | ROADMAP · README · CHANGELOG · HANDOFF sessão 11 início + sessão 12 início · ANALISE_COMPETITIVA · ARCHITECTURE · API · PESQUISA_FONTES · PESQUISA_MERCADO · research/ · sessões 1-10 arquivadas | — | Manual do usuário · API pública doc |

---

## 8 Sprints (~43 dias) — progresso

### Sprint 1 — Ativação rápida (3 dias) ✅ **CONCLUÍDO**
Destravou múltiplas camadas com pouco código.
- [x] Descobrir paths Embrapa (via Swagger + OAuth2) — **7/9 APIs funcionais**
- [x] Coletor IBGE choropleth — **16 métricas ativas, 14 camadas saíram de stub**
- [x] Coletor IBAMA dados abertos — **16.121 autos carregados**
- [x] Coletor MapBiomas Alerta GraphQL — **JWT + query alerts por CAR**

### Sprint 2 — Ficha do imóvel `/imoveis/[car]` ✅ **12/12 ABAS CONCLUÍDAS**
A tela mais importante do produto está **completa**.
- [x] **Sprint 2a** — scaffold + 4 abas (Visão · Dossiê · Histórico · Agronomia)
- [x] **Sprint 2b** — +3 abas (Compliance · Clima · Jurídico)
- [x] **Sprint 2c** — +3 abas (Valuation · Logística · Crédito) + MapPreview header
- [x] **Sprint 2d** — ferramentas de mapa: point analysis + draw polygon + upload KML/GeoJSON + fix choropleth quintis
- [x] **Sprint 2e** (sessão 9) — **Monitoramento** (webhooks CRUD + dispatch async + logs) e **Ações** (laudo PDF reportlab + GeoJSON/GPKG/SHP via geopandas + minuta Claude API)

### Sprint Market ✅ **CONCLUÍDO (sessão 8)**
Tela `/mercado` reescrita com foco na UF do usuário + integração no mapa.
- [x] Collector Agrolink (13 commodities × até 26 UFs × até 265 meses)
- [x] `/mercado` UX centrada: UFPicker + cards por commodity + gráfico histórico
- [x] `/noticias` feed RSS agro (3 filtros: Todas · Mercado · Jurídico)
- [x] Widget "Colorir por preço" no mapa (10 camadas choropleth preço UF)
- [x] Zoom +/- no MapPreview (ficha do imóvel)
- [x] Remoção de todas as indicações de fonte no frontend

### Sprint 3 — Compliance MCR 2.9 expandido ✅ **CONCLUÍDO (sessão 9)**
De 6 para **32 critérios** auditáveis em 5 eixos.
- [x] Backend: 8 fundiários (CAR + SIGEF + TI + UC + SIGMINE + CCIR + ITR + SPU)
- [x] Backend: 8 ambientais (PRODES + DETER + MapBiomas + embargos + autos IBAMA + RL + APP + ANA)
- [x] Backend: 6 trabalhistas (MTE lista suja + CNDT + CAGED + eSocial + NR-31 + CIPATR)
- [x] Backend: 5 jurídicos (DataJud + DJEN + protestos + CNJ + execução fiscal)
- [x] Backend: 5 financeiros (SICOR + CEIS + CNEP + PIX + CCIR)
- [x] Frontend: `/compliance` com checklist interativo + laudo PDF
- [x] Integração com aba Compliance da ficha do imóvel

**Status dos 32 critérios** (pós-Sprint 3):
- 13 com dados reais integrados (41%) — verificação automática
- 19 com status `pending` aguardando Sprint 4 (dados.gov.br) e fontes que exigem integração adicional (CCIR, ITR, CNDT, CEIS/CNEP via Portal Transparência, protestos CENPROT, SPU, SIGMINE, etc.)

### Sprint 4 — 10 coletores dados.gov.br ✅ **CONCLUÍDO (sessão 9)**
Infraestrutura de ingestão + 2 ETLs reais executados.
- [x] Base clients CKAN + Portal Transparência
- [x] 12 modelos PostGIS + log de ingestão
- [x] 10 loaders unificados (sigmine · ana_outorgas · ana_bho · assentamentos · quilombolas · aneel_usinas · aneel_linhas · garantia_safra · ceis · cnep)
- [x] Script master com --all / --only / --status
- [x] Endpoints REST `/api/v1/dados-gov/*` (loaders, status, stats, run)
- [x] Página admin `/dados-gov` frontend com execução inline
- [x] **CEIS** populado com 3.000 registros reais
- [x] **CNEP** populado com 1.620 registros reais
- [x] MCR 2.9 — critérios F05, A08, FI02, FI03 consumindo dados reais

**Status dos loaders** (pós-iteração sessão 9):

| Loader | Status | Registros |
|---|---|---:|
| CEIS | ✅ ativo | 3.000 |
| CNEP | ✅ ativo | 1.620 |
| INCRA Assentamentos | ✅ ativo | 8.214 |
| INCRA Quilombolas | ✅ ativo | 427 |
| ANEEL SIGA usinas | ✅ ativo | 25.417 |
| ANEEL Linhas SIGET | ✅ ativo | 176 |
| IBAMA Termos de Embargo | ✅ ativo | 88.586 |
| **IBAMA Autos de Infração (SIFISC)** | ✅ ativo | **695.439** |
| SIGMINE | ❌ ANM em 502 (externo) | 0 |
| ANA Outorgas | ❌ sem URL CSV estável | 0 |
| ANA BHO | ❌ sem URL CSV estável | 0 |
| Garantia-Safra | ❌ token sem permissão CGU | 0 |
| IBAMA CTF | ❌ dataset específico não identificado | 0 |

**Total operacional**: **822.879 registros reais em 8/12 tabelas**. O fallback automático em `KNOWN_RESOURCES` permite que loaders pendentes sejam ativados adicionando URLs novas sem reescrever código.

### Sprint 5 — Mapa v3 ⏳ **SCAFFOLD PARCIAL (sessão 9)**
Escopo ampliado após feedback Eduardo.
- [x] Scaffold Zustand store + `useMapUrlSync` (commit `6ea730f`)
- [x] Fix UX do mapa: colapsar painel + zoom bottomright + minZoom menor
- [x] LayerInspector com copiar texto/JSON/GeoJSON/KML
- [x] StatsDashboard estilo MapBiomas (barras horizontais)
- [x] Export KML de AOI desenhada/upada
- [ ] Integrar Zustand store ao MapComponent (state → URL)
- [ ] Slider temporal duplo (YYYY-MM) para DETER/PRODES/MapBiomas
- [ ] Drill-down UF → Município (breadcrumb + fly-to)
- [ ] Opacidade individual por camada (slider)
- [ ] Tabs laterais (Camadas/Filtros/Mapa/Exportar)
- [ ] Export CSV/Shapefile da view atual

### Sprint Dossiê Agrofundiário ✅ **CONCLUÍDO (sessão 9)**
- [x] Service multi-input (CAR, GeoJSON, point+radius, bbox, município, CPF/CNPJ)
- [x] 12 coletores detalhados + análises cruzadas
- [x] PDF extenso (20-45 págs) com índice + análises + tabelas
- [x] Frontend `/dossie` com sidebar navegável + 6 personas
- [x] CTAs nos 3 pontos de entrada (LayerInspector, AnalysisDrawer, AcoesTab)

### Sprint Hub Jurídico-Agro ✅ **BACKEND (sessão 9) + FRONTEND (sessão 10) CONCLUÍDOS**
Reposicionamento do módulo jurídico — de "ferramenta para advogado" para hub multi-persona.
- [x] Models: ContratoAgroTemplate, TeseDefesaAgro, LegislacaoAgro, MonitoramentoParte
- [x] Seeds: 12 contratos + 12 teses + 51 normativos-chave
- [x] 12 endpoints REST
- [x] **Frontend `/juridico` com 5 abas** (Processos · Contratos · Teses · Legislação · Monitoramento) — sessão 10, commit `e9b1f26`, 2.710 linhas, 0 deps novas
  - Processos: dossiê consolidado por CPF/CNPJ + risco BAIXO/MÉDIO/ALTO/CRÍTICO + 6 KPIs
  - Contratos: grid filtrável + modal com preview markdown tempo real + exports .doc/.md/clipboard
  - Teses: 7 áreas + accordion lazy com argumentos/precedentes/próxima ação
  - Legislação: filtros UF/IBGE/tema/esfera + agrupamento + link oficial
  - Monitoramento: CRUD + form inline (6 eventos, 3 frequências, webhook)
- [ ] **Calculadora de prescrição administrativa** (concorrente consolidado — art. 1º Lei 9.873/99 e variantes estaduais)
- [ ] Editor de contrato com preenchimento guiado (vs templates estáticos)
- [ ] **Monitoramento ativo:** cron diário que verifica novas entradas IBAMA/CEIS/CNEP/DataJud para CPF cadastrados e dispara webhooks (escopo **Trilha 3** da sessão 11)
- [ ] Expandir base: +30 normativos estaduais · +20 teses · +15 contratos
- [ ] Upload de documento do usuário → OCR + análise de riscos
- [ ] IA sugere tese conforme descrição do caso

### Sprint 6 — Motor jurídico base (5 dias) ⏳
- [ ] STJ dados abertos + TCU webservice → tabela `jurisprudencia`
- [ ] Embedding bge-m3 (modelo em mia-project)
- [ ] Busca híbrida vetorial+textual
- [ ] Tela `/teses` com citações verificáveis (extensão do hub jurídico)
- [ ] **Cruzar jurisprudência com teses cadastradas** (enriquecimento automático de precedentes sugeridos)

### Sprint 7 — Gerador de minutas (7 dias) ⏳
- [ ] Claude API integration (já tem chave via ANTHROPIC_API_KEY)
- [ ] Redação com fundamentação alimentada por teses + legislação do hub
- [ ] Verificação anti-alucinação contra base jurisprudência
- [ ] Tela `/minutas` + export DOCX

### Sprint 8 — Agregador de leilões (10 dias) ⏳
- [ ] Scrapers (Caixa, Spy, Portal Leilão, TJs)
- [ ] Deduplicação + classificação rural
- [ ] Parser LLM edital (red flags)
- [ ] Enriquecimento geo (cruzar com dossiê)
- [ ] Timeline do lote (1ª → 2ª → 3ª praça)
- [ ] Alertas WhatsApp/email/webhook

---

## ✅ SESSÃO 11 REALIZADA — Fundação de testes Anti-Vibe Coding

Sprint dedicada a **disciplina**. Metodologia do Fabio Akita (Flow #588,
abr/2026 e The M.Akita Chronicles de fev/2026: 1.323 testes em 8 dias
controlando AI). Aplicamos ao AgroJus em uma sessão.

**Entregas:**
- **416 testes passing** em ~53s (antes: 0 novos nesta sessão)
- 162 unit + 27 integration + 10 contract + 89 frontend + 155 legacy
- Scaffold profissional: pytest.ini, conftest, VCR cassettes, Makefile,
  docker-compose.test.yml, CI fix (path `agrojus/backend` → `backend`)
- **Fix real entregue pelos contract tests**: Portal da Transparência
  renomeou `orgaoSancionador` → `fonteSancao`. Loader atualizado antes
  de virar bug silencioso.
- 21 testes legados marcados como `xfail` com motivo individual —
  dívida técnica visível e controlada
- `docs/` consolidada: coordination/plans → archive; ANALISE_v2 vira
  canônica; handoffs sessão 1-10 arquivados

**A sessão 11 NÃO consumiu** as trilhas B/C/F das prioridades. Focou 100%
em fundação de testes. Trilhas 1-3 do plano inicial continuam pendentes
e **agora podem ser executadas com segurança**: cada mudança vai quebrar
um teste se errar, cada bug vai virar um teste novo.

---

## 🎯 FOCO DA SESSÃO 12 — 3 Trilhas

Com fundação de testes pronta, agora executamos as 3 trilhas mantendo
TDD:

### 🔵 Trilha 1 — Acesso aos dados (prioridade máxima)
Ver Sprints A, B, C abaixo.

### 🟢 Trilha 2 — Limpar dívida documentada
- Atualizar os 21 testes legados em `LEGACY_XFAILS`
- Criar primeira migration Alembic versionada (schema snapshot atual)
- JWT em httpOnly cookie (hoje localStorage = risco XSS)
- Middleware auth frontend (`proxy.ts` no Next 16)
- Error boundaries (`app/error.tsx` + `app/global-error.tsx`)

### 🟠 Trilha 3 — Features com TDD
- Calculadora de prescrição administrativa (Lei 9.873/99) — pedido explícito
- Cron monitoramento contínuo de CPFs cadastrados
- Sprint 5 mapa v3 (Zustand + slider temporal + drill-down)
- Substituir mocks `/consulta` e `/alertas`

---

## 🎯 FOCO DA SESSÃO 11 (original, agora histórico) — 3 Trilhas

Eduardo decidiu priorizar: **pendências + dívida técnica + garantir acesso
aos dados**. Execução em 3 trilhas encadeadas, começando pela Trilha 1
(auditoria de dados).

### 🔵 Trilha 1 — Acesso aos dados (prioridade máxima)

**Sprint A · Auditoria e reparo de coletores** (1-2 dias)
- [ ] Varrer os 28 coletores: frescor (última execução), taxa de sucesso,
      contagem real vs esperada
- [ ] Re-testar token `dados.gov.br` (bug CloudFront 401 pode ter sido
      corrigido)
- [ ] Re-testar SIGMINE ANM (estava em 502 externo na sessão 9)
- [ ] Re-testar ANA Outorgas + ANA BHO (sem URL estável até sessão 9)
- [ ] Re-testar Garantia-Safra (token CGU sem permissão)
- [ ] Re-testar IBAMA CTF (dataset específico a identificar)
- [ ] Entregável: `docs/AUDITORIA_COLETORES_2026-04-18.md` com ranking de
      urgência e plano de reparo

**Sprint B · Cobertura nacional dos grandes** (3-5 dias)
- [ ] **SICAR nacional** — hoje só MA (faltam ~79M registros)
- [ ] **DETER/PRODES completo** — hoje 50k, deveria ser 800k+
- [ ] **IBAMA embargos** — confirmar atualização mensal (snapshot 88k)
- [ ] **ETL incremental** em todos (delta vs full reload)

**Sprint C · Novos coletores alto impacto** (5-7 dias)
- [ ] Scheduler (APScheduler in-container ou cron docker) para refresh
      automático
- [ ] Observability dos ETLs — `/dados-gov` expandido com gráficos
- [ ] Receita Federal QSA (Casa dos Dados grátis)
- [ ] Histórico MapBiomas 1985-atual

### 🟢 Trilha 2 — Dívida técnica crítica (em paralelo)

**Sprint D · Fundação** (2-3 dias)
- [ ] **Alembic migrations** — substitui `Base.metadata.create_all()` ad-hoc;
      bootstrap com snapshot do schema atual
- [ ] **JWT httpOnly cookie** — hoje em localStorage (risco XSS)
- [ ] **Middleware auth frontend** — no Next 16 o arquivo é `proxy.ts`
      (breaking v16), redirect para `/login` se sem cookie
- [ ] **Error boundaries** — `app/error.tsx` + `app/global-error.tsx`

**Sprint E · Testes mínimos** (3-5 dias)
- [ ] pytest + FastAPI TestClient para 4 endpoints críticos:
      `/property/search`, `/juridico/processos/{cpf}/dossie`, `/dossie`,
      `/compliance/mcr29/full`
- [ ] Vitest + React Testing Library para 3 componentes:
      `ProcessosTab`, `ContratosTab`, `MapComponent`
- [ ] CI GitHub Actions (lint + tsc + pytest)

### 🟠 Trilha 3 — Pendências frontend

**Sprint F · Sprint 5 mapa v3** (3-5 dias) — fecha o iniciado na sessão 9
- [ ] Integrar Zustand store ao `MapComponent` (scaffold existe)
- [ ] Slider temporal duplo (YYYY-MM) para DETER/PRODES/MapBiomas
- [ ] Drill-down UF → Município (breadcrumb + fly-to)
- [ ] Opacidade por camada
- [ ] Export CSV/Shapefile da view

**Sprint G · Substituir mocks**
- [ ] `/consulta` → usar `/property/search` real
- [ ] `/alertas` → usar tabela `environmental_alerts` populada

---

## Próximos Sprints e Ideias novas (pós-sessão 10)

### Sprint 9 — Dossiê Proativo + Monitoramento (~5 dias)
- [ ] Cron diário para monitoramento de partes cadastradas (CPF/CNPJ)
- [ ] Dashboard `/proprietarios/[cpf_cnpj]` com linha do tempo de eventos
- [ ] Webhook disparado a cada novo evento (auto IBAMA, CEIS, CNEP, DataJud, Lista Suja)
- [ ] Export Excel dos eventos para período selecionado
- [ ] Comparação A vs B entre dois CPF/CNPJ (due diligence rápida)

### Sprint 10 — Relatório Bancário (ESG + Basel IV) (~7 dias)
Padrões da indústria financeira:
- [ ] Template "Avaliação de Risco Agro" formato APRAER (CNA/Febraban)
- [ ] Score ESG do imóvel baseado em MCR 2.9 + MapBiomas + SICOR
- [ ] Exposure to deforestation (KPI Basel IV)
- [ ] Relatório ISSB/IFRS S2 (divulgação climática corporativa)

### Sprint 11 — Calculadoras e Ferramentas (~5 dias)
- [ ] **Calculadora de prescrição administrativa** (Lei 9.873/99 + estaduais)
- [ ] Calculadora de multas IBAMA (Dec 6.514/08) com atenuantes e agravantes
- [ ] Calculadora de ITR por hectare (com arbitramento e defesa)
- [ ] Simulador de crédito rural (PRONAF, PRONAMP, Moderinfra)
- [ ] Calculadora de Reserva Legal (% por bioma) com alertas de déficit
- [ ] Simulador de CRA (cota de reserva ambiental)
- [ ] Conversor de unidades rurais (alqueire, hectare, tarefa por estado)

### Sprint 12 — Integrações externas avançadas (~10 dias)
- [ ] **Receita Federal** (QSA via Receita B / Casa dos Dados)
- [ ] **ONR/cartórios** (matrículas via InfoSimples ou API própria)
- [ ] **CCIR/SNCR** (INCRA — após liberação do dados abertos)
- [ ] **SERPRO** (dados cadastrais premium)
- [ ] **SICAR oficial** (API para download de RL/APP detalhadas)
- [ ] **SIFISC** (embargos completos com geometria via API IBAMA)
- [ ] **LexML** scraping para enriquecer legislação agro municipal
- [ ] **Câmaras municipais** das top 100 cidades agrícolas

### Sprint 13 — Inteligência de Mercado Avançada (~7 dias)
- [ ] Basis regional (diferença entre praça e Chicago)
- [ ] Oferta x demanda por commodity por UF/região
- [ ] Alertas de arbitragem logística
- [ ] Índice de custos de produção (Confederação)
- [ ] Previsões climáticas → preços (modelo simples)
- [ ] Safras históricas vs projeção CONAB

### Sprint 14 — API Pública + Parcerias (~7 dias)
- [ ] Portal do Desenvolvedor (chave API + quotas)
- [ ] SDK Python + JavaScript
- [ ] Endpoints públicos read-only
- [ ] Parceria: Agrolink + AgroAgents + Syngenta + Yara + Bayer (integrações B2B)

### Sprint 15 — Mobile + PWA (~10 dias)
- [ ] PWA instalável com offline para dossiê baixado
- [ ] App React Native com câmera (fotografar infração)
- [ ] Geolocalização automática + criação de AOI por trilha
- [ ] Assinatura digital de contratos (ICP-Brasil)

---

## Ideias e pendências cross-cutting

### Jurídico-Agro (expansão)
- [ ] **Calculadora de prescrição administrativa** — pedido explícito do Eduardo. Modelar Lei 9.873/99 art. 1 (5 anos) + art. 21 (intercorrente 3 anos) + variações estaduais. Timeline visual. Alertas de prazo crítico.
- [ ] Editor guiado de contratos (substitui markdown estático por wizard)
- [ ] Assinatura ICP-Brasil / Gov.br dos contratos gerados
- [ ] Versionamento de contratos e teses (track changes legais)
- [ ] Upload de documento do usuário → OCR + análise de riscos (revisão de contrato de arrendamento)
- [ ] IA jurídica que sugere tese conforme descrição do caso
- [ ] Mapa de calor dos processos agro por município/tema

### Dossiê (expansão)
- [ ] Clima histórico completo (10 anos INMET) + projeção
- [ ] Embrapa ZARC integrado (aptidão por cultura/mês)
- [ ] Embrapa SmartSolos (análise de solo por ponto)
- [ ] Embrapa SITE (site de solo)
- [ ] Receita Federal QSA (se proprietário for PJ)
- [ ] Histórico de cobertura MapBiomas (1985-atual)
- [ ] NDVI temporal (SATVeg/Embrapa) para detectar degradação
- [ ] Comparação com imóveis vizinhos (benchmark)
- [ ] Projeção ESG (carbono armazenado, risco climático)

### Mapa v3 (pendentes do Sprint 5)
- [ ] Integrar Zustand store ao MapComponent
- [ ] Slider temporal duplo
- [ ] Drill-down UF → Município
- [ ] Opacidade por camada
- [ ] Tabs laterais
- [ ] Export CSV/Shapefile/PDF da view
- [ ] Comparação A/B de dois CARs lado a lado
- [ ] Modo de apresentação (tela cheia, sem menus)
- [ ] Captura de screenshot estilizada para compartilhamento

### Frontend (UX avançada)
- [ ] Tour guiado para novos usuários (onboarding)
- [ ] Favoritos (CARs e dossiês salvos)
- [ ] Histórico de consultas
- [ ] Compartilhamento de dossiê com permissão (link com expiração)
- [ ] Dashboard executivo (KPIs consolidados)
- [ ] Modo escuro/claro toggle completo
- [ ] Tema Gov.br opcional
- [ ] Notificações in-app (sino no TopBar)

### Backend (dívida técnica)
- [ ] OpenAPI codegen → types TypeScript (`openapi-typescript`)
- [ ] Integrar Zustand store já existente ao MapComponent
- [ ] Middleware auth frontend (`middleware.ts` Next)
- [ ] JWT httpOnly cookie (remover localStorage — XSS risk)
- [ ] Error boundaries (`app/error.tsx`)
- [ ] Testes Vitest + Playwright (mínimo MapComponent + PropertySearch + dossie + juridico)
- [ ] Storybook para design system
- [ ] **Alembic migrations** (substituir `create_tables` — dar previsibilidade a schema changes)
- [ ] Redis para rate_limiter + monitoring persistido
- [ ] Logger Sentry/Axiom + Analytics PostHog
- [ ] Background jobs com Celery (ETLs, monitoramento, webhooks)
- [ ] API de internacionalização (pt_BR / en_US / es_AR para América Latina)

### Coletores adicionais (backlog)
- [ ] SIGMINE ANM (aguardando servidor ANM voltar do 502)
- [ ] ANA Outorgas (scrape SNIRH GeoNetwork)
- [ ] ANA BHO (idem)
- [ ] Garantia-Safra (API Portal Transparência com upgrade de plano)
- [ ] IBAMA CTF (dataset específico a identificar)
- [ ] NDVI SATVeg (Embrapa)
- [ ] ONR matrículas (InfoSimples pago)
- [ ] SNCI legado
- [ ] SPU Terras União
- [ ] ZEE por estado (9 UFs distintas)
- [ ] ANAC aeroportos
- [ ] Terminais intermodais ANTT/ANTAQ
- [ ] CNT condição rodovias

### Compliance (expansão)
- [ ] Integrar 19 critérios ainda pending do MCR 2.9 (CCIR, ITR, CNDT, protestos, etc.)
- [ ] EUDR estendido (datas de abate, rastreabilidade, due diligence statement)
- [ ] Certificações privadas (RTRS, Bonsucro, Rainforest Alliance, Round Table Responsible Soy)
- [ ] ISO 14001 compliance check

### Produto / Negócio
- [ ] Planos (free/pro/enterprise) com limites diferenciados
- [ ] Billing Stripe / Mercado Pago
- [ ] Multi-tenant (workspaces para escritórios e cooperativas)
- [ ] Whitelabel (opção de revender com marca própria)
- [ ] Marketplace de laudos (compre dossiês gerados por terceiros)
- [ ] Seguro rural integrado (alertas de risco → cotação)

### Dados
- [ ] ETL incremental (delta vs full reload)
- [ ] Observability dos ETLs (Grafana)
- [ ] Data lake S3 (backup de todas as ingestões)
- [ ] Versionamento dos datasets (snapshot mensal)

---

## Métricas de sucesso

| Fase | Objetivo | Status |
|---|---|---|
| Sprint 1-2 | Ficha do imóvel funcional com score de compliance | ✅ (10/12 abas + toolbar mapa + MapPreview) |
| Sprint Market | /mercado regionalizado + notícias + choropleth de preço | ✅ (13 commodities × 26 UFs) |
| Sprint 3-5 | 50+ camadas ativas + mapa v3 | 42 ativas (35%) · quintis ✅ · AOI custom ✅ · preço UF ✅ |
| Sprint 6-8 | Produto demonstrável end-to-end: motor jurídico + leilões + webhook | ⏳ |
| Longo prazo | 100% das 119 camadas ativadas ou marcadas "não viáveis sem parceria" | ⏳ |

---

## Decisões técnicas já tomadas (não questionar sem motivo plausível)

- Monolítico modular em FastAPI
- PostGIS 3.4 com GIST em todas geometrias
- SQLAlchemy 2.0 sync (não async) — simplicidade
- JWT stateless (localStorage dev, httpOnly cookie em prod)
- Cache SHA256 em disco com TTL 24h padrão
- Materialized view para dashboard
- Next.js App Router com grupo `(dashboard)`
- Tailwind v4 + shadcn/ui
- react-leaflet 5 + CARTO Dark default
- SWR 2.4 para data fetching
- Docker Compose 2 containers + volume named `agrojus_pgdata`

---

*Documento vivo. Atualizar ao fim de cada sprint.*
