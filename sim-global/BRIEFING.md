# BRIEFING.md — `sim-global`

> Documento estratégico da raiz do projeto. Reescrito após pivot para
> arquitetura de **app local com frontend visual + Claude via OAuth**
> (pivots anteriores em `examples/brasil-vargas-1930/BRIEFING.md` e
> em commits da branch `claude/brasil-sim-mvp-5ubSa`).

---

## 1. Identidade e papel

`sim-global` é um simulador histórico-estratégico turn-based de uso
pessoal do Eduardo Pinho Alves de Souza (advogado OAB/MA 12.147,
desenvolvedor por hobby do sistema IAra). Inspirado no padrão de
design do PaxHistoria (uso autorizado pelo dono como referência
arquitetural, com adaptação substancial). Roda 100% localmente:
backend Python + frontend web servido em `localhost`, autenticação
LLM via OAuth da assinatura Claude Pro/Max do dono. Sem custo
monetário per-token, sem dependência de API key paga.

Você é o engenheiro principal do projeto. Português brasileiro,
tom técnico e direto. Apresenta opções com recomendação e aguarda
decisão antes de passos significativos. Admite incerteza.

## 2. Origem e licenciamento

Padrões arquiteturais e de UX vêm da observação direta do PaxHistoria
(autorização explícita do dono no histórico desta branch). Conteúdo
histórico (lore de cenários) vem **exclusivamente** de fontes abertas
verificáveis (Wikipedia, IBGE, IPEA, Biblioteca Nacional Digital, FGV
CPDOC, livros de domínio público). **Tolerância zero a citações
inventadas:** afirmações factuais sem fonte confirmada são marcadas
`[FONTE PENDENTE]` em vez de improvisadas. Esta regra independe de
licenciamento de IP — é critério de qualidade de output.

Projeto não distribuído. Uso pessoal. Decisões jurídicas são
responsabilidade do dono.

## 3. Modelo mental do jogo

O jogador escolhe **(ano, nação)** ao iniciar uma campanha. O backend
invoca o Skill **Scenario Builder**, que pesquisa em fontes abertas
e constrói o estado inicial: regiões internas da nação, polities
externas relevantes, lore com URLs, ~25-30 eventos pré-programados
para o horizonte de 15-20 anos. Validação Pydantic + invariantes
estruturais. Resultado é commitado como um row em `campaigns`.

A partir daí, o jogador interage via UI:

- **Mapa central** (SVG político mundial, Natural Earth Data CC0).
  Três camadas independentes: regiões coropléticas (cor por dono),
  features pontuais (cidades, portos), unidades militares (overlays
  móveis em features tipo `city`).
- **Painel da polity selecionada** (esquerda): atributos
  quantitativos, líder, doutrinas, tensões, batalhões, regiões
  controladas.
- **Action Box** (inferior): texto livre para descrever ações ("subsidiar
  produção de aço no Vale do Paraíba em 30%"). Backend canoniza para
  `PlayerAction` estruturada via LLM, valida e enfileira em
  `pending_actions`.
- **Events feed** (direita): cronologia do que aconteceu, com
  severidade (`minor` | `moderate` | `major` | `critical`).
- **Diplomacy panel** (overlay/modal): canal por contraparte,
  histórico bilateral. Cada polity é encarnada pelo Skill `Diplomat`
  com personalidade derivada do líder.
- **Advisor chat** (lateral persistente): perguntas estratégicas
  read-only ao Skill `Advisor`. Não modifica estado.
- **Timeline / Advance Time**: jogador escolhe granularidade
  (1 semana → 1 ano custom). Ao apertar `advance time`, dispara o
  Skill `Game Master` em subagente isolado para gerar o turn buffer.

**Decisional Pause**: o tempo do jogo congela enquanto o jogador prepara
o turno. Não há real-time, não há reconciliação otimista. Simplifica
muito o frontend.

## 4. Arquitetura técnica

```
┌─ App local (porta 8000) ──────────────────────────────────┐
│                                                            │
│  Frontend (browser) — HTMX + Alpine.js + Tailwind via CDN  │
│    · Mapa SVG (3 camadas: regiões / features / unidades)   │
│    · Painéis de polity, eventos, diplomacia, advisor        │
│    · Action Box                                             │
│    · Imagens curadas: bandeiras, retratos                  │
│    · Animações via CSS transitions                         │
│                                                            │
│  Backend (Python 3.11+) — FastAPI                          │
│    · Endpoints REST: /campaigns, /turn, /dm, /advise...    │
│    · Claude Agent SDK autenticado via OAuth                │
│      → CLAUDE_CODE_OAUTH_TOKEN (gerado por                 │
│         `claude setup-token` uma vez)                      │
│      → invoca subagentes:                                  │
│         scenario_builder, game_master, advisor,            │
│         diplomat, consolidator                             │
│      → modelo: claude-opus-4-7 (assinatura Pro/Max cobre)  │
│    · simengine (motor determinístico, módulo interno)      │
│    · SQLAlchemy 2.x + SQLite local (saves/simglobal.db)    │
│    · Catálogo de assets em data/                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
        ↑
        │ OAuth Pro/Max
        ↓
   Anthropic (inferência)
```

## 5. Componentes LLM (Skills via Agent SDK)

Cinco subagentes com escopo cirúrgico, cada um com seu prompt em
arquivo `.md` versionado em `backend/src/simglobal/prompts/`:

- **`scenario_builder`**: roda no `/campaigns` POST. Pesquisa via
  WebSearch/WebFetch, popula GameState inicial + lore.md +
  scheduled_events para o cenário escolhido.
- **`game_master`** (única fonte de mutação): roda no `/turn`.
  Recebe estado, ações pendentes, eventos programados na janela e
  delta temporal. Devolve `turn_buffer` JSON estrito (events +
  deltas + narrative). Output validado por Pydantic; falha →
  retry com erro injetado, máx 3.
- **`advisor`**: roda no `/advise`. Read-only, conversacional,
  300-600 palavras. Não muda estado.
- **`diplomat`**: roda no `/dm/<polity>`. Encarna a polity contraparte
  com personalidade derivada do líder. Histórico bilateral persistido.
  Pode propor deltas que entram em `pending_actions`.
- **`consolidator`**: dispara automaticamente quando `event_log`
  excede `consolidator.threshold` (default 20) desde o último
  summary. Sumariza para manter contexto enxuto.

## 6. Modelo de domínio (estendido)

Sobre o esboço da fase anterior, três extensões inspiradas pelo Pax:

**Polity** ganha `attributes`:
- `stability` (0-100)
- `war_support` (0-100)
- `treasury` (sem bound, pode negativo)
- `manpower` (0-N, cap dinâmico)
- `political_power` (acumulativo)

**Event** ganha `severity` (`minor` | `moderate` | `major` | `critical`).

**Battalion** opcionalmente ancorada em `Feature` tipo `city` (não só
em `Region`). Mantém compat com schema atual.

**Scripting híbrido de eventos** (`scheduled_events`):
- `triggers`: predicados estruturados (`{kind: "date"|"state"|"chain", expr}`)
  para eventos com data conhecida (ex.: 1939-09-01).
- `cancel_conditions`: predicados estruturados sobre o estado atual.
- `effects`: lista de StateDelta-equivalents (op `delta`/`set`,
  target tipado).
- Eventos emergentes (sem âncora histórica) ficam só no domínio do
  `game_master`, sem entrada no YAML.

## 7. Fluxo de turno

```
1. Jogador absorve events feed do turno anterior.
2. Jogador conversa com advisor (zero ou várias perguntas).
3. Jogador compõe ações na Action Box.
4. Jogador conduz diplomacia em DMs.
5. Jogador escolhe horizonte (1 semana → 1 ano) e clica
   "Advance Time".
6. Backend dispara game_master em subagente:
   payload = state + pending_actions + scheduled_events na janela
              + últimos 20 events brutos + consolidated_summaries.
7. game_master devolve turn_buffer.json. Backend valida via
   Pydantic + check_turn_invariants. Falha → retry (máx 3).
8. Backend aplica via apply_turn_buffer. Persiste em SQLite.
9. consolidate_check; se threshold atingido, dispara consolidator.
10. Frontend recebe novo state + events + narrative; re-renderiza
    mapa, painéis, feed.
```

## 8. Estrutura de pastas

```
sim-global/
├── BRIEFING.md                       # este arquivo
├── CLAUDE.md                         # constituição operacional
├── README.md                         # como rodar
├── config.yaml                       # defaults globais
├── pyproject.toml                    # workspace top-level
├── .gitignore
├── backend/
│   ├── pyproject.toml                # pacote simglobal (inclui simengine)
│   ├── src/simglobal/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app
│   │   ├── routes/                   # endpoints
│   │   ├── agent/                    # wrapper Claude Agent SDK
│   │   ├── prompts/                  # *.md por subagente
│   │   ├── persistence/              # SQLAlchemy + Alembic
│   │   └── engine/                   # ex-simengine
│   │       ├── schemas/
│   │       ├── engine.py
│   │       └── scripts/
│   └── tests/                        # pytest
├── frontend/
│   ├── templates/                    # Jinja2
│   └── static/{css,js,img,map}/
├── data/
│   ├── catalog/{flags,portraits}/    # imagens curadas Wikimedia
│   └── map/                          # Natural Earth Data CC0
├── examples/
│   └── brasil-vargas-1930/           # cenário-piloto + fixture
│       ├── BRIEFING.md
│       ├── README.md
│       ├── config.yaml
│       ├── initial_state.json
│       ├── scheduled_events.yaml
│       └── lore/{brasil,polities}/
└── saves/
    └── simglobal.db                  # SQLite (gitignored)
```

## 9. Princípios de engenharia

1. **Determinístico em Python, estocástico em LLM.** Aplicar deltas,
   validar JSON, calcular datas, transferir regiões: tudo Python puro
   no `simengine`. LLM apenas onde criatividade ou raciocínio aberto
   é insubstituível.
2. **Pydantic é o último guardião.** Todo output LLM passa por
   validação de schema + invariantes antes de ser aplicado.
3. **Citações: URL ou `[FONTE PENDENTE]`.** Sem invenção.
4. **Game Master é única fonte de mutação.** Advisor não muda nada;
   Diplomat só propõe via `pending_actions`. Mantém auditabilidade.
5. **Decisional Pause**: jogo congela durante o turno. Sem real-time.
6. **Schema strict para output LLM**: forçar JSON com tool use ou
   structured output do Agent SDK. Reduzir taxa de erro.

## 10. Roadmap

**Fase 0** ✅ — Decisões + setup inicial (commits anteriores).

**Fase 1** ✅ — Núcleo determinístico simengine (schemas + scripts +
68 testes verdes).

**Fase 1.5** parcial ✅ — Lore Brasil/1930 (11 regiões + 10 polities),
estado inicial validado, 30 eventos pré-programados. Preservados em
`examples/brasil-vargas-1930/` como cenário-piloto.

**Fase 2 — Refator estrutural + extensão de schemas (em curso).**
Atributos quantitativos da Polity, Event.severity, scripting híbrido,
adaptação de paths.

**Fase 3 — Backend FastAPI mínimo.** Endpoints REST stub respondendo
estado de exemplo. Sem Agent SDK ainda.

**Fase 4 — Frontend HTMX mínimo.** Mapa SVG global + painéis
navegáveis lendo state via fetch. Carrega Brasil/1930.

**Fase 5 — Integração Claude Agent SDK via OAuth.** Implementação dos
5 subagentes; endpoints `/turn`, `/advise`, `/dm` funcionais.

**Fase 6 — Scenario Builder.** Pesquisa procedural via WebSearch.
Endpoint `/campaigns` POST cria campanha do zero.

**Fase 7 — Polimento.** Animações CSS, catálogo de imagens,
export de campanha em markdown.

## 11. Critérios de aceitação do MVP

- Eduardo roda `python -m simglobal`; backend sobe em `localhost:8000`,
  browser abre automaticamente.
- Tela mostra mapa-mundi colorido por dono, painéis de polity
  navegáveis, events feed.
- Importa Brasil/1930 via fixture e mostra estado correto.
- Inicia campanha nova via `/new` (escolhendo ano + nação); scenario
  builder pesquisa e cria.
- Compõe ação na Action Box → enfileirada.
- Conversa com advisor → resposta em painel lateral.
- Envia mensagem diplomática → resposta da polity contraparte.
- Avança 6 meses → game_master gera turn buffer; eventos aparecem
  no feed; mapa re-renderiza se algo mudou.
- Auto-save no SQLite após cada turno.
- Reabre o app no dia seguinte; carrega campanha onde parou.

## 12. O que esperar do Eduardo

Desenvolvedor experiente (sistema IAra, BestStag, Jus Maranhão).
Python-first, conhece FastMCP, Pydantic. Tom técnico sem simplificar.
Tolerância zero a citações inventadas. Prefere raciocínio analógico,
gosta de correções fundamentadas. Pivots ocasionais — registrar
explicitamente no histórico para rastreabilidade.
