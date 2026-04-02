---
id: VIS-V89-A
verbete: V89
tipo: infografico
posicao: meia-pagina
---

# Visual V89-A: Matriz energetica do Maranhao

## 1. Briefing para designer
**O que e**: Grafico de pizza ou waffle chart mostrando a matriz energetica do MA por fonte, com destaque para eolica (55%).
**Dados**: Eolica 55%, Hidro 18%, Termo 15%, Solar 6%, Biomassa 4%, Outras 2%.
**Paleta**: Tons de ocre e azul-esverdeado para energia limpa, cinza para termoeletrica.
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="200" cy="200" r="150" fill="none" stroke="#ddd" stroke-width="30"/>
  <!-- Eolica 55% = ~198 graus -->
  <circle cx="200" cy="200" r="150" fill="none" stroke="#C8952E" stroke-width="30"
    stroke-dasharray="198 565" stroke-dashoffset="0" transform="rotate(-90 200 200)"/>
  <text x="280" y="100" fill="#C8952E" font-size="14" font-weight="bold">Eolica 55%</text>
  <!-- Hidro 18% -->
  <circle cx="200" cy="200" r="150" fill="none" stroke="#4A90D9" stroke-width="30"
    stroke-dasharray="65 565" stroke-dashoffset="-198" transform="rotate(-90 200 200)"/>
  <text x="300" y="250" fill="#4A90D9" font-size="12">Hidro 18%</text>
  <!-- Termo 15% -->
  <circle cx="200" cy="200" r="150" fill="none" stroke="#999" stroke-width="30"
    stroke-dasharray="54 565" stroke-dashoffset="-263" transform="rotate(-90 200 200)"/>
  <text x="100" y="330" fill="#999" font-size="12">Termo 15%</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Clean donut chart infographic showing energy matrix of Maranhao Brazil. Dominant wind power slice (55%) in ochre gold, hydroelectric (18%) in blue, thermal (15%) in grey, solar (6%) in yellow, biomass (4%) in green. Small wind turbine icon in center. Editorial data visualization style, white background. --ar 1:1 --v 6"

**NAO incluir**: Rostos, textos embutidos.
