# Playbook de Produção — Quem é o Maranhão?

> Manual operacional. Define o processo passo a passo para produzir cada unidade de conteúdo. Leia junto com `style-guide-editorial.md` (como escrever) e `guia-de-pesquisa.md` (como pesquisar).

---

## 1. VISÃO GERAL DO PROJETO

### O que estamos produzindo

```
QUEM É O MARANHÃO?
├── LIVRO (400+ páginas, 24 capítulos, ~150 tópicos)
│   ├── Edição premium (capa dura, grande formato)
│   ├── Edição popular (brochura)
│   └── E-book (PDF + ePub)
├── YOUTUBE (~150 vídeos de 8min, ensaio visual)
├── REELS/SHORTS (~500+ pílulas de 60s, série numerada)
├── DOCUMENTÁRIO (1-2h, meta futura)
└── MARCA @quemeomaranhao
```

### Hierarquia de conteúdo

```
PARTE (6 — divisórias visuais com epígrafe e parágrafo-ponte)
  └── CAPÍTULO (24 — com subtítulo-resposta e epígrafe)
        └── TÓPICO (800-1.200 palavras, autocontido, modular)
              → Gera: 1 vídeo YouTube 8min
              → Gera: 1 briefing visual
              └── SUBTÓPICO (150-300 palavras, emerge da pesquisa)
                    → Gera: 1 Reel/Short numerado
```

### As 6 Partes

| Parte | Nome | Capítulos | Arco |
|-------|------|-----------|------|
| I | O Chão | Cap 1 | O palco: terra e biomas |
| II | A Formação | Cap 2-7 | De onde viemos: primeiros habitantes → colônia → ouro branco → escravidão → levantes → ascensão e queda |
| III | O Povo | Cap 8-10 | Quem somos: indígenas → povo → diáspora |
| IV | As Criações | Cap 11-16 | O que inventamos: boi → festas → música → fé → letras → comida |
| V | O Território e a Estrutura | Cap 17-22 | Onde vivemos: São Luís → território → economia → turismo → poder → educação |
| VI | O Amanhã | Cap 23-24 | Para onde ir: esporte/cultura pop → futuro |

### Tese e fio condutor

**Tese**: Por que a riqueza do Maranhão não fica no Maranhão? O padrão se repete com diferentes mercadorias, em diferentes séculos — mas a estrutura é a mesma.

**Fio condutor**: A pergunta "Quem é o Maranhão?" — cada capítulo responde de um ângulo diferente.

### Transições entre Partes

Cada Parte termina com um parágrafo-ponte:

- I → II: *"Esse é o palco. Agora, a história que aconteceu nele."*
- II → III: *"Essa é a história de como o Maranhão se formou. Mas quem são os maranhenses que essa formação produziu?"*
- III → IV: *"Um povo marcado por tanto — e que, apesar de tudo, criou tanto."*
- IV → V: *"Essa criação não acontece no abstrato. Acontece em lugares concretos, com indicadores reais."*
- V → VI: *"Se o diagnóstico é claro, os caminhos também podem ser."*

---

## 2. DOCUMENTOS DE REFERÊNCIA

Antes de produzir qualquer conteúdo, o Claude deve ter lido:

| Documento | O que define | Arquivo |
|-----------|-------------|---------|
| Coordenação | Estrutura, capítulos, tópicos, estado do projeto | `coordination-v2.md` |
| Style Guide Editorial | Tom, voz, vocabulário, ganchos, boxes, referências, anti-padrões | `style-guide-editorial.md` |
| Guia de Pesquisa | Fontes, hierarquia, banco de dados, validação, processo | `guia-de-pesquisa.md` |
| Proposta Editorial | Visão geral, público, tese, diferencial | `proposta-editorial.md` |
| Este playbook | Processo de produção, templates, fluxo, coordenação | `playbook.md` |

**Regra**: ao iniciar qualquer sessão, ler `coordination-v2.md` + este playbook. Consultar os demais conforme necessário.

---

## 3. PROCESSO DE PRODUÇÃO — FLUXO POR TÓPICO

A unidade de produção é o **tópico** (800-1.200 palavras). Capítulos são conjuntos de tópicos. O fluxo para cada tópico é:

```
┌─────────────────────────────────────────────────┐
│  ETAPA 0: PREPARAÇÃO                            │
│  Ler coordination-v2.md, identificar tópico,    │
│  entender posição no arco                       │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ETAPA 1: PESQUISA                              │
│  Seguir guia-de-pesquisa.md                     │
│  Pesquisa web ativa + banco de dados            │
│  Saída: research.md + banco-de-fontes.yaml      │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ETAPA 2: OUTLINE DO TÓPICO                     │
│  Esqueleto com argumento, fontes, gancho,       │
│  conexões, boxes previstos                      │
│  Saída: outline.md                              │
│                                                 │
│  → AUTOR APROVA OUTLINE ←                      │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ETAPA 3: REDAÇÃO DO TÓPICO                     │
│  Seguir style-guide-editorial.md                │
│  800-1.200 palavras, notas de rodapé,           │
│  ganchos, pontes, boxes, glossário              │
│  Saída: draft-v1.md                             │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ETAPA 4: DERIVADOS                             │
│  Roteiro YouTube 8min                           │
│  Roteiro(s) Reel/Short                          │
│  Briefing visual (storyboard textual)           │
│  Saída: youtube.md, reels.md, visual.md         │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ETAPA 5: REVISÃO                               │
│  Factual + narrativa + padrão + derivados       │
│  Saída: review.md                               │
│                                                 │
│  Aprovado → autor | Ajustes → volta p/ 3 ou 4  │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ETAPA 6: APROVAÇÃO DO AUTOR                    │
│                                                 │
│  Aprovado → final/                              │
│  Com ajustes → volta p/ etapa indicada          │
│  Rejeitar → volta p/ pesquisa                   │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  ATUALIZA COORDINATION-V2.MD                    │
│  Status do tópico, conexões, dados validados    │
└─────────────────────────────────────────────────┘
```

---

## 4. ETAPAS DETALHADAS

### Etapa 0: Preparação

**Antes de qualquer trabalho**:

1. Ler `coordination-v2.md` — entender estado atual do projeto
2. Identificar o tópico a produzir (ex: 4.2 — O algodão)
3. Verificar:
   - Qual capítulo? Qual Parte?
   - Qual é o subtítulo-resposta do capítulo?
   - Há material existente em `drafts/`?
   - Quais tópicos vizinhos já existem? (para pontes)
   - Quais conexões cruzadas são esperadas?

---

### Etapa 1: Pesquisa

**Processo completo definido em `guia-de-pesquisa.md`**. Resumo:

1. Definir escopo e argumento central do tópico
2. Consultar banco de dados centralizado (`references/banco-de-fontes.yaml`)
3. Pesquisa por categoria: dados oficiais → historiografia → academia → fontes primárias
4. Pesquisa web ativa (Google Scholar, IBGE, repositórios)
5. Catalogar fontes no banco de dados
6. Produzir relatório de pesquisa

**Mínimos**: 3+ fontes por tópico, 2+ categorias, todo dado com fonte.

**Saída**: relatório integrado em `drafts/cap-XX-titulo/research.md`

---

### Etapa 2: Outline do tópico

**Objetivo**: esqueleto que o autor aprova antes da redação.

**Template**:

```markdown
# Outline — Tópico X.Y: [Título]

## Argumento central
[1-2 frases: o que este tópico mostra/defende]

## Posição no arco
- Capítulo: [nº e título]
- Parte: [nº e nome]
- Como avança a tese: [1 frase]

## Gancho de abertura
- Tipo: [pergunta / cena / dado / anedota / contraste / frase-gatilho]
- Conteúdo: [o gancho em si]

## Estrutura do texto
1. [Bloco 1 — ~200-300 palavras]: [o que cobre]
   - Dados-chave: [com fonte]
   - Citação: [se houver]
2. [Bloco 2 — ~200-300 palavras]: [o que cobre]
   - ...
3. [Bloco 3 — ~200-300 palavras]: [o que cobre]
   - ...

## Texto-ponte
- De: [tópico anterior] → Como conecta
- Para: [tópico seguinte] → Como conecta

## Conexões cruzadas
- ↗ Tópico X.Z: [natureza da conexão]
- ↗ Tópico W.V: [natureza da conexão]

## Boxes previstos
- [ ] [Tipo]: [tema] (~X palavras)

## Glossário inline
- [ ] [termo]: [definição curta prevista]

## Infográfico/mapa sugerido
- [ ] [descrição]

## Extensão estimada
[X palavras texto principal + X palavras boxes]
```

**O outline é apresentado ao autor. Só avança com aprovação.**

**Saída**: `drafts/cap-XX-titulo/outline.md`

---

### Etapa 3: Redação do tópico

**Regras completas em `style-guide-editorial.md`**. Resumo:

| Aspecto | Regra |
|---------|-------|
| Extensão | 800-1.200 palavras (texto principal) |
| Voz | 2ª pessoa predominante |
| Tom | Eduardo Bueno — irônico, pop, rigoroso |
| Abertura | Gancho alternado (pergunta, cena, dado, anedota, contraste) |
| Fontes | Notas de rodapé numeradas por capítulo |
| Dados | Inline + infográficos para séries |
| Boxes | Orgânico (biográfico, curiosidade, "E se?", glossário lateral) |
| Pontes | 1-3 frases conectando ao tópico seguinte |
| Conexões | Mínimo 2 (texto + ícone ↗) |
| Anti-padrões | Sem clichês, sem listas disfarçadas, sem texto genérico |

**Checklist antes de finalizar o draft**:

```
☐ 800-1.200 palavras
☐ Gancho de abertura (não definição, não resumo)
☐ Voz 2ª pessoa predominante
☐ Notas de rodapé para afirmações factuais
☐ Texto-ponte para tópico seguinte
☐ Mínimo 2 conexões cruzadas
☐ Sem clichês proibidos
☐ Sem anti-padrões
☐ Vocabulário conforme style guide (escravizado, povos indígenas, etc.)
☐ Posicionamento político conforme style guide
```

**Saída**: `drafts/cap-XX-titulo/draft-v1.md`

---

### Etapa 4: Derivados

Cada tópico gera 3 outputs derivados do texto principal:

#### 4a. Roteiro YouTube (8 min)

**Formato**: ensaio visual narrado. Estilo Kurzgesagt/Vox.

**Template**:

```markdown
# Roteiro YouTube — Tópico X.Y: [Título]

**Duração**: ~8 min (~1.200 palavras de narração)
**Estilo**: Ensaio visual narrado
**Narração**: Voz IA
**Legendas**: PT-BR + EN

## Gancho (0:00-0:30)
[Abertura que prende — pode ser diferente do livro]
VISUAL: [descrição da cena/imagem/infográfico]

## Desenvolvimento (0:30-6:30)
### Bloco 1: [subtema] (0:30-2:30)
NARRAÇÃO: [texto]
VISUAL: [descrição]

### Bloco 2: [subtema] (2:30-4:30)
NARRAÇÃO: [texto]
VISUAL: [descrição]

### Bloco 3: [subtema] (4:30-6:30)
NARRAÇÃO: [texto]
VISUAL: [descrição]

## Fechamento (6:30-7:30)
NARRAÇÃO: [reflexão/gancho para próximo]
VISUAL: [descrição]

## CTA (7:30-8:00)
NARRAÇÃO: "Se você não sabia disso sobre o Maranhão, se inscreve.
Quem é o Maranhão? A gente descobre junto."
VISUAL: Logo @quemeomaranhao + próximo vídeo

## Fontes na descrição
- [lista de fontes principais]
```

#### 4b. Roteiro(s) Reel/Short

**Formato**: pílula de ~60 segundos, série numerada.

**Template**:

```markdown
# Reel — Quem é o Maranhão? #[N]: [Título]

**Duração**: ~60s (~150-200 palavras)
**Formato**: Vertical 9:16
**Narração**: Voz IA
**Legenda**: PT-BR + EN

## Hook (0-5s)
[Frase de impacto que prende no scroll]
VISUAL: [descrição]

## Conteúdo (5-50s)
[Texto da narração]
VISUAL: [descrição, transições]

## Fechamento (50-60s)
"Quem é o Maranhão? #[N]."
VISUAL: Logo + "Segue pra descobrir mais"
```

**Quantos Reels por tópico**: depende dos subtópicos que emergirem. Mínimo 1, sem máximo.

#### 4c. Briefing visual (storyboard textual)

**Para cada imagem, infográfico ou mapa previsto no tópico**.

**Template**:

```markdown
# Briefing Visual — Tópico X.Y

## Imagem 1: [título/descrição curta]
- **Tipo**: [infográfico / mapa / cena histórica / foto / ilustração IA]
- **Conteúdo**: [descrição detalhada do que deve mostrar]
- **Dados**: [se infográfico, quais dados exatos com fonte]
- **Referência visual**: [se houver referência de estilo]
- **Paleta**: [cores predominantes, conforme style guide visual]
- **Texto na imagem**: [se houver legendas, rótulos]
- **Uso**: [livro página X / YouTube minuto X / Reel #N]

## Imagem 2: ...
```

**Saída**: `drafts/cap-XX-titulo/youtube.md`, `reels.md`, `visual.md`

---

### Etapa 5: Revisão

**Três verificações + uma quarta para derivados**:

#### 5a. Verificação factual
- Toda afirmação com nota de rodapé está correta?
- Dados numéricos conferem com a fonte citada?
- Nomes, datas, grafias corretos?
- Citações fiéis ao original?

#### 5b. Verificação narrativa
- Abre com gancho (não definição)?
- Tem fio narrativo claro dentro do tópico?
- Avança a tese do livro?
- Pontes de entrada/saída funcionam?
- Conexões cruzadas fazem sentido?

#### 5c. Verificação de padrão
- 800-1.200 palavras?
- Segue style guide (voz, tom, vocabulário)?
- Segue sensibilidades editoriais?
- Sem anti-padrões?
- Boxes acrescentam (não repetem)?
- Glossário inline para termos novos?

#### 5d. Verificação de derivados
- Roteiro YouTube cobre o essencial do tópico?
- Reels funcionam isoladamente?
- Briefing visual é específico o suficiente para produzir?

**Veredito**:
- **Aprovado** → vai para o autor
- **Ajustes menores** → lista → volta para etapa 3 ou 4
- **Reescrever** → explica por quê → volta para etapa 2

**Saída**: `drafts/cap-XX-titulo/review.md`

---

### Etapa 6: Aprovação do autor

O autor lê o tópico revisado e decide:

| Veredito | Ação |
|----------|------|
| **Aprovado** | Move para `final/cap-XX-titulo/topico-X.Y.md` |
| **Com ajustes** | Lista o que mudar → volta para etapa 3 ou 4 |
| **Rejeitar** | Explica por quê → volta para etapa 1 ou 2 |

Após aprovação:
- Atualizar status do tópico em `coordination-v2.md`
- Registrar dados validados
- Registrar conexões cruzadas confirmadas

---

## 5. ORGANIZAÇÃO DE ARQUIVOS

### Estrutura de pastas

```
maranhao-book-plugin/
├── coordination-v2.md          # Memória do projeto
├── playbook.md                 # Este arquivo
├── style-guide-editorial.md    # Como escrever
├── guia-de-pesquisa.md         # Como pesquisar
├── proposta-editorial.md       # Visão geral do projeto
├── checklist-documentos.md     # Status dos documentos
│
├── references/
│   └── banco-de-fontes.yaml    # Banco centralizado de fontes
│
├── drafts/
│   └── cap-XX-titulo/
│       ├── research.md          # Pesquisa (todos os tópicos do cap)
│       ├── outline.md           # Outline (todos os tópicos do cap)
│       ├── draft-v1.md          # Texto (todos os tópicos do cap)
│       ├── youtube.md           # Roteiros YouTube
│       ├── reels.md             # Roteiros Reels
│       ├── visual.md            # Briefings visuais
│       └── review.md            # Revisão
│
├── final/
│   └── cap-XX-titulo/
│       └── topico-X.Y.md       # Tópico aprovado
│
└── rejected/
    └── [material descartado com justificativa]
```

### Convenções de nomeação

- Pastas de capítulo: `cap-XX-titulo-em-slug` (ex: `cap-04-o-ouro-branco`)
- Sempre 2 dígitos no número do capítulo (01, 02... 24)
- Slugs em minúscula, separados por hífen
- Sem acentos nos nomes de arquivo/pasta

---

## 6. PRODUÇÃO POR CAPÍTULO vs. POR TÓPICO

### Quando produzir o capítulo inteiro de uma vez

- Capítulos com poucos tópicos (3-5) e forte interdependência
- Quando o autor pede "faz o capítulo X inteiro"
- Quando há material existente em `drafts/` para adaptar

**Neste caso**: pesquisa de todos os tópicos → outline do capítulo → redação sequencial → derivados → revisão do conjunto.

### Quando produzir tópico a tópico

- Capítulos grandes (8+ tópicos)
- Quando o autor quer aprovar aos poucos
- Quando tópicos são muito independentes entre si

**Neste caso**: cada tópico passa pelo fluxo completo antes de iniciar o próximo.

### Regra geral

O autor decide. Se não disser, **produzir o capítulo inteiro** (pesquisa conjunta, outline conjunto, aprovação do outline, depois redação tópico a tópico).

---

## 7. ADAPTAÇÃO DE MATERIAL EXISTENTE

Há material em `drafts/` dos capítulos 1-6 que precisa ser **adaptado** ao novo formato.

### Processo de adaptação

1. **Ler** o material existente (research.md, draft)
2. **Avaliar**: o que é reaproveitável? O que precisa de nova pesquisa?
3. **Extrair**: dados, fontes, citações úteis → catalogar no banco de dados
4. **Reescrever** no novo formato:
   - Texto antigo era ensaio longo (8-12k palavras por capítulo)
   - Texto novo é modular (800-1.200 palavras por tópico, com pontes)
   - Tom e voz conforme `style-guide-editorial.md`
5. **Não copiar** — reescrever. O material antigo é base de pesquisa, não rascunho final

### Mapa de adaptação

| Material existente | Capítulo novo | Tópicos |
|-------------------|---------------|---------|
| `cap-01-a-encruzilhada/` | Cap 1 — A Terra | 1.1, 1.8 |
| `cap-02-natureza-viva/` | Cap 1 — A Terra | 1.2-1.7, 1.9-1.10 |
| `cap-03-os-primeiros/` | Cap 2 — Antes de Tudo | 2.1-2.3 |
| `cap-04-a-franca-a-holanda-e-portugal/` | Cap 3 — A Colônia | 3.1-3.3 |
| `cap-05-o-ouro-branco/` | Cap 3-4 | 3.4-3.6, 4.1-4.4 |
| `cap-06-a-ferida/` | Cap 5 — A Ferida | 5.1-5.5 |

---

## 8. COORDENAÇÃO E ATUALIZAÇÃO

### O coordination-v2.md

É a **fonte de verdade** do projeto. Contém:
- Estrutura completa (capítulos, tópicos, status)
- Dados validados
- Decisões consolidadas

### Quando atualizar

| Evento | Atualizar |
|--------|-----------|
| Tópico muda de estado (pesquisa → outline → draft → aprovado) | Status na tabela do capítulo |
| Novo dado validado | Tabela "Dados Validados" |
| Decisão editorial tomada | Lista "Decisões Consolidadas" |
| Conexão cruzada confirmada | (futuro: mapa de conexões) |
| Material existente adaptado | Status e campo "Material Existente" |

### Início de sessão

Toda sessão de trabalho começa com:

```
1. Ler coordination-v2.md (estado atual)
2. Ler playbook.md (processo)
3. Identificar próximo tópico a produzir
4. Verificar material existente em drafts/
5. Iniciar pelo passo 0 (Preparação)
```

---

## 9. PILOTO

### Tópico piloto: 1.1 — A Encruzilhada

O primeiro tópico produzido no novo formato será **1.1 — A Encruzilhada: três biomas, dois mundos, um estado**.

**Por quê**: abre o livro, tem material existente, testa todos os elementos do fluxo.

**Entregas do piloto**:
- [ ] Pesquisa atualizada (research.md)
- [ ] Fontes catalogadas no banco de dados (banco-de-fontes.yaml)
- [ ] Outline aprovado (outline.md)
- [ ] Texto do tópico (800-1.200 palavras, novo formato)
- [ ] Roteiro YouTube 8min (youtube.md)
- [ ] Roteiro(s) Reel/Short (reels.md)
- [ ] Briefing visual (visual.md)
- [ ] Revisão completa (review.md)
- [ ] Aprovação do autor

**O piloto serve como prova de conceito.** Após aprovado, o template está validado e a produção em escala começa.

---

## 10. REGRAS DE OURO

1. **Nada se escreve sem pesquisa.** Nada.
2. **Nada se redige sem outline aprovado.** O esqueleto evita retrabalho.
3. **Todo dado tem fonte.** Se não tem fonte, não entra no livro.
4. **Todo tópico avança a tese.** Se não avança, por que existe?
5. **Todo tópico se conecta.** Mínimo 2 conexões cruzadas.
6. **O autor tem veto absoluto.** Nenhum tópico é final sem aprovação humana.
7. **O coordination-v2.md é sempre atualizado.** É a única fonte de verdade.
8. **Pesquisa web ativa.** Claude busca fontes reais, não inventa.
9. **Modular com pontes.** Cada tópico funciona sozinho E no fluxo.
10. **Os derivados nascem do texto.** YouTube e Reels são adaptações do livro, não conteúdo separado.

---

## 11. ORDEM DE PRODUÇÃO

### Fase atual: Documentação

```
1. ✅ Proposta Editorial
2. ✅ Style Guide Textual
3. ✅ Guia de Pesquisa
4. ✅ Playbook de Produção (este documento)
5. ⬜ Style Guide Visual
6. ⬜ Estrutura Completa com subtópicos (emergem da pesquisa)
```

### Fase seguinte: Piloto

```
7. Tópico 1.1 — A Encruzilhada (fluxo completo)
   → Aprovação do autor
```

### Fase seguinte: Produção

```
8. Capítulo 1 completo (tópicos 1.1-1.10)
9. Capítulo por capítulo, na ordem natural (Cap 2, 3, 4...)
   → Ou na ordem que o autor preferir
```

**Princípio**: qualidade sobre velocidade. Sem prazo fixo. A produção avança conforme o autor aprova.
