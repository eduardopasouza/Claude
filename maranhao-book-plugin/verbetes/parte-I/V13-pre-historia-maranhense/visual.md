---
id: VIS-V13-A
verbete: V13
tipo: mapa
posicao: página-inteira
---

# Visual V13-A: Mapa dos sítios arqueológicos do Maranhão

## 1. Briefing para designer
**O que é**: Mapa do estado do Maranhão mostrando a distribuição dos três grandes tipos de sítios arqueológicos pré-coloniais — sambaquis no litoral, sítios rupestres no sul e estearias na Baixada Maranhense.
**Dados**:
- 300+ sítios catalogados no CNSA/IPHAN
- Sambaquis: concentrados na Ilha de São Luís e litoral ocidental. Marcador: ícone de concha
- Arte rupestre: concentrados na Chapada das Mesas (Carolina, Estreito, Riachão). Marcador: ícone de mão/pintura
- Estearias: rios Pindaré e Maracu, Baixada Maranhense. Marcador: ícone de palafita
- Destaque especial: Sítio Chácara Rosane (São Luís) — marcador maior, com legenda
- Referência: rios principais (Pindaré, Mearim, Tocantins, Parnaíba) em azul
- Biomas simplificados como fundo: Amazônia (verde escuro, oeste), Cerrado (ocre, sul), litoral (azul claro)
**Referência de estilo**: Kurzgesagt — mapa temático limpo, fundo creme, elementos flat
**Paleta**: Verde-mata #2D6A4F (acento principal, Parte I), Azul-mar #1B4965 (rios/litoral), Ocre #C8952E (cerrado), Terracota #B5533E (marcadores rupestres), Creme #FAF3E8 (fundo)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado
**Elementos**:
- Contorno do estado do Maranhão
- Divisão de biomas em 3 zonas (Amazônia, Cerrado, litoral) com preenchimento sutil
- Rios principais como linhas azuis
- 3 clusters de ícones: conchas (litoral NW), mãos pintadas (sul), palafitas (centro-norte)
- Legenda com os 3 tipos e cores
- Pin especial no Sítio Chácara Rosane com callout
**Layout**: Mapa centralizado, legenda no canto inferior esquerdo, callout do Chácara Rosane no canto superior direito
**Cores**: Verde-mata para moldura e título; Azul-mar para rios; Terracota para rupestres; Ocre para sambaquis; Verde escuro para estearias

```svg
<!-- SVG esquemático — placeholder para designer -->
<svg viewBox="0 0 800 900" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="800" height="900" fill="#FAF3E8"/>
  <!-- Título -->
  <text x="400" y="40" text-anchor="middle" font-size="20" fill="#2D6A4F" font-weight="bold">Sítios Arqueológicos do Maranhão</text>
  <!-- Contorno MA (simplificado) -->
  <path d="M200,150 L600,150 L650,300 L600,500 L550,700 L300,750 L150,500 L180,300 Z" fill="#FAF3E8" stroke="#2B2B2B" stroke-width="2"/>
  <!-- Zona Amazônia -->
  <path d="M200,150 L350,150 L300,500 L150,500 L180,300 Z" fill="#2D6A4F" opacity="0.15"/>
  <!-- Zona Cerrado -->
  <path d="M300,500 L550,700 L300,750 Z" fill="#C8952E" opacity="0.15"/>
  <!-- Zona Litoral -->
  <path d="M350,150 L600,150 L650,300 L600,350 L400,200 Z" fill="#1B4965" opacity="0.1"/>
  <!-- Sambaquis (litoral) -->
  <circle cx="480" cy="200" r="8" fill="#C8952E"/>
  <circle cx="500" cy="220" r="8" fill="#C8952E"/>
  <circle cx="460" cy="210" r="8" fill="#C8952E"/>
  <!-- Chácara Rosane (destaque) -->
  <circle cx="490" cy="195" r="14" fill="#C8952E" stroke="#B5533E" stroke-width="3"/>
  <text x="510" y="190" font-size="10" fill="#2B2B2B">Chácara Rosane</text>
  <!-- Rupestres (sul) -->
  <circle cx="420" cy="620" r="8" fill="#B5533E"/>
  <circle cx="440" cy="640" r="8" fill="#B5533E"/>
  <circle cx="400" cy="650" r="8" fill="#B5533E"/>
  <!-- Estearias (centro) -->
  <circle cx="320" cy="380" r="8" fill="#2D6A4F"/>
  <circle cx="340" cy="400" r="8" fill="#2D6A4F"/>
  <!-- Rios -->
  <path d="M250,350 L350,400 L400,500" fill="none" stroke="#1B4965" stroke-width="1.5" stroke-dasharray="4"/>
  <!-- Legenda -->
  <rect x="50" y="780" width="300" height="100" fill="#FAF3E8" stroke="#2B2B2B" stroke-width="0.5"/>
  <circle cx="70" cy="800" r="6" fill="#C8952E"/>
  <text x="85" y="805" font-size="11" fill="#2B2B2B">Sambaquis (litoral, 6.000-8.000 anos)</text>
  <circle cx="70" cy="825" r="6" fill="#B5533E"/>
  <text x="85" y="830" font-size="11" fill="#2B2B2B">Arte rupestre (Chapada das Mesas)</text>
  <circle cx="70" cy="850" r="6" fill="#2D6A4F"/>
  <text x="85" y="855" font-size="11" fill="#2B2B2B">Estearias (Baixada Maranhense)</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Editorial map illustration of Maranhão state, Brazil, showing archaeological site distribution. Three types of markers: shell-shaped icons along the northwest coast (sambaquis, 6000-8000 years old), hand-print icons in the southern plateau region near Carolina (rock art, Chapada das Mesas), and stilt-house icons in the central lowlands near rivers Pindaré and Maracu (estearias, pre-colonial lake dwellings). Highlight one special site: Sítio Chácara Rosane in São Luís with a callout box showing '43 skeletons, 100,000 artifacts, 6,000+ years'. Background shows simplified biome zones: dark green for Amazon (west), ochre for Cerrado (south), light blue for coast (north). Major rivers in blue. Clean editorial style, warm palette with green (#2D6A4F) as accent, cream background (#FAF3E8). Kurzgesagt-inspired flat design. No photorealism."
**Estilo**: Infográfico editorial flat, estilo Kurzgesagt
**Referência**: National Geographic archaeological maps
**NAO incluir**: fotografias, texturas realistas, tipografia serifada

---

---
id: VIS-V13-B
verbete: V13
tipo: diagrama
posicao: corpo
---

# Visual V13-B: Timeline — 8.000 a.C. a 1500 d.C.

## 1. Briefing para designer
**O que é**: Timeline visual horizontal mostrando as três grandes tradições arqueológicas do Maranhão em paralelo, com marcos comparativos globais para contextualização.
**Dados**:
- Linha do tempo: 8.000 a.C. a 1.500 d.C. (10.000 anos)
- Faixa 1 — Sambaquis: 8.000 a.C. a ~1.000 a.C. (litoral, cor: Ocre)
- Faixa 2 — Arte rupestre: período indeterminado, representar como faixa tracejada (Chapada das Mesas, cor: Terracota)
- Faixa 3 — Estearias: ~1.000 d.C. a 1.500 d.C. (rios, cor: Verde-mata)
- Marcos comparativos (abaixo da timeline):
  - ~8.000 a.C.: Início da agricultura na Mesopotâmia
  - ~4.500 a.C.: Primeiras pirâmides do Egito
  - ~3.000 a.C.: Stonehenge
  - ~750 a.C.: Fundação de Roma
  - 1.500 d.C.: Chegada dos europeus ao MA
- Ponto destacado: Sítio Chácara Rosane (~4.000 a.C.) na faixa dos sambaquis
**Referência de estilo**: Timeline editorial com faixas coloridas paralelas, clean
**Paleta**: Ocre #C8952E (sambaquis), Terracota #B5533E (rupestres), Verde-mata #2D6A4F (estearias), Carvão #2B2B2B (marcos globais), Creme #FAF3E8 (fundo)
**Tamanho**: Meia página (largura total, ~10cm de altura)

## 2. SVG simplificado
**Elementos**:
- Eixo horizontal: 8.000 a.C. a 1.500 d.C., com marcações a cada 1.000 anos
- 3 faixas horizontais paralelas (sambaquis, rupestres, estearias) com início/fim indicando período de ocupação
- Faixa rupestre tracejada (período incerto)
- Pontos de marco abaixo do eixo (pirâmides, Stonehenge, Roma, etc.)
- Ponto especial na faixa sambaqui: Chácara Rosane
**Layout**: Horizontal, leitura da esquerda (passado) para a direita (presente)

```svg
<!-- SVG esquemático — placeholder para designer -->
<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="900" height="300" fill="#FAF3E8"/>
  <!-- Título -->
  <text x="450" y="25" text-anchor="middle" font-size="16" fill="#2D6A4F" font-weight="bold">10.000 anos de ocupação humana no Maranhão</text>
  <!-- Eixo -->
  <line x1="50" y1="180" x2="850" y2="180" stroke="#2B2B2B" stroke-width="1"/>
  <!-- Marcações de tempo -->
  <text x="50" y="200" font-size="9" fill="#2B2B2B">8000 a.C.</text>
  <text x="210" y="200" font-size="9" fill="#2B2B2B">6000 a.C.</text>
  <text x="370" y="200" font-size="9" fill="#2B2B2B">4000 a.C.</text>
  <text x="530" y="200" font-size="9" fill="#2B2B2B">2000 a.C.</text>
  <text x="690" y="200" font-size="9" fill="#2B2B2B">0</text>
  <text x="830" y="200" font-size="9" fill="#2B2B2B">1500</text>
  <!-- Faixa Sambaquis -->
  <rect x="50" y="60" width="560" height="25" rx="4" fill="#C8952E" opacity="0.7"/>
  <text x="55" y="78" font-size="10" fill="white" font-weight="bold">Sambaquis (litoral)</text>
  <!-- Ponto Chácara Rosane -->
  <circle cx="370" cy="72" r="6" fill="#B5533E" stroke="white" stroke-width="2"/>
  <text x="380" y="55" font-size="8" fill="#B5533E">Chácara Rosane</text>
  <!-- Faixa Rupestres (tracejada) -->
  <rect x="130" y="95" width="500" height="25" rx="4" fill="#B5533E" opacity="0.3" stroke="#B5533E" stroke-dasharray="6"/>
  <text x="135" y="113" font-size="10" fill="#B5533E" font-weight="bold">Arte rupestre (Chapada — período incerto)</text>
  <!-- Faixa Estearias -->
  <rect x="690" y="130" width="140" height="25" rx="4" fill="#2D6A4F" opacity="0.7"/>
  <text x="695" y="148" font-size="10" fill="white" font-weight="bold">Estearias</text>
  <!-- Marcos globais -->
  <line x1="50" y1="215" x2="50" y2="230" stroke="#2B2B2B" stroke-width="0.5"/>
  <text x="50" y="245" font-size="8" fill="#2B2B2B">Agricultura</text>
  <text x="50" y="255" font-size="8" fill="#2B2B2B">Mesopotâmia</text>
  <line x1="330" y1="215" x2="330" y2="230" stroke="#2B2B2B" stroke-width="0.5"/>
  <text x="330" y="245" font-size="8" fill="#2B2B2B">Pirâmides</text>
  <line x1="450" y1="215" x2="450" y2="230" stroke="#2B2B2B" stroke-width="0.5"/>
  <text x="450" y="245" font-size="8" fill="#2B2B2B">Stonehenge</text>
  <line x1="610" y1="215" x2="610" y2="230" stroke="#2B2B2B" stroke-width="0.5"/>
  <text x="610" y="245" font-size="8" fill="#2B2B2B">Roma</text>
  <line x1="850" y1="215" x2="850" y2="230" stroke="#2B2B2B" stroke-width="0.5"/>
  <text x="830" y="245" font-size="8" fill="#2B2B2B">Europeus</text>
  <text x="830" y="255" font-size="8" fill="#2B2B2B">no MA</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Horizontal timeline infographic spanning 8000 BC to 1500 AD showing human occupation of Maranhão, Brazil. Three parallel colored bands: ochre band (#C8952E) for coastal sambaquis (shell mounds, 8000-1000 BC), terracotta dashed band (#B5533E) for rock art (Chapada das Mesas, uncertain period), and green band (#2D6A4F) for estearias (lake dwellings, 1000-1500 AD). Below the timeline axis, small markers for global reference points: Mesopotamian agriculture (8000 BC), Egyptian pyramids (4500 BC), Stonehenge (3000 BC), Rome (750 BC), European arrival (1500 AD). Special marker on sambaqui band: Sítio Chácara Rosane (~4000 BC, 43 skeletons). Clean editorial infographic style, cream background (#FAF3E8), flat design. Kurzgesagt-inspired. No photorealism."
**Estilo**: Infográfico editorial flat
**Referência**: BBC History timelines, Kurzgesagt
**NAO incluir**: fotografias, texturas 3D, fontes decorativas
