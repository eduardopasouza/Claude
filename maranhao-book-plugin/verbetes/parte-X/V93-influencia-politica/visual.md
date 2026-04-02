---
id: VIS-V93-A
verbete: V93
tipo: infografico
posicao: meia-pagina
---

# Visual V93-A: Timeline da influencia maranhense em Brasilia

## 1. Briefing para designer
**O que e**: Timeline vertical (1945-2025) mostrando cargos nacionais ocupados por maranhenses: governadores, senadores, presidente, ministros, STF.
**Dados**: Vitorino Freire (1945-65), Sarney governador (1966), Sarney presidente (1985-90), Sarney presidente do Senado (3x), Lobao ministro, Dino governador (2015), Dino STF (2023).
**Paleta**: Carvao #2B2B2B com destaques em vermelho-bumba.
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 400 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Eixo vertical -->
  <line x1="100" y1="30" x2="100" y2="570" stroke="#2B2B2B" stroke-width="2"/>

  <!-- Marcos -->
  <circle cx="100" cy="80" r="6" fill="#8B0000"/>
  <text x="120" y="75" fill="#333" font-size="11">1945 — Vitorino Freire domina o MA</text>

  <circle cx="100" cy="150" r="6" fill="#8B0000"/>
  <text x="120" y="145" fill="#333" font-size="11">1966 — Sarney governador</text>

  <circle cx="100" cy="250" r="10" fill="#8B0000"/>
  <text x="120" y="245" fill="#333" font-size="12" font-weight="bold">1985 — Sarney presidente</text>

  <circle cx="100" cy="330" r="6" fill="#8B0000"/>
  <text x="120" y="325" fill="#333" font-size="11">1995 — Sarney preside o Senado (1a vez)</text>

  <circle cx="100" cy="410" r="6" fill="#8B0000"/>
  <text x="120" y="405" fill="#333" font-size="11">2008 — Lobao ministro MEM</text>

  <circle cx="100" cy="480" r="6" fill="#8B0000"/>
  <text x="120" y="475" fill="#333" font-size="11">2015 — Dino governador (quebra Sarney)</text>

  <circle cx="100" cy="540" r="10" fill="#8B0000"/>
  <text x="120" y="535" fill="#333" font-size="12" font-weight="bold">2023 — Dino no STF</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Vertical timeline infographic showing political milestones of Maranhao state in Brazilian national politics from 1945 to 2025. Dark charcoal background with red accent markers at key moments. Clean editorial design, serif typography, magazine style. --ar 2:3 --v 6"

**NAO incluir**: Rostos, fotos, caricaturas.
