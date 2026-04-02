---
id: VIS-V83-A
verbete: V83
tipo: infografico
posicao: meia-pagina
---

# Visual V83-A: Comparativo de calado — portos brasileiros

## 1. Briefing para designer
**O que e**: Infografico vertical mostrando o perfil de profundidade (calado) dos principais portos brasileiros, como se fossem cortes transversais do mar. Itaqui destacado com seus 23m.
**Dados**: Santos 15m, Paranagua 12-14m, Rio Grande 14m, Tubarao 21m, Itaqui 23m. Linha de agua na superficie, perfil do fundo.
**Paleta**: Azul-marinho para agua, ocre #C8952E para destaque de Itaqui, cinza para demais.
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Linha d'agua -->
  <line x1="50" y1="100" x2="750" y2="100" stroke="#4A90D9" stroke-width="3"/>
  <text x="10" y="105" fill="#4A90D9" font-size="12">Nivel do mar</text>

  <!-- Santos -->
  <rect x="100" y="100" width="80" height="150" fill="#4A90D9" opacity="0.3"/>
  <text x="110" y="270" fill="#333" font-size="12">Santos</text>
  <text x="115" y="290" fill="#666" font-size="11">15m</text>

  <!-- Paranagua -->
  <rect x="220" y="100" width="80" height="130" fill="#4A90D9" opacity="0.3"/>
  <text x="222" y="250" fill="#333" font-size="12">Paranagua</text>
  <text x="240" y="270" fill="#666" font-size="11">13m</text>

  <!-- Rio Grande -->
  <rect x="340" y="100" width="80" height="140" fill="#4A90D9" opacity="0.3"/>
  <text x="342" y="260" fill="#333" font-size="12">R. Grande</text>
  <text x="360" y="280" fill="#666" font-size="11">14m</text>

  <!-- Tubarao -->
  <rect x="460" y="100" width="80" height="210" fill="#4A90D9" opacity="0.4"/>
  <text x="465" y="330" fill="#333" font-size="12">Tubarao</text>
  <text x="480" y="350" fill="#666" font-size="11">21m</text>

  <!-- Itaqui - destaque -->
  <rect x="580" y="100" width="100" height="230" fill="#C8952E" opacity="0.8"/>
  <text x="595" y="355" fill="white" font-size="14" font-weight="bold">ITAQUI</text>
  <text x="610" y="375" fill="white" font-size="13" font-weight="bold">23m</text>

  <!-- Navio Valemax silhueta -->
  <text x="580" y="85" fill="#C8952E" font-size="11">Valemax: calado 23m</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Cross-section comparison of Brazilian port depths, showing water profiles side by side. Five ports with decreasing depth left to right, the rightmost (Itaqui, 23 meters) dramatically deeper, highlighted in ochre gold. A massive cargo ship silhouette at the deepest port. Clean technical illustration style, blueprint aesthetic, navy blue water, ochre highlight. --ar 4:3 --v 6"

**NAO incluir**: Rostos, textos embutidos, bandeiras.
