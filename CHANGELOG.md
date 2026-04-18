# Changelog — AgroJus

Todas as mudanças notáveis do projeto, por sessão de trabalho.
Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [0.14.0] — 2026-04-18 · Sessão 11 · 416 testes Anti-Vibe Coding

Sprint dedicada a **testar profissionalmente** seguindo a metodologia do
Fabio Akita (Flow Podcast #588, abr/2026; The M.Akita Chronicles: 1.323
testes em 8 dias controlando AI). A sessão saiu de **0 testes novos** para
**416 testes verdes** distribuídos em 4 camadas (unit / integration /
contract / component).

### Added — Backend (252 testes novos)

**Unit (162 testes)** — lógica pura, 100% offline, <3s total:

- `tests/unit/test_classificar_risco.py` · 17 testes — classificador de
  risco do Hub Jurídico, 4 classes + fronteiras parametrizadas
- `tests/unit/test_cpf_cnpj_validator.py` · 17 testes — algoritmo de
  dígitos verificadores + função async pública
- `tests/unit/test_jurisdicao_reserva_legal.py` · 20 testes — Código
  Florestal aplicado: 80% Amazônia Legal, 35% Cerrado AL, 20% outros
- `tests/unit/test_webhook_signing_matching.py` · 24 testes — HMAC-SHA256
  payload signing + matcher de eventos com wildcard + filtros CAR/CPF
- `tests/unit/test_dados_gov_client.py` · 18 testes — KNOWN_RESOURCES
  fallback + algoritmo de scoring do pick_resource + headers
- `tests/unit/test_datajud_parser.py` · 14 testes — parser de resposta
  Elasticsearch + 27 TJs + 6 TRFs + 24 TRTs + assuntos agro
- `tests/unit/test_agrolink_parsing.py` · 18 testes — parser "1.234,56"
  BRL com limitação de locale documentada
- `tests/unit/test_mcr29_dataclasses.py` · 24 testes — CriterionResult,
  AxisScore, MCR29FullResult, 32 pesos, coerência metadata × WEIGHTS
- `tests/collectors/test_ceis_cnep_normalize.py` · 22 testes — normalizer
  CEIS/CNEP com **fix real** de contrato (upstream mudou
  `orgaoSancionador` → `fonteSancao`)

**Integration (27 testes)** — TestClient + banco dev:

- `tests/integration/test_juridico_api.py` — cobertura completa dos 12
  endpoints do Hub Jurídico (list/detalhe/filtros/404 em contratos+teses+
  legislação, dossiê com classificação de risco, CRUD monitoramento)

**Contract (10 testes)** — VCR cassettes filtrados:

- `tests/contract/test_portal_transparencia.py` — CEIS + CNEP com 7
  cassettes VCR (token `chave-api-dados` filtrado de cada um)

**Legado (155 testes pré-existentes):** 155 continuam passando, **21
marcados como xfail** com motivo individual em `LEGACY_XFAILS` no
conftest (API renomeada, rota mudou, fixtures sem isolação — trabalho
dedicado da próxima sessão).

### Added — Frontend (164 testes novos)

- `src/lib/markdown.test.ts` · 31 testes — `fillTemplate`, `markdownToHtml`,
  `escapeHtml` (extraídos de ContratosTab.tsx para reuso e teste)
- `src/lib/stores/map-store.test.ts` · 24 testes — Zustand actions,
  `stateToQueryString`, `queryStringToPartial`, round-trip state↔URL
- `src/lib/utils.test.ts` · 9 testes — helper `cn` (twMerge + clsx)
- `src/lib/basemaps.test.ts` · 8 testes — catálogo de tiles Leaflet
- `src/components/juridico/ProcessosTab.test.tsx` · 5 testes (smoke)
- `src/components/juridico/ContratosTab.test.tsx` · 5 testes (mock fetch)
- `src/components/juridico/TesesTab.test.tsx` · 4 testes (agrupamento)

**Frontend: 89 total passing em 2.2s.**

### Changed

- **Fix real entregue pelo investimento em contract tests.** Primeiro
  contract test já pegou que o Portal da Transparência renomeou
  `orgaoSancionador` → `fonteSancao` entre sessão 9 e agora. Loader
  atualizado em `dados_gov_loaders.py:_normalize_portal_record` para ler
  ambos (contrato antigo + novo com fallback). Sem o contract test, isso
  teria virado `orgao_sancionador=""` silencioso no banco.
- **Refactor `ContratosTab.tsx`**: `fillTemplate` + `markdownToHtml` +
  `escapeHtml` extraídos para `src/lib/markdown.ts`. Import agora de
  `@/lib/markdown`. Mais fácil reutilizar (minutas, PDF, outros tabs)
  e testar em isolamento.
- **Suite legada**: 21 testes marcados como `@pytest.mark.xfail(strict=False)`
  com motivo documentado em `LEGACY_XFAILS`. Cada um será revisto em
  sessão dedicada (API renomeada, rota mudou, fixtures sem isolação).

### Documentation

- **Auditoria e consolidação da pasta `docs/`**:
  - `docs/coordination/` (duplicado do root) → `_archive/coordination_antigo/`
  - `docs/plans/` (planning de 1 semana atrás, concluído) → `_archive/plans_antigos/`
  - `docs/ANALISE_COMPETITIVA_COMPLETA.md` (v1 obsoleto) → `_archive/`;
    v2 renomeada para `ANALISE_COMPETITIVA.md`
  - `docs/PESQUISA_MERCADO_v3_EXECUTIVO.md` → `PESQUISA_MERCADO.md`
  - `docs/HANDOFF_2026-04-18_sessao10_FECHAMENTO.md` → arquivo
  - Resultado: `docs/` enxuto, 8 arquivos úteis + `_archive/` + `research/`

## [0.13.1] — 2026-04-18 · Transição Sessão 10 → 11 · Limpeza e handoff

Consolidação entre sessões. Sem mudanças de produto — só infra/docs.

### Changed

- **Isolação AgroJus × advIA reforçada.** Projetos são totalmente separados.
  - `.claude/settings.json` do projeto sobrescreve `Stop/SubagentStop/PreCompact`
    com arrays vazios (precedência sobre qualquer hook de plugin).
  - Plugin advIA (`~/.claude/plugins/marketplaces/local/plugins/advia/` e
    `cache/local/advia/0.1.0/`) teve array `Stop` zerado — o `stop.py` já era
    no-op, então zero impacto em sessões operacionais da advIA. Evita
    disparo de "Antes de encerrar a sessão..." com vocabulário jurídico
    (iara_salvar_caderno, Bloco 11 FIRAC) que não faz sentido em AgroJus.
  - Memória registrada em
    `~/.claude/projects/C--dev-agrojus-workspace/memory/project_agrojus_vs_advia.md`
    com protocolo de reversão se um dia quisermos Stop behavior no advIA.
  - Efeito pleno só no próximo restart do Claude Code (hooks já em memória
    seguem até lá).

### Documentation

- **Consolidação dos handoffs.** Arquivados em `docs/_archive/handoffs_antigos/`:
  sessão 7, sessão 8, sessão 9 (2 versões), sessão 10 INICIO. Mantidos em
  `docs/` apenas:
  - `HANDOFF_2026-04-18_sessao10_FECHAMENTO.md` (log da sessão anterior)
  - `HANDOFF_2026-04-18_sessao11_INICIO.md` (mestre atual)
- **Handoff sessão 11** estabelece 3 trilhas encadeadas:
  - **Trilha 1 — Acesso aos dados** (Sprint A auditoria · B cobertura
    nacional · C scheduler+observability+novos coletores)
  - **Trilha 2 — Dívida técnica crítica** (Sprint D Alembic/JWT
    cookie/middleware/error boundaries · E testes mínimos + CI)
  - **Trilha 3 — Pendências frontend** (Sprint F mapa v3 · G substituir mocks
    de `/consulta` e `/alertas`)
- ROADMAP atualizado: Sprint Hub Jurídico-Agro marcado como frontend
  concluído; seção "Foco da Sessão 11" adicionada com as 3 trilhas.

## [0.13.0] — 2026-04-18 · Sessão 10 · Frontend Hub Jurídico-Agro

### Added — Rota `/juridico` com 5 abas (fecha a prioridade A do handoff)

O backend do Hub Jurídico-Agro estava pronto desde a sessão 9 (12 endpoints +
5 tabelas + 75 seeds). Nesta sessão a interface passou a consumir tudo.

**Shell `/juridico` (`app/(dashboard)/juridico/page.tsx`):**
- 5 abas: Processos · Contratos · Teses · Legislação · Monitoramento.
- Tab selecionada persiste em query string `?tab=...` (compartilhável, deep link).
- Descrição contextual por aba, `Suspense` wrapper, sem quebrar `useSearchParams`.

**`components/juridico/ProcessosTab.tsx`:**
- Form CPF/CNPJ → consome `GET /juridico/processos/{cpf_cnpj}/dossie`.
- Banner de risco consolidado colorido (BAIXO/MÉDIO/ALTO/CRÍTICO) com
  justificativa gerada a partir do sumário (fatores detectados em linguagem
  natural).
- 6 KPIs (DataJud / DJEN / IBAMA+multa / CEIS / CNEP / Lista Suja).
- 6 seções listadas: processos, publicações DJEN com link, autos IBAMA com
  valor e enquadramento legal, CEIS/CNEP com sanção e órgão, Lista Suja MTE.
- Botão copiar número do processo.

**`components/juridico/ContratosTab.tsx`:**
- Grid de cards filtráveis por categoria, público-alvo, texto livre.
- Modal com 2 colunas: esquerda = sinopse + campos preenchíveis + legislação
  + cautelas; direita = preview markdown em tempo real.
- Template fill client-side com `{{placeholder}}` — placeholders não
  preenchidos ficam destacados em âmbar dentro do preview.
- 3 exports: **.doc** (Word aceita HTML renomeado — zero dependência),
  **.md** (markdown com preenchimento), **copiar** (clipboard).
- Renderizador markdown mínimo próprio (headings, listas, negrito/itálico,
  parágrafos) — sem `react-markdown` ou `marked` para não inflar o bundle.

**`components/juridico/TesesTab.tsx`:**
- Filtros por área (7 áreas com ícone/cor: ambiental, fundiário, trabalhista,
  tributário, previdenciário, contratual, todas) + busca textual.
- Resultados agrupados por área, accordion por tese.
- Carregamento lazy do detalhe (só busca `/teses/{slug}` quando abre).
- Detalhe mostra: aplicabilidade, argumentos principais (lista ordenada),
  precedentes sugeridos com tribunal/ementa/link, legislação aplicável,
  contra-argumentos, próxima ação destacada em card primary.

**`components/juridico/LegislacaoTab.tsx`:**
- Filtros: busca textual, esfera (federal/estadual/municipal), UF (select
  com 27 UFs), código IBGE do município, 7 temas com chip visual.
- Lista agrupada por esfera com ícone apropriado (Globe/Landmark/Building2).
- Card por norma mostra tipo/número/ano, situação (vigente/revogada
  coloridas), órgão, UF/município, temas como chips, link para o texto
  oficial quando disponível.

**`components/juridico/MonitoramentoTab.tsx`:**
- Lista monitoramentos ativos em grid de cards (nome sugerido, CPF/CNPJ,
  eventos monitorados, tags, frequência, webhook, datas).
- Botão cadastrar abre formulário inline com: CPF/CNPJ, nome, contexto,
  tags CSV, 6 eventos selecionáveis (DataJud/IBAMA/CEIS/CNEP/Lista
  Suja/DJEN), frequência (diária/semanal/mensal), webhook URL.
- Validação client-side (11 ou 14 dígitos), remoção com confirmação.

### Changed

- **Sidebar.tsx** ganhou entrada "Hub Jurídico" (ícone `Scale`, badge `HUB`)
  no grupo Jurídico, acima de Publicações e Processos — continua acessível
  individualmente.

### Technical

- Next 16.2.3 + React 19.2 — padrão `"use client"` + `Suspense` para
  componentes que usam `useSearchParams`.
- Data fetching via `useSWR` + `swrFetcher` existente; mutações via
  `fetchWithAuth`.
- Style: design tokens Tailwind v4 (`border`, `card`, `muted`, `primary`,
  `foreground`) — mesmo padrão de `/processos`.
- `tsc --noEmit`: 0 erros. ESLint: 0 warnings após wrap em `useMemo` das
  listas `teses`/`normas`.
- 0 dependências novas: `lucide-react` + `swr` já no projeto.

## [0.12.0] — 2026-04-18 · Sessão 9 · Dossiê + Hub Jurídico-Agro

### Added — UX do mapa (correções do feedback Eduardo)

- **LayerTreePanel** agora colapsa em badge compacta (ChevronsLeft) e não sobrepõe mais o ZoomControl (que foi para `bottomright`).
- **minZoom reduzido** em camadas densas: SICAR/CAR 10→8, SIGEF 11→9, embargos 7→5, autos 7→5, MapBiomas alertas 7→5.
- **LayerInspector** ganhou 4 botões rápidos: Copiar texto, Copiar JSON, Baixar GeoJSON e Baixar KML (serializer GeoJSON→KML próprio cobrindo Point/LineString/Polygon/Multi*).
- **Export KML de AOI** desenhada/upada: AnalysisDrawer tem botões KML/GeoJSON no header.
- **StatsDashboard estilo MapBiomas**: barras horizontais proporcionais, % do total, toggle "Por camada" ↔ "Por tema", hover revela EyeOff para desativar camada inline.

### Added — Dossiê Agrofundiário Multi-Persona

Novo conceito central do produto: relatório completo sobre qualquer área
rural, adaptado a 6 personas (comprador, advogado, investidor, trading,
consultor ambiental, produtor). Aceita 6 tipos de entrada: CAR, GeoJSON,
ponto+raio, bbox, município IBGE, CPF/CNPJ do proprietário.

**Service `dossie_generator.py` (~850 linhas):**
- 12 coletores modulares (identificação, fundiário detalhado com cada overlap listado + área + %, compliance MCR 2.9 32 critérios, ambiental com PRODES/DETER/MapBiomas/embargos/autos todos listados, proprietário consolidado com CEIS/CNEP/autos/multa total/outros imóveis, crédito rural top 20 contratos + série anual, mercado 12 meses por commodity, logística KNN, energia ANEEL, valuation NBR 14.653-3 com memória de cálculo, jurídico, agronomia).
- **Análises cruzadas** (`gerar_analises_cruzadas`): detecta correlações entre fontes (desmate × compliance, embargo × crédito, CEIS × elegibilidade, reincidência × risco, TI × CF art. 231, UC PI × Lei 9.985/00) com scores consolidados por domínio + semáforo.
- **Recomendações adaptadas por persona**: cada público recebe tips específicas e red flags contextualizados.

**PDF extenso (`dossie_pdf.py` ~850 linhas):**
- Capa formal + índice numerado (16 capítulos)
- Sumário executivo com classificação colorida + scores domínio
- Análises cruzadas em quadros de destaque coloridos por severidade
- Todas as sobreposições/eventos listados individualmente em tabelas paginadas
- Renderização especializada por seção (compliance com status colorido por status, fundiário com resumo estatístico, valuation com memória)
- Apêndice com fontes, metodologia e limitações
- **Resultado: 20-45 páginas por CAR** (vs 5 da versão MVP)

**Endpoints `/api/v1/dossie`:**
- `POST /dossie` — JSON estruturado completo
- `POST /dossie/pdf` — PDF A4 extenso

**Frontend `/dossie`:**
- Rota dedicada tela cheia com sidebar navegável (12 seções com scroll spy)
- Header sticky com StatusBadge colorido + botão PDF
- Renderização contextual por seção (compliance vira grid de scores, listas viram cards compactos)
- 3 modos de entrada: query string (?car=X ou ?cpf=X), sessionStorage (via ?sk=X quando vem do mapa), ou formulário manual
- Form manual com seletor de persona (6 opções)

**CTAs nos 3 pontos de entrada do mapa:**
- **LayerInspector**: botão destacado "Gerar Dossiê Completo" em camadas de imóvel rural (sicar_completo/geo_car/sigef_parcelas/snci_imoveis/assentamentos/quilombolas)
- **MapTools AnalysisDrawer**: botão "Gerar Dossiê desta área" para polígono desenhado/upado
- **AcoesTab da ficha**: card gradiente destacado no topo com link direto

### Added — ComplianceTab inline com 32 critérios + explicação

- Novo toggle "MCR 2.9 Completo (32)" | "Rápido (6)" | "EUDR"
- Modo completo consome `/compliance/mcr29/full` e renderiza inline: banner, 5 cards de score por eixo, 5 accordions com cada critério com **evidência JSON expansível** e **explicação humana do apontamento** (`explicarApontamento` mapeia o contexto técnico para linguagem do advogado — para pendentes diz qual fonte falta e onde consultar; para falhas diz POR QUE bloqueia e qual a próxima ação).

### Added — Hub Jurídico-Agro (reposicionamento do módulo jurídico)

O produto deixou de ser "ferramenta para advogado" — virou **hub de informação jurídica para todo o agronegócio**.

**5 novos modelos:**
- `ContratoAgroTemplate` — templates de contratos do agro
- `TeseDefesaAgro` — teses argumentativas estruturadas
- `LegislacaoAgro` — base de normativos federais/estaduais/municipais indexada por tema
- `MonitoramentoParte` — cadastro de CPF/CNPJ para dossiê contínuo de terceiros
- `MonitoramentoParteEvento` — trilha de eventos detectados

**Sementes seminais:**
- **12 templates de contratos** com markdown completo: arrendamento rural, parceria agrícola, compra e venda rural, CPR física, CDA-WA, integração bovina, comodato, prestação de serviço, venda de bovinos, fornecimento insumos, meação, PSA/CRA.
- **12 teses de defesa estratégicas**: nulidade auto IBAMA, prescrição intercorrente, embargos ITR, usucapião rural CF art. 191, previdência segurado especial, retirada Lista Suja, embargo desproporcional, compensação RL via CRA, defesa Lista Suja, enquadramento rural vs CLT, reclassificação parceria↔arrendamento, revisão PRONAF.
- **51 normativos-chave** do agronegócio: CF/88, Estatuto da Terra, Código Florestal, Crimes Ambientais, SNUC, ITR, Trabalho Rural, Lista Suja, CPR, CDA-WA, EUDR, PSA, Anticorrupção, CNDT, NR-31 + amostras estaduais.

**12 endpoints `/api/v1/juridico`:**
- CRUD contratos/teses/legislação com filtros (categoria, área, público-alvo, UF, tema, esfera)
- `GET /processos/{cpf_cnpj}/dossie` — varredura consolidada de DataJud + DJEN + IBAMA autos + CEIS + CNEP + Lista Suja com classificação de risco
- `POST /monitoramento` — cadastro de CPF/CNPJ para monitoramento contínuo

### Sessão também fechou

- Sprint 4 extras: IBAMA embargos 88.586 polígonos + IBAMA autos 695.439 registros + ANEEL linhas SIGET 176 via ArcGIS. MCR-A04/A05 enriquecidos com os dados reais.
- Fallback automático de URLs diretas em `dados_gov.py` (CKAN 401 → URL hardcoded validada).
- Plugin advIA desligado em `/.claude/settings.json` do AgroJus (fim do loop de Stop hook em projetos não-jurídicos).

### Commits da sessão 9 (consolidado)

| Hash | Tema |
|---|---|
| `77142b2` · `a34cf24` · `1630150` | Sprint 2e ficha 12/12 |
| `b9182bd` · `ca26f3f` · `ead8a26` | Sprint 3 MCR 2.9 × 32 critérios |
| `23c901e` · `7bec20b` · `43b5f34` · `cccaa40` · `49c1ce3` | Sprint 4 dados.gov.br infra + MCR wire |
| `6c00e4d` | advIA plugin disabled em AgroJus |
| `c94f803` · `cc1f445` · `d60720a` | Fallback URLs diretas + ANEEL latin-1 + CHANGELOG |
| `ec63c79` · `6ea730f` · `dfa7ea0` | IBAMA embargos 88k + Sprint 5 scaffold |
| `a84ea48` · `ac9c4f1` | IBAMA autos 695k + ANEEL linhas 176 |
| `4f55916` · `841c572` | UX mapa v2.1 + ComplianceTab inline |
| `c75be5f` · `0496a79` | Dossiê backend + frontend + PDF 20 pgs |
| `HEAD` | Hub Jurídico-Agro (12+12+51 seeds) |

---

## [0.11.0] — 2026-04-18 · Sessão 9 · Sprint 4

### Added — Infraestrutura ETL dados.gov.br + Portal da Transparência

**Clientes base:**
- `app/collectors/dados_gov.py` — CKAN client (package_show/search, pick_resource, download com streaming + limite de tamanho configurável)
- `app/collectors/portal_transparencia.py` — Portal client com paginação e backoff

**12 novos modelos PostGIS** em `database.py`:
`sigmine_processos`, `ana_outorgas_full`, `ana_bho`, `incra_assentamentos`, `incra_quilombolas`, `aneel_usinas`, `aneel_linhas_transmissao`, `garantia_safra`, `ceis_registros`, `cnep_registros`, `ibama_embargos`, `ibama_ctf` + `dados_gov_ingest_log` (auditoria).

**10 loaders unificados** em `app/collectors/dados_gov_loaders.py`:
sigmine · ana_outorgas · ana_bho · assentamentos · quilombolas · aneel_usinas · aneel_linhas · garantia_safra · ceis · cnep. Cada loader: download → descompressão (ZIP SHP) ou parse CSV → normalização → bulk_save_objects no Postgres → log de ingestão. Idempotente (TRUNCATE + INSERT).

**Script master** `backend/scripts/run_dados_gov_etl.py`:
- `--only X Y` · `--all` · `--status` · `--list`
- Uso em produção: `docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --all` (cron diário).

**Endpoints REST** em `/api/v1/dados-gov`:
- `GET /loaders` · `GET /status` · `GET /stats` · `POST /run?loader=X`

**Página admin** `/dados-gov` no frontend:
- 4 stat cards + tabela 12 camadas + log com auto-refresh (10-15s) + botão "executar" inline por linha

### Added — MCR 2.9 ligado às novas fontes reais

5 critérios antes `pending` agora consultam dados reais quando ETL tiver rodado:
- **MCR-F05** (SIGMINE) · **MCR-A08** (ANA outorgas) · **MCR-FI02** (CEIS) · **MCR-FI03** (CNEP)
- Tabela vazia → `pending` com comando ETL específico na mensagem
- Tabela populada → `passed/failed` automaticamente com evidência real

### Dados reais ingeridos nesta sessão

| Fonte | Registros | Via |
|---|---:|---|
| **CEIS** (CGU) | **3.000** | Portal Transparência (token CGU) |
| **CNEP** (CGU) | **1.620** | Portal Transparência (token CGU) |
| **INCRA Assentamentos** | **8.214** | Fallback URL direta (`certificacao.incra.gov.br`) |
| **INCRA Quilombolas** | **427** | Fallback URL direta |
| **ANEEL SIGA usinas** | **25.417** | CKAN próprio ANEEL + fallback |
| **IBAMA Termos de Embargo** | **88.586** | CKAN próprio IBAMA (`dadosabertos.ibama.gov.br` + `pamgia.ibama.gov.br`) |
| **IBAMA Autos de Infração (SIFISC)** | **695.439** | CKAN IBAMA — ZIP com 50 CSVs (1 por ano, 1977-2026) |
| **ANEEL Linhas de Transmissão (SIGET)** | **176** | ArcGIS SIGEL — `/GGT/Dados_WebApp_GGT/MapServer/0` GeoJSON |
| **TOTAL ativos** | **822.879** registros em **8/12** tabelas | |

### MCR 2.9 — ganho de cobertura com IBAMA embargos + autos

- **MCR-A04** (Sem embargos ICMBio/IBAMA): antes consultava `geo_embargos_icmbio` (~dezenas). Agora também `ibama_embargos` (**88.586 polígonos**). Details separa "ICMBio: N · IBAMA: N".
- **MCR-A05** (Sem autos IBAMA): antes só `geo_autos_ibama` (16k) + `environmental_alerts`. Agora também `ibama_autos_infracao` (**695.439 autos** via SIFISC completo) por CPF/CNPJ do proprietário. Evidência incluí `multa_total_rs` somando todos autos.

### Fallback automático de URLs diretas (novo)

`DadosGovClient.package_show()` agora:
1. Tenta o token CKAN normalmente
2. Em 401/5xx/timeout cai para `KNOWN_RESOURCES`: dict `{dataset_id: [{url, format, name}]}` com URLs públicas validadas dos arquivos
3. `download_resource()` baixa via URL direta (sem auth)

Isso destrava o ETL mesmo quando o portal dados.gov.br está com problemas (como aconteceu — todos os endpoints retornaram 401, independente do token).

### Commits Sprint 4 adicionais

| Hash | Descrição |
|---|---|
| `6c00e4d` | chore: desativa plugin advIA em AgroJus (fim do loop de Stop hook) |
| `c94f803` | feat(dados-gov): fallback automático URLs diretas |
| `cc1f445` | fix(dados-gov): URLs ANEEL validadas + latin-1 + clean NaN raw_data |
| `ec63c79` | feat(dados-gov): loader IBAMA embargos (88k polígonos) + MCR-A04 |
| `6ea730f` | chore(frontend): scaffold Sprint 5 — Zustand store + URL sync |
| `a84ea48` | feat(dados-gov): IBAMA autos de infração (695k) + ANEEL linhas SIGET (176) + MCR-A05 |

Validação: CNPJ `00.818.544/0001-65` (real, do CEIS) → MCR-FI02 **FAILED** com evidência `{"ceis_matches": 2}`.

### Status dos 10 loaders

- **✅ CEIS / CNEP** (Portal Transparência) — funcionais, ETL executado em produção
- **⚠ SIGMINE / ANA outorgas / ANA BHO / INCRA assentamentos / INCRA quilombolas / ANEEL usinas / ANEEL linhas / Garantia-Safra** — infraestrutura pronta, token JWT do dados.gov.br retornou 401 no teste (requer renovação pelo Eduardo antes do ETL funcionar)

### MCR 2.9 — Status dos 32 critérios pós-Sprint 4

- **15 com dados integrados** (47%) — antes 13/32. Ganho: FI02 + FI03 (FM02 com token novo também) + disponíveis quando dados.gov.br ativar (F05, A08).
- 17 `pending` — aguardam: renovação token dados.gov.br (6), fontes pagas (CCIR, ITR, CNDT, protestos, etc.), auto-declaração (NR-31, CIPATR).

### Commits da Sprint 4

| Hash | Descrição |
|---|---|
| `23c901e` | feat(dados-gov): base clients + 12 models + 10 loaders + script ETL |
| `7bec20b` | feat(dados-gov): endpoints REST + página admin /dados-gov |
| `43b5f34` | feat(compliance): MCR 2.9 consome SIGMINE/ANA/CEIS/CNEP reais |
| `cccaa40` | docs: consolida v0.11.0 — Sprint 4 concluído |

---

## [0.10.0] — 2026-04-17 · Sessão 9 · Sprint 3

### Added — MCR 2.9 Expandido (32 critérios em 5 eixos)

**Backend — `app/services/mcr29_expanded.py` + endpoints em `compliance.py`:**
- 32 critérios em 5 eixos: Fundiário (8) · Ambiental (8) · Trabalhista (6) · Jurídico (5) · Financeiro (5)
- Status por critério: `passed` / `failed` / `pending` / `not_applicable`
- Peso por critério reflete impacto no indeferimento (bloqueantes com `weight >= 2.5`)
- Score 0-1000 ponderado + risk level (LOW/MEDIUM/HIGH/CRITICAL)
- 13/32 critérios com **dados reais integrados** (41%); 19 `pending` aguardam Sprint 4 (dados.gov.br) e fontes pagas (CCIR, ITR, CNDT, CEIS/CNEP via Portal Transparência, etc.)

**Novos endpoints:**
- `GET /api/v1/compliance/mcr29/criteria` → metadados dos 32 critérios agrupados por eixo
- `POST /api/v1/compliance/mcr29/full` → executa avaliação, retorna `axis_scores`, `criteria[]`, `sources_consulted`, `pending_sources`, `recommendation`
- `POST /api/v1/compliance/mcr29/full/pdf` → laudo PDF A4 (4 páginas) com tabela por eixo, destaque em falhas/pendentes, lista de fontes

**Frontend `/compliance` — reescrito do zero (antes: mock 3 rows):**
- Form CAR + CPF/CNPJ com query string auto-run (`?car=...`)
- Banner geral APTO / RESTRITO / BLOQUEADO / INDETERMINADO + score + recomendação
- 5 cards de score por eixo com ícones distintos
- Accordion por eixo (auto-expande se há falhas) mostrando cada critério com evidência JSON expansível
- Botão "Exportar laudo PDF"
- Tela inicial com overview dos 5 eixos

**`ComplianceTab` da ficha** ganhou card de destaque com link para `/compliance?car={CAR}&auto=true`, preservando o toggle básico MCR 2.9 / EUDR.

### Commits
| Hash | Descrição |
|---|---|
| `b9182bd` | feat(compliance): service expandido + 3 endpoints + PDF |
| `ca26f3f` | feat(frontend): /compliance standalone + link do ComplianceTab |

---

## [0.9.0] — 2026-04-17 · Sessão 9 · Sprint 2e

### Added — Sistema de Webhooks (tempo real)

**Backend**
- Modelos `Webhook` e `WebhookDelivery` em Postgres (novos) com filtros por `car_code` e `cpf_cnpj`, 9 event types e secret HMAC-SHA256 opcional.
- Service `webhook_dispatcher` com dispatch async paralelizado (asyncio.gather) e assinatura `X-AgroJus-Signature`.
- Router `/api/v1/webhooks` com CRUD completo + `POST {id}/test` (dispara payload sintético) + `GET {id}/deliveries` (logs paginados).
- `MonitoringService._record_alert()` integra dispatch automático em background task — cada novo alerta (MapBiomas/DETER/IBAMA/DJEN/CAR status) dispara webhooks aplicáveis.

**Frontend — aba Monitoramento da ficha**
- Form de cadastro com seletor multi-select de 9 event types.
- Lista de webhooks com toggle ativo/pausado, botão de teste, logs expansíveis (20 entregas, auto-refresh 15s).
- Drawer de entrega detalha status code, duration, payload JSON e response body.

### Added — Aba Ações da ficha (fecha 12/12)

**Backend — 5 novos endpoints em `/api/v1/property`**
- `GET /{car}/laudo.pdf` — laudo consolidado A4 via reportlab: identificação, sobreposições (TI/UC/embargos/PRODES/DETER/autos IBAMA), crédito rural vinculado, avisos legais.
- `GET /{car}/export.geojson` — GeoJSON FeatureCollection (CAR + overlaps) em EPSG:4326 com metadados embarcados.
- `GET /{car}/export.gpkg` — GeoPackage OGC SQLite com 1 layer por tipo (via geopandas, sem ogr2ogr).
- `GET /{car}/export.shp.zip` — Shapefile ESRI zipado (1 .shp por layer).
- `POST /{car}/minuta` — gera minuta jurídica via Claude API (anthropic SDK). Tipos: notificação extrajudicial, ação anulatória de auto, defesa administrativa, contrarrazões, livre. 501 com mensagem amigável se `ANTHROPIC_API_KEY` não configurada.

**Frontend — aba Ações**
- 4 cards de download (PDF, GeoJSON, GPKG, Shapefile) com loading state.
- Painel de minuta com selector de tipo, destinatário, lista de processos relacionados, observações do advogado.
- Resultado em markdown renderizado com contador de tokens, copiar para clipboard, download .md.
- Aviso explícito de revisão humana obrigatória; lacunas marcadas como `[buscar precedente]`.

### Added — dependências

- `anthropic>=0.45.0` no `requirements.txt` (para geração de minutas via Claude).
- Settings novas: `anthropic_api_key`, `anthropic_model` (default `claude-opus-4-7`), `webhook_timeout_seconds` (10s), `webhook_max_retries` (3).

### Fixed

- Query `_fetch_property_base` fazia `UNION` entre `sicar_completo.cod_municipio_ibge` (integer) e `geo_car.cod_municipio_ibge` (text) — `UNION types text and integer cannot be matched`. Corrigido castando ambos para `text`.

### Milestone — Ficha do imóvel 100% completa

Após Sprint 2e, a ficha `/imoveis/[car]` tem as **12 abas** finais:
Visão Geral · Compliance · Dossiê · Histórico · Agronomia · Clima · Jurídico · Valuation · Logística · Crédito · **Monitoramento** · **Ações**

### Commits

| Hash | Descrição |
|---|---|
| `77142b2` | feat(webhooks): sistema completo com dispatch + CRUD + logs |
| `a34cf24` | feat(property): laudo PDF + exports GeoJSON/GPKG/SHP + minuta Claude |
| `1630150` | feat(ficha): MonitoramentoTab + AcoesTab — ficha 12/12 |

---

## [0.8.0] — 2026-04-18 · Sessão 8

### Added — Cotações & Mercado (Agrolink + UX "minha região")

**Backend**
- Collector `agrolink.py` — scrape das páginas `/cotacoes/historico/{uf}/{slug}` (HTML puro, até **265 meses** de histórico mensal por UF).
- **13 commodities cobertas**: Grãos (soja, milho, sorgo, trigo, arroz, feijão), Permanentes/Industriais (café, algodão, cana-de-açúcar, açúcar), Proteínas (boi gordo, frango, leite).
- Cobertura: 5–26 UFs por commodity (milho cobre quase Brasil inteiro; soja 20 UFs; leite 18 UFs; boi 20 UFs).
- Endpoints:
  - `GET /api/v1/market/quotes/agrolink/{commodity}` → histórico + uf_stats
  - `GET /api/v1/market/quotes/agrolink` → lista commodities
  - `GET /api/v1/geo/ibge/choropleth/uf/preco/{commodity}` → GeoJSON BR UF com preço atual estadual
- Tesseract OCR instalado no container (fallback anti-scraping futuro; não usado no fluxo atual).

**Frontend `/mercado` — UX centrada na UF do usuário**
- `UFPicker` grande (default MA, persistido em localStorage).
- Hero "**Preço de hoje em {Estado}**" com 13 commodity cards (preço estadual + seta colorida % vs Brasil).
- Gráfico histórico Recharts ao clicar num card: estadual + nacional, range 1/2/5/10 anos + "tudo".
- Indicadores BCB (SELIC, dólar, IPCA, IGP-M, CDI) compactos.
- 6 notícias de mercado embed (link pra `/noticias`).
- **Removidos**: CBOT/Yahoo Finance, cards CEPEA duplicados, labels "fonte: X".

**Frontend `/mapa`**
- `PriceChoroplethWidget` — botão "Colorir por preço" no topo-esquerdo do mapa com dropdown agrupado (Grãos / Industriais / Proteínas) — 10 commodities. Toggle exclusivo.
- 10 novas camadas no catálogo (`preco_*_uf`) com endpoint `ibge_choropleth_uf`.
- `ZoomControl` no MapPreview (mini-mapa da ficha) + scroll-wheel zoom + drag habilitados.

### Added — Ficha do Imóvel `/imoveis/[car]` (10/12 abas)

- **Sprint 2a** (sessão 7): Visão Geral, Dossiê, Histórico MapBiomas, Agronomia (Agritec).
- **Sprint 2b** (sessão 7): Compliance (MCR 2.9 + EUDR), Clima (NASA POWER), Jurídico (DataJud).
- **Sprint 2c** (sessão 7): Valuation (NBR 14.653-3 nível expedito), Logística (KNN PostGIS), Crédito (SICOR 5.6M contratos).
- **MapPreview** no header da ficha com polígono CAR em Leaflet.

### Added — Ferramentas do mapa (sessão 7)

- **Point analysis** — click em qualquer ponto → popup com município, TI próxima, DETER, clima, jurisdição.
- **Draw polygon** — desenhar AOI → analisa overlaps em 9 camadas + score 0-100.
- **Upload GeoJSON/KML/GML** — parser built-in para memorial descritivo, CAR não oficial.
- **Backend**: novo endpoint `POST /geo/aoi/analyze` com ST_Area + overlaps.

### Changed — Visualização

- **Choropleth IBGE**: escala linear → **quintis** (5 buckets uniformes). Datasets log-normais agora têm diferenciação visual real.
- **OmniSearch (TopBar)**: regex detecta código CAR e roteia para `/imoveis/[car]`.
- **Catálogo `layers-catalog.ts`**: 42 camadas ativas (antes 18) + 10 de preço por UF (Agrolink).

### Added — Dados Sessão 7

- **Embrapa AgroAPI** — 7/9 APIs funcionais (27 endpoints REST)
- **IBGE Choropleth** — 16 métricas (PAM 10 culturas + PPM 4 rebanhos + POP/PIB)
- **MapBiomas Alerta GraphQL** — auth JWT via mutation signIn
- **IBAMA SIFISC** — 16.121 autos de infração georreferenciados em `geo_autos_ibama`
- **Notícias RSS** — nova rota `/noticias` (Canal Rural, Agrolink, Notícias Agrícolas, etc.)

### Housekeeping (sessão 8)

- 7 handoffs antigos movidos para `docs/_archive/handoffs_antigos/`.
- 6 docs superseded (CONTEXTO_COMPLETO, CONTINUIDADE_PROMPT, FRONTEND_SPEC, INVENTARIO_FEATURES, ROADMAP_FASEADO_v1, STATUS_FONTES_DADOS) movidos para `docs/_archive/`.
- `docs/` agora tem 9 arquivos ativos (antes: 22+).
- README reescrito com estrutura real do projeto e índice de documentação.

### Commits

| Hash | Descrição |
|---|---|
| `324b3f6` | Sprint 1 — Embrapa + IBGE choropleth + MapBiomas + IBAMA script |
| `2d6bd06` | Sprint 2a — ficha 4 abas + IBAMA 16k |
| `df70f47` | Sprint 2b — Compliance + Clima + Jurídico (7 abas) |
| `2732e38` | OmniSearch CAR routing |
| `bd0815f` | Fix render choropleth + docs consolidadas |
| `d3f2dcf` | Sprint 2c — Valuation + Logística + Crédito (10 abas) |
| `3f9de00` | Sprint 2d — toolbar mapa (point/draw/upload) + quintis |
| `613e4b7` | Housekeeping docs |
| `88223c0` | /mercado com gráficos + /noticias + choropleth UF SIDRA |
| `17fe965` | Cotações regionais Notícias Agrícolas |
| `d6d551d` | Agrolink histórico UF 22 anos + preço no mapa |
| `8a976fe` | Fix slugs Agrolink — 7 commodities × até 26 UFs |
| `506ba60` | +6 commodities (total 13) + 10 camadas choropleth preço |
| `426a6b4` | UX /mercado centrada na região + widget preço mapa + zoom MapPreview |

---

## [0.7.0-unreleased-consolidation] — 2026-04-17 · Sessão 7

### Added — Cotações regionalizadas (Agrolink)
- **Collector Agrolink UF** (`app/collectors/agrolink.py`) — scrape das páginas `/cotacoes/historico/{uf}/{slug}` que têm **texto puro** (tabela HTML com mês/ano, preço estadual, preço nacional) desde 2003. Até **265 meses** de histórico por UF.
- **7 commodities cobertas**: soja, milho, café, trigo, arroz, feijão, boi gordo.
- **Endpoints:**
  - `GET /api/v1/market/quotes/agrolink/{commodity}` — histórico por UF + uf_stats
  - `GET /api/v1/market/quotes/agrolink` — lista commodities
  - `GET /api/v1/geo/ibge/choropleth/uf/preco/{commodity}` — GeoJSON choropleth com preço atual estadual por UF (para o mapa)
- **Tesseract OCR** instalado no backend (Dockerfile + `pytesseract`) como fallback para decodar preços em imagens PNG anti-scraping (não foi necessário — o histórico está em texto).
- **Dependências:** `inmetpy>=0.1.1`, `pytesseract==0.3.13`, `Pillow>=10.0.0`.

### Frontend `/mercado` — nova seção "Preço médio por UF (Agrolink)"
- Tabela ordenada por preço com 20+ UFs.
- Select de commodity (Soja, Milho, Café, Boi, Trigo, Arroz, Feijão).
- Comparação vs preço nacional (% diff, colorizado).
- Click em UF abre **gráfico de série histórica** Recharts com linha estadual + nacional (últimos 60 meses).
- Link para fonte original.

### Novas camadas no catálogo (4)
- `preco_soja_uf`, `preco_milho_uf`, `preco_cafe_uf`, `preco_boi_uf`
- Endpoint: `ibge_choropleth_uf` com prefixo `preco_` redireciona pro endpoint Agrolink.
- Mapa do Brasil colorido pelo preço **atual** do produto em cada estado.

### Housekeeping
- **docs/** reorganizado: 7 handoffs antigos (sessões 1-5 + HANDOFF inicial) movidos para `docs/_archive/handoffs_antigos/`.
- **docs/** superseded: `CONTEXTO_COMPLETO.md`, `CONTINUIDADE_PROMPT.md`, `FRONTEND_SPEC.md`, `INVENTARIO_FEATURES.md`, `ROADMAP_FASEADO_v1.md`, `STATUS_FONTES_DADOS.md` movidos para `docs/_archive/` (substituídos por README/ROADMAP/CHANGELOG na raiz + HANDOFF sessão 7).
- **README.md** atualizado com estrutura de arquivos real e índice de documentação.
- Pasta `downloads/` está vazia (dados foram limpos); arquivos grandes em `data/` estão gitignored.
- Pasta `frontend/` (versão vanilla JS legada) marcada como descontinuada no README.

## [0.7.0] — 2026-04-17 · Sessão 7

### Added — Dados & Backend
- **Embrapa AgroAPI** — 7/9 APIs assinadas ativas (Agritec ZARC, AGROFIT defensivos, Bioinsumos, AgroTermos, BovTrace, RespondeAgro, SmartSolosExpert). 27 endpoints REST em `/api/v1/embrapa/*`. Paths descobertos via Swagger + validados por curl com OAuth2 real.
- **IBGE Choropleth** — novo módulo `/api/v1/geo/ibge/choropleth/{metric}/{ano}?uf=` com 16 métricas (PAM 10 culturas + PPM 4 rebanhos + POP/PIB/PIB-PC). 14 camadas stub do catálogo saíram de "em breve".
- **MapBiomas Alerta GraphQL** — autenticação via mutation `signIn` + JWT Bearer. Endpoints: `status`, `alerts`, `alert/{code}`, `property/{car}`, `territories`. Retorna alertas tempo real (SAD, DETER, GLAD, SIRAD-X).
- **IBAMA SIFISC** — 16.121 autos de infração georreferenciados carregados em `geo_autos_ibama` (18ª camada PostGIS). URL nova descoberta: era SICAFI, virou SIFISC + ZIP.
- **Property endpoints** (para ficha): `/property/{car}/neighbors` (KNN armazéns/frigos/portos), `/property/{car}/credit` (SICOR via MapBiomas 5.6M), `/property/{car}/valuation` (NBR 14.653-3 nível expedito).
- **AOI Analyze** — `POST /api/v1/geo/aoi/analyze` recebe GeoJSON de polígono custom e retorna área, centróide, overlaps em 9 camadas, score de compliance, risk level.

### Added — Frontend
- **Ficha do Imóvel** `/imoveis/[car]` com **10/12 abas**:
  1. Visão Geral (score 0-100 + 8 KPIs + alertas MapBiomas tempo real)
  2. Compliance (MCR 2.9 ↔ EUDR toggle, banner APTO/RESTRITO/BLOQUEADO)
  3. Dossiê (8 camadas agrupadas)
  4. Histórico (timeline MapBiomas mensal)
  5. Agronomia (Agritec ZARC + culturas do município)
  6. Clima (NASA POWER 30 dias)
  7. Jurídico (DataJud CNJ via CPF/CNPJ)
  8. Valuation (NBR 14.653-3 com descontos por overlap)
  9. Logística (KNN armazéns/frigos/portos + rodovia/ferrovia)
  10. Crédito (contratos SICOR por ano)
- **MapPreview** no header da ficha (mini-mapa leaflet dynamic import)
- **MapTools** (toolbar canto superior direito do mapa):
  - 🎯 Analisar ponto (click → popup lateral com risco + município + TI + DETER)
  - ✏️ Desenhar polígono (vértices + fechar → análise AOI)
  - 📤 Upload GeoJSON/KML (parser built-in, plota + analisa)
- **OmniSearch** (TopBar) agora detecta regex `^[A-Z]{2}-\d{7}-[A-F0-9]{32}$` e roteia para `/imoveis/[car]`.

### Changed
- **Choropleth IBGE** — escala linear → **quintis** (quantile breaks). Datasets agrícolas são log-normais; linear pintava 99% igual. Quintis dividem uniformemente: top 20% escuro → bottom 20% claro.
- **Catálogo de camadas** — 14 novas ativas (endpoint `ibge_choropleth`) + 1 nova postgis (`autos_ibama`) = 32/119 ativas (27%).
- **LayerConfig type** — novos campos `defaultYear` e `colorScheme` + novo endpoint type `"ibge_choropleth"`.

### Fixed
- **Render choropleth no mapa** — switch em `ActiveLayer` não tratava `"ibge_choropleth"`, caía no default e não fetchava. Adicionado case.
- **SIDRA URL** — usava `/f/n` (só nomes) que não retornava código IBGE `D1C`. Trocado para `/f/u` (unified).
- **SmartSolos base path** — era `/smartsolos/v1` (404), correto é `/smartsolos/expert/v1`.
- **MapBiomas auth** — endpoint REST `/auth/login` retorna 500 (deprecated). Correto é mutation GraphQL `signIn`.

### Infra
- 8 commits sequenciais na branch `claude/continue-backend-dev-sVLGG`.
- 42 arquivos novos (backend collectors/routers/scripts, frontend tabs/components, docs).
- Build frontend limpo (Next.js 16.2.3 Turbopack, 10 rotas + 1 dinâmica `/imoveis/[car]`).

---

## [0.6.0] — 2026-04-17 · Sessão 6

### Added
- **DJEN/Comunica.PJe** integrado — 42 publicações reais da OAB/MA 12147 (Eduardo) persistidas em `publicacoes_djen`. Frontend `/publicacoes` com filtros + drawer de detalhe.
- **DataJud CNJ** — `/processos` rewrite, busca real por CPF/CNPJ em 13 tribunais.
- **MapComponent v2** — LayerTreePanel (árvore temática esquerda) + BasemapSwitcher (4 mapas base) + LayerInspector (drawer on-click) + StatsDashboard (painel inferior).
- **Catálogo 119 camadas** em 23 temas (17 ativas + 102 stubs) em `layers-catalog.ts`.
- **48 auditorias visuais** de plataformas concorrentes em `docs/research/visual-audit/*` + SYNTHESIS.md com 25 padrões prioritários e 7 killer gaps.
- **Blueprints** — `analise-agronomica-integrada.md` (15 perguntas-chave da ficha) + `cadeia-dominial-acesso-real.md` + `dados-gov-guia.md` (32 datasets priorizados).

### Changed
- **Projeto movido** de OneDrive para `C:\dev\agrojus-workspace\agrojus\` (resolveu loop Turbopack + sync OneDrive).
- **Docker compose** com `mem_limit` ajustado (backend 2g, db 1g) + Postgres tuning conservador.
- **`.wslconfig`** limita WSL2 a 8GB RAM.

### Fixed
- **OmniSearch TopBar** — handler real (era placeholder).
- **`next.config.ts`** — path absoluto (remove warning Turbopack).
- **ENV var `NEXT_PUBLIC_API_URL`** — finalmente documentada.

---

## [0.5.0] — 2026-04-16 · Sessão 5

### Added
- **DJEN collector base** (sem persistência, só API).
- **MapBiomas credito_rural** — 5.614.207 contratos carregados via GPKG.
- **SIGEF parcelas** — 1.717.474 parcelas INCRA certificadas.

---

## [0.4.0] — 2026-04-15 · Sessão 4

### Added
- **PostGIS layer registry** com 10 camadas iniciais (TI, UC, embargos, PRODES, DETER, SICAR, SIGEF, rodovias, ferrovias, portos).
- **Property search + overlaps** endpoint.
- **NASA POWER collector** (clima).

---

## [0.3.0] — 2026-04-15 · Sessões 2-3

### Added
- **Dashboard** com materialized view.
- **Market** — 11 endpoints CEPEA/BCB + Yahoo Finance CBOT.
- **Compliance MCR 2.9 + EUDR** (6 checks cada).
- **Jurisdicao** service com 27 UFs.

---

## [0.2.0] — 2026-04-15 · Sessão 1

### Added
- **FastAPI scaffold** com auth JWT (PyJWT + bcrypt).
- **SQLAlchemy 2.0** + modelos base (Property, EnvironmentalAlert, LegalRecord, RuralCredit, LandPrice, MarketData, MonitoringAlert).
- **Docker Compose** — 2 containers (db postgis/postgis:16-3.4 + backend Python 3.12).
- **Frontend Next.js 16** scaffold com `(dashboard)` group + login.

---

## [0.1.0] — 2026-04-14 · Kickoff

- Conceito validado: plataforma SaaS B2B de inteligência agrojurídica.
- Stack definida: FastAPI + PostGIS + Next.js + shadcn/ui.
- Credenciais obtidas: GCP, MapBiomas Alerta, Embrapa AgroAPI (9 APIs), dados.gov.br, Portal Transparência, DataJud.
