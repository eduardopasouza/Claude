---
id: VIS-V87-A
verbete: V87
tipo: infografico
posicao: meia-pagina
---

# Visual V87-A: Para onde vai a riqueza maranhense

## 1. Briefing para designer
**O que e**: Mapa-mundi com setas proporcionais saindo de Sao Luis para os principais destinos de exportacao. Grossura da seta proporcional ao valor.
**Dados**: China 55% (seta grossa), Japao 8%, Coreia 5%, Paises Baixos 4%, EUA 4%, outros 24%.
**Paleta**: Ocre #C8952E para setas, cinza para mapa-base.
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Mapa simplificado -->
  <circle cx="250" cy="250" r="8" fill="#C8952E"/>
  <text x="220" y="275" fill="#C8952E" font-size="10" font-weight="bold">Itaqui</text>

  <!-- Seta China (grossa) -->
  <line x1="260" y1="245" x2="650" y2="180" stroke="#C8952E" stroke-width="8" opacity="0.8"/>
  <text x="600" y="170" fill="#333" font-size="12">China 55%</text>

  <!-- Seta Japao -->
  <line x1="260" y1="240" x2="700" y2="150" stroke="#C8952E" stroke-width="3"/>
  <text x="660" y="140" fill="#333" font-size="10">Japao 8%</text>

  <!-- Seta Europa -->
  <line x1="255" y1="235" x2="450" y2="120" stroke="#C8952E" stroke-width="3"/>
  <text x="410" y="110" fill="#333" font-size="10">Europa 8%</text>

  <!-- Seta EUA -->
  <line x1="245" y1="240" x2="200" y2="150" stroke="#C8952E" stroke-width="2"/>
  <text x="150" y="140" fill="#333" font-size="10">EUA 4%</text>

  <!-- Total -->
  <text x="250" y="330" fill="#333" font-size="14" font-weight="bold">US$9,5 bilhoes (2023)</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "World map with proportional flow arrows emanating from a single point on the northeast coast of Brazil (Sao Luis), showing trade flows. Largest arrow to China (east Asia), medium arrows to Japan and Europe, thin arrows to USA. Ochre gold arrows on muted grey world map. Clean data visualization style, editorial quality. --ar 16:9 --v 6"

**NAO incluir**: Rostos, textos embutidos, bandeiras.
