# Quem é o Maranhão?

Almanaque visual do Maranhão — 100+ verbetes com dados e alma.

## Arquivos principais

| Arquivo | Função |
|---------|--------|
| `coordination-v3.md` | **Ler sempre ao iniciar.** Visão, índice completo, regras, pipeline. |
| `playbook-v2.md` | Manual de produção: 10 skills com templates, exemplos e checklists. |
| `proposta-editorial-v2.md` | Proposta editorial formal. |
| `style-guide-editorial.md` | Guia de estilo editorial: voz, tom, vocabulário, regras. |
| `style-guide-visual.md` | Identidade visual: paleta, tipografia, grid, boxes, vídeo. |
| `registro-producao.md` | Dashboard de produção: verbetes concluídos, reels, visuais. |
| `epilogo-bussola.md` | Ensaio-epílogo (escrito primeiro como calibrador de tom). |
| `registro-decisoes-73-rodadas.md` | Histórico de 296 decisões em 74 rodadas. |
| `banco-dados/dados-centrais.yaml` | Banco central de dados factuais. |

## Estrutura

```
maranhao-book-plugin/
├── coordination-v3.md
├── playbook-v2.md
├── proposta-editorial-v2.md
├── style-guide-editorial.md
├── style-guide-visual.md
├── registro-producao.md
├── epilogo-bussola.md
├── registro-decisoes-73-rodadas.md
├── banco-dados/
│   └── dados-centrais.yaml
├── verbetes/
│   └── parte-XX/VXX-titulo/
│       ├── research.md, outline.md, texto.md
│       ├── reel.md, visual.md, youtube.md
├── templates/
├── references/
└── legacy/                 # Versão anterior (referência)
```

## Como usar

**Iniciar sessão**: Ler `coordination-v3.md`

**Produzir verbete**: Seguir pipeline em `playbook-v2.md`
```
Pesquisa → Outline → [Aprovação] → Texto → Reel → Visual → [Review]
```

**Consultar decisões**: `registro-decisoes-73-rodadas.md`

**Verificar dados**: `banco-dados/dados-centrais.yaml`

## Diretriz-mestra

**DADOS + ALMA** — rigor de dados com alma literária. Cada número conta uma história humana.
