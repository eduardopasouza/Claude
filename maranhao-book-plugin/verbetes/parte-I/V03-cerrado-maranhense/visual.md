---
id: VIS-V03-A
verbete: V03
tipo: infografico
posicao: página-inteira
---

# Visual V03-A: A floresta invertida — corte transversal do Cerrado

## 1. Briefing para designer
**O que é**: Infográfico de corte transversal mostrando uma árvore do Cerrado acima e abaixo do solo. A copa é baixa (5m); as raízes vão a 15m. Comparação lateral com árvore amazônica (copa 30m, raízes 2m). Mensagem visual: o Cerrado é uma floresta invertida.
**Dados**:
- Copa da árvore do Cerrado: 3-5 metros
- Raízes: 10-15 metros de profundidade
- Biomassa subterrânea: 70%+ do total
- Copa de árvore amazônica: 25-35 metros
- Raízes amazônicas: 1-2 metros
- Solo poroso → setas mostrando infiltração de água → lençol freático
**Referência de estilo**: Kurzgesagt — cores vibrantes, sem ruído, dados integrados
**Paleta**: Verde-mata #2D6A4F (vegetação), Ocre #C8952E (solo/cerrado), Azul-mar #1B4965 (água/lençol), Creme #FAF3E8 (fundo)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<!-- SVG esquemático — placeholder para designer -->
<svg viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="600" fill="#FAF3E8"/>
  <text x="250" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">A FLORESTA INVERTIDA</text>
  <!-- Linha do solo -->
  <line x1="0" y1="250" x2="500" y2="250" stroke="#C8952E" stroke-width="3"/>
  <text x="490" y="245" text-anchor="end" font-size="9" fill="#C8952E">nível do solo</text>
  <!-- Árvore do Cerrado — esquerda -->
  <rect x="100" y="200" width="8" height="50" fill="#5C4033"/>
  <circle cx="104" cy="190" r="30" fill="#2D6A4F" opacity="0.8"/>
  <text x="104" y="175" text-anchor="middle" font-size="8" fill="white">5m</text>
  <!-- Raízes do Cerrado -->
  <line x1="104" y1="250" x2="90" y2="500" stroke="#5C4033" stroke-width="2"/>
  <line x1="104" y1="250" x2="118" y2="480" stroke="#5C4033" stroke-width="2"/>
  <line x1="104" y1="250" x2="75" y2="460" stroke="#5C4033" stroke-width="1.5"/>
  <text x="104" y="520" text-anchor="middle" font-size="8" fill="#5C4033">15m de raízes</text>
  <text x="104" y="140" text-anchor="middle" font-size="10" fill="#2B2B2B" font-weight="bold">CERRADO</text>
  <!-- Árvore Amazônica — direita -->
  <rect x="350" y="100" width="12" height="150" fill="#5C4033"/>
  <circle cx="356" cy="80" r="50" fill="#2D6A4F" opacity="0.8"/>
  <text x="356" y="70" text-anchor="middle" font-size="8" fill="white">30m</text>
  <!-- Raízes Amazônicas -->
  <line x1="356" y1="250" x2="340" y2="290" stroke="#5C4033" stroke-width="2"/>
  <line x1="356" y1="250" x2="372" y2="285" stroke="#5C4033" stroke-width="2"/>
  <text x="356" y="305" text-anchor="middle" font-size="8" fill="#5C4033">2m de raízes</text>
  <text x="356" y="25" text-anchor="middle" font-size="10" fill="#2B2B2B" font-weight="bold">AMAZÔNIA</text>
  <!-- Lençol freático -->
  <rect x="0" y="480" width="500" height="120" fill="#1B4965" opacity="0.15"/>
  <text x="250" y="540" text-anchor="middle" font-size="10" fill="#1B4965">LENÇOL FREÁTICO</text>
  <!-- Setas de infiltração -->
  <text x="200" y="350" text-anchor="middle" font-size="8" fill="#1B4965">↓ água infiltra</text>
  <text x="200" y="440" text-anchor="middle" font-size="8" fill="#1B4965">↓ recarga hídrica</text>
  <!-- Fonte -->
  <text x="490" y="590" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: Ab'Sáber, 2003; Haridasan, 2000</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Scientific illustration showing cross-section comparison: Cerrado tree (left) vs Amazonian tree (right). Cerrado: small twisted crown 5m above ground, massive root system extending 15m below ground. Amazon: tall canopy 30m above, shallow roots 2m. Ground level clearly marked. Below ground shows soil layers with water table at 15m depth. Cerrado roots reach the water table. Arrows showing water infiltration. Clean editorial infographic style, warm palette: deep green, golden ochre, cream background. Style: Kurzgesagt meets Nature journal. No photorealism."
**Estilo**: Infográfico científico-editorial
**NÃO incluir**: fotografias, texturas realistas, 3D

---

---
id: VIS-V03-B
verbete: V03
tipo: mapa
posicao: corpo
---

# Visual V03-B: MATOPIBA — a fronteira da soja

## 1. Briefing para designer
**O que é**: Mapa do MATOPIBA mostrando os 4 estados (MA, TO, PI, BA) com área de expansão da soja em destaque. Maranhão em evidência — 33 municípios do sul com ponto em Balsas. Seta logística: Balsas → Ferrovia Carajás → Itaqui.
**Dados**:
- MATOPIBA: 73 milhões de hectares
- MA: 33 municípios, 3,2 mi ha de soja, 10,8 mi ton/ano
- Rota: Balsas → EF Carajás → Terminal Itaqui → exportação
- 49,9% do Cerrado nacional desmatado
**Referência de estilo**: Bloomberg/Reuters data maps
**Paleta**: Ocre #C8952E (Cerrado/soja), Verde-mata #2D6A4F (vegetação remanescente), Vermelho-bumba #C23B22 (desmatamento), Creme #FAF3E8 (fundo)
**Tamanho**: Meia página

## 2. Prompt para IA generativa
**Prompt**: "Editorial map of MATOPIBA region in Brazil highlighting four states: Maranhão, Tocantins, Piauí, Bahia. Soybean expansion area shown in golden ochre overlay. Maranhão's 33 southern municipalities highlighted. City of Balsas marked as epicenter. Logistic route shown: Balsas to Carajás Railway to Port of Itaqui in São Luís. Small inset showing Brazil with MATOPIBA region highlighted. Clean data-journalism style. Warm cream background, ochre and green palette. Style: Bloomberg visual journalism meets Kurzgesagt warmth."
**Estilo**: Mapa de dados jornalístico
**NÃO incluir**: fotografias, relevo detalhado, excesso de rótulos
