---
id: VIS-V05-A
verbete: V05
tipo: mapa
posicao: página-inteira
---

# Visual V05-A: Mapa do litoral maranhense — três setores

## 1. Briefing para designer
**O que é**: Mapa ilustrado do litoral do Maranhão dividido em três setores geomorfológicos: Reentrâncias Maranhenses (oeste), Golfão Maranhense (centro) e Costa oriental (leste). Página inteira.
**Dados**:
- Litoral total: 640 km
- Setor Oeste — Reentrâncias Maranhenses: 2,6 milhões de hectares, APA desde 1991, Sítio Ramsar 1993, 16 municípios
- Setor Centro — Golfão: Baía de São Marcos + Baía de São José, amplitude de maré até 7m, São Luís na Ilha do Maranhão
- Setor Leste — Costa oriental: dunas, restingas, lagoas pluviais, Lençóis Maranhenses, Delta do Parnaíba
- UCs destacadas: APA Reentrâncias, RESEX Cururupu, PNLM, RESEX Delta do Parnaíba
- Municípios-chave: Cururupu, São Luís, Alcântara, Barreirinhas, Tutóia
- Cobertura de mangue indicada (área hachurada verde-escuro)
**Referência de estilo**: Mapa esquemático editorial — não cartografia técnica, estilo DK ou Monocle
**Paleta**: Verde-mangue (#1E8449) para manguezais, Azul-mar (#1B4F72) para oceano, Branco-areia (#F5F5DC) para dunas/costa leste, Terracota (#BA4A00) para pontos de cidade
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Silhueta do litoral maranhense (simplificada)
- Três zonas coloridas: verde-escuro (oeste/mangue), cinza-azulado (centro/golfão), branco-areia (leste/dunas)
- Ícones: palmeira (Reentrâncias), prédio (São Luís), duna (Lençóis)
- Pontos para cidades, linhas para rios
- Legenda lateral com dados de cada setor
**Layout**: Horizontal, costa orientada ao norte

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Oceano Atlântico -->
  <rect x="0" y="0" width="800" height="150" fill="#1B4F72" opacity="0.3"/>
  <text x="400" y="80" text-anchor="middle" fill="#1B4F72" font-size="16" font-weight="bold">OCEANO ATLÂNTICO</text>

  <!-- Setor Oeste — Reentrâncias -->
  <rect x="20" y="150" width="250" height="200" fill="#1E8449" opacity="0.4" rx="10"/>
  <text x="145" y="180" text-anchor="middle" fill="#1E8449" font-size="12" font-weight="bold">REENTRÂNCIAS</text>
  <text x="145" y="200" text-anchor="middle" fill="#1E8449" font-size="10">2,6 mi ha | APA + Ramsar</text>
  <text x="145" y="220" text-anchor="middle" fill="#1E8449" font-size="10">Maior sistema de baías</text>
  <text x="145" y="240" text-anchor="middle" fill="#1E8449" font-size="10">do Atlântico Sul</text>
  <!-- Cururupu -->
  <circle cx="100" cy="270" r="5" fill="#BA4A00"/>
  <text x="115" y="275" fill="#BA4A00" font-size="9">Cururupu</text>

  <!-- Setor Centro — Golfão -->
  <rect x="290" y="150" width="200" height="200" fill="#1B4F72" opacity="0.2" rx="10"/>
  <text x="390" y="180" text-anchor="middle" fill="#1B4F72" font-size="12" font-weight="bold">GOLFÃO</text>
  <text x="390" y="200" text-anchor="middle" fill="#1B4F72" font-size="10">Baía de São Marcos</text>
  <text x="390" y="220" text-anchor="middle" fill="#1B4F72" font-size="10">Maré: até 7m amplitude</text>
  <!-- São Luís -->
  <circle cx="390" cy="260" r="7" fill="#BA4A00"/>
  <text x="405" y="265" fill="#BA4A00" font-size="9" font-weight="bold">São Luís</text>
  <!-- Alcântara -->
  <circle cx="350" cy="280" r="4" fill="#BA4A00"/>
  <text x="320" y="295" fill="#BA4A00" font-size="9">Alcântara</text>

  <!-- Setor Leste — Costa oriental -->
  <rect x="510" y="150" width="270" height="200" fill="#F5F5DC" opacity="0.6" rx="10"/>
  <text x="645" y="180" text-anchor="middle" fill="#8B7355" font-size="12" font-weight="bold">COSTA ORIENTAL</text>
  <text x="645" y="200" text-anchor="middle" fill="#8B7355" font-size="10">Dunas, restingas, lagoas</text>
  <text x="645" y="220" text-anchor="middle" fill="#8B7355" font-size="10">Lençóis Maranhenses</text>
  <!-- Barreirinhas -->
  <circle cx="600" cy="260" r="5" fill="#BA4A00"/>
  <text x="615" y="265" fill="#BA4A00" font-size="9">Barreirinhas</text>
  <!-- Tutóia -->
  <circle cx="720" cy="270" r="4" fill="#BA4A00"/>
  <text x="735" y="275" fill="#BA4A00" font-size="9">Tutóia</text>

  <!-- Legenda -->
  <text x="20" y="385" fill="#333" font-size="11" font-weight="bold">640 km de litoral — 2º mais extenso do Brasil</text>
  <text x="20" y="398" fill="#666" font-size="9">36% dos manguezais brasileiros concentrados no setor oeste</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Illustrated editorial map of the Maranhão coastline, Brazil, divided into three distinct sectors. West: Reentrâncias Maranhenses with dense dark green mangrove coverage, intricate coastline of bays and estuaries. Center: Golfão Maranhense with São Marcos Bay, showing São Luís island and Alcântara across the bay. East: Oriental coast with white sand dunes transitioning into Lençóis Maranhenses. Bird's eye view, slightly angled. Color palette: deep green for mangroves, deep blue for ocean, beige/white for dunes. Clean editorial style, DK or Monocle atlas quality. Include small icons: scarlet ibis (west), colonial buildings (center), sand dunes (east). No excessive text — labels will be added by designer."
**Estilo**: Cartografia editorial ilustrada (DK / Monocle / National Geographic)
**NÃO incluir**: Grade de coordenadas, estradas, texto definitivo em português

---

---
id: VIS-V05-B
verbete: V05
tipo: infográfico
posicao: meia-página
---

# Visual V05-B: Ciclo da maré — 12 horas no manguezal

## 1. Briefing para designer
**O que é**: Infográfico dividido em duas cenas (díptico) mostrando o mesmo trecho de manguezal na maré alta e na maré baixa. Meia página.
**Dados**:
- MARÉ ALTA: raízes submersas, peixes nos labirintos, garça empoleirada, caranguejos nas tocas, ostras abertas
- MARÉ BAIXA: lodaçal exposto, caranguejos fora das tocas, marisqueiras coletando, maçaricos sondando, ostras fechadas
- Amplitude: até 7m na Baía de São Marcos
- Ciclo: 2× por dia, regido pela lua
- Espécies-chave: mangue-vermelho (raízes-escora), siriúba (pneumatóforos), mangue-branco
**Referência de estilo**: Infográfico tipo corte lateral (Kurzgesagt / National Geographic Kids) — duas cenas lado a lado, mesmo cenário, horários diferentes
**Paleta**: Azul-mar (#1B4F72) para água alta, Verde-mangue (#1E8449) para vegetação, Terracota (#BA4A00) para lama exposta, Dourado (#D4AC0D) para detalhes
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Díptico — esquerda (maré alta, azul dominante, fauna subaquática) e direita (maré baixa, marrom dominante, fauna de superfície + humanos). Mesmo cenário de raízes de mangue em ambos.
**Layout**: Horizontal, duas cenas separadas por linha vertical tracejada

## 3. Prompt para IA generativa
**Prompt**: "Educational diptych infographic showing the same mangrove ecosystem at two different tidal states. LEFT PANEL (High Tide): mangrove roots submerged in murky blue-brown water, fish swimming among the root labyrinth, oysters open on roots, crabs hidden in burrows, a great blue heron perched on a branch above. RIGHT PANEL (Low Tide): same scene but water has receded, exposing dark mud, crabs emerging from burrows, a woman (marisqueira) collecting shellfish knee-deep in mud, shorebirds (maçaricos) probing the mudflat, oysters closed. Cross-section view showing above and below waterline. Clean scientific illustration style, National Geographic quality. Color palette: deep blue and green for high tide, terracotta and brown for low tide. Warm tropical light."
**Estilo**: Infográfico científico-editorial, corte lateral
**NÃO incluir**: Texto definitivo (será inserido em português pelo designer)
