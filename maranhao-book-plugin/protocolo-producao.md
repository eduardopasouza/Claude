# Protocolo de Produção — Quem é o Maranhão?

> Regras de comportamento para produção sequencial de verbetes. Claude deve ler este arquivo no início de cada sessão de produção.

---

## Rotina de início de sessão

```
1. Ler protocolo-producao.md (este arquivo)
2. Ler roadmap.md (estado do projeto, fila ativa, alertas)
3. Identificar próximo verbete na fila de produção
4. Confirmar com o autor: "Próximo: V[XX] — [Título]. Início a pesquisa?"
5. Seguir pipeline completo abaixo
```

---

## Pipeline por verbete (obrigatório, nesta ordem)

### Etapa 1 — PESQUISA (research.md)

```
Ações obrigatórias:
├── Busca web (mín. 5 buscas diferentes, variando termos)
├── Mín. 3 fontes por afirmação factual
├── Verificação cruzada: todo dado confrontado com ≥1 fonte adicional
├── Registrar TODOS os dados verificados no banco YAML
│   ├── Confrontar com dados já existentes no banco
│   ├── Se dado já existe → verificar se fontes convergem
│   ├── Se dado é novo → adicionar com categoria, fonte, ano_base
│   └── Se há divergência → registrar nota com ambas as fontes
├── Hierarquia de fontes: primária > acadêmica > oficial > jornalística
└── Dossier completo com lacunas identificadas
```

**Output**: `verbetes/parte-XX/VXX-titulo/research.md`

### Etapa 2 — OUTLINE (outline.md)

```
Conteúdo obrigatório:
├── Tese do verbete (1 frase)
├── Estrutura (Abertura → Blocos nomeados → Fechamento)
├── Boxes planejados (tipo + título + justificativa)
├── Visuais planejados (tipo + dados + posição)
├── Cross-references mapeados (V[XX]: razão da conexão)
├── YouTube avaliado (sim/não + ângulo se sim)
└── Palavras estimadas
```

**Output**: `verbetes/parte-XX/VXX-titulo/outline.md`

### ⏸️ PAUSA — Aguardar aprovação do autor

> Apresentar outline completo ao autor. Só avançar após aprovação explícita.

### Etapa 3 — TEXTO (texto.md)

```
Regras de escrita:
├── YAML frontmatter completo (id, titulo, parte, tipo, palavras, boxes, cross_references, dados_yaml, status)
├── Abertura com gancho (NUNCA definição)
├── Dados sempre contextualizados (comparação, proporção, analogia)
├── Fio da água (se aplicável — orgânico, nunca forçado)
├── Boxes embutidos com marcação correta (<!-- BOX: [série] — [título] -->)
├── Cross-references marcados no texto e na margem
├── Marcadores de layout para designer (<!-- INFOGRÁFICO: ... -->)
├── Notas de rodapé com fonte para toda afirmação factual
└── Tom: literário, narrador maranhense implícito (ver style-guide-editorial.md)
```

**Output**: `verbetes/parte-XX/VXX-titulo/texto.md`

### Etapa 4 — REELS (reel-1.md, reel-2.md, reel-3.md)

```
Padrão:
├── Mín. 2 reels por verbete, máx. 4
├── Formato base: Pergunta + Resposta + Surpresa
├── Durações: 30s (curiosidade), 60s (história), 90s (complexo)
├── YAML frontmatter com id, verbete, duração, formato, hashtags
├── Hook nos primeiros 3 segundos
├── Texto de tela definido
├── Narração completa escrita
└── Surpresa/CTA no final
```

**Output**: `verbetes/parte-XX/VXX-titulo/reel-N.md`

### Etapa 5 — VISUAL (visual.md)

```
Briefing triplo obrigatório:
├── Layer 1 — Briefing textual para designer humano
│   ├── O que é, dados, referência de estilo, paleta, tamanho
├── Layer 2 — SVG esquemático
│   ├── Elementos, layout, cores (hex), texto
└── Layer 3 — Prompt de IA generativa
    ├── Prompt detalhado em inglês (Midjourney/DALL-E)
    ├── Estilo, referência, NÃO incluir
```

**Output**: `verbetes/parte-XX/VXX-titulo/visual.md`

### Etapa 6 — YOUTUBE (youtube.md) — quando aplicável

**Critério**: YouTube obrigatório se (a) verbete-âncora OU (b) texto > 4.000 palavras. Nos demais, Claude sugere no outline e o autor decide.

```
Roteiro completo de 8min:
├── HOOK (0:00-0:30): narração + visual
├── ATO 1-3: narração + B-roll + infográficos + transições
├── FECHAMENTO: reflexão + CTA
└── NOTAS: trilha, animações, infográficos, refs, timestamps, tags SEO, fontes
```

**Output**: `verbetes/parte-XX/VXX-titulo/youtube.md`

### Etapa 7 — ATUALIZAÇÕES (obrigatórias após cada verbete)

```
Atualizar TODOS estes registros:
├── registro-producao.md
│   ├── Adicionar verbete à tabela da fase correspondente
│   ├── Atualizar totais (palavras, reels, visuais)
│   └── Atualizar log de produção (data + verbete + status)
├── roadmap.md
│   ├── Dashboard (totais)
│   ├── Progresso por Parte (contagem + barra)
│   ├── Fila ativa (marcar concluído, avançar seta)
│   └── Métricas evolutivas (nova linha)
├── banco-dados/dados-centrais.yaml
│   └── Confirmar que todos os dados novos foram registrados na Etapa 1
├── changelog.md
│   └── Nova entrada: data + verbete + resumo do que foi produzido
├── bibliography-core.md (se novas fontes relevantes apareceram)
└── GIT: commit + push (OBRIGATÓRIO)
    ├── git add -A
    ├── git commit -m "feat(VXX): [título] — pipeline completo"
    └── git push origin claude/maranhao-book-plugin-Gzrj9
```

**Regra de Git**: Todo verbete concluído DEVE ser commitado e pushado no repositório antes de iniciar o próximo. O commit message segue o padrão: `feat(VXX): [título resumido] — pipeline completo`. Correções e reorganizações usam `fix:` ou `chore:`.

---

## Fluxo de verificação cruzada de dados

```
DADO ENCONTRADO NA WEB
  │
  ├── Buscar ≥1 fonte adicional para confirmar
  │     ├── Confirmado por ≥2 fontes → DADO VERIFICADO
  │     └── Divergência entre fontes → Registrar ambas + nota
  │
  ├── Verificar se já existe no banco YAML
  │     ├── SIM, mesmo valor → Referenciar ID existente
  │     ├── SIM, valor diferente → Investigar, atualizar se fonte melhor
  │     └── NÃO → Adicionar novo registro
  │
  └── Registrar no banco com campos completos:
        id: [CAT]-[NNN]
        categoria: [tipo]
        descricao: "..."
        valor: "..."
        fonte: "..."
        ano_base: YYYY
        verbetes: [VXX, VYY]
```

---

## Fila de produção

### Fase 3 — Completar Partes zeradas + avançar cronológicas (24 verbetes)

```
Bloco 3A — Parte I (O Chão)
V01 → V02 → V06 → V13

Bloco 3B — Parte II (Os Primeiros)
V16 → V17 → V21

Bloco 3C — Parte III (A Conquista)
V25 → V24

Bloco 3D — Parte IV (O Povo Negro)
V33 → V35 → V37 → V36 → V39 → V38

Bloco 3E — Partes zeradas (V, VII, X, XI)
V40 → V46 → V61 → V62 → V63 → V94 → V92 → V100 → V103
```

### Fase 4 — Partes temáticas VI-IX (28 verbetes)
*(Definir ordem detalhada ao iniciar Fase 4)*

### Fase 5 — Verbetes restantes (~26 verbetes)
*(Definir ordem detalhada ao iniciar Fase 5)*

### Fase 6 — Fechamento
*(Epílogo final, apêndices, revisão cruzada, sumário)*

---

## Checklist pós-verbete (antes de avançar para o próximo)

```
☐ research.md completo com fontes verificadas
☐ outline.md aprovado pelo autor
☐ texto.md com YAML frontmatter completo
☐ Mín. 2 cross-references no texto
☐ Boxes embutidos (se aplicáveis)
☐ Mín. 2 reels produzidos
☐ visual.md com briefing triplo
☐ Dados novos registrados no banco YAML
☐ registro-producao.md atualizado
☐ changelog.md atualizado
☐ Nenhum dado sem fonte no texto
☐ Tom consistente com epílogo-bússola
```

---

## Documentos de referência (ordem de leitura)

| Prioridade | Documento | Função |
|------------|-----------|--------|
| 1 | `protocolo-producao.md` | Este arquivo. Regras de comportamento |
| 2 | `roadmap.md` | Estado do projeto, fila, métricas, alertas |
| 3 | `registro-producao.md` | Log histórico bruto de produção |
| 4 | `coordination-v3.md` | Índice completo dos 106 verbetes |
| 5 | `playbook-v2.md` | Templates e checklists das 10 skills |
| 6 | `style-guide-editorial.md` | Tom, voz, vocabulário, sensibilidades |
| 7 | `style-guide-visual.md` | Paleta, tipografia, grid, boxes visuais |
| 8 | `foundation.md` | Fundamentação teórica |
| 9 | `vision.md` | Premissas editoriais e expectativas |
| 10 | `banco-dados/dados-centrais.yaml` | Banco central de dados factuais |

---

*Protocolo de Produção v1 — 2026-04-01*
