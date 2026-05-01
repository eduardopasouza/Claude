---
description: Envia mensagem diplomática para uma polity estrangeira e captura a resposta.
argument-hint: <polity> [mensagem opcional inline]
---

# /dm $ARGUMENTS

Inicie sessão diplomática com a polity nomeada (primeira palavra de
`$ARGUMENTS`):

1. Confirme que a polity está em `state.polities` e não é o
   `state.player_polity`. Se não, listar polities válidas e abortar.
2. Se houver texto adicional após o nome da polity em `$ARGUMENTS`,
   tratar como a mensagem do Brasil. Caso contrário, perguntar ao
   jogador qual é o conteúdo da mensagem.
3. Invocar Skill `diplomat` passando:
   - estado atual
   - polity contraparte
   - histórico bilateral em
     `saves/<campanha>/diplomatic_log/<polity>.json`
   - lore em `data/lore/polities/<polity>.md`
   - mensagem do Brasil
4. Apresentar a resposta da polity ao jogador, em prosa.
5. O Skill `diplomat` deve ter feito append no
   `diplomatic_log/<polity>.json`. Se ele propôs deltas
   (`proposed_deltas`), adicionar ao `pending_actions.json` como
   nova `PlayerAction` com:
   - `description`: "Diplomacia com <polity>: <resumo>"
   - `submitted_on`: state.current_date
   - `category`: "diplomacia"
   - `target_polities`: [<polity>]

Os deltas só se materializam no estado quando o próximo `/turn`
rodar e o Skill `simulator` decidir como integrá-los à narrativa.
