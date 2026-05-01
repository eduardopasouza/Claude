---
description: Carrega uma campanha existente (checkout da branch correspondente).
argument-hint: <nome-campanha>
---

# /load $ARGUMENTS

1. Validar que `$ARGUMENTS` está em formato kebab-case e que existe
   uma branch `campaign/$ARGUMENTS`. Se não existir, listar campanhas
   disponíveis (`git branch --list 'campaign/*'`) e abortar.
2. Se houver mudanças não commitadas na branch atual, alertar o
   jogador e abortar (sem `git stash` automático).
3. `git checkout campaign/$ARGUMENTS`.
4. Validar `saves/$ARGUMENTS/current_state.json` via
   `python -m simengine.scripts.validate_state`.
5. Apresentar status report ao jogador:
   - Data in-game.
   - Polities (nome, líder, número de regiões).
   - Relações diplomáticas envolvendo o player_polity.
   - Ações pendentes em `pending_actions.json`.
   - Próximos eventos pré-programados na janela de 12 meses adiante.
