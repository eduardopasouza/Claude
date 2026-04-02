---
id: VIS-V08-A
verbete: V08
tipo: mapa-hidrográfico
posicao: página-inteira
---

# Visual V08-A: As 12 bacias do Maranhão — o telhado e a calha

## 1. Briefing para designer
**O que é**: Mapa hidrográfico do Maranhão mostrando as 12 bacias, com rios principais nomeados e setas indicando direção do fluxo (predominantemente S→N). Baixada Maranhense destacada como zona de inundação sazonal.
**Dados**:
- 12 bacias: Itapecuru, Mearim, Pindaré, Grajaú, Parnaíba, Gurupi, Turiaçu, Tocantins, Munim, Pericumã, Maracaçumé, Preguiças
- Rios principais com extensão
- Setas S→N indicando direção do fluxo
- Baixada Maranhense: hachura azul (zona de inundação)
- Nascentes no Cerrado (pontos de origem)
- São Luís e foz do Itapecuru marcados
**Referência de estilo**: Kurzgesagt + atlas hidrográfico
**Paleta**: Azul-mar #1B4965 (rios), Verde-mata #2D6A4F (Cerrado/nascentes), Azul-claro #87CEEB (Baixada/lagos), Creme #FAF3E8 (fundo), Ocre #C8952E (relevo)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 450 550" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="550" fill="#FAF3E8"/>
  <text x="225" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">AS 12 BACIAS — O TELHADO E A CALHA</text>
  <!-- Contorno do estado (simplificado) -->
  <rect x="40" y="40" width="370" height="460" fill="#F5ECD7" rx="15" stroke="#2B2B2B" stroke-width="1"/>
  <!-- Cerrado (nascentes - sul) -->
  <rect x="40" y="340" width="370" height="160" fill="#C8952E" rx="0 0 15 15" opacity="0.15"/>
  <text x="225" y="490" text-anchor="middle" fill="#C8952E" font-size="10" font-style="italic">CERRADO — nascentes</text>
  <!-- Baixada (centro-norte) -->
  <ellipse cx="200" cy="180" rx="120" ry="60" fill="#87CEEB" opacity="0.3"/>
  <text x="200" y="185" text-anchor="middle" fill="#1B4965" font-size="9">BAIXADA MARANHENSE</text>
  <!-- Atlântico (norte) -->
  <rect x="40" y="35" width="370" height="30" fill="#1B4965" opacity="0.15"/>
  <text x="225" y="55" text-anchor="middle" fill="#1B4965" font-size="9">ATLÂNTICO</text>
  <!-- Rios com setas S→N -->
  <line x1="250" y1="450" x2="250" y2="70" stroke="#1B4965" stroke-width="2.5"/>
  <text x="260" y="260" fill="#1B4965" font-size="9" font-weight="bold">Itapecuru</text>
  <polygon points="250,70 245,85 255,85" fill="#1B4965"/>
  <line x1="180" y1="470" x2="170" y2="80" stroke="#1B4965" stroke-width="2"/>
  <text x="150" y="300" fill="#1B4965" font-size="8">Mearim</text>
  <polygon points="170,80 165,95 175,95" fill="#1B4965"/>
  <line x1="120" y1="430" x2="130" y2="100" stroke="#1B4965" stroke-width="1.5"/>
  <text x="95" y="270" fill="#1B4965" font-size="8">Pindaré</text>
  <line x1="150" y1="440" x2="155" y2="140" stroke="#1B4965" stroke-width="1.5"/>
  <text x="125" y="350" fill="#1B4965" font-size="8">Grajaú</text>
  <!-- Rios-fronteira -->
  <line x1="400" y1="480" x2="400" y2="50" stroke="#1B4965" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="415" y="260" fill="#1B4965" font-size="8" writing-mode="tb">Parnaíba</text>
  <line x1="50" y1="300" x2="50" y2="50" stroke="#1B4965" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="30" y="175" fill="#1B4965" font-size="7" writing-mode="tb">Gurupi</text>
  <!-- São Luís -->
  <circle cx="280" cy="60" r="5" fill="#C23B22"/>
  <text x="290" y="58" fill="#2B2B2B" font-size="8" font-weight="bold">São Luís</text>
  <!-- Legenda -->
  <line x1="50" y1="520" x2="70" y2="520" stroke="#1B4965" stroke-width="2"/>
  <text x="75" y="524" font-size="8" fill="#2B2B2B">Rio principal</text>
  <line x1="150" y1="520" x2="170" y2="520" stroke="#1B4965" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="175" y="524" font-size="8" fill="#2B2B2B">Rio-fronteira</text>
  <ellipse cx="280" cy="520" rx="15" ry="6" fill="#87CEEB" opacity="0.4"/>
  <text x="300" y="524" font-size="8" fill="#2B2B2B">Baixada (inundável)</text>
  <text x="430" y="545" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: ANA, NuGeo-UEMA, 2022</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Hydrographic map of Maranhão state showing 12 river basins flowing predominantly from south to north. Major rivers labeled: Itapecuru, Mearim, Pindaré, Grajaú, Turiaçu. Border rivers: Parnaíba (east), Gurupi (northwest), Tocantins (south). Arrows showing S-to-N flow direction. Cerrado highlands in south shown in subtle ochre (watershed origin). Baixada Maranhense in center-north shown in pale blue (seasonal flood zone). Atlantic Ocean at top. São Luís marked in red. Clean editorial cartographic style. Warm cream background. Style: Kurzgesagt meets National Geographic hydrographic atlas. No photorealism, data-rich."
**Estilo**: Mapa hidrográfico editorial
**NÃO incluir**: fotografias, relevo 3D, excesso de rótulos menores

---

---
id: VIS-V08-B
verbete: V08
tipo: comparativo
posicao: corpo
---

# Visual V08-B: Baixada Maranhense — cheia vs. seca

## 1. Briefing para designer
**O que é**: Duas imagens lado a lado (ou sobrepostas com slider) da Baixada Maranhense: janeiro (cheia) e julho (seca). Mesma área, duas paisagens radicalmente diferentes.
**Dados**:
- Janeiro: campos inundados, 700 lagos visíveis, azul dominante
- Julho: campos secos, lagos reduzidos, verde/marrom dominante
- Área: ~20.000 km²
- Escala temporal: 6 meses de diferença
**Referência de estilo**: NASA Earth Observatory before/after
**Paleta**: Azul (cheia) vs. Verde-ocre (seca). Moldura em Creme.
**Tamanho**: Meia página (dois frames lado a lado)

## 2. Prompt para IA generativa
**Prompt**: "Split comparison illustration of Baixada Maranhense region. LEFT (January/wet season): landscape filled with interconnected lakes, flooded fields, water buffaloes in shallow water, fishing canoes, lush green. RIGHT (July/dry season): same landscape with lakes mostly gone, exposed dry grassland, cattle grazing, cracked earth at edges. Same geographic footprint, radically different landscape. Clean editorial illustration style. Labels: 'Janeiro — Cheia' and 'Julho — Seca'. Warm palette. Style: Kurzgesagt meets scientific illustration. No photorealism."
**Estilo**: Comparativo sazonal
**NÃO incluir**: fotografias de satélite reais (usar ilustração estilizada)
