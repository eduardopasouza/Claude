---
id: VIS-V86-A
verbete: V86
tipo: mapa
posicao: pagina-inteira
---

# Visual V86-A: Mapa do avanco da soja no cerrado maranhense

## 1. Briefing para designer
**O que e**: Mapa do Maranhao mostrando o avanco da area plantada de soja no cerrado sul-maranhense em tres momentos: 2000, 2010, 2023. Tres camadas de cor sobre o mapa, como uma mancha que cresce.
**Dados**: 2000: ~300 mil ha (concentrados em Balsas). 2010: ~700 mil ha (expansao para Tasso Fragoso, Alto Parnaiba). 2023: ~1,2 milhao ha (cobrindo toda a mesorregiao sul).
**Paleta**: Cerrado original em verde-oliva, soja em amarelo-ouro, areas de conflito em vermelho.
**Tamanho**: Pagina inteira.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 600 700" xmlns="http://www.w3.org/2000/svg">
  <!-- Contorno MA simplificado -->
  <path d="M100,100 L400,80 L500,200 L480,500 L300,650 L150,500 L100,300 Z" fill="#E8E0D0" stroke="#333" stroke-width="2"/>

  <!-- Cerrado original (sul) -->
  <ellipse cx="350" cy="500" rx="150" ry="120" fill="#6B7F3B" opacity="0.3"/>
  <text x="280" y="510" fill="#4A5A2A" font-size="12">Cerrado original</text>

  <!-- Soja 2000 -->
  <circle cx="350" cy="520" r="30" fill="#D4A843" opacity="0.7"/>
  <text x="390" y="525" fill="#C8952E" font-size="10">2000</text>

  <!-- Soja 2010 -->
  <circle cx="350" cy="510" r="60" fill="#D4A843" opacity="0.5"/>
  <text x="420" y="490" fill="#C8952E" font-size="10">2010</text>

  <!-- Soja 2023 -->
  <ellipse cx="350" cy="500" rx="120" ry="90" fill="#D4A843" opacity="0.3"/>
  <text x="420" y="430" fill="#C8952E" font-size="10">2023</text>

  <!-- Balsas -->
  <circle cx="350" cy="530" r="5" fill="#333"/>
  <text x="360" y="545" fill="#333" font-size="11">Balsas</text>

  <!-- Legenda -->
  <rect x="50" y="620" width="15" height="15" fill="#6B7F3B"/>
  <text x="70" y="633" fill="#333" font-size="11">Cerrado</text>
  <rect x="170" y="620" width="15" height="15" fill="#D4A843"/>
  <text x="190" y="633" fill="#333" font-size="11">Soja</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Satellite-style map of southern Maranhao Brazil showing agricultural expansion over cerrado biome, three time periods overlaid. Natural cerrado in olive green giving way to uniform yellow-gold soybean fields expanding from a central point outward. Clean cartographic style, topographic feel, ochre and green palette. --ar 3:4 --v 6"

**NAO incluir**: Rostos, textos embutidos, bandeiras.
