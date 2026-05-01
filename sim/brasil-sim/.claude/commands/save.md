---
description: Commit explícito do estado atual da campanha (checkpoint manual).
---

# /save

Use para forçar um checkpoint fora do fluxo automático de fim de
turno (útil antes de pausar, antes de uma decisão arriscada, ou
depois de várias interações sem turno fechado).

1. Validar branch é `campaign/<nome>`.
2. `git status --short` para ver o que mudou em `saves/<nome>/`.
3. Se nada mudou, reportar e não commitar.
4. Caso contrário:
   - `git add saves/<nome>/`
   - `git commit -m "Save manual <data-in-game>: <descrição curta>"`
5. Confirmar ao jogador o hash curto do commit.

Não fazer push automático: o jogador pode querer revisar antes.
