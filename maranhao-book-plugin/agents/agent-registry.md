# Registro de Agentes — Livro sobre o Maranhão

## Arquitetura

```
┌─────────────────────────────────────────┐
│          ORQUESTRADOR (editor-chefe)    │
│  Coordena, prioriza, distribui tarefas  │
└──────────┬──────────────────────────────┘
           │
    ┌──────┴──────────────────────────────┐
    │                                      │
    ▼                                      ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│PESQUISAR │  │ REDIGIR  │  │ REVISAR  │  │ COMPILAR │
│ (skill)  │→ │ (skill)  │→ │ (skill)  │→ │ (skill)  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
    ▲              ▲              │              │
    │              └──── REJEITAR ┘              │
    │                                            ▼
    │                                     ┌──────────┐
    └──────────────── feedback ──────────│  LIVRO   │
                                         └──────────┘
```

## Agentes Disponíveis

### 1. Editor-Chefe (orquestrador)
- **ID**: `editor-chefe`
- **Função**: Coordenação geral do projeto. Distribui tarefas, define prioridades, resolve conflitos editoriais, aprova conteúdo final.
- **Skills**: Todas (supervisão)
- **Ativa**: Sempre

### 2. Pesquisador Histórico
- **ID**: `pesquisador-historico`
- **Função**: Pesquisa sobre história colonial, imperial e republicana do Maranhão
- **Skills**: `research`, `fact-check`
- **Capítulos**: 2, 3, 11
- **Especialidades**: Documentos históricos, cronologias, fontes primárias

### 3. Pesquisador Cultural
- **ID**: `pesquisador-cultural`
- **Função**: Pesquisa sobre manifestações culturais, festas, religiosidade, artes
- **Skills**: `research`
- **Capítulos**: 4, 5, 6, 8
- **Especialidades**: Etnografia, patrimônio imaterial, entrevistas, registros culturais

### 4. Pesquisador Ambiental-Geográfico
- **ID**: `pesquisador-ambiental`
- **Função**: Pesquisa sobre meio ambiente, geografia, ecossistemas, biodiversidade
- **Skills**: `research`
- **Capítulos**: 1, 10, 11
- **Especialidades**: Dados ambientais, mapas, biodiversidade, questões ecológicas

### 5. Pesquisador Socioeconômico
- **ID**: `pesquisador-socioeconomico`
- **Função**: Pesquisa sobre indicadores sociais, economia, políticas públicas
- **Skills**: `research`, `fact-check`
- **Capítulos**: 11, 12
- **Especialidades**: Dados IBGE/IPEA, economia, educação, saúde, infraestrutura

### 6. Redator Narrativo
- **ID**: `redator-narrativo`
- **Função**: Redação de seções com foco narrativo-literário (aberturas, cenas, perfis)
- **Skills**: `writing`
- **Capítulos**: 1, 4, 5, 9, 10, 13
- **Estilo**: Prosa fluida, descritiva, evocativa

### 7. Redator Analítico
- **ID**: `redator-analitico`
- **Função**: Redação de seções com foco analítico-ensaístico (dados, argumentos, contextos)
- **Skills**: `writing`
- **Capítulos**: 2, 3, 6, 11, 12
- **Estilo**: Ensaístico, argumentativo, baseado em dados

### 8. Redator Gastronômico-Cultural
- **ID**: `redator-gastronomico`
- **Função**: Redação de seções sobre gastronomia, saberes tradicionais, cotidiano
- **Skills**: `writing`
- **Capítulos**: 7, 8
- **Estilo**: Sensorial, descritivo, caloroso

### 9. Revisor Editorial
- **ID**: `revisor-editorial`
- **Função**: Revisão de estilo, tom, coesão e adequação editorial
- **Skills**: `review`
- **Capítulos**: Todos
- **Foco**: Qualidade narrativa, adequação ao tom, sensibilidades editoriais

### 10. Verificador Factual
- **ID**: `verificador-factual`
- **Função**: Checagem de fatos, datas, nomes, dados estatísticos
- **Skills**: `fact-check`
- **Capítulos**: Todos
- **Foco**: Precisão, fontes, referências cruzadas

### 11. Compilador
- **ID**: `compilador`
- **Função**: Integração de seções em capítulos e capítulos em livro
- **Skills**: `compile`
- **Capítulos**: Todos
- **Foco**: Consistência, transições, numeração, referências cruzadas

---

## Fluxo de Trabalho por Seção

```
1. editor-chefe         → Define prioridade e atribui tarefa
2. pesquisador-*        → Executa skill:research → output: research-file.md
3. editor-chefe         → Valida pesquisa, autoriza redação
4. redator-*            → Executa skill:writing (input: research-file) → output: draft.md
5. revisor-editorial    → Executa skill:review → output: review-report.md
6. verificador-factual  → Executa skill:fact-check → output: fact-check-report.md
7a. Se APROVADO         → compilador executa skill:compile
7b. Se REVISÃO MENOR    → redator-* ajusta → volta para step 5
7c. Se REVISÃO MAIOR    → redator-* reescreve → volta para step 5
7d. Se REJEITADO        → volta para step 2 com novo briefing
```

## Regras de Atribuição

| Capítulo | Pesquisador | Redator | Notas |
|----------|------------|---------|-------|
| 1 - A Terra Antes do Nome | ambiental | narrativo | Foco em paisagem e povos originários |
| 2 - A Marca Colonial | histórico | analítico | Rigor cronológico essencial |
| 3 - Sangue e Resistência | histórico | analítico | Sensibilidade editorial máxima |
| 4 - Bumba-Meu-Boi | cultural | narrativo | Vivência e imersão |
| 5 - Tambores e Terreiros | cultural | narrativo | Respeito religioso, evitar folclorização |
| 6 - Atenas Brasileira | cultural | analítico | Perfis literários com análise |
| 7 - A Mesa Maranhense | cultural | gastronômico | Sensorial e descritivo |
| 8 - Saberes Tradicionais | cultural + ambiental | gastronômico | Valorizar conhecimento popular |
| 9 - São Luís | ambiental + histórico | narrativo | Equilíbrio patrimônio/modernidade |
| 10 - Além da Capital | ambiental | narrativo | Diversidade territorial |
| 11 - Desigualdades | socioeconômico + histórico | analítico | Dados atualizados obrigatórios |
| 12 - Reinvenção | socioeconômico | analítico | Prospectivo, não ufanista |
| 13 - Epílogo | — | narrativo | Síntese reflexiva |
