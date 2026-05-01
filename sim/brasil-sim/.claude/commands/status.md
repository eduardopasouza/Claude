---
description: Status report da campanha em curso.
---

# /status

Leia `saves/<campanha>/current_state.json`,
`pending_actions.json` e `event_log.jsonl` (últimas 5 linhas), e
apresente:

1. **Cabeçalho:** data in-game, nome da campanha (= nome da branch
   sem o prefixo `campaign/`), polity jogador.
2. **Polities:** uma linha cada com `<nome> · líder · <N> regiões ·
   <M> tensões internas`. Destaque a polity jogador.
3. **Relações diplomáticas** envolvendo o player_polity: `<polity>
   — <status> · opinião <X→Brasil>/<Brasil→X>`.
4. **Ações pendentes:** lista de `description` em
   `pending_actions.json`. Se vazia, dizer "nenhuma".
5. **Histórico recente:** últimas 5 entradas de `event_log.jsonl`,
   uma linha cada (`<data>: <description>`).
6. **Eventos programados próximos:** ler
   `data/scheduled_events/era_vargas.yaml` e listar os que caem em
   `[current_date, current_date + 12 meses]` que não estejam
   marcados como já ocorridos no log. Mostrar `<data>: <id>`.

Manter o report curto — esse comando deve dar visão de mapa, não
narrar.
