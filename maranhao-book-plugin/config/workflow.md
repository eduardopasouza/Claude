# Sistema de Orquestração e Workflow

## Visão Geral

O livro é produzido em **ondas**, não sequencialmente. Capítulos de diferentes Livros podem estar em fases diferentes simultaneamente, maximizando o uso paralelo dos agentes.

---

## Fases de Produção

### Fase 0: Setup (única vez)
```
[ ] Importar contexto da Manus AI
[ ] Validar/ajustar estrutura de capítulos com o autor
[ ] Confirmar diretrizes editoriais
[ ] Configurar agentes e skills
[ ] Definir ordem de prioridade dos capítulos
```

### Fase 1: Pesquisa
```
Entrada: Briefing do editor-chefe (capítulo, seção, escopo, foco)
Agente: pesquisador-* (conforme matriz de atribuição)
Skill: research
Saída: research/{cap-XX}/{secao-X.X}-research.md

Critérios de aprovação:
- Todas as subseções cobertas
- Mínimo de fontes por tipo (conforme editorial-guidelines)
- Dados quantitativos com fonte e ano
- Lacunas explicitamente identificadas
- Sugestões narrativas incluídas
```

### Fase 2: Redação
```
Entrada: Pesquisa aprovada + briefing do editor-chefe
Agente: redator-* (conforme matriz)
Skill: writing
Saída: drafts/{cap-XX}/v{N}-secao-{X.X}.md

Critérios de entrega:
- Metadados YAML completos
- Extensão dentro do range (6.000-12.000 palavras por capítulo)
- Abertura narrativa + desenvolvimento + fechamento reflexivo
- Notas de rodapé para todas as afirmações factuais
- Sem dados inventados
```

### Fase 3: Revisão (paralela)
```
3a. Revisão Editorial
    Agente: revisor-editorial
    Skill: review
    Saída: reviews/{cap-XX}/review-{secao-X.X}.md

3b. Verificação Factual
    Agente: verificador-factual
    Skill: fact-check
    Saída: reviews/{cap-XX}/factcheck-{secao-X.X}.md

As duas revisões acontecem em PARALELO.
```

### Fase 4: Decisão
```
Editor-chefe analisa os reports de revisão e fact-check.

Decisões possíveis:
→ APROVADO (nota ≥ 9.0): Vai para compilação
→ REVISÃO MENOR (7.0-8.9): Redator ajusta pontos específicos → volta Fase 3
→ REVISÃO MAIOR (5.0-6.9): Redator reescreve seções → volta Fase 3
→ REJEITAR (< 5.0): Volta para Fase 1 com novo briefing

Máximo de 3 ciclos de revisão. Após isso, escalona para o autor.
```

### Fase 5: Compilação
```
Quando TODAS as seções de um capítulo estão aprovadas:

Agente: compilador
Skill: compile (nivel: secao_capitulo)
Saída: compiled/{cap-XX-titulo}.md

Tarefas:
- Integrar seções em capítulo coeso
- Ajustar transições
- Renumerar notas de rodapé
- Verificar referências cruzadas
- Adicionar epígrafe
- Atualizar metadados finais
```

### Fase 6: Aprovação do Autor
```
Capítulo compilado é apresentado ao autor (humano).

Decisões:
→ APROVADO: Capítulo finalizado
→ COM AJUSTES: Lista de mudanças → editor-chefe distribui
→ REPENSAR: Volta para fase anterior conforme necessidade
```

### Fase 7: Compilação Final
```
Quando TODOS os capítulos dos 7 Livros estão aprovados:

Agente: compilador
Skill: compile (nivel: capitulo_livro)
Saída: final/maranhao-enciclopedia-narrativa.md

Tarefas:
- Montar volume completo
- Gerar sumário
- Compilar bibliografia geral
- Compilar glossário (Apêndice B)
- Gerar cronologia (Apêndice A)
- Montar índice onomástico (Apêndice H)
- Verificar todas as referências cruzadas
- Contagem final de palavras
```

---

## Estrutura de Diretórios de Trabalho

```
maranhao-book-plugin/
├── config/                          # Configurações (já existe)
├── skills/                          # Definições de skills (já existe)
├── agents/                          # Configurações de agentes (já existe)
├── references/                      # Bibliografias e fontes (já existe)
├── research/                        # OUTPUT da Fase 1
│   ├── cap-01/
│   │   ├── secao-1.1-research.md
│   │   ├── secao-1.2-research.md
│   │   └── ...
│   ├── cap-02/
│   └── ...
├── drafts/                          # OUTPUT da Fase 2
│   ├── cap-01/
│   │   ├── v1-secao-1.1.md
│   │   ├── v2-secao-1.1.md         # (se houve revisão)
│   │   └── ...
│   └── ...
├── reviews/                         # OUTPUT da Fase 3
│   ├── cap-01/
│   │   ├── review-secao-1.1.md
│   │   ├── factcheck-secao-1.1.md
│   │   └── ...
│   └── ...
├── compiled/                        # OUTPUT da Fase 5
│   ├── cap-01-o-chao.md
│   ├── cap-02-natureza-viva.md
│   └── ...
├── final/                           # OUTPUT da Fase 7
│   └── maranhao-enciclopedia.md
└── tracking/                        # Estado do projeto
    └── status-board.md
```

---

## Tracking Board

Modelo de acompanhamento mantido pelo editor-chefe:

```
| Cap | Seção | Pesq | Red | Rev | Fact | Comp | Status | Notas |
|-----|-------|------|-----|-----|------|------|--------|-------|
| 1   | 1.1   | ⬜   | ⬜  | ⬜  | ⬜   | ⬜   | —      |       |
| 1   | 1.2   | ⬜   | ⬜  | ⬜  | ⬜   | ⬜   | —      |       |
| ...                                                            |
```

Legenda: ⬜ Pendente | 🔄 Em andamento | ✅ Aprovado | ❌ Rejeitado | ⏸️ Bloqueado

---

## Prioridade Sugerida de Produção

### Onda 1 (capítulos-âncora)
Capítulos que definem o tom e a ambição do livro:
1. **Cap 4** (O Choque colonial) — testa o narrador histórico
2. **Cap 9** (Bumba-Meu-Boi) — testa o etnógrafo cultural
3. **Cap 1** (O Chão) — abre o livro, define a voz
4. **Cap 18** (O Futuro) — testa a dimensão propositiva

### Onda 2 (coração do livro)
5. Cap 5 (O Sangue)
6. Cap 7 (O Povo)
7. Cap 10 (Tambores e Fé)
8. Cap 11 (Atenas)

### Onda 3 (completude)
9. Cap 2 (Natureza)
10. Cap 3 (Povos Originários)
11. Cap 6 (Província à Periferia)
12. Cap 8 (Invisíveis)

### Onda 4 (território e economia)
13. Cap 13 (A Mesa)
14. Cap 14 (São Luís)
15. Cap 15 (Interior)
16. Cap 12 (Reggae e Sons)

### Onda 5 (estrutura e poder)
17. Cap 16 (Economia)
18. Cap 17 (Política)

### Onda 6 (fechamento)
19. Epílogo
20. Apêndices
21. Compilação final

---

## Regras de Operação Paralela

- **Pesquisadores** podem trabalhar em múltiplos capítulos simultaneamente
- **Redatores** trabalham em 1 capítulo por vez (foco na qualidade)
- **Revisores** podem revisar em paralelo (diferentes capítulos)
- **Compilador** só atua quando um capítulo inteiro está aprovado
- **Editor-chefe** opera continuamente, monitorando todas as fases
- **Máximo de 4 agentes ativos** simultaneamente (gerenciabilidade)
