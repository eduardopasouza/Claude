# Good Parenting Plugin

Plugin de apoio à paternidade para Claude Code. Ajuda Eduardo a ser o melhor pai possível para Bernardo.

## Como usar

Use `/good-parenting` para iniciar uma conversa sobre qualquer tema parental. O orquestrador vai rotear automaticamente para a skill certa.

### Skills disponíveis:
- `/good-parenting` — Orquestrador principal (roteia automaticamente)
- `/good-parenting:saude` — Saúde, sintomas, alimentação, sono, desenvolvimento
- `/good-parenting:diario` — Registrar marcos, eventos, observações
- `/good-parenting:orientacao` — Disciplina, limites, rotina, comportamento
- `/good-parenting:autodesenvolvimento` — Vícios, hábitos, autocuidado, ser exemplo
- `/good-parenting:relacionamento` — Casal, intimidade, sogra, família
- `/good-parenting:educacao` — Escola, atividades, planejamento, finanças
- `/good-parenting:onboarding` — Novo cadastro ou atualização de perfil

## Estrutura de memória

```
good-parenting/
├── memoria/
│   ├── perfis/           # Perfis permanentes (pai, filho, família)
│   ├── sessoes/          # Registro de cada sessão
│   ├── diretrizes/       # Decisões firmes de criação
│   └── diario/           # Diário mensal de Bernardo
│       └── YYYY-MM.md
├── memoria-geral.md      # Consolidação de todas as interações
└── skills/               # (reservado para extensões futuras)
```

## Regras fundamentais

1. **SEMPRE** ler memória antes de responder qualquer pergunta parental
2. **NUNCA** dar resposta genérica — contextualizar com dados da família
3. **SEMPRE** atualizar memória após interação significativa
4. **NUNCA** substituir profissional de saúde — orientar buscar atendimento quando necessário
5. Respostas em português brasileiro, tom direto e prático
6. Respeitar as diretrizes de criação já definidas pelo pai
