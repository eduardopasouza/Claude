---
id: VIS-V88-A
verbete: V88
tipo: infografico
posicao: meia-pagina
---

# Visual V88-A: A cadeia de valor que falta

## 1. Briefing para designer
**O que e**: Infografico mostrando a cadeia de valor do aluminio e do ferro, destacando quais etapas acontecem no Maranhao (poucas) e quais acontecem fora.
**Dados**: Bauxita (Para) → Alumina (MA) → Aluminio (Canada/Noruega) → Produtos (mundo). Minerio (Para) → Transporte (MA) → Aco (China) → Produtos (mundo). MA aparece apenas nos estagios intermediarios.
**Paleta**: Ocre para etapas no MA, cinza para etapas fora.
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Cadeia aluminio -->
  <text x="50" y="30" fill="#333" font-size="14" font-weight="bold">Cadeia do Aluminio</text>
  <rect x="50" y="50" width="120" height="40" fill="#999" rx="5"/>
  <text x="65" y="75" fill="white" font-size="11">Bauxita (PA)</text>
  <text x="175" y="75" fill="#333" font-size="16">→</text>
  <rect x="200" y="50" width="120" height="40" fill="#C8952E" rx="5"/>
  <text x="215" y="75" fill="white" font-size="11">Alumina (MA)</text>
  <text x="325" y="75" fill="#333" font-size="16">→</text>
  <rect x="350" y="50" width="140" height="40" fill="#999" rx="5"/>
  <text x="355" y="75" fill="white" font-size="11">Aluminio (Canada)</text>
  <text x="495" y="75" fill="#333" font-size="16">→</text>
  <rect x="520" y="50" width="140" height="40" fill="#999" rx="5"/>
  <text x="530" y="75" fill="white" font-size="11">Produtos (mundo)</text>

  <!-- Cadeia ferro -->
  <text x="50" y="150" fill="#333" font-size="14" font-weight="bold">Cadeia do Ferro</text>
  <rect x="50" y="170" width="120" height="40" fill="#999" rx="5"/>
  <text x="60" y="195" fill="white" font-size="11">Minerio (PA)</text>
  <text x="175" y="195" fill="#333" font-size="16">→</text>
  <rect x="200" y="170" width="130" height="40" fill="#C8952E" rx="5"/>
  <text x="205" y="195" fill="white" font-size="11">Transporte (MA)</text>
  <text x="335" y="195" fill="#333" font-size="16">→</text>
  <rect x="360" y="170" width="120" height="40" fill="#999" rx="5"/>
  <text x="375" y="195" fill="white" font-size="11">Aco (China)</text>
  <text x="485" y="195" fill="#333" font-size="16">→</text>
  <rect x="510" y="170" width="140" height="40" fill="#999" rx="5"/>
  <text x="520" y="195" fill="white" font-size="11">Produtos (mundo)</text>

  <!-- Legenda -->
  <rect x="50" y="250" width="20" height="15" fill="#C8952E"/>
  <text x="75" y="263" fill="#333" font-size="11">Etapa no MA</text>
  <rect x="200" y="250" width="20" height="15" fill="#999"/>
  <text x="225" y="263" fill="#333" font-size="11">Etapa fora do MA</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Industrial value chain diagram showing two parallel flows (aluminum and iron ore), with only the middle stages highlighted in ochre gold (representing Maranhao's participation) while upstream and downstream stages are in grey. Clean corporate infographic style, horizontal flow arrows, editorial quality. --ar 16:9 --v 6"

**NAO incluir**: Rostos, logos corporativos.
