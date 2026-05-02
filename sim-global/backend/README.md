# simengine

Motor determinístico compartilhado pelos simuladores em `sim/`. Pacote
Python invocado pelos Skills via Bash — nunca faz chamadas de LLM.

## Instalação local

```bash
cd sim/dev
pip install -e ".[dev]"
```

Após isso, `python -c "import simengine"` deve funcionar e
`python -m pytest` roda a suíte. Use `python -m pytest` em vez de
`pytest` direto: no ambiente Claude Code o binário `pytest` global vive
em outro venv sem `pydantic` instalado.

## Estrutura

- `src/simengine/schemas/` — modelos Pydantic do estado de jogo
  (Polity, Region, Event, GameState, etc.). _A criar na Fase 1._
- `src/simengine/scripts/` — executáveis chamados via
  `python -m simengine.scripts.<nome>`: `validate_state`,
  `validate_turn`, `apply_delta`, `consolidate_check`. _A criar na
  Fase 1._
- `tests/` — pytest cobrindo schemas e scripts.

## Versões consumidoras

- `sim/brasil-sim/` — Era Vargas 1930-1945.
- _futuras_: `sim/global-sim/` ou outras nações.

## Princípios

Toda lógica determinística (validação, aplicação de delta, cálculo de
data, transferência de região) vive aqui. A separação rígida em relação
aos Skills LLM é o que mantém o jogo auditável e barato em contexto.
