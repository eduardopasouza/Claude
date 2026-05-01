---
description: Avança o jogo em N meses, processando ações pendentes e eventos pré-programados.
argument-hint: <N>
---

# /turn $ARGUMENTS

Execute o loop de turno definido em `sim/brasil-sim/CLAUDE.md` com
N = `$ARGUMENTS` meses:

1. Validar que a branch atual é `campaign/<nome>`. Se não, abortar
   e instruir o jogador a criar/checkout uma branch de campanha.
2. Validar `saves/<nome>/current_state.json` via
   `python -m simengine.scripts.validate_state <path>`. Se falhar,
   abortar.
3. Invocar Skill `simulator` (context fork) com:
   - current_state.json
   - pending_actions.json
   - eventos pré-programados de `data/scheduled_events/era_vargas.yaml`
     cuja janela cruza N meses adiante de current_date
   - últimos 20 eventos de event_log.jsonl
   - todos os entries de consolidated_summaries.json (se existir)
   - delta temporal N
4. Validar `turn_buffer.json` gerado via
   `python -m simengine.scripts.validate_turn <state> <buffer>`.
5. Em caso de falha de validação: devolver ao simulator com
   stderr completo e pedir nova versão. Máximo 3 tentativas. Após
   a 3ª, abortar e reportar — NÃO commitar nada.
6. Aplicar via `python -m simengine.scripts.apply_delta <state> <buffer> <event_log> <pending>`.
7. Verificar consolidação via
   `python -m simengine.scripts.consolidate_check <event_log> <summaries> <config>`.
   Se `should_consolidate` for true, invocar Skill `consolidator`
   (context fork).
8. Auto-commit:
   - `git add saves/<nome>/`
   - `git commit -m "Turno <data-in-game>: <resumo>"`
   (resumo = primeira frase da `narrative` do turn_buffer)
9. Apresentar a `narrative` do turno ao jogador, mais comentário
   curto do mestre destacando o que mudou no estado.
