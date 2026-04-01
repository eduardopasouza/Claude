---
id: VIS-V37-A
verbete: V37
tipo: mapa
posicao: corpo
---

# Visual V37-A: Mapa das Terras de Preto, de Santo e de Indio no Maranhao

## 1. Briefing para designer
**O que e**: Mapa tematico do Maranhao mostrando a distribuicao das tres categorias de posse coletiva da terra. Tres camadas de informacao (Terras de Preto, Terras de Santo, Terras de Indio) representadas por cores distintas mas harmonizadas dentro da paleta roxo-tambor.
**Dados**:
- 868 comunidades quilombolas certificadas (FCP 2024) — concentradas em: Alcantara, Penalva, Pinheiro, Turiacu, Cururupu, Guimaraes, Codo, Serrano, regiao do Baixo Parnaiba
- Terras de Santo: vale do Itapecuru, Baixada Maranhense, Alcantara (documentacao dispersa, sem numero exato consolidado)
- Terras de Indio: sobreposicao parcial com TIs demarcadas — Guajajara (centro-oeste MA), Ka'apor (noroeste), Krenye, Krikati (sudoeste)
- Destaque: Serrano/MA (58,5% preto — maior do Brasil)
**Referencia de estilo**: Mapa limpo, esquematico, sem excesso de detalhe topografico. Inspiraçao nos mapas do Projeto Nova Cartografia Social da Amazonia (PNCSA)
**Paleta**:
- Terras de Preto: #5E3A7E (roxo-tambor) — cor principal
- Terras de Santo: #C8952E (ocre) — pontos ou areas
- Terras de Indio: #2D6A4F (verde-mata) — areas hachuradas
- Fundo do mapa: #FAF3E8 (creme)
- Linhas e textos: #2B2B2B (carvao)
- Destaque Serrano: circulo vermelho-bumba #C1292E com callout
**Tamanho**: Pagina inteira (23x28cm)

## 2. SVG simplificado
**Elementos**:
- Contorno do Maranhao (forma simplificada)
- Pontos/clusters para Terras de Preto (concentrados no litoral norte, Baixada, vale do Itapecuru)
- Marcadores para Terras de Santo (triangulos ocre no vale do Itapecuru e Alcantara)
- Areas hachuradas para Terras de Indio (centro-oeste e noroeste)
- Callout para Serrano com dado "58,5% preta"
- Legenda com tres cores
- Titulo: "Tres formas de pertencer a terra"
**Layout**: Mapa centralizado, legenda no canto inferior esquerdo, callout de Serrano no canto direito
**Cores**: #5E3A7E, #C8952E, #2D6A4F, #FAF3E8, #2B2B2B, #C1292E

```svg
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="800" height="600" fill="#FAF3E8"/>

  <!-- Titulo -->
  <text x="400" y="40" text-anchor="middle" font-family="serif" font-size="22" fill="#2B2B2B" font-weight="bold">Tres formas de pertencer a terra</text>
  <text x="400" y="62" text-anchor="middle" font-family="serif" font-size="14" fill="#5E3A7E">Terras de Preto, de Santo e de Indio no Maranhao</text>

  <!-- Contorno simplificado do MA -->
  <path d="M250,100 L450,80 L550,120 L580,200 L560,350 L500,450 L400,500 L300,480 L220,400 L200,300 L210,200 Z"
        fill="#F5EDE0" stroke="#2B2B2B" stroke-width="2"/>

  <!-- Terras de Preto — pontos roxos (litoral norte, Baixada, Itapecuru) -->
  <circle cx="320" cy="150" r="8" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="350" cy="170" r="6" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="300" cy="180" r="7" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="340" cy="200" r="5" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="280" cy="220" r="6" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="360" cy="230" r="8" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="310" cy="260" r="5" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="400" cy="190" r="6" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="430" cy="210" r="5" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="370" cy="280" r="7" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="450" cy="300" r="6" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="340" cy="320" r="5" fill="#5E3A7E" opacity="0.7"/>

  <!-- Terras de Santo — triangulos ocre (Itapecuru, Alcantara) -->
  <polygon points="350,155 356,168 344,168" fill="#C8952E"/>
  <polygon points="380,210 386,223 374,223" fill="#C8952E"/>
  <polygon points="310,190 316,203 304,203" fill="#C8952E"/>
  <polygon points="420,250 426,263 414,263" fill="#C8952E"/>

  <!-- Terras de Indio — areas hachuradas verdes (centro-oeste, noroeste) -->
  <ellipse cx="280" cy="350" rx="50" ry="60" fill="#2D6A4F" opacity="0.25" stroke="#2D6A4F" stroke-width="1.5" stroke-dasharray="6,3"/>
  <ellipse cx="260" cy="200" rx="35" ry="45" fill="#2D6A4F" opacity="0.25" stroke="#2D6A4F" stroke-width="1.5" stroke-dasharray="6,3"/>

  <!-- Destaque Serrano -->
  <circle cx="400" cy="340" r="12" fill="none" stroke="#C1292E" stroke-width="3"/>
  <line x1="412" y1="340" x2="560" y2="320" stroke="#C1292E" stroke-width="1.5"/>
  <rect x="560" y="305" width="200" height="45" rx="5" fill="#C1292E" opacity="0.1" stroke="#C1292E" stroke-width="1"/>
  <text x="660" y="322" text-anchor="middle" font-family="serif" font-size="12" fill="#C1292E" font-weight="bold">SERRANO</text>
  <text x="660" y="340" text-anchor="middle" font-family="serif" font-size="11" fill="#2B2B2B">58,5% preta — maior do Brasil</text>

  <!-- Sao Luis -->
  <circle cx="370" cy="130" r="5" fill="#2B2B2B"/>
  <text x="385" y="128" font-family="serif" font-size="11" fill="#2B2B2B">Sao Luis</text>

  <!-- Legenda -->
  <rect x="50" y="460" width="280" height="120" rx="8" fill="#FAF3E8" stroke="#2B2B2B" stroke-width="1"/>
  <text x="70" y="485" font-family="serif" font-size="13" fill="#2B2B2B" font-weight="bold">Legenda</text>

  <circle cx="80" cy="505" r="7" fill="#5E3A7E" opacity="0.7"/>
  <text x="100" y="510" font-family="serif" font-size="11" fill="#2B2B2B">Terras de Preto (comunidades quilombolas)</text>

  <polygon points="80,528 86,541 74,541" fill="#C8952E"/>
  <text x="100" y="537" font-family="serif" font-size="11" fill="#2B2B2B">Terras de Santo (ordens religiosas)</text>

  <ellipse cx="80" cy="560" rx="10" ry="7" fill="#2D6A4F" opacity="0.25" stroke="#2D6A4F" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="100" y="564" font-family="serif" font-size="11" fill="#2B2B2B">Terras de Indio (ocupacao originaria)</text>

  <!-- Fonte -->
  <text x="400" y="590" text-anchor="middle" font-family="serif" font-size="9" fill="#888">Fontes: FCP 2024, PNCSA 2005-2015, IBGE 2022. Localizacao esquematica.</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Aerial view of a rural quilombola community in Maranhao, Brazil. Small houses with terracotta roofs scattered around an old colonial chapel with whitewashed walls, surrounded by babassu palm trees and green fields. Warm late afternoon light, golden hour. The landscape shows the transition between cerrado and tropical forest. A red dirt road connects the houses. Style: painterly, warm earth tones with purple and ochre accents, documentary photography aesthetic with artistic treatment. No text, no people visible."
**Estilo**: Fotografia documental com tratamento artistico, tons terrosos quentes
**Referencia**: Fotografias de Joao Roberto Ripper (comunidades tradicionais brasileiras), mescladas com estetica de livro coffee table
**NAO incluir**: Texto sobreposto, pessoas reconheciveis, estetica turistica, estereotipos de pobreza

---

---
id: VIS-V37-B
verbete: V37
tipo: diagrama
posicao: corpo
---

# Visual V37-B: Timeline — Da sesmaria ao titulo (ou a falta dele)

## 1. Briefing para designer
**O que e**: Timeline horizontal mostrando a evolucao do regime fundiario no Brasil e seus efeitos sobre comunidades tradicionais do Maranhao. De 1530 (sesmarias) a 2003 (Decreto 4.887), com destaques ironicos nos pontos de inflexao.
**Dados**:
- 1530: Regime de sesmarias (terra distribuida pela Coroa)
- 1759: Expulsao dos jesuitas (origem das Terras de Santo)
- 1850: Lei de Terras (terra so por compra)
- 1888: Abolicao (liberdade sem terra)
- 1988: CF art. 68 ADCT (reconhecimento quilombola)
- 2003: Decreto 4.887 (regulamentacao da titulacao)
- 2024: 868 comunidades certificadas, ~40 tituladas
**Referencia de estilo**: Timeline limpa, horizontal, com marcadores verticais. Ironia visual: a barra de "tempo sem protecao" (1850-1988) deve ser visualmente dominante.
**Paleta**: Roxo-tambor (#5E3A7E) para marcos positivos, vermelho-bumba (#C1292E) para marcos negativos, carvao (#2B2B2B) para texto, creme (#FAF3E8) fundo
**Tamanho**: Meia pagina horizontal (23x14cm)

## 2. SVG simplificado
**Elementos**: Linha horizontal com marcos, textos curtos, setas
**Layout**: Da esquerda (1530) para direita (2024), com espaco proporcional ao tempo

```svg
<svg viewBox="0 0 900 250" xmlns="http://www.w3.org/2000/svg">
  <rect width="900" height="250" fill="#FAF3E8"/>

  <text x="450" y="25" text-anchor="middle" font-family="serif" font-size="16" fill="#2B2B2B" font-weight="bold">Da sesmaria ao titulo (ou a falta dele)</text>

  <!-- Linha principal -->
  <line x1="50" y1="120" x2="850" y2="120" stroke="#2B2B2B" stroke-width="2"/>

  <!-- Barra de exclusao 1850-1988 -->
  <rect x="370" y="110" width="350" height="20" fill="#C1292E" opacity="0.15"/>
  <text x="545" y="105" text-anchor="middle" font-family="serif" font-size="9" fill="#C1292E">138 anos sem protecao</text>

  <!-- 1530 -->
  <line x1="80" y1="100" x2="80" y2="140" stroke="#5E3A7E" stroke-width="2"/>
  <text x="80" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#5E3A7E" font-weight="bold">1530</text>
  <text x="80" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#2B2B2B">Sesmarias</text>
  <text x="80" y="172" text-anchor="middle" font-family="serif" font-size="8" fill="#888">(posse por uso)</text>

  <!-- 1759 -->
  <line x1="250" y1="100" x2="250" y2="140" stroke="#C8952E" stroke-width="2"/>
  <text x="250" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#C8952E" font-weight="bold">1759</text>
  <text x="250" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#2B2B2B">Expulsao</text>
  <text x="250" y="172" text-anchor="middle" font-family="serif" font-size="9" fill="#2B2B2B">dos jesuitas</text>
  <text x="250" y="184" text-anchor="middle" font-family="serif" font-size="8" fill="#888">(nasce Terra de Santo)</text>

  <!-- 1850 -->
  <line x1="370" y1="100" x2="370" y2="140" stroke="#C1292E" stroke-width="3"/>
  <text x="370" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#C1292E" font-weight="bold">1850</text>
  <text x="370" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#C1292E">Lei de Terras</text>
  <text x="370" y="172" text-anchor="middle" font-family="serif" font-size="8" fill="#C1292E">(so por compra)</text>

  <!-- 1888 -->
  <line x1="440" y1="100" x2="440" y2="140" stroke="#C1292E" stroke-width="2"/>
  <text x="440" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#C1292E" font-weight="bold">1888</text>
  <text x="440" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#2B2B2B">Abolicao</text>
  <text x="440" y="172" text-anchor="middle" font-family="serif" font-size="8" fill="#888">(liberdade sem terra)</text>

  <!-- 1988 -->
  <line x1="720" y1="100" x2="720" y2="140" stroke="#5E3A7E" stroke-width="2"/>
  <text x="720" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#5E3A7E" font-weight="bold">1988</text>
  <text x="720" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#2B2B2B">CF art. 68</text>
  <text x="720" y="172" text-anchor="middle" font-family="serif" font-size="8" fill="#888">(quilombos reconhecidos)</text>

  <!-- 2003 -->
  <line x1="780" y1="100" x2="780" y2="140" stroke="#5E3A7E" stroke-width="2"/>
  <text x="780" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#5E3A7E" font-weight="bold">2003</text>
  <text x="780" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#2B2B2B">Decreto 4.887</text>
  <text x="780" y="172" text-anchor="middle" font-family="serif" font-size="8" fill="#888">(regulamentacao)</text>

  <!-- 2024 -->
  <line x1="840" y1="100" x2="840" y2="140" stroke="#C1292E" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="840" y="90" text-anchor="middle" font-family="serif" font-size="10" fill="#C1292E" font-weight="bold">2024</text>
  <text x="840" y="160" text-anchor="middle" font-family="serif" font-size="9" fill="#C1292E">868 certificadas</text>
  <text x="840" y="172" text-anchor="middle" font-family="serif" font-size="8" fill="#C1292E">~40 tituladas</text>

  <!-- Nota ironica -->
  <text x="450" y="220" text-anchor="middle" font-family="serif" font-size="10" fill="#5E3A7E" font-style="italic">"Trinta e sete palavras na Constituicao. Trinta e sete anos depois, quarenta titulos."</text>

  <!-- Fonte -->
  <text x="450" y="245" text-anchor="middle" font-family="serif" font-size="8" fill="#888">Fontes: Legislacao brasileira, FCP 2024, INCRA 2023.</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Abstract artistic timeline showing the history of land rights in Maranhao, Brazil. Left side shows organic, natural land with communal farming, babassu palms, and community life. Center shows a sharp dividing line (representing the 1850 Land Law) with legal documents and barriers. Right side shows modern bureaucratic obstacles contrasting with resilient communities. Color palette: deep purple (#5E3A7E), ochre (#C8952E), earth tones, cream background. Style: editorial illustration, sophisticated, slightly surrealist, inspired by Brazilian social art. No text."
**Estilo**: Ilustracao editorial, sofisticada, levemente surrealista
**Referencia**: Ilustracoes de Noma Bar (minimalismo conceitual) mescladas com arte social brasileira (Portinari, sem ser literal)
**NAO incluir**: Texto, estereotipos raciais, estetica de vitimizacao, excesso de realismo fotografico
