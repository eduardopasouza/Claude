---
id: VIS-V18-A
verbete: V18
tipo: diagrama-aldeia
posicao: página-inteira
---

# Visual V18-A: A aldeia circular Timbira — planta baixa

## 1. Briefing para designer
**O que é**: Planta baixa esquemática de aldeia Timbira. Círculo de casas, pátio central, caminhos radiais. Divisão em metades (leste/oeste) com cores diferentes. Informações sobre cada espaço.
**Dados**:
- Círculo: ~15-25 casas dispostas em anel
- Pátio central (ã): espaço público, assembleia, ritual
- Caminhos radiais: do pátio a cada casa
- Metade leste: cor quente (associada ao sol, verão, seca)
- Metade oeste: cor fria (associada à lua, inverno, chuva)
- Eixo imaginário N-S dividindo as metades
- Casas uxorilocais (marido vai para casa da esposa)
- Cerrado ao redor da aldeia
**Referência de estilo**: Kurzgesagt meets antropologia visual
**Paleta**: Terracota #B5533E (metade leste), Verde-mata #2D6A4F (metade oeste), Ocre #C8952E (pátio/caminhos), Creme #FAF3E8 (fundo), Areia (cerrado ao redor)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="500" fill="#FAF3E8"/>
  <text x="250" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">A ALDEIA CIRCULAR TIMBIRA</text>
  <!-- Cerrado ao redor -->
  <circle cx="250" cy="260" r="220" fill="#D4C5A9" opacity="0.3"/>
  <!-- Círculo de casas -->
  <circle cx="250" cy="260" r="170" fill="none" stroke="#2B2B2B" stroke-width="1" stroke-dasharray="4,4"/>
  <!-- Metade leste (direita) -->
  <rect x="250" y="90" width="170" height="340" fill="#B5533E" opacity="0.08" rx="0"/>
  <text x="370" y="115" fill="#B5533E" font-size="9" font-weight="bold">METADE LESTE</text>
  <text x="370" y="128" fill="#B5533E" font-size="7">(sol, seca, calor)</text>
  <!-- Metade oeste (esquerda) -->
  <rect x="80" y="90" width="170" height="340" fill="#2D6A4F" opacity="0.08"/>
  <text x="120" y="115" fill="#2D6A4F" font-size="9" font-weight="bold">METADE OESTE</text>
  <text x="120" y="128" fill="#2D6A4F" font-size="7">(lua, chuva, frio)</text>
  <!-- Eixo divisório -->
  <line x1="250" y1="80" x2="250" y2="440" stroke="#2B2B2B" stroke-width="1" stroke-dasharray="6,3"/>
  <!-- Pátio central -->
  <circle cx="250" cy="260" r="40" fill="#C8952E" opacity="0.3"/>
  <text x="250" y="255" text-anchor="middle" fill="#5C4033" font-size="9" font-weight="bold">PÁTIO (ã)</text>
  <text x="250" y="268" text-anchor="middle" fill="#5C4033" font-size="7">assembleia • ritual</text>
  <!-- Casas (pontos ao redor do círculo) -->
  <circle cx="250" cy="90" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="330" cy="105" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="395" cy="160" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="415" cy="230" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="410" cy="300" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="375" cy="365" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="320" cy="410" r="8" fill="#B5533E" opacity="0.6"/>
  <circle cx="170" cy="105" r="8" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="105" cy="160" r="8" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="85" cy="230" r="8" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="90" cy="300" r="8" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="125" cy="365" r="8" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="180" cy="410" r="8" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="250" cy="430" r="8" fill="#2D6A4F" opacity="0.4"/>
  <!-- Caminhos radiais (alguns) -->
  <line x1="250" y1="220" x2="250" y2="98" stroke="#C8952E" stroke-width="0.8" opacity="0.5"/>
  <line x1="250" y1="300" x2="250" y2="422" stroke="#C8952E" stroke-width="0.8" opacity="0.5"/>
  <line x1="210" y1="260" x2="93" y2="230" stroke="#C8952E" stroke-width="0.8" opacity="0.5"/>
  <line x1="290" y1="260" x2="407" y2="230" stroke="#C8952E" stroke-width="0.8" opacity="0.5"/>
  <!-- Labels -->
  <text x="420" y="265" fill="#2B2B2B" font-size="7">← casa (uxorilocal)</text>
  <text x="250" y="475" text-anchor="middle" font-size="9" fill="#2B2B2B">O círculo reflete a cosmologia: duas metades complementares, pátio público no centro</text>
  <text x="490" y="495" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: Nimuendajú, 1946; Melatti, 1978</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Aerial view diagram of a Timbira circular village in the Brazilian cerrado. Perfect circle of houses around a central clearing (patio). Radial paths connecting center to each house like wheel spokes. Village divided into two halves by an imaginary line: east half in warm terracotta tones, west half in cool green tones. Cerrado savanna surrounding the village. Clean anthropological diagram style with warm palette. Labels for central patio, ceremonial halves, and houses. Warm cream background. Style: Kurzgesagt meets ethnographic illustration. Bird's-eye perspective. No photorealism."
**Estilo**: Diagrama antropológico editorial
**NÃO incluir**: fotografias aéreas reais, representações estereotipadas
