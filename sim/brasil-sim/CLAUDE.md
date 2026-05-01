# CLAUDE.md — brasil-sim (Era Vargas 1930-1945)

> Este arquivo é a constituição **específica** da versão `brasil-sim`.
> As regras gerais do projeto vivem em `sim/CLAUDE.md` (raiz acima);
> aqui só fica o que é particular desta versão.

## Contexto da versão
Antes de operar, leia `BRIEFING.md` desta pasta. Recorte:
Brasil 1930-11-03 a 1945-10-29, 10 regiões brasileiras + 10 polities-bloco
externas (Argentina, Uruguai, Paraguai, Chile, Bolívia, EUA, Reino Unido,
Alemanha, Itália, Japão).

## Configuração operacional
Parâmetros ficam em `sim/brasil-sim/config.yaml`. Hoje há um único:
- `consolidator.threshold` (default 20) — número de eventos brutos em
  `event_log.jsonl` que dispara consolidação automática.

## Skills disponíveis nesta versão
- `advisor`: análise estratégica visível ao jogador.
  Disparo: jogador pede análise, opinião ou recomendação estratégica.
- `simulator` (`context: fork`): geração de `turn_buffer.json`.
  Disparo: APENAS dentro do fluxo `/turn`. Nunca solto.
- `diplomat`: resposta de polity estrangeira.
  Disparo: comando `/dm <polity>` ou jogador descreve mensagem
  diplomática em prosa.
- `consolidator` (`context: fork`): sumarização de `event_log.jsonl`.
  Disparo: automático quando o threshold de `config.yaml` é atingido
  desde o último consolidated_summary.

## Loop de turno (`/turn N`)
1. Validar que a branch atual é `campaign/<nome>`. Se não, abortar.
2. Validar que `saves/<nome>/current_state.json` carrega via Pydantic
   (`python -m simengine.scripts.validate_state`).
3. Invocar Skill `simulator` com payload contendo:
   - `current_state.json`
   - `pending_actions.json`
   - eventos pré-programados em `data/scheduled_events/era_vargas.yaml`
     cuja janela de gatilho cruza os N meses adiante
   - últimos 20 eventos de `event_log.jsonl`
   - todos os entries de `consolidated_summaries.json`
   - delta temporal N
4. Simulator escreve `saves/<nome>/turn_buffer.json`.
5. Rodar `python -m simengine.scripts.validate_turn`.
   - Se falhar, devolver ao simulator com mensagem de erro e pedir nova
     versão. Máximo 3 tentativas. Após a 3ª, abortar o turno, reportar
     ao jogador, NÃO commitar nada do buffer.
6. Rodar `python -m simengine.scripts.apply_delta`. Atualiza
   `current_state.json`, faz append em `event_log.jsonl` e limpa
   `pending_actions.json`.
7. Rodar `python -m simengine.scripts.consolidate_check`. Se threshold
   atingido, invocar Skill `consolidator`.
8. Auto-commit:
   ```
   git add saves/<nome>/
   git commit -m "Turno <data-in-game>: <resumo>"
   ```
9. Apresentar narrativa do turno ao jogador (texto livre extraído do
   `turn_buffer.json` mais comentário do mestre).

## Slash commands
- `/turn N` — loop de turno acima.
- `/dm <polity>` — invocar Skill `diplomat` para a polity indicada.
- `/save` — commit explícito (caso o jogador queira checkpoint fora do
  fluxo automático de fim de turno).
- `/load <campanha>` — checkout da branch da campanha.
- `/status` — status report da campanha em curso.

## Regras específicas desta versão
- `simulator` só é invocado dentro de `/turn`. Nunca solto.
- `turn_buffer.json` é transitório: nunca commitado se o turno foi
  abortado.
- Branch de campanha segue padrão `campaign/<nome>` em kebab-case
  (ex.: `campaign/vargas-tenentista`).
