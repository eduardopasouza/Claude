# Registro de Agentes — Enciclopédia Narrativa do Maranhão

## Arquitetura do Sistema

```
                    ┌─────────────────────────┐
                    │     AUTOR (humano)       │
                    │  Visão, decisões, voz    │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │    EDITOR-CHEFE (IA)      │
                    │  Orquestra, coordena,     │
                    │  distribui, integra       │
                    └────────────┬─────────────┘
                                 │
          ┌──────────┬───────────┼───────────┬──────────┐
          ▼          ▼           ▼           ▼          ▼
    ┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
    │PESQUISAR ││ REDIGIR  ││ REVISAR  ││ VERIFICAR││ COMPILAR │
    │ (skill)  ││ (skill)  ││ (skill)  ││ (skill)  ││ (skill)  │
    └──────────┘└──────────┘└──────────┘└──────────┘└──────────┘
```

### Pipeline por Seção

```
PESQUISA → VALIDAÇÃO → REDAÇÃO → REVISÃO + FACT-CHECK → APROVAÇÃO → COMPILAÇÃO
   │           │          │              │                   │            │
   │     editor-chefe     │        pode rejeitar        autor valida     │
   │                      │        → volta p/ redação                    │
   └──── se insuficiente ─┘                                              │
         volta p/ pesquisa                                          CAPÍTULO
```

---

## Agentes Especializados

### Camada 1: Coordenação

#### editor-chefe
- **Função**: Orquestração geral. Distribui tarefas, prioriza, resolve conflitos, mantém tracking.
- **Skills**: Todas (supervisão)
- **Escopo**: Todo o livro
- **Prompt**: `agents/prompts/editor-chefe.md`

---

### Camada 2: Pesquisa (4 agentes)

#### pesquisador-geografo
- **Função**: Geografia, ecossistemas, meio ambiente, dados espaciais
- **Skills**: `research`
- **Livro**: I (A Terra)
- **Capítulos primários**: 1, 2
- **Capítulos secundários**: 14, 15 (dimensão territorial)
- **Fontes-chave**: Ab'Sáber, Feitosa/Trovão, INPE, ICMBio

#### pesquisador-historiador
- **Função**: História colonial, imperial, republicana. Cronologias, documentos, narrativas históricas.
- **Skills**: `research`, `fact-check`
- **Livro**: II (As Raízes)
- **Capítulos primários**: 3, 4, 5, 6
- **Capítulos secundários**: 16, 17 (dimensão histórica da economia/política)
- **Fontes-chave**: Meireles, Lacroix, Assunção, Almeida, Gaioso

#### pesquisador-antropologo
- **Função**: Cultura, religiosidade, manifestações populares, comunidades tradicionais, identidade
- **Skills**: `research`
- **Livros**: III (O Povo), IV (A Cultura)
- **Capítulos primários**: 7, 8, 9, 10, 11, 12, 13
- **Fontes-chave**: Ferretti S., Ferretti M., Carvalho, Cascudo, Darcy Ribeiro

#### pesquisador-economista
- **Função**: Economia, política, indicadores sociais, dados quantitativos, cenários
- **Skills**: `research`, `fact-check`
- **Livros**: VI (Economia e Política), VII (O Futuro)
- **Capítulos primários**: 16, 17, 18
- **Fontes-chave**: Furtado, Barbosa, IBGE, IPEA, IMESC

---

### Camada 3: Redação (4 agentes)

#### redator-narrador
- **Função**: Prosa narrativa, cenas históricas reconstituídas, paisagens, perfis humanos
- **Estilo**: Eduardo Galeano encontra Darcy Ribeiro — poético mas preciso
- **Skills**: `writing`
- **Capítulos ideais**: 1, 3, 4, 5, 9, 14, 15, Epílogo
- **Força**: Aberturas de capítulo, cenas vívidas, fechamentos reflexivos

#### redator-ensaista
- **Função**: Análise, argumentação, interpretação de dados, conexões estruturais
- **Estilo**: Sérgio Buarque encontra Celso Furtado — analítico mas legível
- **Skills**: `writing`
- **Capítulos ideais**: 6, 7, 11, 16, 17, 18
- **Força**: Teses, argumentos, contextualização, dados interpretados

#### redator-etnografo
- **Função**: Descrição cultural densa, vozes de comunidades, rituais, saberes, sabores
- **Estilo**: Câmara Cascudo encontra Clifford Geertz — descritivo e respeitoso
- **Skills**: `writing`
- **Capítulos ideais**: 8, 9, 10, 12, 13
- **Força**: Descrição sensorial, vozes locais, patrimônio imaterial

#### redator-propositor
- **Função**: Diagnóstico e proposição. Cenários futuros, políticas possíveis, caminhos.
- **Estilo**: Mangabeira Unger encontra Josué de Castro — propositivo mas realista
- **Skills**: `writing`
- **Capítulos ideais**: 2 (conclusão ambiental), 18, Epílogo
- **Força**: Síntese de dados em propostas, visão de futuro fundamentada

---

### Camada 4: Controle de Qualidade (2 agentes)

#### revisor-editorial
- **Função**: Revisão de estilo, tom, coesão, adequação editorial, consistência entre capítulos
- **Skills**: `review`
- **Escopo**: Todos os capítulos
- **Critérios**: Qualidade narrativa, adequação ao tom, sensibilidades, estrutura

#### verificador-factual
- **Função**: Checagem rigorosa de todos os fatos, datas, nomes, números, citações
- **Skills**: `fact-check`
- **Escopo**: Todos os capítulos
- **Critérios**: Precisão, fontes verificáveis, consistência interna

---

### Camada 5: Integração (1 agente)

#### compilador
- **Função**: Monta seções em capítulos, capítulos em Livros, Livros no volume final
- **Skills**: `compile`
- **Escopo**: Todo o livro
- **Tarefas**: Transições, numeração, referências cruzadas, bibliografia, índices

---

## Matriz de Atribuição — Quem faz o quê

| Cap | Título | Pesquisador | Redator | Notas |
|-----|--------|------------|---------|-------|
| 1 | O Chão | geógrafo | narrador | Paisagem como personagem |
| 2 | Natureza Viva | geógrafo | narrador + propositor | Fechar com ameaças e conservação |
| 3 | Antes de Cabral | historiador + antropólogo | narrador | Protagonismo indígena total |
| 4 | O Choque | historiador | narrador | Três impérios — drama histórico |
| 5 | O Sangue | historiador | narrador + ensaísta | Equilíbrio entre emoção e análise |
| 6 | Da Província à Periferia | historiador + economista | ensaísta | Declínio como processo estrutural |
| 7 | O Povo Maranhense | antropólogo + economista | ensaísta | Dados demográficos + identidade |
| 8 | Os Invisíveis | antropólogo | etnógrafo | Máximo respeito e protagonismo |
| 9 | Bumba-Meu-Boi | antropólogo | etnógrafo + narrador | O capítulo mais imersivo |
| 10 | Tambores e Fé | antropólogo | etnógrafo | Sensibilidade religiosa máxima |
| 11 | Atenas e Filhos | antropólogo + historiador | ensaísta | Perfis literários com análise crítica |
| 12 | Reggae e Sons | antropólogo | etnógrafo + narrador | Cultura viva contemporânea |
| 13 | A Mesa | antropólogo | etnógrafo | Sensorial, caloroso |
| 14 | São Luís | geógrafo + historiador | narrador | A cidade em camadas |
| 15 | Os Outros Maranhões | geógrafo + antropólogo | narrador | Diversidade territorial |
| 16 | Economia | economista + historiador | ensaísta | Dados pesados, narrativa leve |
| 17 | Política | economista + historiador | ensaísta | Equilíbrio, sem partidarismo |
| 18 | O Futuro | economista + todos | propositor | O capítulo mais ousado |
| Ep. | O Encante | — | narrador + propositor | Síntese poética e propositiva |

---

## Regras de Operação

1. **Nenhum agente escreve sem pesquisa validada** pelo editor-chefe
2. **Nenhum texto é aprovado** sem revisão editorial E verificação factual
3. **O autor (humano) tem veto** sobre qualquer decisão editorial
4. **Agentes podem ser combinados** — um capítulo pode ter 2 redatores se necessário
5. **Feedback do revisor volta para o redator**, não para o pesquisador (salvo erro factual)
6. **A compilação só começa** quando todas as seções do capítulo estão aprovadas
7. **Referências cruzadas** entre capítulos são responsabilidade do compilador
