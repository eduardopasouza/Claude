---
id: VIS-V91-A
verbete: V91
tipo: mapa
posicao: pagina-inteira
---

# Visual V91-A: O X logistico do Maranhao

## 1. Briefing para designer
**O que e**: Mapa do Brasil central e norte mostrando as duas ferrovias (EFC e FNS) convergindo para Itaqui, mais as rodovias principais. Formato de X com Itaqui no vertice.
**Dados**: EFC: Carajas(PA)→Sao Luis. FNS: Anapolis(GO)→Itaqui. BR-010 norte-sul. BR-135 Sao Luis-Balsas. Itaqui como ponto de convergencia.
**Paleta**: Vermelho para EFC, azul para FNS, cinza para rodovias, ocre para Itaqui.
**Tamanho**: Pagina inteira.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 600 700" xmlns="http://www.w3.org/2000/svg">
  <!-- Brasil simplificado -->
  <path d="M100,50 L500,50 L550,300 L500,600 L200,650 L50,400 Z" fill="#F0EBE0" stroke="#ccc"/>

  <!-- EFC (vermelho) -->
  <line x1="150" y1="250" x2="400" y2="150" stroke="#8B0000" stroke-width="4"/>
  <text x="180" y="230" fill="#8B0000" font-size="11">Carajas</text>
  <text x="350" y="140" fill="#8B0000" font-size="11">EFC</text>

  <!-- FNS (azul) -->
  <line x1="300" y1="500" x2="400" y2="150" stroke="#4A90D9" stroke-width="4"/>
  <text x="280" y="520" fill="#4A90D9" font-size="11">Anapolis</text>
  <text x="320" y="350" fill="#4A90D9" font-size="11">FNS</text>

  <!-- Itaqui (ponto de convergencia) -->
  <circle cx="400" cy="150" r="12" fill="#C8952E"/>
  <text x="415" y="145" fill="#C8952E" font-size="14" font-weight="bold">ITAQUI</text>

  <!-- Rodovias (cinza) -->
  <line x1="400" y1="150" x2="350" y2="450" stroke="#999" stroke-width="2" stroke-dasharray="5"/>
  <text x="340" y="440" fill="#999" font-size="10">BR-135</text>

  <!-- Seta para o mundo -->
  <line x1="412" y1="148" x2="500" y2="100" stroke="#C8952E" stroke-width="3" marker-end="url(#arrow)"/>
  <text x="490" y="90" fill="#C8952E" font-size="12">→ China, Europa</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Schematic map of Brazil showing two railway lines forming an X pattern converging on a single port point on the northeast coast. One line comes from the northwest (red, iron ore), another from the south (blue, soybeans). The convergence point is highlighted in ochre gold with an arrow pointing eastward across the Atlantic. Clean cartographic style, muted earth tones, editorial quality. --ar 3:4 --v 6"

**NAO incluir**: Rostos, textos embutidos, logos.
