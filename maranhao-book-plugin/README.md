# Maranhão Inteiro — Terra, povo e futuro

Plugin para produção do livro.

## Arquivos

| Arquivo | Função |
|---------|--------|
| `coordination.md` | Estado do projeto. **Ler sempre ao iniciar.** |
| `playbook.md` | Processo completo: tese, arco, etapas, regras. |
| `skills/research.md` | Pesquisa profunda com fontes |
| `skills/write.md` | Redação narrativa com dados |
| `skills/review.md` | Revisão editorial e factual |

## Como usar

**Modo interativo**: "Vamos pensar no capítulo 3" → conversa, pesquisa, escreve junto.

**Modo delegado**: "Pesquisa o capítulo 14" → entrega research.md para aprovação.

**Fluxo completo**: Pesquisa → Outline → [Aprovação] → Redação → Revisão → [Aprovação]

## Estrutura de trabalho

```
drafts/
├── cap-XX-titulo/
│   ├── research.md    # Pesquisa
│   ├── outline.md     # Esqueleto (aprovado pelo autor)
│   ├── draft-vN.md    # Versões do texto
│   └── review.md      # Feedback de revisão
└── rejected/          # Material rejeitado (referência)

final/                 # Capítulos aprovados pelo autor
references/            # Bibliografia e dados
```
