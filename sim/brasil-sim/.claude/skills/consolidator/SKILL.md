---
name: consolidator
description: Sumariza um bloco do event_log.jsonl em um ConsolidatedSummary, mantendo o contexto futuro enxuto. Disparado automaticamente quando o número de eventos não-consolidados excede o threshold de config.yaml. Use context fork para isolar o trabalho de leitura do event log.
context: fork
---

# Consolidator — sumarizador de histórico

Tarefa: ler o bloco de eventos brutos não consolidados e produzir
um único `ConsolidatedSummary` que preserve o essencial para
decisões futuras.

## Inputs (passados pelo orquestrador)

- `saves/<campanha>/event_log.jsonl`: linha-por-linha JSON de
  eventos. Considere apenas os posteriores a
  `last_summary_period_end` (data fornecida pelo orquestrador, ou
  `null` se for a primeira consolidação).
- `saves/<campanha>/current_state.json`: para contexto (nomes
  atuais de líderes, status diplomáticos), não para modificar.

## Output

Append em `saves/<campanha>/consolidated_summaries.json`. O arquivo
é um JSON array. Adicione um novo objeto no final:

```json
{
  "period_start": "1930-11-03",
  "period_end": "1932-06-30",
  "key_events": [
    "Posse de Vargas em 1930-11-03.",
    "Centralização administrativa pela nomeação de interventores.",
    "Crescimento de oposição paulista..."
  ],
  "state_changes_summary": "Texto entre 200 e 400 palavras descrevendo o arco do período: principais mudanças de estado (regiões, governo, doutrinas, tensões), trajetória diplomática, escalada militar.",
  "emerging_tensions": [
    "Oposição paulista crescente",
    "Cisão tenentista interna",
    "Desconfiança argentina"
  ],
  "generated_at": "1932-07-01"
}
```

### Campos

- `period_start`: data do primeiro evento considerado
  (`last_summary_period_end + 1` se houver, ou primeira data do
  log).
- `period_end`: data do último evento considerado
  (geralmente igual a `state.current_date`).
- `key_events`: 5–15 frases curtas. Pular trivialidades; preservar
  pontos de inflexão.
- `state_changes_summary`: prosa que costura os eventos em
  narrativa coerente.
- `emerging_tensions`: o que NÃO foi resolvido e ainda pesa nas
  decisões futuras.
- `generated_at`: data atual in-game (`current_state.current_date`).

## Princípios

1. **Compressão narrativa, não eliminação total.** Eventos triviais
   somem; tensões e arcos persistem.
2. **Foco no que afeta decisões futuras.** Personagens relevantes,
   tensões abertas, alinhamentos diplomáticos permanecem visíveis.
   Detalhes táticos somem.
3. **Tamanho final do summary fica em ~500–1000 tokens no total.**
   Se ficar maior que isso, o consolidator está copiando demais.

## O que NÃO fazer

- Não modifique o `event_log.jsonl` original. Ele é arquivo morto
  a partir do summary; o orquestrador cuidará de marcação se
  precisar.
- Não modifique `current_state.json`.
- Não invente eventos não presentes no log.
- Não consolide eventos posteriores ao `current_date`.
