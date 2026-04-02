---
id: VIS-V09-A
verbete: V09
tipo: infográfico
posicao: página-inteira
---

# Visual V09-A: Corte transversal — o paradoxo explicado

## 1. Briefing para designer
**O que é**: Infográfico de corte transversal (lateral) mostrando as camadas geológicas dos Lençóis Maranhenses — o mecanismo que cria as lagoas. Visual principal do verbete, página inteira.
**Dados**:
- Superfície: dunas de areia branca (quartzo), 30-50 m de altura
- Camada de areia porosa: 2-3 m de espessura
- Formação Barreiras: camada impermeável de argila (Terciário)
- Lençol freático: a ~3 m de profundidade
- Lagoa interdunar: até 100 m de comprimento, até 3 m de profundidade
- Setas indicando: chuva → absorção pela areia → bloqueio pela argila → lençol sobe → lagoa aflora
**Referência de estilo**: Infográfico tipo National Geographic — corte de terreno em perspectiva isométrica ou lateral limpa, com camadas coloridas e legendas
**Paleta**: Branco-areia (#F5F5DC) para dunas, Azul-mar (#1B4F72) para água/lagoas, Terracota (#BA4A00) para Formação Barreiras, Verde-mangue (#1E8449) para vegetação nas bordas
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Perfil lateral de 3 dunas com 2 vales interdunares
- Camada azul clara (lençol freático) sob as dunas
- Camada marrom (Formação Barreiras) como base impermeável
- Lagoas azuis nos vales (preenchimento até a superfície)
- Setas azuis: chuva descendo → seta lateral na argila (bloqueio) → seta subindo (lençol)
- Legendas com dados
**Layout**: Horizontal, leitura da esquerda para a direita
**Cores**: Branco (#F5F5DC) dunas, Azul (#1B4F72) água, Marrom (#BA4A00) argila, Verde (#1E8449) vegetação

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Formação Barreiras (camada impermeável) -->
  <rect x="0" y="300" width="800" height="100" fill="#BA4A00" opacity="0.8"/>
  <text x="400" y="360" text-anchor="middle" fill="white" font-size="14" font-weight="bold">FORMAÇÃO BARREIRAS (argila impermeável — Terciário)</text>

  <!-- Lençol freático -->
  <rect x="0" y="260" width="800" height="40" fill="#1B4F72" opacity="0.3"/>
  <text x="700" y="285" text-anchor="middle" fill="#1B4F72" font-size="11">lençol freático (~3m)</text>

  <!-- Dunas -->
  <path d="M0,260 Q100,140 200,260 Q300,100 400,260 Q500,120 600,260 Q700,140 800,260" fill="#F5F5DC" stroke="#D4AC0D" stroke-width="1"/>

  <!-- Lagoas nos vales -->
  <ellipse cx="200" cy="252" rx="50" ry="12" fill="#1B4F72" opacity="0.7"/>
  <ellipse cx="400" cy="252" rx="60" ry="14" fill="#1B4F72" opacity="0.7"/>
  <ellipse cx="600" cy="252" rx="45" ry="11" fill="#1B4F72" opacity="0.7"/>

  <!-- Setas de chuva -->
  <line x1="300" y1="30" x2="300" y2="100" stroke="#1B4F72" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="320" y1="40" x2="320" y2="110" stroke="#1B4F72" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="340" y="50" fill="#1B4F72" font-size="12">chuva (1.200–2.000 mm/ano)</text>

  <!-- Seta de bloqueio -->
  <line x1="150" y1="300" x2="250" y2="300" stroke="red" stroke-width="2"/>
  <text x="200" y="320" text-anchor="middle" fill="red" font-size="10">↓ BLOQUEIO ↓</text>

  <!-- Seta de subida -->
  <line x1="400" y1="290" x2="400" y2="255" stroke="#1B4F72" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="440" y="275" fill="#1B4F72" font-size="10">água sobe</text>

  <!-- Legendas -->
  <text x="200" y="240" text-anchor="middle" fill="white" font-size="10" font-weight="bold">LAGOA</text>
  <text x="300" y="180" text-anchor="middle" fill="#8B7355" font-size="10">duna (30-50m)</text>

  <!-- Escala -->
  <text x="20" y="390" fill="white" font-size="10">Escala vertical exagerada para clareza</text>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#1B4F72"/>
    </marker>
  </defs>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Cross-section geological diagram of Lençóis Maranhenses National Park, Brazil. Cutaway view showing: white quartz sand dunes (30-50m tall) on top, crystal clear blue freshwater lagoons in the interdune valleys, a layer of impermeable Barreiras Formation clay underneath, and the water table connecting the lagoons. Arrows showing rain falling on dunes, water percolating through sand, being blocked by clay, and rising to form lagoons. Clean infographic style, National Geographic quality, educational diagram, labeled layers. Color palette: white sand, deep blue water, terracotta clay, light blue sky. Isometric perspective, highly detailed, professional scientific illustration."
**Estilo**: Infográfico científico editorial (National Geographic / Kurzgesagt)
**Referência**: Cortes geológicos de revistas de divulgação científica
**NÃO incluir**: Pessoas, animais, texto em inglês (o texto será adicionado em português pelo designer)

---

---
id: VIS-V09-B
verbete: V09
tipo: infográfico
posicao: meia-página
---

# Visual V09-B: Ciclo sazonal — o calendário das lagoas

## 1. Briefing para designer
**O que é**: Infográfico circular (tipo relógio/calendário) mostrando o ciclo anual das lagoas dos Lençóis. Meia página.
**Dados**:
- Jan-Jun: CHUVAS — precipitação intensa, lençol freático sobe
- Mai-Ago: LAGOAS CHEIAS — pico, até 41% do parque coberto
- Jul-Set: MELHOR VISITA — lagoas cheias, clima mais ameno
- Set-Dez: SECA — evaporação voraz, 1m/mês de perda, lagoas desaparecem
- Dunas migram 4-25 m/ano; lagoas se reformam em novos lugares
**Referência de estilo**: Infográfico circular tipo "wheel of the year", com 12 meses ao redor e ícones/cores indicando cada fase
**Paleta**: Azul-mar (#1B4F72) para meses úmidos, Dourado-babaçu (#D4AC0D) para meses secos, Branco-areia (#F5F5DC) para transições
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Círculo dividido em 12 setores (meses), gradiente de azul (jan-jul) a dourado (ago-dez), ícones de chuva/sol/lagoa em cada quadrante, dados-chave nos 4 pontos cardeais
**Layout**: Circular, leitura horária começando em janeiro (topo)

## 3. Prompt para IA generativa
**Prompt**: "Circular calendar infographic showing the annual cycle of Lençóis Maranhenses lagoons. 12 months arranged in a circle. January to June: blue gradient, rain icons, water rising. May to August: deep blue, full lagoons, peak. September to December: golden/amber gradient, sun icons, evaporation, lagoons disappearing. Center: aerial photo of dunes with lagoons. Clean modern infographic style, data visualization, minimal text placeholders. Color palette: deep blue for wet season, golden amber for dry season, white sand background."
**Estilo**: Infográfico editorial moderno, dados visuais
**NÃO incluir**: Texto definitivo (será adicionado em português)

---

---
id: VIS-V09-C
verbete: V09
tipo: mapa
posicao: corpo
---

# Visual V09-C: Mapa de localização — PNLM

## 1. Briefing para designer
**O que é**: Mapa de localização do Parque Nacional dos Lençóis Maranhenses no contexto do estado do Maranhão. Tamanho de coluna ou meia página.
**Dados**:
- Contorno do Maranhão com destaque para a região do PNLM (costa leste)
- Municípios: Barreirinhas, Santo Amaro do Maranhão, Primeira Cruz
- Rios: Preguiças, Negro, Periá
- Comunidades: Queimada dos Britos (centro), Atins (costa), Mandacaru, Caburé
- Área do parque: 155.000 ha (Decreto 86.060/1981)
- São Luís marcada como referência (capital)
- Oceano Atlântico ao norte
**Referência de estilo**: Mapa esquemático limpo, estilo editorial (não Google Maps)
**Paleta**: Branco-areia (#F5F5DC) para área de dunas, Azul-mar (#1B4F72) para oceano/rios, Verde-mangue (#1E8449) para vegetação, Terracota (#BA4A00) para pontos de comunidade
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Silhueta do Maranhão, retângulo/polígono destacando área do PNLM na costa leste, pontos para cidades, linhas para rios, legenda
**Layout**: Mapa orientado ao norte, com inset mostrando posição no Brasil

## 3. Prompt para IA generativa
**Prompt**: "Clean editorial map of Maranhão state, Brazil, highlighting Lençóis Maranhenses National Park on the eastern coast. Minimalist cartographic style. Show: park boundary in white/beige (dune area), Atlantic Ocean in deep blue to the north, rivers (Preguiças, Negro) as thin blue lines, town markers for Barreirinhas and Santo Amaro, São Luís marked as capital city. Small inset showing Maranhão's position in Brazil. Color palette: beige for dunes, deep blue ocean, green for vegetation, terracotta for settlements. Clean, modern, editorial quality."
**Estilo**: Cartografia editorial moderna
**NÃO incluir**: Detalhes topográficos excessivos, estradas, grade de coordenadas
