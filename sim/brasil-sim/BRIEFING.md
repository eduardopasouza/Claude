# Briefing técnico — Simulador histórico-estratégico brasileiro

> **Como usar este documento:** este é o briefing-raiz do projeto `brasil-sim`, salvo na raiz do repositório como `BRIEFING.md`. É consumido pelo Claude Code rodando no ambiente cloud em https://claude.ai/code, com este repositório clonado. Este documento é dirigido ao Claude Code que vai retomar a tarefa.

---

## 1. Identidade e papel

Você é o engenheiro principal de um projeto pessoal do Eduardo Pinho Alves de Souza (advogado OAB/MA 12.147, desenvolvedor por hobby do sistema IAra). O projeto é um **simulador histórico-estratégico turn-based focado no Brasil da Era Vargas (1930–1945)**, executado dentro do ambiente Claude Code na nuvem, com você (o próprio Claude Code) como motor narrativo e de simulação. Não é um produto comercial nem replicação de software de terceiro — é exercício técnico próprio, IP do Eduardo, baseado em padrão arquitetural genérico de domínio público. Uso pessoal, single-player, sem ambição de distribuir.

Você se comunica em português brasileiro, tom técnico e direto, parágrafos fluidos. Apresenta opções com recomendação e aguarda decisão antes de executar passos significativos. Admite incerteza quando há.

## 2. Origem do projeto e o que NÃO é

Este projeto nasceu da análise do padrão arquitetural usado por um jogo chamado PaxHistoria (alternate-history sandbox com IA generativa). O **padrão** — separação por papel funcional com prompts dedicados, motor de turnos determinístico, consolidação periódica de contexto — é design genérico, documentado, e reproduzível sem necessidade de qualquer informação proprietária.

**Restrições explícitas:**

1. Não copie prompts, lore, mapas, schemas ou código-fonte do PaxHistoria. O que se aproveita é apenas o padrão de design.
2. Todo conteúdo histórico deve vir de fontes abertas: Wikipedia, IBGE, IPEA, Biblioteca Nacional Digital, livros de domínio público. Cite as fontes em comentários nos arquivos de lore.
3. Tolerância zero para citações inventadas. Se não souber a fonte, marque `[FONTE PENDENTE]` e não improvise.

## 3. Decisões fechadas

As quatro decisões pendentes do briefing original foram tomadas:

**3.1. Recorte temporal:** Era Vargas, 1930-11-03 (posse provisória) a 1945-10-29 (deposição). Janela densa em eventos verificáveis, com tensão diplomática (Eixo/Aliados) e doméstica simultâneas.

**3.2. Granularidade do mapa brasileiro:** 10 regiões históricas customizadas (esboço, iterar antes de fixar):
- Norte (Amazônia)
- Nordeste açucareiro (zona da mata pernambucana, Alagoas, Sergipe, parte da Bahia)
- Nordeste sertanejo (interior do CE, RN, PB, PI, MA)
- Centro-Oeste pecuário (Goiás, Mato Grosso oriental)
- São Paulo cafeeiro
- Rio-Vale do Paraíba (industrial-administrativo, capital federal)
- Minas mineradora-cafeeira
- Sul gaúcho (RS estancieiro)
- Sul colonial (SC e PR, imigração europeia)
- Mato Grosso fronteiriço (oeste e Pantanal)

**3.3. Escopo externo:** 10 polities-bloco como atores diplomáticos:
Argentina, Uruguai, Paraguai, Chile, Bolívia, EUA, Reino Unido, Alemanha, Itália, Japão.

**3.4. Stack de execução:** Python 3.11+, Pydantic, PyYAML, pytest. Sem SDK Anthropic, sem cliente HTTP, sem `.env`, sem Click, sem SQLite. A interface é o próprio chat do Claude Code; persistência é arquivos JSON/YAML versionados em git.

## 4. Arquitetura

### 4.1. Princípio organizador

O motor do jogo é o próprio Claude Code rodando na sessão cloud. O código Python no repositório existe apenas como **ferramenta determinística** invocada via Bash: validação de schemas, aplicação de deltas, checagem de invariantes. Nenhuma chamada de API LLM é feita pelo código Python.

A separação por papel funcional acontece via **Agent Skills**: cada componente é uma pasta em `.claude/skills/<nome>/` com um `SKILL.md` que o Claude Code carrega sob demanda quando o contexto da conversa indica relevância. O agente principal (Claude Code raiz da sessão) atua como mestre do jogo e orquestrador; os Skills são modos especializados que ele invoca conforme o fluxo.

### 4.2. Componentes do MVP (4 Skills)

**Skill `advisor`** (`context` padrão, roda na conversa principal). Conselheiro narrativo do jogador. Recebe estado atual e histórico recente; devolve análise estratégica em prosa imersiva, em roleplay como conselheiro do chefe de governo brasileiro. Não tem poder de mudar o mundo. A saída fica visível na conversa porque é o que o jogador quer ler.

**Skill `simulator`** (`context: fork` no frontmatter). O motor real de eventos. Recebe estado atual, ações submetidas pelo jogador na rodada e delta temporal (quantos meses pular). Gera **JSON estruturado** em `saves/<campanha>/turn_buffer.json` contendo lista de eventos ocorridos, alterações de estado e narrativa textual. Roda em subagent isolado para não poluir contexto principal com payloads longos. O agente principal lê o resultado, valida via `scripts/validate_turn.py`, aplica deltas via `scripts/apply_delta.py`.

**Skill `diplomat`** (`context` padrão). Simula resposta de polity estrangeira a uma mensagem do jogador. Recebe estado da contraparte, histórico bilateral e mensagem recebida; devolve resposta em prosa visível ao jogador mais delta proposto na relação (concorda/recusa/contraproposta) escrito em `saves/<campanha>/diplomatic_log/<polity>.json`. Diferente do advisor: aqui você *é* o outro ator, não conselheiro do jogador.

**Skill `consolidator`** (`context: fork`). Sumarizador de histórico. Disparado quando `event_log.jsonl` excede N entradas (configurável, sugestão inicial: 20). Recebe bloco de eventos brutos e devolve resumo estruturado em `saves/<campanha>/consolidated_summaries.json`. Eventos brutos vão para arquivo morto; contexto futuro recebe apenas o resumo. Sem isso, campanhas longas viram bombas de contexto.

### 4.3. Schema de estado (Pydantic, esboço)

```python
class GameState(BaseModel):
    current_date: date
    player_polity: str  # "Brasil"
    polities: dict[str, Polity]
    regions: dict[str, Region]
    diplomatic_relations: dict[str, DiplomaticRelation]  # chave "polA::polB" ordenada
    pending_actions: list[PlayerAction]

class Polity(BaseModel):
    name: str
    government_type: str
    leader: str  # nome do chefe de governo no momento
    capital_region: str
    owned_regions: list[str]
    military_units: list[Battalion]
    doctrines: list[str]  # ex.: "industrialismo nacional", "neutralidade ativa"
    internal_tensions: list[str]  # ex.: "oposição comunista", "tenentismo"

class Region(BaseModel):
    name: str
    type: Literal["land", "coastal", "ocean", "strait"]
    owner: str | None
    population_estimate_thousands: int
    economic_profile: str  # ex.: "café exportador", "industrial nascente"
    features: list[MapFeature]

class Event(BaseModel):
    date: date
    category: Literal["diplomatic", "military", "internal", "economic", "natural"]
    description: str
    affected_polities: list[str]
    affected_regions: list[str]
    caused_by: Literal["player_action", "scheduled", "emergent"]
```

`event_log.jsonl` é arquivo append-only (um JSON por linha) separado do `current_state.json` para evitar reescrever histórico inteiro a cada turno. `consolidated_summaries.json` guarda resumos do consolidator. Os campos acima são esboço; itere antes de fixar.

### 4.4. Loop de turno

```
1. Player abre sessão em claude.ai/code; VM clona o repo.
2. Agente principal lê CLAUDE.md (constituição), confere se há campanha
   ativa em saves/, carrega current_state.json se houver.
3. Player interage livremente:
   - Pede análise → agente principal invoca Skill `advisor`.
   - Envia mensagem para polity X → invoca Skill `diplomat`.
   - Submete ação ("nacionalizar petróleo", "negociar empréstimo")
     → agente grava em saves/<campanha>/pending_actions.json.
4. Player digita /turn N (slash command) → agente principal:
   a) Chama Skill `simulator` com estado, ações pendentes, eventos
      pré-programados que caem na janela, sumários consolidados +
      últimos N eventos brutos.
   b) Recebe turn_buffer.json gerado pelo subagent.
   c) Roda scripts/validate_turn.py. Se falhar, devolve ao simulator
      com mensagem de erro até passar (máx. 3 tentativas).
   d) Roda scripts/apply_delta.py para atualizar current_state.json,
      append em event_log.jsonl, limpar pending_actions.json.
   e) Roda scripts/consolidate_check.py. Se threshold atingido,
      invoca Skill `consolidator`.
   f) Auto-commit: git commit com mensagem
      "Campanha <nome> - turno <data>".
5. Volta ao passo 3 com estado novo.
```

### 4.5. Eventos pré-programados (esqueleto histórico Era Vargas)

Para o recorte 1930–1945, modele em `data/scheduled_events/era_vargas.yaml` cerca de 25–30 eventos historicamente ancorados que disparam por proximidade temporal **a menos que o jogador aja para impedir ou que condições do estado os cancelem**. Núcleo mínimo:

- 1932-07: Revolução Constitucionalista de São Paulo
- 1934-07: promulgação da Constituição de 1934
- 1935-11: Intentona Comunista
- 1937-11: Golpe do Estado Novo
- 1938-05: Intentona Integralista
- 1939-09: início da 2ª Guerra na Europa
- 1942-08: Brasil declara guerra ao Eixo
- 1944-07: FEB embarca para a Itália
- 1945-02: vitória de Monte Castelo
- 1945-10: deposição de Vargas

Cada evento tem: `date`, `trigger_window_days`, `description` (com fonte citada), `cancel_conditions` (lista de predicados sobre o estado), `default_effects` (deltas aplicados se nada cancelar). O Simulator lê o YAML a cada turno e injeta no contexto os eventos cuja janela cruza o delta temporal.

### 4.6. Persistência via git

**Crítico para o ambiente cloud.** Cada sessão Claude Code começa em VM nova com clone fresco do repo. Só persiste o que está commitado. Implicações:

- Cada save de campanha é um commit. Não há "save mid-turn" sem commit.
- Recomendação: branch dedicada por campanha (ex. `campaign/vargas-tenentista`). Permite manter múltiplas campanhas paralelas sem conflito, e dá histórico imutável de cada decisão.
- Auto-commit ao final de cada `/turn` é instrução obrigatória no `CLAUDE.md` raiz.
- O `main` permanece com infraestrutura e schemas; conteúdo de campanhas vive em branches.

## 5. Estrutura de pastas

```
brasil-sim/
├── BRIEFING.md                        # este documento
├── CLAUDE.md                          # constituição do agente principal
├── README.md                          # gerado por você
├── pyproject.toml
├── .gitignore
├── .claude/
│   ├── skills/
│   │   ├── advisor/SKILL.md
│   │   ├── simulator/SKILL.md         # frontmatter: context: fork
│   │   ├── diplomat/SKILL.md
│   │   └── consolidator/SKILL.md      # frontmatter: context: fork
│   └── commands/
│       ├── turn.md                    # /turn N
│       ├── save.md                    # /save (commit explícito)
│       ├── load.md                    # /load <campanha>
│       └── diplomatic-message.md      # /dm <polity>
├── src/
│   ├── schemas/                       # Pydantic
│   │   ├── __init__.py
│   │   ├── game_state.py
│   │   ├── polity.py
│   │   ├── region.py
│   │   ├── event.py
│   │   └── diplomatic.py
│   └── scripts/
│       ├── validate_turn.py           # valida turn_buffer.json
│       ├── apply_delta.py             # aplica deltas ao estado
│       └── consolidate_check.py       # confere threshold
├── data/
│   ├── initial_state/
│   │   └── vargas_1930.json
│   ├── scheduled_events/
│   │   └── era_vargas.yaml
│   └── lore/
│       ├── brasil/                    # background por região
│       └── polities/                  # background por polity externa
├── tests/                             # pytest cobrindo schemas e scripts
└── saves/
    └── <campaign-name>/
        ├── current_state.json
        ├── event_log.jsonl
        ├── consolidated_summaries.json
        ├── pending_actions.json
        ├── turn_buffer.json           # buffer transitório do simulator
        └── diplomatic_log/
            └── <polity>.json
```

## 6. Princípios de engenharia

**Separação determinístico vs. estocástico.** Toda lógica que pode ser determinística (aplicar transferência de região, atualizar relação diplomática, validar JSON, calcular data) é Python puro em `src/scripts/`. Skills LLM só são chamados onde criatividade narrativa ou raciocínio aberto é insubstituível. A lição-chave do PaxHistoria mal aplicada é colocar regras de transferência de região no prompt do simulador como texto livre, o que produz erros. Não repita.

**Validação por Pydantic é o enforcement principal.** Como não há mais "structured outputs via tool_use" (o ambiente cloud não usa SDK), o que garante que o Simulator não corrompa o estado é `scripts/validate_turn.py` rodando Pydantic sobre o `turn_buffer.json`. Se falhar, o agente principal devolve ao simulator com mensagem de erro e tenta de novo. Sem Pydantic robusto, o jogo derrapa.

**Skills como markdown, não strings hardcoded.** Cada Skill é uma pasta em `.claude/skills/` com `SKILL.md` próprio. Permite iteração sem mexer em código e versionamento limpo via git diff.

**Logging via event_log.jsonl.** Toda mutação de estado registra um Event correspondente. Sem isso, depurar comportamento estranho é impossível. O log é append-only em formato JSONL para inspeção rápida com `tail`, `jq`, etc.

**Testes determinísticos primeiro.** Schemas Pydantic, validação de turn buffer, aplicação de deltas, consolidate_check — tudo testável sem invocar Skill. pytest cobre essa camada antes de testar componentes LLM.

**CLAUDE.md é a constituição.** O arquivo `CLAUDE.md` na raiz é a instrução que o agente principal carrega no início de toda sessão. Nele vai: papel do agente, fluxo de turno, regras de quando invocar cada Skill, regra de auto-commit ao final de cada turno, regra de branch por campanha. Mantenha-o sob 250 linhas e versionado.

## 7. Roadmap incremental

**Fase 0a — Decisões e calibragem.** ✅ Concluída. Quatro decisões fechadas (seção 3).

**Fase 0b — Setup inicial.** Criar repo `brasil-sim` no GitHub, conectar ao Claude Code via /web-setup, scaffolding: `CLAUDE.md`, estrutura de pastas, `pyproject.toml` mínimo, `.gitignore`, README. Sem componentes ainda. Critério de saída: sessão Claude Code abre o repo limpo, lê BRIEFING.md e CLAUDE.md sem erro.

**Fase 1 — Núcleo determinístico.** Schemas Pydantic completos em `src/schemas/`, scripts em `src/scripts/`, testes pytest cobrindo o núcleo, estado inicial Era Vargas em `data/initial_state/vargas_1930.json`. Critério: rodar via Bash `python -m src.scripts.apply_delta --state X --delta Y` válido com persistência em arquivo, e `pytest` verde.

**Fase 1.5 — Pesquisa histórica e lore.** Markdown de background em `data/lore/`, com URL de fonte ao lado de cada afirmação factual (Wikipedia, IBGE, Biblioteca Nacional Digital, livros de domínio público). Cobertura: as 10 regiões brasileiras e as 10 polities externas. Onde fonte verificável faltar, marca `[FONTE PENDENTE]` e segue. Eduardo revisa antes de fechar a fase.

**Fase 2 — Skill `advisor`.** Implementa `.claude/skills/advisor/SKILL.md`. Iteramos voz e profundidade da análise contra estado de teste. Critério: Eduardo aprova explicitamente.

**Fase 3 — Skill `simulator` + eventos pré-programados.** `.claude/skills/simulator/SKILL.md` com `context: fork`, instrução para gerar `turn_buffer.json` validável. YAML completo de eventos históricos em `data/scheduled_events/era_vargas.yaml` (~25–30 eventos). Loop completo: submeter ação → `/turn 6` → ver eventos aplicados.

**Fase 3.5 — Checkpoint estrutural.** Campanha curta simulada de 1930-11 a 1933-11, observando: fidelidade dos eventos pré-programados, estabilidade do `turn_buffer.json`, plausibilidade das emergências, comportamento do auto-commit. Validação por inspeção manual de Eduardo.

**Fase 4 — Skill `diplomat`.** Canal por polity, persistência de histórico bilateral em `saves/<campanha>/diplomatic_log/<polity>.json`. Slash command `/dm <polity>`.

**Fase 5 — Skill `consolidator`.** Disparo automático quando event log excede limiar. Teste em campanha longa simulada (50+ turnos) confirmando que a consolidação preserva coerência narrativa e mantém o contexto enxuto.

**Fase 6 — Polimento.** Slash commands restantes (`/save`, `/load`, `/status`), export de campanha completa para markdown narrativo (`scripts/export_campaign.py`), comandos de inspeção do log.

**Fora do MVP:** os outros quatro componentes do padrão original (Suggested Action, Next Speaker, Description to Action, Auto Jump Forward), interface web, multi-campanha em paralelo na mesma branch.

## 8. Critérios de aceitação do MVP (fim da Fase 6)

- Eduardo abre sessão em claude.ai/code, repo é clonado, agente lê CLAUDE.md.
- Inicia campanha Era Vargas com estado em 1930-11-03 (posse de Vargas).
- Conversa com advisor sobre estratégia (saída na conversa principal).
- Submete ações livres ("nacionalizar produção de petróleo", "negociar empréstimo com Washington").
- Envia mensagens diplomáticas via `/dm <polity>` e recebe respostas coerentes.
- Digita `/turn 6` e vê eventos plausíveis (mistura de pré-programados — Revolução Constitucionalista de 1932 dispara se nada bloquear — e emergentes derivados de ações).
- Auto-commit funciona ao final de cada turno.
- Salva em branch `campaign/<nome>` e retoma em sessão posterior.
- Campanha longa (50+ turnos) não degrada por inchaço de contexto, graças ao consolidator.

## 9. O que esperar do Eduardo

Desenvolvedor experiente (mantém o sistema IAra, projeto BestStag, plataforma Jus Maranhão), trabalha em Python, familiaridade com FastMCP, Pydantic, ferramentas modernas, e em particular com o padrão SKILL.md (que usa no IAra). Você pode falar técnico sem simplificar.

**Tolerância zero para citações inventadas.** Ao alimentar lore histórico, busque fonte de verdade e cite com URL. Se não souber, marque `[FONTE PENDENTE]`. Não improvise.

Prefere raciocínio analógico e intuitivo, gosta de receber correções, responde bem a "olha, aqui sua premissa não fecha porque X" — desde que você tenha argumento real.

## 10. Primeira mensagem ao Eduardo

Quando ele abrir uma sessão Claude Code com este briefing pela primeira vez (Fase 0b), sua primeira resposta deve ser algo como:

> Li o BRIEFING.md. As quatro decisões da seção 3 estão fechadas. Próximo passo é a Fase 0b: criar o scaffolding (CLAUDE.md, estrutura de pastas, pyproject.toml mínimo, README, .gitignore). Quer que eu proponha o conteúdo do CLAUDE.md primeiro para você revisar, ou começo direto pelo scaffolding e depois você revisa tudo no commit?

Não comece a escrever código de domínio (schemas, scripts, skills) antes de a Fase 0b estar fechada com commit aprovado.
