# CLAUDE.md — Quem é o Maranhão?

## O que é este projeto

Almanaque visual do Maranhão — livro de 106 verbetes (entradas independentes) em 11 Partes, formato coffee table book (23x28cm). Diretriz-mestra: **DADOS + ALMA** — rigor de dados com alma literária.

Tudo está dentro de `maranhao-book-plugin/`.

## Estado atual

- **Fase**: 3 (Fases 1 e 2 concluídas a 100%)
- **Verbetes produzidos**: 15 de 106 (14%)
- **Palavras escritas**: ~59.600
- **Próximo verbete**: V01 — Coordenadas: onde fica o Maranhão
- **Branch**: `claude/maranhao-book-plugin-Gzrj9`

## Rotina de início de sessão

1. Ler `maranhao-book-plugin/protocolo-producao.md` — pipeline, fila de produção, checklist
2. Ler `maranhao-book-plugin/registro-producao.md` — dashboard (onde parou, totais)
3. Identificar próximo verbete na fila e confirmar com o autor
4. Seguir pipeline completo

## Pipeline por verbete

```
PESQUISA (research.md) → OUTLINE (outline.md) → ⏸️ APROVAÇÃO → TEXTO (texto.md) → REELS (reel-N.md) → VISUAL (visual.md) → [YOUTUBE] → ATUALIZAR REGISTROS
```

### Regras críticas

- **Web search obrigatório** para toda pesquisa
- **Mín. 3 fontes** por afirmação factual
- **Verificação cruzada**: todo dado confrontado com ≥1 fonte adicional antes de usar
- **Banco YAML alimentado na pesquisa**: todo dado verificado vai para `banco-dados/dados-centrais.yaml` DURANTE a pesquisa (não depois). Confrontar com dados existentes para evitar duplicatas e contradições
- **3 matrizes iguais**: indígena = africana = europeia em profundidade
- **Nunca abrir verbete com definição** — sempre gancho (pergunta, cena, dado surpresa)
- **Dado nunca solto** — sempre contextualizado (comparação, proporção, analogia)
- **Outline precisa de aprovação** do autor antes de redigir
- **Após cada verbete concluído**: atualizar registro-producao.md, changelog.md, e banco YAML

### Tom

Literário (crônica/ensaio). Narrador maranhense implícito ("nossa terra"). Inspiração: Eduardo Bueno (ironia), Eliane Brum (profundidade). Ironia com história, neutralidade com o presente. O epílogo-bússola (`epilogo-bussola.md`) é o calibrador de tom — ler se tiver dúvida.

## Fila da Fase 3 (24 verbetes)

```
Parte I:   V01 → V02 → V06 → V13
Parte II:  V16 → V17 → V21
Parte III: V25 → V24
Parte IV:  V33 → V35 → V37 → V36 → V39 → V38
Partes V/VII/X/XI: V40 → V46 → V61 → V62 → V63 → V94 → V92 → V100 → V103
```

## Estrutura de cada verbete

Cada verbete vive em `maranhao-book-plugin/verbetes/parte-XX/VXX-titulo/` com estes arquivos:

| Arquivo | Obrigatório | Conteúdo |
|---------|-------------|----------|
| research.md | Sim | Dossier de pesquisa com fontes |
| outline.md | Sim | Esqueleto aprovado pelo autor |
| texto.md | Sim | Texto final em Markdown + YAML frontmatter |
| reel-1.md, reel-2.md, reel-3.md | Mín. 2 | Roteiros de reels (30-90s) |
| visual.md | Sim | Briefing triplo (designer + SVG + prompt IA) |
| youtube.md | Só quando indicado | Roteiro 8min (verbetes fortes) |

## Arquivos de referência (ordem de importância)

| # | Arquivo | Função |
|---|---------|--------|
| 1 | `protocolo-producao.md` | Regras de produção, pipeline, fila, checklist |
| 2 | `registro-producao.md` | Dashboard — totais, fases, log |
| 3 | `coordination-v3.md` | Índice completo dos 106 verbetes |
| 4 | `playbook-v2.md` | Templates das 10 skills com checklists |
| 5 | `style-guide-editorial.md` | Tom, voz, vocabulário, sensibilidades, anti-patterns |
| 6 | `style-guide-visual.md` | Paleta, tipografia, grid, boxes visuais |
| 7 | `foundation.md` | Fundamentação teórica (referencial, premissas, teses por Parte) |
| 8 | `vision.md` | Premissas editoriais e expectativas quantitativas |
| 9 | `changelog.md` | Registro cronológico de toda produção |
| 10 | `epilogo-bussola.md` | Calibrador de tom (ensaio-epílogo rascunho) |
| 11 | `banco-dados/dados-centrais.yaml` | 160+ entradas factuais verificadas |
| 12 | `references/bibliography-core.md` | 43 obras nucleares por categoria |

## Fluxo de dados no banco YAML

```
Dado encontrado na web
  → Buscar ≥1 fonte adicional
  → Verificar se já existe no banco (evitar duplicata)
  → Se novo: adicionar com id, categoria, descricao, valor, fonte, ano_base, verbetes
  → Se existente com valor diferente: investigar, atualizar se fonte melhor, registrar nota
  → Referenciar no texto via dados_yaml: [GEO-001, DEM-003]
```

Prefixos: `GEO`, `DEM`, `IND`, `QUI`, `ECO`, `CUL`, `HIS`, `SOC`, `AMB`, `TUR`

## Não fazer

- Não abrir verbete com definição de dicionário
- Não usar dado sem fonte e sem contextualização
- Não avançar para próximo verbete sem completar pipeline do atual
- Não escrever sem pesquisa web prévia
- Não inventar dados — se não encontrou fonte, marcar como lacuna
- Não forçar humor em temas de sofrimento (escravidão, pobreza)
- Não acusar nomes, empresas ou setores diretamente (dados falam por si)
- Não esquecer de atualizar registro-producao.md e changelog.md após cada verbete
