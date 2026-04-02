---
id: VIS-V12-A
verbete: V12
tipo: mapa-delta
posicao: página-inteira
---

# Visual V12-A: O delta do Parnaíba — os cinco braços

## 1. Briefing para designer
**O que é**: Mapa do delta do Parnaíba visto de cima mostrando os 5 braços do rio se abrindo em leque, as 73 ilhas, e a divisão MA/PI. Manguezais em verde, água em azul, dunas em ocre. Guarás estilizados.
**Dados**:
- 5 braços: Igaraçu, Santa Rosa, Melancieira, Caju, Tutóia (de leste a oeste)
- 73 ilhas (maior: Ilha Grande de Santa Isabel)
- Margem esquerda: MA (Araioses, Tutóia)
- Margem direita: PI (Parnaíba, Luís Correia)
- Área: ~2.700 km²
- Manguezais entre os braços
- Oceano Atlântico ao norte
**Referência de estilo**: Kurzgesagt + National Geographic delta maps
**Paleta**: Azul-mar #1B4965 (rio/mar), Verde-mata #2D6A4F (manguezal), Ocre #C8952E (dunas/areia), Vermelho-bumba #C23B22 (guarás), Creme #FAF3E8 (fundo)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="500" fill="#FAF3E8"/>
  <text x="250" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">DELTA DO PARNAÍBA — OS CINCO BRAÇOS</text>
  <!-- Oceano Atlântico -->
  <rect x="0" y="30" width="500" height="120" fill="#1B4965" opacity="0.2"/>
  <text x="250" y="80" text-anchor="middle" fill="#1B4965" font-size="11">OCEANO ATLÂNTICO</text>
  <!-- Rio Parnaíba vindo do sul -->
  <line x1="250" y1="480" x2="250" y2="300" stroke="#1B4965" stroke-width="6"/>
  <text x="265" y="450" fill="#1B4965" font-size="9" font-weight="bold">Parnaíba</text>
  <!-- 5 braços se abrindo -->
  <line x1="250" y1="300" x2="100" y2="140" stroke="#1B4965" stroke-width="3"/>
  <text x="80" y="155" fill="#1B4965" font-size="7">Tutóia</text>
  <line x1="250" y1="300" x2="170" y2="140" stroke="#1B4965" stroke-width="3"/>
  <text x="155" y="155" fill="#1B4965" font-size="7">Caju</text>
  <line x1="250" y1="300" x2="250" y2="140" stroke="#1B4965" stroke-width="3"/>
  <text x="255" y="155" fill="#1B4965" font-size="7">Melancieira</text>
  <line x1="250" y1="300" x2="330" y2="140" stroke="#1B4965" stroke-width="3"/>
  <text x="320" y="155" fill="#1B4965" font-size="7">Santa Rosa</text>
  <line x1="250" y1="300" x2="400" y2="140" stroke="#1B4965" stroke-width="3"/>
  <text x="395" y="155" fill="#1B4965" font-size="7">Igaraçu</text>
  <!-- Ilhas (manguezal) entre braços -->
  <ellipse cx="135" cy="220" rx="30" ry="40" fill="#2D6A4F" opacity="0.5"/>
  <ellipse cx="210" cy="200" rx="35" ry="50" fill="#2D6A4F" opacity="0.5"/>
  <ellipse cx="290" cy="210" rx="40" ry="45" fill="#2D6A4F" opacity="0.5"/>
  <ellipse cx="365" cy="200" rx="30" ry="40" fill="#2D6A4F" opacity="0.5"/>
  <!-- Ilha Grande -->
  <ellipse cx="320" cy="220" rx="50" ry="30" fill="#2D6A4F" opacity="0.3" stroke="#2D6A4F" stroke-width="1"/>
  <text x="320" y="225" text-anchor="middle" fill="white" font-size="7">Ilha Grande de Santa Isabel</text>
  <!-- Guarás estilizados -->
  <text x="180" y="190" font-size="10" fill="#C23B22">●●●</text>
  <text x="178" y="180" fill="#C23B22" font-size="6">guarás</text>
  <!-- Labels MA/PI -->
  <text x="80" y="350" fill="#2B2B2B" font-size="10" font-style="italic">MARANHÃO</text>
  <text x="350" y="350" fill="#2B2B2B" font-size="10" font-style="italic">PIAUÍ</text>
  <!-- Cidades -->
  <circle cx="70" cy="250" r="3" fill="#2B2B2B"/>
  <text x="50" y="265" fill="#2B2B2B" font-size="7">Tutóia</text>
  <circle cx="420" cy="250" r="3" fill="#2B2B2B"/>
  <text x="405" y="265" fill="#2B2B2B" font-size="7">Parnaíba</text>
  <!-- Dados -->
  <text x="250" y="475" text-anchor="middle" font-size="9" fill="#2B2B2B">73 ilhas • 2.700 km² • 5 braços • 1 dos 3 deltas em mar aberto do mundo</text>
  <text x="490" y="495" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: ANA, IBGE, ICMBio, 2022</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Aerial view illustration of Parnaíba River Delta showing the river splitting into five branches (labeled: Igaraçu, Santa Rosa, Melancieira, Caju, Tutóia) as it reaches the Atlantic Ocean. Islands between the branches covered in mangrove forest (deep green). Sandy dunes in ochre on outer islands. Scarlet ibis (guarás) shown as red dots on mangroves. Labels: MARANHÃO on left bank, PIAUÍ on right bank. Atlantic Ocean at top. Clean editorial cartographic style. 73 islands visible. Warm cream background. Style: Kurzgesagt aerial map meets National Geographic delta illustration. No photorealism."
**Estilo**: Mapa aéreo editorial do delta
**NÃO incluir**: fotografias de satélite reais, excesso de topônimos
