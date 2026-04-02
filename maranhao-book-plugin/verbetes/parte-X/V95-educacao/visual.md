---
id: VIS-V95-A
verbete: V95
tipo: infografico
posicao: meia-pagina
---

# Visual V95-A: IDEB comparativo MA vs. Brasil vs. CE

## 1. Briefing para designer
**O que e**: Grafico de barras triplas (MA, Brasil, CE) para tres niveis educacionais. Mostra a defasagem do MA.
**Dados**: Anos iniciais: MA 5,1 / BR 5,8 / CE 6,3. Anos finais: MA 4,2 / BR 5,1 / CE 5,4. EM: MA 3,6 / BR 4,2 / CE 4,4.
**Paleta**: Carvao #2B2B2B para MA, cinza medio para Brasil, vermelho-bumba para Ceara (referencia).
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Grupo Anos Iniciais -->
  <rect x="50" y="120" width="40" height="102" fill="#2B2B2B"/>
  <rect x="95" y="84" width="40" height="138" fill="#999"/>
  <rect x="140" y="54" width="40" height="168" fill="#8B0000"/>
  <text x="70" y="260" fill="#333" font-size="10">Anos iniciais</text>

  <!-- Grupo Anos Finais -->
  <rect x="230" y="156" width="40" height="66" fill="#2B2B2B"/>
  <rect x="275" y="108" width="40" height="114" fill="#999"/>
  <rect x="320" y="96" width="40" height="126" fill="#8B0000"/>
  <text x="260" y="260" fill="#333" font-size="10">Anos finais</text>

  <!-- Grupo EM -->
  <rect x="410" y="180" width="40" height="42" fill="#2B2B2B"/>
  <rect x="455" y="156" width="40" height="66" fill="#999"/>
  <rect x="500" y="144" width="40" height="78" fill="#8B0000"/>
  <text x="440" y="260" fill="#333" font-size="10">Ensino medio</text>

  <!-- Legenda -->
  <rect x="50" y="280" width="12" height="12" fill="#2B2B2B"/>
  <text x="67" y="291" fill="#333" font-size="10">MA</text>
  <rect x="120" y="280" width="12" height="12" fill="#999"/>
  <text x="137" y="291" fill="#333" font-size="10">Brasil</text>
  <rect x="190" y="280" width="12" height="12" fill="#8B0000"/>
  <text x="207" y="291" fill="#333" font-size="10">Ceara</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Bar chart comparing education indicators (IDEB scores) across three categories for three regions. Dark charcoal bars (lowest), grey bars (middle), dark red bars (highest). Clean editorial infographic, white background, minimal design. --ar 16:9 --v 6"

**NAO incluir**: Rostos, textos embutidos.
