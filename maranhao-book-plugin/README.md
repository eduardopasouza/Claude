# Maranhão — Enciclopédia Narrativa

Plugin para produção do livro. Três skills, um arquivo de coordenação.

## Como Usar

### Modo interativo (trabalhar junto)
Abra uma conversa e diga o que quer fazer:
- "Vamos pensar no capítulo sobre os povos originários"
- "Pesquisa sobre o reggae no Maranhão"
- "Escreve a seção sobre a Balaiada"
- "Revisa o que temos do capítulo 4"

### Modo delegado (mandar e revisar depois)
- "Pesquisa e escreve o capítulo 12"
- "Revisa todos os capítulos prontos"

### Estado do projeto
Tudo está em `coordination.md` — estrutura, o que existe, decisões, padrão de qualidade.

## Estrutura

```
maranhao-book-plugin/
├── coordination.md      # Estado do projeto (ler sempre ao iniciar)
├── skills/
│   ├── research.md      # Pesquisa profunda com fontes
│   ├── write.md         # Redação narrativa com dados
│   └── review.md        # Revisão editorial e factual
├── drafts/              # Capítulos em produção
│   ├── cap-XX-titulo/
│   │   ├── research.md  # Material de pesquisa
│   │   ├── draft-vN.md  # Versões do texto
│   │   └── review.md    # Feedback de revisão
│   └── rejected/        # Material rejeitado (referência)
├── references/          # Bibliografia e dados
└── final/               # Capítulos aprovados pelo autor
```
