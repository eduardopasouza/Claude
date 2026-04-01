# Playbook de Produção v2 — Quem é o Maranhão?

> Manual operacional completo. Define processo, skills, templates e checklists.
> Versão: 2.0 | Data: 2026-03-17

---

## 1. VISÃO GERAL

### O que produzimos

```
QUEM É O MARANHÃO?
├── LIVRO (100+ verbetes, coffee table 23×28cm)
│   ├── Edição premium (capa dura)
│   └── E-book (EPUB + PDF interativo)
├── YOUTUBE (~30-50 vídeos de 8min, verbetes-âncora)
├── REELS/SHORTS (1+ por verbete, série numerada)
└── MARCA @quemeomaranhao
```

### Pipeline por verbete

```
PESQUISA → OUTLINE → [APROVAÇÃO] → TEXTO → REEL → VISUAL → [REVIEW]
   ↓          ↓                       ↓       ↓       ↓
 dossiê    esqueleto              markdown   script  briefing
   web      YAML+MD                +YAML    30-90s   triplo
```

**Regra**: 1 verbete completo por vez. Não avançar para o próximo sem finalizar o atual.

---

## 2. SKILLS

### 2.1 SKILL: RESEARCH (Pesquisa)

**Objetivo**: Dossiê completo com fontes verificáveis para um verbete.

**Regra**: Web search OBRIGATÓRIO para todo dossiê. Mínimo 3 fontes por afirmação factual.

#### Template: `research.md`

```markdown
---
verbete: V[XX] — [Título]
parte: [Parte X]
data: YYYY-MM-DD
status: rascunho | revisado | aprovado
fontes_consultadas: [número]
---

# Dossiê de Pesquisa — V[XX]: [Título]

## Resumo executivo
[3-5 linhas: o que este verbete precisa contar]

## Dados-chave
| Dado | Valor | Fonte | Ano |
|------|-------|-------|-----|
| ... | ... | ... | ... |

## Narrativa principal
[Parágrafos com as informações encontradas, organizadas por subtema]

## Dados comparativos
- vs. vizinhos: ...
- vs. Brasil: ...
- vs. mundo: ... (quando relevante)

## Fontes primárias encontradas
[Documentos históricos, relatos, leis, cartas]

## Lacunas
[O que NÃO conseguiu encontrar — flag para o autor]

## Boxes sugeridos
- Lenda: ...
- Maranhense desconhecido: ...
- Documento: ...
- Contrafactual: ...

## Fontes
1. [Autor. Título. Editora, ano. p. XX]
2. [URL — acessado em YYYY-MM-DD]
```

#### Checklist Research
- [ ] Web search realizado (mínimo 5 buscas diferentes)
- [ ] Mínimo 3 fontes por afirmação factual
- [ ] Dados com ano-base identificado
- [ ] Comparações contextuais incluídas (regional/nacional/global)
- [ ] Fontes primárias buscadas
- [ ] Lacunas identificadas e flagadas
- [ ] Hierarquia de fontes respeitada (acadêmica > institucional > jornalística)
- [ ] Flag de incerteza onde necessário

---

### 2.2 SKILL: WRITE (Redação)

**Objetivo**: Texto final do verbete em Markdown + YAML frontmatter + marcações de layout.

**Tom**: Literário (crônica/ensaio, Eliane Brum). Narrador maranhense implícito.

#### Template: `texto.md`

```markdown
---
id: V[XX]
titulo: "[Título]"
parte: [número]
tipo: verbete-âncora | verbete | verbete-curto | verbete-mapa
palavras: [contagem]
boxes:
  - tipo: lenda | maranhense | brasil | mundo | receita | glossario | documento | contrafactual
    titulo: "[Título do box]"
cross_references: [V12, V45, V78]
fio_da_agua: true | false
dados_yaml: [lista de IDs do banco central]
status: rascunho | revisado | aprovado
---

# [Título do Verbete]

> [Epígrafe ou dado de impacto — opcional]

[ABERTURA — gancho variável: pergunta, cena, dado, imagem]

[CORPO — desenvolvimento narrativo com dados integrados]

<!-- LAYOUT: infográfico [descrição] -->

[CONTINUAÇÃO]

<!-- BOX: [tipo] — [título] -->
[Conteúdo do box]
<!-- /BOX -->

[FECHAMENTO — gancho para próximo verbete ou reflexão]

---
**Fontes**: [lista resumida]
**Veja também**: V[XX], V[XX]
```

#### Regras de escrita
1. **Abertura**: Nunca começar com definição. Sempre gancho (pergunta, cena, dado surpreendente)
2. **Dados**: Sempre contextualizados (comparação, proporção, analogia). Nunca dados soltos
3. **Fio da água**: Se `fio_da_agua: true`, incluir referência orgânica a água/rios/mares
4. **Três matrizes**: Indígena, africana e europeia com peso IGUAL
5. **Humor**: Só onde cabe. Nunca em temas de sofrimento
6. **Cross-references**: Marcar palavras-chave que apontam para outros verbetes
7. **Layout marks**: Usar comentários HTML para indicar onde entram infográficos, mapas, boxes

#### Checklist Write
- [ ] YAML frontmatter completo
- [ ] Abertura com gancho (não definição)
- [ ] Dados contextualizados (nunca soltos)
- [ ] Fio da água incluído (se aplicável)
- [ ] Boxes marcados com tipo correto
- [ ] Cross-references indicados
- [ ] Marcações de layout para designer
- [ ] Fontes listadas
- [ ] Tom consistente com style guide

---

### 2.3 SKILL: OUTLINE (Esqueleto)

**Objetivo**: Estrutura do verbete para aprovação antes da redação.

#### Template: `outline.md`

```markdown
---
id: V[XX]
titulo: "[Título]"
parte: [número]
tipo: verbete-âncora | verbete | verbete-curto
palavras_estimadas: [número]
boxes_planejados: [número]
youtube: sim | não | sugerir
reels: [número estimado]
---

# Outline — V[XX]: [Título]

## Tese do verbete
[1 frase: o que este verbete quer dizer]

## Estrutura
1. **Abertura**: [tipo de gancho + descrição]
2. **Bloco 1**: [subtema] — [dados-chave]
3. **Bloco 2**: [subtema] — [dados-chave]
4. **Bloco N**: ...
5. **Fechamento**: [como fecha + conexão com próximo]

## Boxes
- [Tipo]: [Título] — [descrição breve]

## Infográficos/Visuais planejados
- [Descrição do visual] — [dados que usa]

## Cross-references
- V[XX]: [razão da conexão]

## Sugestão YouTube
[Sim/Não. Se sim: ângulo do vídeo de 8min]
```

#### Checklist Outline
- [ ] Tese clara em 1 frase
- [ ] Estrutura com blocos nomeados
- [ ] Boxes identificados por tipo
- [ ] Visuais planejados
- [ ] Cross-references mapeados
- [ ] YouTube avaliado

---

### 2.4 SKILL: REEL (Roteiro de Reel/Short)

**Objetivo**: Roteiro de 30-90 segundos para Instagram Reels / YouTube Shorts / TikTok.

**Formato padrão**: Pergunta + Resposta + Surpresa

#### Template: `reel.md`

```markdown
---
id: REEL-V[XX]-[N]
verbete: V[XX]
duracao: 30s | 60s | 90s
formato: pergunta-resposta-surpresa | lista | comparação | timeline
hashtags: ["#QuemEoMaranhao", "#MaranhaoXX"]
---

# Reel V[XX]-[N]: [Título curto]

## HOOK (0-3s)
[Pergunta ou frase de impacto — texto na tela]

## DESENVOLVIMENTO (3-20s / 3-50s / 3-70s)
[Narração + indicações visuais]

**TELA**: [texto overlay]
**VISUAL**: [o que aparece]
**NARRAÇÃO**: "[o que é dito]"

## SURPRESA/CTA (últimos 5-10s)
[Dado surpreendente ou chamada para ação]

**TELA**: "Quem é o Maranhão? #[número]"

## Notas de produção
- Trilha sugerida: [gênero/mood]
- Transições: [tipo]
- Referência visual: [link ou descrição]
```

#### Durações
| Tipo | Duração | Quando usar |
|------|---------|-------------|
| Curiosidade | 30s | Dado surpreendente isolado |
| História | 60s | Narrativa com contexto |
| Complexo | 90s | Tema que precisa de mais desenvolvimento |

#### Checklist Reel
- [ ] Hook nos primeiros 3 segundos
- [ ] Texto overlay definido
- [ ] Narração escrita por extenso
- [ ] Surpresa no final
- [ ] Duração adequada ao conteúdo
- [ ] Hashtags incluídas
- [ ] ID da série numerado

---

### 2.5 SKILL: VISUAL (Briefing Visual)

**Objetivo**: Briefing triplo para cada visual do livro (designer + IA + SVG).

**Pipeline visual**: SVGs simples + prompts IA + briefings arte final (3 camadas)

#### Paleta maranhense
> **Fonte autoritativa**: ver `style-guide-visual.md` para paleta completa e usos detalhados.

| Cor | Hex | Uso |
|-----|-----|-----|
| Ocre | #C8952E | Cor-base, fundos, títulos |
| Terracota | #B5533E | Destaques, acentos, boxes |
| Verde-mata | #2D6A4F | Natureza, Amazônia, dados positivos |
| Azul-mar | #1B4965 | Água, litoral, mapas |
| Areia | #E8D5B7 | Fundo de boxes |
| Creme | #FAF3E8 | Fundo de página |
| Carvão | #2B2B2B | Texto, contraste, fundo vídeo |
| Vermelho-bumba | #C1292E | Alertas, dados negativos, destaque pontual |
| Roxo-tambor | #5E3A7E | Cultura afro-maranhense, religiosidade |

#### Template: `visual.md`

```markdown
---
id: VIS-V[XX]-[LETRA]
verbete: V[XX]
tipo: infográfico | mapa | ilustração | foto-briefing | página-visual | diagrama
posicao: abertura | corpo | página-inteira | box
---

# Visual V[XX]-[LETRA]: [Descrição curta]

## 1. Briefing para designer
**O que é**: [descrição clara do visual]
**Dados**: [números e informações que devem aparecer]
**Referência de estilo**: [link ou descrição]
**Paleta**: [cores desta peça]
**Tamanho**: [página inteira / meia página / coluna / box]

## 2. SVG simplificado
**Elementos**: [lista de formas e texto]
**Layout**: [descrição do arranjo]
**Cores**: [hex codes]
```svg
<!-- SVG esquemático aqui -->
```

## 3. Prompt para IA generativa
**Prompt**: "[prompt detalhado em inglês para Midjourney/DALL-E/etc]"
**Estilo**: [estilo artístico desejado]
**Referência**: [imagem ou artista de referência]
**NÃO incluir**: [elementos a evitar]
```

#### Tipos de mapa
| Função | Estilo |
|--------|--------|
| Localização | Esquemático, limpo |
| Terras Indígenas | Preciso, georreferenciado |
| Histórico | Estilizado, vintage |
| Fluxos/rotas | Setas e linhas sobre mapa base |

#### Checklist Visual
- [ ] Briefing textual claro para designer humano
- [ ] SVG esquemático com dados corretos
- [ ] Prompt de IA em inglês, detalhado
- [ ] Paleta maranhense respeitada
- [ ] Tamanho e posição definidos
- [ ] Dados verificados contra banco YAML

---

### 2.6 SKILL: BOX (Boxes das 8 séries)

**Objetivo**: Conteúdo dos boxes que acompanham os verbetes.

#### Formatos por série

| Série | Extensão | Formato |
|-------|----------|---------|
| Lenda | 150-300 palavras | Narrativo, tom de contação |
| Maranhense desconhecido | 100-200 palavras | Mini-bio + dado surpreendente |
| E no Brasil | 100-200 palavras | Comparação direta |
| Enquanto isso no mundo | 100-200 palavras | Sincronia temporal |
| Receita | 200-400 palavras | Narrativa + ingredientes + modo |
| Glossário | 50-100 palavras | Expressão + definição + exemplo de uso |
| Documento | 100-300 palavras | Citação + contextualização |
| Contrafactual | 150-250 palavras | Provocação + análise breve |

#### Template: `box dentro do texto.md`

```markdown
<!-- BOX: [série] — [título] -->
### [Ícone da série] [Título]

[Conteúdo formatado conforme a série]

*Fonte: [quando aplicável]*
<!-- /BOX -->
```

#### Checklist Box
- [ ] Série identificada corretamente
- [ ] Extensão dentro do padrão da série
- [ ] Tom adequado à série
- [ ] Posicionamento no verbete faz sentido
- [ ] Fonte indicada (quando factual)

---

### 2.7 SKILL: YOUTUBE (Roteiro de vídeo 8min)

**Objetivo**: Roteiro completo de ensaio visual de 8 minutos (estilo Kurzgesagt/Nerdologia).

**Critério**: Claude sugere ao finalizar cada outline. Só para verbetes maiores/mais fortes.

#### Template: `youtube.md`

```markdown
---
id: YT-V[XX]
verbete: V[XX]
titulo_video: "[Título para YouTube]"
duracao: ~8min
thumbnail_idea: "[descrição da thumbnail]"
---

# Roteiro YouTube — V[XX]: [Título]

## HOOK (0:00-0:30)
**NARRAÇÃO**: "[texto exato]"
**VISUAL**: [descrição do que aparece na tela]

## ATO 1 — [Subtítulo] (0:30-2:30)
**NARRAÇÃO**: "[texto]"
**B-ROLL**: [descrição]
**INFOGRÁFICO**: [descrição animada]
**TRANSIÇÃO**: [tipo]

## ATO 2 — [Subtítulo] (2:30-5:00)
[mesmo formato]

## ATO 3 — [Subtítulo] (5:00-7:00)
[mesmo formato]

## FECHAMENTO (7:00-8:00)
**NARRAÇÃO**: "[texto — reflexão final + CTA]"
**VISUAL**: [encerramento]
**CTA**: "Se inscreva / Próximo vídeo: V[XX]"

## NOTAS DE PRODUÇÃO
- **Trilha**: [gênero, mood, referências]
- **Animações**: [lista de animações necessárias]
- **Infográficos**: [lista com dados]
- **Referências visuais**: [links/descrições]
- **Timestamps para descrição**: [lista]
- **Tags SEO**: [lista]

## FONTES DO VÍDEO
[Para colocar na descrição do YouTube]
```

#### Checklist YouTube
- [ ] Hook nos primeiros 30 segundos
- [ ] Narração escrita por extenso (não tópicos)
- [ ] B-roll descrito para cada segmento
- [ ] Infográficos animados descritos
- [ ] Transições indicadas
- [ ] Trilha sugerida
- [ ] CTA no final
- [ ] Timestamps
- [ ] Fontes para descrição
- [ ] Thumbnail descrita

---

### 2.8 SKILL: INFOGRÁFICO

**Objetivo**: Briefing específico para infográficos complexos (diferentes do visual briefing padrão).

#### Template

```markdown
---
id: INFO-V[XX]-[N]
verbete: V[XX]
tipo: timeline | comparativo | mapa-fluxo | painel-dados | processo
dados_fonte: [IDs do banco YAML]
---

# Infográfico V[XX]-[N]: [Título]

## Dados brutos
| ... | ... |
[tabela com todos os dados que entram]

## Hierarquia visual
1. [Dado principal — maior destaque]
2. [Dados secundários]
3. [Contexto]

## Layout descrito
[Descrição textual do layout: o que fica onde, fluxo de leitura]

## Paleta
[Cores específicas deste infográfico]

## Referência
[Link ou descrição de infográfico similar]
```

---

### 2.9 SKILL: SOCIAL-MEDIA

**Objetivo**: Adaptar conteúdo de cada verbete para diferentes plataformas.

#### Formatos

| Plataforma | Formato | Extensão |
|------------|---------|----------|
| Instagram (post) | Carrossel 5-10 slides | 1 frase por slide + dado visual |
| Instagram (caption) | Texto | 200-300 palavras + hashtags |
| Twitter/X | Thread | 5-10 tweets encadeados |
| LinkedIn | Artigo curto | 300-500 palavras |

---

### 2.10 SKILL: REVIEW (Revisão)

**Objetivo**: Revisão em 3 etapas com checklist hierárquico.

#### Etapa 1 — Autorevisão (Claude)
**Checklist obrigatório**:
- [ ] Dados conferidos contra banco YAML
- [ ] Fontes verificadas (mín. 3 por afirmação)
- [ ] Tom consistente com style guide
- [ ] Fio da água presente (se aplicável)
- [ ] Três matrizes com peso igual
- [ ] Cross-references corretos
- [ ] YAML frontmatter completo
- [ ] Sem dados soltos (todos contextualizados)
- [ ] Marcações de layout para designer

**Checklist recomendado**:
- [ ] Variação de aberturas (não repetir ganchos)
- [ ] Boxes posicionados no melhor momento
- [ ] Linguagem inclusiva sem ser forçada
- [ ] Referências a água orgânicas (não forçadas)

**Checklist polimento**:
- [ ] Ritmo de frases (curtas e longas alternadas)
- [ ] Eliminação de clichês
- [ ] Precisão de adjetivos

#### Etapa 2 — Revisão cruzada (Claude em sessão separada)
- Ler verbete sem contexto prévio
- Verificar se é autocontido
- Identificar afirmações sem fonte
- Testar se a abertura prende
- Verificar coerência com outros verbetes já produzidos

#### Etapa 3 — Aprovação do autor
- Texto apresentado com marcações de layout
- Autor aprova, pede ajustes ou rejeita

---

## 3. BANCO DE DADOS CENTRAL

**Arquivo**: `banco-dados/dados-centrais.yaml`

Toda informação factual usada em mais de 1 verbete deve estar no banco central. O texto referencia o banco; nunca inventar dados.

**Campos obrigatórios**:
```yaml
- id: [CAT]-[NNN]        # Prefixo da categoria + número sequencial
  categoria: [ver lista]  # geografia | demografia | indígena | quilombo | economia | cultura | história | social | meio-ambiente | turismo
  descricao: "..."        # O que o dado descreve (frase curta)
  valor: "..."            # O dado em si (número, percentual, fato)
  fonte: "..."            # Fonte completa (autor/instituição, ano, documento)
  ano_base: YYYY          # Ano de referência do dado
  verbetes: [V01, V05]    # Lista de verbetes que usam este dado
```

**Prefixos por categoria**:
`GEO` (geografia), `DEM` (demografia), `IND` (indígena), `QUI` (quilombo), `ECO` (economia), `CUL` (cultura), `HIS` (história), `SOC` (social), `AMB` (meio-ambiente), `TUR` (turismo)

**Regra de indexação — quando registrar novo dado**:

1. **Durante a pesquisa**: todo dado factual encontrado na web que tenha fonte verificável deve ser registrado no banco YAML, mesmo que só um verbete o use por enquanto
2. **Verificação cruzada obrigatória**: antes de registrar, confrontar o dado com pelo menos 1 fonte adicional. Se houver divergência, registrar ambas as fontes e marcar com flag:
   ```yaml
   nota: "Divergência: fonte A diz X, fonte B diz Y. Adotado valor de fonte A (mais recente/oficial)."
   ```
3. **Confronto com banco existente**: antes de adicionar, verificar se o dado já existe no banco. Se existir, atualizar se a nova fonte for mais recente ou mais confiável. Nunca duplicar.
4. **Numeração sequencial**: usar o próximo número disponível na categoria (ex: se último GEO é GEO-025, próximo é GEO-026)
5. **Verbetes**: listar todos os verbetes que usam ou poderão usar o dado
6. **Dados efêmeros**: dados que mudam anualmente (PIB, população, indicadores) devem ter `ano_base` explícito e nota na introdução do livro sobre data de corte

**Hierarquia de confiabilidade das fontes**:
> Fonte autoritativa: ver `style-guide-editorial.md` seção 14.3 para versão completa.

```
1. Fontes primárias > 2. Acadêmicas > 3. Dados oficiais > 4. Jornalísticas > 5. Audiovisuais
6. Wikipedia → NUNCA como fonte final, apenas ponto de partida
```

**Regra**: Evolutivo. Começar básico, expandir conforme verbetes são produzidos.

---

## 4. CAPACIDADES DO CLAUDE

### O que Claude faz bem
- Textos narrativos com dados (livro, ensaios, boxes)
- Roteiros completos (YouTube, Reels)
- SVGs simples (mapas esquemáticos, diagramas, ícones)
- Prompts para IA generativa (Midjourney, DALL-E)
- Briefings visuais detalhados para designers
- Organização de dados em YAML/JSON
- Pesquisa web com fontes
- Revisão editorial e factual
- Adaptação multiplataforma

### O que Claude NÃO faz
- Gerar imagens (fotografias, ilustrações complexas)
- Gerar áudio ou vídeo
- Acessar banco de dados em tempo real
- Validar informações sem pesquisa web

### Implicação prática
Todo visual do livro passa por briefing triplo: (1) descrição textual para designer humano, (2) SVG esquemático que Claude gera, (3) prompt de IA generativa que Claude escreve. A execução final é humana ou por ferramenta externa.

---

## 5. REGRAS GERAIS

1. **1 verbete por vez** — pipeline completo antes de avançar
2. **Web obrigatório** — toda pesquisa usa web search
3. **3 fontes mínimo** — por afirmação factual
4. **Verificação cruzada obrigatória** — todo dado pesquisado na web deve ser confrontado com pelo menos 1 fonte adicional antes de ser usado no texto
5. **Banco YAML alimentado na pesquisa** — todo dado factual verificado deve ser registrado no banco central (`dados-centrais.yaml`) durante a fase de pesquisa, não depois. Confrontar com dados já existentes no banco para evitar duplicatas e contradições
6. **3 matrizes iguais** — indígena = africana = europeia em profundidade
7. **Fio da água** — orgânico, nunca forçado
8. **Dados + alma** — nunca dado sem contexto, nunca narrativa sem dado
9. **Aprovação** — outline precisa de OK do autor antes de redigir
10. **Review** — 3 etapas, checklist hierárquico

---

*Playbook v2 — 2026-03-17*
*Referência: coordination-v3.md + registro-decisoes-73-rodadas.md*
