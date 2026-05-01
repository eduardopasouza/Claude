# brasil-sim — Era Vargas (1930-1945)

Versão `brasil-sim` do simulador histórico-estratégico em `sim/`.
Recorte: Brasil de 1930-11-03 (posse provisória de Vargas) a
1945-10-29 (deposição). 10 regiões brasileiras + 10 polities-bloco
externas como atores diplomáticos.

A documentação completa do projeto está em
[`BRIEFING.md`](BRIEFING.md) (estratégia) e
[`CLAUDE.md`](CLAUDE.md) (constituição operacional desta versão).
A constituição genérica do motor está em
[`../CLAUDE.md`](../CLAUDE.md).

## Como jogar

Rode dentro do Claude Code com este repositório clonado.

### Iniciar uma campanha nova

```bash
git checkout -b campaign/<nome-em-kebab-case>
mkdir -p saves/<nome-em-kebab-case>
cp data/initial_state/vargas_1930.json saves/<nome-em-kebab-case>/current_state.json
echo '[]' > saves/<nome-em-kebab-case>/pending_actions.json
touch saves/<nome-em-kebab-case>/event_log.jsonl
```

Depois disso, abra o Claude Code apontando para `sim/brasil-sim/` e
deixe o agente seguir o checklist de início de sessão definido em
[`CLAUDE.md`](CLAUDE.md).

### Slash commands

Os comandos abaixo estão definidos em `.claude/commands/`:

| Comando            | Função                                                        |
| ------------------ | ------------------------------------------------------------- |
| `/turn N`          | Avança N meses, processa ações pendentes e eventos do YAML.   |
| `/dm <polity>`     | Abre canal diplomático com uma polity estrangeira.            |
| `/save`            | Commit explícito (checkpoint manual fora do fluxo de turno).  |
| `/load <campanha>` | Checkout da branch `campaign/<campanha>`.                     |
| `/status`          | Status report curto da campanha em curso.                     |

### Skills

Em `.claude/skills/`:

| Skill          | Disparo                                                 | Contexto |
| -------------- | ------------------------------------------------------- | -------- |
| `advisor`      | Jogador pede análise estratégica.                       | normal   |
| `simulator`    | Apenas dentro de `/turn`.                               | fork     |
| `diplomat`     | Comando `/dm` ou prosa diplomática direcionada.         | normal   |
| `consolidator` | Automático quando event_log excede `consolidator.threshold` em [`config.yaml`](config.yaml). | fork |

## Conteúdo histórico

- [`data/lore/brasil/`](data/lore/brasil/) — background das 10
  regiões brasileiras + overview de 1930.
- [`data/lore/polities/`](data/lore/polities/) — background das 10
  polities estrangeiras.
- [`data/scheduled_events/era_vargas.yaml`](data/scheduled_events/era_vargas.yaml)
  — eventos pré-programados disparados pelo simulator.
- [`data/initial_state/vargas_1930.json`](data/initial_state/vargas_1930.json)
  — estado canônico em 1930-11-03 (template para nova campanha).

Todo conteúdo histórico é de fontes abertas (Wikipedia, IBGE,
Biblioteca Nacional Digital, FGV/CPDOC, etc.) com URL citada no
próprio arquivo. Pontos onde a fonte é dúbia ou não foi confirmada
estão marcados como `[FONTE PENDENTE]` para revisão humana.

## Exportar campanha completa

A qualquer momento:

```bash
python -m simengine.scripts.export_campaign saves/<campanha>/
```

Gera `saves/<campanha>/CAMPAIGN.md` com cronologia consolidada,
estado final e apêndice diplomático.

## Persistência

- Estado canônico vive em `saves/<campanha>/current_state.json`.
- Histórico bruto em `event_log.jsonl` (append-only).
- Resumos em `consolidated_summaries.json` (gerados pelo
  consolidator).
- Histórico bilateral por polity em `diplomatic_log/<polity>.json`.
- `turn_buffer.json` é transitório — gitignored.
- Cada `/turn` faz auto-commit. Para checkpoint manual fora de turno,
  use `/save`.
