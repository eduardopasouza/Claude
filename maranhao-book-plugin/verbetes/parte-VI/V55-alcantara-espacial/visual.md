---
id: VIS-V55-A
verbete: V55
tipo: mapa
posicao: página-inteira
---

# Visual V55-A: Mapa-mundi de bases de lançamento — a vantagem equatorial de Alcântara

## 1. Briefing para designer
**O que é**: Mapa-mundi centrado no Atlântico, mostrando as principais bases de lançamento orbital do mundo com linhas de latitude destacadas. Alcântara aparece em destaque por sua proximidade ao equador. Página inteira.
**Dados**:
- Linha do equador (0°) destacada em vermelho/dourado
- Cabo Canaveral, EUA: 28°29'N — 1.500+ lançamentos orbitais — operacional
- Kourou (CSG), Guiana Francesa: 5°14'N — 300+ lançamentos — operacional (Ariane 6)
- Alcântara (CLA), Brasil: 2°18'S — 0 lançamentos orbitais — suborbital/comercialização
- Sriharikota (SDSC), Índia: 13°43'N — 100+ lançamentos — operacional (PSLV/GSLV)
- Broglio/San Marco, Quênia: 2°56'S — 9 lançamentos (1967-1988) — desativada
- Dados de economia de combustível: Alcântara economiza 31% vs. Canaveral, 13% vs. Kourou para órbitas GEO
- Azimute livre de Alcântara: 240° sobre o Atlântico
**Referência de estilo**: Kurzgesagt — flat design, formas geométricas limpas, cores vibrantes sobre fundo escuro
**Paleta**: Azul-mar (#1B4F72) para oceanos/fundo, Cinza (#888) para continentes, Terracota (#BA4A00) para Alcântara (destaque), Branco para dados e linhas de latitude, Dourado para a linha do equador
**Tamanho**: Página inteira (23x28 cm)

## 2. SVG simplificado
**Elementos**:
- Mapa-mundi simplificado (contornos dos continentes)
- Linhas de latitude horizontais tracejadas (0°, 5°N, 13°N, 28°N)
- Linha do equador espessa e destacada
- Ícones de foguete em cada base, tamanho proporcional ao número de lançamentos
- Alcântara com anel pulsante (destaque) e foguete vazio/transparente (zero lançamentos)
- Caixa de dados ao lado de cada base: latitude, total de lançamentos
- Caixa comparativa no canto inferior: economia de combustível de Alcântara vs. concorrentes
**Layout**: Horizontal, projeção equirretangular simplificada

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="800" height="500" fill="#0D2137"/>

  <!-- Oceanos (fundo já serve) -->

  <!-- Continentes simplificados -->
  <!-- América do Sul -->
  <path d="M200,230 L230,210 L260,220 L270,260 L260,320 L240,370 L220,380 L210,350 L200,280 Z" fill="#888" opacity="0.5"/>
  <!-- América do Norte -->
  <path d="M150,100 L250,80 L280,120 L260,180 L220,200 L170,190 L140,150 Z" fill="#888" opacity="0.5"/>
  <!-- África -->
  <path d="M380,180 L430,170 L460,200 L470,260 L450,330 L420,350 L390,320 L370,260 L370,210 Z" fill="#888" opacity="0.5"/>
  <!-- Europa -->
  <path d="M370,100 L420,90 L450,110 L440,150 L400,170 L370,160 Z" fill="#888" opacity="0.5"/>
  <!-- Índia -->
  <path d="M530,170 L560,160 L570,200 L550,240 L530,220 Z" fill="#888" opacity="0.5"/>

  <!-- Linha do equador -->
  <line x1="0" y1="250" x2="800" y2="250" stroke="#D4AC0D" stroke-width="2.5"/>
  <text x="790" y="247" text-anchor="end" fill="#D4AC0D" font-size="10" font-weight="bold">0° EQUADOR</text>

  <!-- Linhas de latitude -->
  <line x1="0" y1="235" x2="800" y2="235" stroke="#fff" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.3"/>
  <text x="790" y="232" text-anchor="end" fill="#fff" font-size="8" opacity="0.4">5°N</text>

  <line x1="0" y1="210" x2="800" y2="210" stroke="#fff" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.3"/>
  <text x="790" y="207" text-anchor="end" fill="#fff" font-size="8" opacity="0.4">13°N</text>

  <line x1="0" y1="165" x2="800" y2="165" stroke="#fff" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.3"/>
  <text x="790" y="162" text-anchor="end" fill="#fff" font-size="8" opacity="0.4">28°N</text>

  <!-- Cabo Canaveral — 28°N, 1500+ -->
  <circle cx="230" cy="165" r="18" fill="#1B4F72" opacity="0.6"/>
  <polygon points="225,175 235,175 230,150" fill="#fff"/>
  <text x="250" y="160" fill="#fff" font-size="9" font-weight="bold">Cabo Canaveral</text>
  <text x="250" y="172" fill="#fff" font-size="8">28°29'N | 1.500+ lanc.</text>

  <!-- Kourou — 5°N, 300+ -->
  <circle cx="260" cy="235" r="12" fill="#1B4F72" opacity="0.6"/>
  <polygon points="256,242 264,242 260,225" fill="#fff"/>
  <text x="275" y="230" fill="#fff" font-size="9" font-weight="bold">Kourou</text>
  <text x="275" y="242" fill="#fff" font-size="8">5°14'N | 300+ lanc.</text>

  <!-- ALCANTARA — 2°S, 0 -->
  <circle cx="240" cy="255" r="14" fill="none" stroke="#BA4A00" stroke-width="2.5"/>
  <circle cx="240" cy="255" r="20" fill="none" stroke="#BA4A00" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>
  <polygon points="236,262 244,262 240,245" fill="#BA4A00" opacity="0.4" stroke="#BA4A00" stroke-width="1"/>
  <text x="200" y="278" fill="#BA4A00" font-size="10" font-weight="bold">ALCANTARA</text>
  <text x="200" y="290" fill="#BA4A00" font-size="8">2°18'S | 0 lanc. orbitais</text>

  <!-- Sriharikota — 13°N, 100+ -->
  <circle cx="545" cy="210" r="10" fill="#1B4F72" opacity="0.6"/>
  <polygon points="541,217 549,217 545,200" fill="#fff"/>
  <text x="560" y="205" fill="#fff" font-size="9" font-weight="bold">Sriharikota</text>
  <text x="560" y="217" fill="#fff" font-size="8">13°43'N | 100+ lanc.</text>

  <!-- Broglio/San Marco — 2°S, 9 (desativada) -->
  <circle cx="430" cy="255" r="5" fill="#888" opacity="0.4"/>
  <text x="440" y="258" fill="#888" font-size="8">Broglio 2°56'S | 9 (desat.)</text>

  <!-- Caixa de dados — economia de combustível -->
  <rect x="520" y="340" width="250" height="90" fill="#0D2137" stroke="#BA4A00" stroke-width="1" rx="6"/>
  <text x="535" y="360" fill="#BA4A00" font-size="10" font-weight="bold">VANTAGEM ALCANTARA</text>
  <text x="535" y="378" fill="#fff" font-size="9">vs. Canaveral: -31% combustivel</text>
  <text x="535" y="393" fill="#fff" font-size="9">vs. Kourou: -13% combustivel</text>
  <text x="535" y="408" fill="#fff" font-size="9">Azimute livre: 240° sobre Atlantico</text>
  <text x="535" y="423" fill="#BA4A00" font-size="9" font-weight="bold">Lancamentos orbitais: 0</text>

  <!-- Titulo -->
  <text x="400" y="30" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold">BASES DE LANCAMENTO — LATITUDE E DESEMPENHO</text>
  <text x="400" y="48" text-anchor="middle" fill="#D4AC0D" font-size="11">Quanto mais perto do equador, menos combustivel. Quanto mais investimento, mais lancamentos.</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "World map infographic in Kurzgesagt flat design style showing major rocket launch sites. Dark navy background (#0D2137) with simplified continent outlines in grey. Prominent golden equator line glowing across the map. Five launch sites marked with rocket icons scaled by number of launches: Cape Canaveral (28°N, large rocket, 1500+ launches), Kourou (5°N, medium rocket, 300+), Sriharikota (13°N, medium rocket, 100+), Broglio Kenya (2°S, tiny faded rocket, 9 launches, deactivated), and Alcantara Brazil (2°S, empty/ghost rocket outline in terracotta red, 0 orbital launches). Alcantara highlighted with pulsing rings to show it has the best location but zero results. Horizontal latitude lines at 0°, 5°, 13°, 28° marked. Data box in corner showing fuel savings: -31% vs Canaveral, -13% vs Kourou. Clean geometric style, vibrant colors on dark background, no text — labels added separately."
**Estilo**: Kurzgesagt (In a Nutshell) — flat design, fundo escuro, formas geométricas vibrantes
**NÃO incluir**: Texto definitivo em português (será inserido pelo designer), fotografia real

---

---
id: VIS-V55-B
verbete: V55
tipo: timeline
posicao: meia-página
---

# Visual V55-B: Linha do tempo do programa espacial brasileiro em Alcântara

## 1. Briefing para designer
**O que é**: Timeline vertical/horizontal mostrando os marcos do programa espacial brasileiro de 1979 a 2025, com destaque para o ciclo de fracassos e recomeços. Meia página.
**Dados**:
- 1979: Missão Espacial Completa Brasileira (MECB) lançada pelo governo militar
- 1983: Criação do CLA — Centro de Lançamento de Alcântara (Decreto 88.136)
- 1986-87: Remoção de 312 famílias quilombolas para instalação da base
- 1997: VLS-1 V01 — falha no 1° estágio, foguete destruído em voo
- 1999: VLS-1 V02 — autodestruído por desvio de trajetória
- 2003: Explosão do VLS-1 V03 — 21 técnicos mortos, torre destruída
- 2019: Acordo de Salvaguardas Tecnológicas (AST) com os EUA
- 2024: Termo de Compromisso (AGU) — 78.105 ha quilombo, 9.256 ha CLA
- 2025: Sentença da Corte IDH — 1a sobre quilombolas, Brasil condenado, US$ 4 mi em reparacoes
**Referência de estilo**: Vox editorial timeline — eixo central com eventos alternando lados, ícones minimalistas, tipografia forte
**Paleta**: Azul-mar (#1B4F72) para marcos institucionais, Cinza (#888) para marcos neutros, Terracota/Vermelho (#BA4A00) para fracassos e conflitos, Preto (#1C1C1C) para marcos quilombolas
**Tamanho**: Meia página (~11x14 cm)

## 2. SVG simplificado
**Elementos**:
- Eixo vertical central representando o tempo (1979-2025)
- Marcos alternando esquerda e direita do eixo
- Ícones: foguete (marcos espaciais), casa (marcos quilombolas), explosão (2003), balança (marcos jurídicos)
- Cor de cada marco indica natureza: azul (institucional), vermelho (fracasso), preto (quilombola)
- 2003 com destaque especial — ícone maior, cor vermelha, "21 mortos"
**Layout**: Vertical, leitura de cima para baixo

```svg
<svg viewBox="0 0 400 650" xmlns="http://www.w3.org/2000/svg">
  <!-- Titulo -->
  <text x="200" y="25" text-anchor="middle" fill="#1C1C1C" font-size="13" font-weight="bold">PROGRAMA ESPACIAL BRASILEIRO EM ALCANTARA</text>
  <text x="200" y="42" text-anchor="middle" fill="#888" font-size="9">1979 — 2025 | 46 anos, 0 lancamentos orbitais</text>

  <!-- Eixo central -->
  <line x1="200" y1="55" x2="200" y2="620" stroke="#888" stroke-width="2"/>

  <!-- 1979 — MECB -->
  <circle cx="200" cy="75" r="6" fill="#1B4F72"/>
  <text x="185" y="69" text-anchor="end" fill="#1B4F72" font-size="10" font-weight="bold">1979</text>
  <text x="220" y="79" fill="#333" font-size="9">MECB — Missao Espacial Completa</text>

  <!-- 1983 — CLA -->
  <circle cx="200" cy="130" r="6" fill="#1B4F72"/>
  <text x="185" y="124" text-anchor="end" fill="#1B4F72" font-size="10" font-weight="bold">1983</text>
  <text x="220" y="134" fill="#333" font-size="9">Criacao do CLA (Decreto 88.136)</text>

  <!-- 1986-87 — Remocao quilombolas -->
  <circle cx="200" cy="185" r="6" fill="#1C1C1C"/>
  <text x="185" y="179" text-anchor="end" fill="#1C1C1C" font-size="10" font-weight="bold">1986-87</text>
  <text x="220" y="183" fill="#1C1C1C" font-size="9">312 familias quilombolas removidas</text>
  <text x="220" y="195" fill="#888" font-size="8">32 comunidades → 7 agrovilas</text>

  <!-- 1997 — VLS falha 1 -->
  <circle cx="200" cy="245" r="6" fill="#BA4A00"/>
  <text x="185" y="239" text-anchor="end" fill="#BA4A00" font-size="10" font-weight="bold">1997</text>
  <text x="220" y="249" fill="#BA4A00" font-size="9">VLS-1 V01 — falha no 1o estagio</text>

  <!-- 1999 — VLS falha 2 -->
  <circle cx="200" cy="300" r="6" fill="#BA4A00"/>
  <text x="185" y="294" text-anchor="end" fill="#BA4A00" font-size="10" font-weight="bold">1999</text>
  <text x="220" y="304" fill="#BA4A00" font-size="9">VLS-1 V02 — autodestruido em voo</text>

  <!-- 2003 — EXPLOSAO (destaque) -->
  <circle cx="200" cy="365" r="12" fill="#BA4A00"/>
  <text x="200" y="370" text-anchor="middle" fill="#fff" font-size="8" font-weight="bold">21</text>
  <text x="185" y="355" text-anchor="end" fill="#BA4A00" font-size="11" font-weight="bold">2003</text>
  <text x="220" y="360" fill="#BA4A00" font-size="10" font-weight="bold">EXPLOSAO — 21 mortos</text>
  <text x="220" y="374" fill="#BA4A00" font-size="8">VLS-1 V03. Torre destruida.</text>
  <text x="220" y="386" fill="#BA4A00" font-size="8">Programa efetivamente abandonado.</text>

  <!-- 2019 — AST -->
  <circle cx="200" cy="440" r="6" fill="#888"/>
  <text x="185" y="434" text-anchor="end" fill="#888" font-size="10" font-weight="bold">2019</text>
  <text x="220" y="444" fill="#333" font-size="9">Acordo EUA-Brasil (AST)</text>

  <!-- 2024 — Termo quilombo -->
  <circle cx="200" cy="505" r="6" fill="#1C1C1C"/>
  <text x="185" y="499" text-anchor="end" fill="#1C1C1C" font-size="10" font-weight="bold">2024</text>
  <text x="220" y="503" fill="#1C1C1C" font-size="9">Termo de Compromisso (AGU)</text>
  <text x="220" y="515" fill="#888" font-size="8">78.105 ha quilombo | 9.256 ha CLA</text>

  <!-- 2025 — Sentenca Corte IDH -->
  <circle cx="200" cy="570" r="8" fill="#1C1C1C" stroke="#BA4A00" stroke-width="2"/>
  <text x="185" y="564" text-anchor="end" fill="#1C1C1C" font-size="10" font-weight="bold">2025</text>
  <text x="220" y="567" fill="#1C1C1C" font-size="9" font-weight="bold">Sentenca Corte IDH</text>
  <text x="220" y="580" fill="#888" font-size="8">1a sobre quilombolas. Brasil condenado.</text>
  <text x="220" y="592" fill="#888" font-size="8">US$ 4 mi reparacoes. Titulacao em 3 anos.</text>

  <!-- Legenda -->
  <circle cx="30" cy="638" r="4" fill="#1B4F72"/>
  <text x="40" y="641" fill="#333" font-size="8">Institucional</text>
  <circle cx="120" cy="638" r="4" fill="#BA4A00"/>
  <text x="130" y="641" fill="#333" font-size="8">Fracasso/Tragedia</text>
  <circle cx="240" cy="638" r="4" fill="#1C1C1C"/>
  <text x="250" y="641" fill="#333" font-size="8">Quilombola/Juridico</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Vertical editorial timeline infographic showing Brazil's space program at Alcantara from 1979 to 2025. Clean Vox-style design with a central vertical axis. Events alternate left and right with minimalist icons: rocket icon for space milestones (1979 MECB, 1983 CLA creation), house icon for quilombola events (1986 family removal, 2024 land accord), explosion icon for failures (1997, 1999 rocket failures, 2003 disaster). The 2003 explosion is the largest event — depicted with a dramatic burst icon and '21 dead' prominently displayed. Later events: 2019 US agreement (handshake icon), 2024 quilombo accord (scales of justice), 2025 Inter-American Court ruling (gavel). Color coding: navy blue for institutional, terracotta red for failures, black for quilombola/legal. White background, strong typography, generous whitespace. Vox / The Pudding editorial style. No final text — labels added separately."
**Estilo**: Infografico editorial (Vox / The Pudding) — eixo limpo, tipografia forte, espacamento generoso
**NAO incluir**: Texto definitivo em portugues (sera inserido pelo designer), fotografias reais
