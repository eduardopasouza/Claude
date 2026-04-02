---
id: VIS-V20-A
verbete: V20
tipo: infografico-linguistico
posicao: página-inteira
---

# Visual V20-A: As línguas indígenas do Maranhão — árvore linguística

## 1. Briefing para designer
**O que é**: Árvore/diagrama mostrando os dois troncos linguísticos (Tupi e Macro-Jê) e as línguas indígenas vivas no Maranhão. Cada língua com número de falantes e localização.
**Dados**:
- TRONCO TUPI → Família Tupi-Guarani:
  - Tenetehara (Guajajara): ~30.000 falantes — centro MA
  - Ka'apor: ~2.300 falantes — noroeste MA
  - Awá-Guajá: ~350 falantes — noroeste MA (AMEAÇADA)
- TRONCO MACRO-JÊ → Família Jê → Ramo Timbira:
  - Canela (Ramkokamekrá + Apãniekrá): ~3.900 falantes — centro-sul MA
  - Gavião (Pukobiyé): ~900 falantes — centro-sul MA
  - Krikati: ~1.300 falantes — centro-sul MA
- Total: ~38.750 falantes em ~8 línguas
- Código de cor por ameaça: verde (segura), amarelo (vulnerável), vermelho (criticamente ameaçada)
**Referência de estilo**: Árvore filogenética + Kurzgesagt
**Paleta**: Terracota #B5533E (Macro-Jê/Jê), Verde-mata #2D6A4F (Tupi), Vermelho #C23B22 (ameaçada), Ocre #C8952E (tronco), Creme #FAF3E8 (fundo)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 500 550" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="550" fill="#FAF3E8"/>
  <text x="250" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">LÍNGUAS INDÍGENAS DO MARANHÃO</text>
  <!-- Tronco Tupi (esquerda) -->
  <line x1="150" y1="500" x2="150" y2="120" stroke="#2D6A4F" stroke-width="4"/>
  <text x="150" y="520" text-anchor="middle" fill="#2D6A4F" font-size="11" font-weight="bold">TUPI</text>
  <text x="150" y="535" text-anchor="middle" fill="#2D6A4F" font-size="8">Família Tupi-Guarani</text>
  <!-- Ramificações Tupi -->
  <line x1="150" y1="200" x2="60" y2="100" stroke="#2D6A4F" stroke-width="2"/>
  <rect x="10" y="60" width="100" height="40" fill="#2D6A4F" rx="5" opacity="0.8"/>
  <text x="60" y="78" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Tenetehara</text>
  <text x="60" y="92" text-anchor="middle" fill="white" font-size="7">~30.000 falantes</text>
  <line x1="150" y1="250" x2="60" y2="170" stroke="#2D6A4F" stroke-width="2"/>
  <rect x="10" y="145" width="100" height="40" fill="#2D6A4F" rx="5" opacity="0.8"/>
  <text x="60" y="163" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Ka'apor</text>
  <text x="60" y="177" text-anchor="middle" fill="white" font-size="7">~2.300 falantes</text>
  <line x1="150" y1="300" x2="60" y2="240" stroke="#C23B22" stroke-width="2"/>
  <rect x="10" y="220" width="100" height="40" fill="#C23B22" rx="5" opacity="0.9"/>
  <text x="60" y="238" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Awá-Guajá</text>
  <text x="60" y="252" text-anchor="middle" fill="white" font-size="7">~350 ⚠ AMEAÇADA</text>
  <!-- Tronco Macro-Jê (direita) -->
  <line x1="350" y1="500" x2="350" y2="120" stroke="#B5533E" stroke-width="4"/>
  <text x="350" y="520" text-anchor="middle" fill="#B5533E" font-size="11" font-weight="bold">MACRO-JÊ</text>
  <text x="350" y="535" text-anchor="middle" fill="#B5533E" font-size="8">Família Jê → Ramo Timbira</text>
  <!-- Ramificações Jê -->
  <line x1="350" y1="200" x2="440" y2="100" stroke="#B5533E" stroke-width="2"/>
  <rect x="390" y="60" width="100" height="40" fill="#B5533E" rx="5" opacity="0.8"/>
  <text x="440" y="78" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Canela</text>
  <text x="440" y="92" text-anchor="middle" fill="white" font-size="7">~3.900 falantes</text>
  <line x1="350" y1="250" x2="440" y2="170" stroke="#B5533E" stroke-width="2"/>
  <rect x="390" y="145" width="100" height="40" fill="#B5533E" rx="5" opacity="0.8"/>
  <text x="440" y="163" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Krikati</text>
  <text x="440" y="177" text-anchor="middle" fill="white" font-size="7">~1.300 falantes</text>
  <line x1="350" y1="300" x2="440" y2="240" stroke="#B5533E" stroke-width="2"/>
  <rect x="390" y="220" width="100" height="40" fill="#B5533E" rx="5" opacity="0.8"/>
  <text x="440" y="238" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Gavião</text>
  <text x="440" y="252" text-anchor="middle" fill="white" font-size="7">~900 falantes</text>
  <!-- Centro: dados -->
  <text x="250" y="400" text-anchor="middle" font-size="10" fill="#2B2B2B" font-weight="bold">~38.750 falantes</text>
  <text x="250" y="418" text-anchor="middle" font-size="9" fill="#2B2B2B">~8 línguas vivas</text>
  <text x="250" y="436" text-anchor="middle" font-size="8" fill="#2B2B2B">Estado mais diverso linguisticamente do Nordeste</text>
  <!-- Legenda -->
  <rect x="180" y="460" width="10" height="10" fill="#2D6A4F"/>
  <text x="195" y="470" font-size="8" fill="#2B2B2B">Tupi</text>
  <rect x="230" y="460" width="10" height="10" fill="#B5533E"/>
  <text x="245" y="470" font-size="8" fill="#2B2B2B">Macro-Jê</text>
  <rect x="290" y="460" width="10" height="10" fill="#C23B22"/>
  <text x="305" y="470" font-size="8" fill="#2B2B2B">Ameaçada</text>
  <text x="490" y="545" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: Rodrigues, 2002; ISA, 2024; UNESCO, 2023</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Linguistic family tree diagram showing indigenous languages of Maranhão state, Brazil. Two main trunks: TUPI (left, deep green) branching into Tenetehara (30,000 speakers), Ka'apor (2,300), and Awá-Guajá (350, marked as endangered in red). MACRO-JÊ (right, terracotta) branching into Canela (3,900), Krikati (1,300), and Gavião (900). Tree grows upward from bottom. Each language shown as a leaf/node with speaker count. Endangered languages highlighted in red. Central data: ~38,750 total speakers, ~8 living languages. Clean editorial infographic style. Warm cream background. Style: Kurzgesagt meets phylogenetic tree. No photographs."
**Estilo**: Árvore filogenética editorial
**NÃO incluir**: fotografias, representações de pessoas, estilo infantil
