---
id: VIS-V94-A
verbete: V94
tipo: infografico
posicao: pagina-inteira
---

# Visual V94-A: O painel dos numeros — MA vs. Brasil

## 1. Briefing para designer
**O que e**: Dashboard de pagina inteira com 8-10 indicadores sociais e economicos do Maranhao comparados com a media brasileira. Cada indicador aparece como barra horizontal dupla (MA em vermelho, Brasil em cinza). Os indicadores: IDH, PIB per capita, esgoto tratado (%), analfabetismo (%), mortalidade infantil (por mil), esperanca de vida, pobreza (%), Gini, trabalho informal (%), acesso a internet (%). Fundo escuro (Carvao), dados negativos em Vermelho-bumba, dados positivos (onde MA se destaca) em Verde-mata. Titulo: "MARANHAO vs. BRASIL: O PAINEL".
**Dados**: Todos os valores da tabela do texto (ver research.md para numeros exatos).
**Referencia de estilo**: Dashboard tipo The Economist / Financial Times — limpo, sem decoração, dados puros. Sem icones fofos. Sem emojis. Tipografia forte.
**Paleta**: Fundo Carvao (#2B2B2B). Texto branco (#FFFFFF). Barras MA: Vermelho-bumba (#C1292E). Barras Brasil: cinza medio (#888888). Destaques positivos: Verde-mata (#2D6A4F).
**Tamanho**: Pagina inteira (23x28cm)

## 2. SVG simplificado
**Elementos**: Barras horizontais pareadas, rotulos a esquerda, valores a direita
**Layout**: Titulo no topo, 8 pares de barras empilhados verticalmente, fonte na base
**Cores**: Fundo #2B2B2B, barras #C1292E e #888888, texto #FFFFFF

```svg
<svg viewBox="0 0 800 1000" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="1000" fill="#2B2B2B"/>
  <text x="400" y="50" text-anchor="middle" font-size="26" fill="#FFFFFF" font-weight="bold">MARANHAO vs. BRASIL: O PAINEL</text>
  <text x="400" y="80" text-anchor="middle" font-size="14" fill="#888888">Fontes: IBGE, PNUD, SNIS, DataSUS | 2021-2022</text>
  <!-- Legenda -->
  <rect x="250" y="95" width="20" height="12" fill="#C1292E"/>
  <text x="275" y="106" font-size="12" fill="#FFFFFF">Maranhao</text>
  <rect x="400" y="95" width="20" height="12" fill="#888888"/>
  <text x="425" y="106" font-size="12" fill="#FFFFFF">Brasil</text>
  <!-- IDH -->
  <text x="30" y="155" font-size="14" fill="#FFFFFF" font-weight="bold">IDH</text>
  <rect x="180" y="140" width="338" height="18" fill="#C1292E" rx="3"/>
  <text x="525" y="155" font-size="13" fill="#C1292E">0,676</text>
  <rect x="180" y="162" width="377" height="18" fill="#888888" rx="3"/>
  <text x="565" y="177" font-size="13" fill="#888888">0,754</text>
  <!-- PIB per capita -->
  <text x="30" y="220" font-size="14" fill="#FFFFFF" font-weight="bold">PIB per capita</text>
  <rect x="180" y="205" width="155" height="18" fill="#C1292E" rx="3"/>
  <text x="342" y="220" font-size="13" fill="#C1292E">R$ 15.757</text>
  <rect x="180" y="227" width="400" height="18" fill="#888888" rx="3"/>
  <text x="587" y="242" font-size="13" fill="#888888">R$ 40.688</text>
  <!-- Esgoto -->
  <text x="30" y="285" font-size="14" fill="#FFFFFF" font-weight="bold">Esgoto tratado</text>
  <rect x="180" y="270" width="31" height="18" fill="#C1292E" rx="3"/>
  <text x="218" y="285" font-size="13" fill="#C1292E">3,9%</text>
  <rect x="180" y="292" width="410" height="18" fill="#888888" rx="3"/>
  <text x="597" y="307" font-size="13" fill="#888888">51,2%</text>
  <!-- Analfabetismo -->
  <text x="30" y="350" font-size="14" fill="#FFFFFF" font-weight="bold">Analfabetismo</text>
  <rect x="180" y="335" width="312" height="18" fill="#C1292E" rx="3"/>
  <text x="499" y="350" font-size="13" fill="#C1292E">15,6%</text>
  <rect x="180" y="357" width="112" height="18" fill="#888888" rx="3"/>
  <text x="299" y="372" font-size="13" fill="#888888">5,6%</text>
  <!-- Mortalidade infantil -->
  <text x="30" y="415" font-size="14" fill="#FFFFFF" font-weight="bold">Mort. infantil</text>
  <rect x="180" y="400" width="304" height="18" fill="#C1292E" rx="3"/>
  <text x="491" y="415" font-size="13" fill="#C1292E">15,2/mil</text>
  <rect x="180" y="422" width="238" height="18" fill="#888888" rx="3"/>
  <text x="425" y="437" font-size="13" fill="#888888">11,9/mil</text>
  <!-- Esperanca de vida -->
  <text x="30" y="480" font-size="14" fill="#FFFFFF" font-weight="bold">Esperanca vida</text>
  <rect x="180" y="465" width="357" height="18" fill="#C1292E" rx="3"/>
  <text x="544" y="480" font-size="13" fill="#C1292E">71,4 anos</text>
  <rect x="180" y="487" width="378" height="18" fill="#888888" rx="3"/>
  <text x="565" y="502" font-size="13" fill="#888888">75,5 anos</text>
  <!-- Pobreza -->
  <text x="30" y="545" font-size="14" fill="#FFFFFF" font-weight="bold">Pobreza</text>
  <rect x="180" y="530" width="400" height="18" fill="#C1292E" rx="3"/>
  <text x="587" y="545" font-size="13" fill="#C1292E">~50%</text>
  <rect x="180" y="552" width="232" height="18" fill="#888888" rx="3"/>
  <text x="419" y="567" font-size="13" fill="#888888">~29%</text>
  <!-- Separador -->
  <line x1="30" y1="600" x2="770" y2="600" stroke="#888888" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="400" y="625" text-anchor="middle" font-size="12" fill="#888888">MAS TAMBEM:</text>
  <!-- Porto -->
  <text x="30" y="665" font-size="14" fill="#FFFFFF" font-weight="bold">Porto de Itaqui</text>
  <rect x="180" y="650" width="460" height="18" fill="#2D6A4F" rx="3"/>
  <text x="647" y="665" font-size="13" fill="#2D6A4F">2o maior do Brasil</text>
  <!-- Energia -->
  <text x="30" y="710" font-size="14" fill="#FFFFFF" font-weight="bold">Energia</text>
  <rect x="180" y="695" width="400" height="18" fill="#2D6A4F" rx="3"/>
  <text x="587" y="710" font-size="13" fill="#2D6A4F">Superavitario</text>
  <!-- Nota final -->
  <text x="400" y="780" text-anchor="middle" font-size="16" fill="#FFFFFF" font-weight="bold">O paradoxo e este: os dados de cima e os de baixo</text>
  <text x="400" y="800" text-anchor="middle" font-size="16" fill="#FFFFFF" font-weight="bold">sao do mesmo estado.</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Minimalist data dashboard infographic with dark charcoal background. Eight horizontal bar chart pairs comparing Maranhao state (red bars) versus Brazil national average (gray bars) across social indicators: HDI, GDP per capita, sewage coverage, illiteracy, infant mortality, life expectancy, poverty rate, inequality index. Clean sans-serif typography. Two positive indicators at bottom in green (port ranking, energy surplus). Style: The Economist, Financial Times data visualization. No decorative elements. Pure data. 23x28cm vertical format."
**Estilo**: Visualizacao de dados editorial — The Economist / FT
**Referencia**: Financial Times Big Read infographics; Our World in Data
**NAO incluir**: fotografias, icones decorativos, emojis, imagens de pessoas, imagens de pobreza

---

---
id: VIS-V94-B
verbete: V94
tipo: infografico
posicao: corpo
---

# Visual V94-B: Arco de melhoria 2000-2022

## 1. Briefing para designer
**O que e**: Grafico de linhas mostrando a evolucao de 3 indicadores do Maranhao vs. Brasil ao longo de 22 anos (2000-2022). Indicadores: IDH (subiu), analfabetismo (caiu), mortalidade infantil (caiu). Para cada indicador, duas linhas: MA (vermelho) e Brasil (cinza). O grafico mostra convergencia lenta — MA melhora mais rapido, mas parte de base muito mais baixa. Anotacoes nos pontos-chave (2003: inicio Bolsa Familia; 2010: marco SUS; 2022: dado mais recente).
**Dados**: IDH MA 2000: 0,476 → 2010: 0,639 → 2021: 0,676. IDH Brasil 2000: 0,612 → 2010: 0,727 → 2021: 0,754. Analfabetismo MA 2000: 28,8% → 2010: 20,9% → 2022: 15,6%. Analfabetismo Brasil 2000: 12,4% → 2010: 8,6% → 2022: 5,6%. Mortalidade infantil MA 2000: 42,7 → 2010: 22,4 → 2021: 15,2. Mortalidade infantil Brasil 2000: 26,1 → 2010: 16,0 → 2021: 11,9.
**Paleta**: Fundo claro Creme (#FAF3E8). Linhas MA: Vermelho-bumba (#C1292E). Linhas Brasil: Carvao (#2B2B2B). Anotacoes em Ocre (#C8952E). Area entre linhas (gap) em cinza claro.
**Tamanho**: Meia pagina / corpo de texto

## 2. SVG simplificado
**Elementos**: 3 mini-graficos empilhados verticalmente, cada um com 2 linhas (MA e Brasil), eixo X = anos (2000, 2010, 2022), eixo Y = valor do indicador
**Layout**: Tres paineis horizontais, titulo sobre cada um

## 3. Prompt para IA generativa
**Prompt**: "Clean line chart infographic showing improvement trajectory of three social indicators over 22 years (2000-2022). Three stacked panels: HDI (rising), illiteracy rate (falling), infant mortality (falling). Each panel has two lines: red for Maranhao state, dark gray for Brazil national average. The gap between lines narrows slightly over time but persists. Annotated key dates. Warm cream background. Minimalist style, no grid, subtle axes. Style reference: Our World in Data, Hans Rosling Gapminder. Vertical format for print."
**Estilo**: Gapminder / Our World in Data — dado limpo, sem decoracao
**Referencia**: Hans Rosling's visualization style; Our World in Data charts
**NAO incluir**: icones decorativos, backgrounds complexos, 3D effects

---

---
id: VIS-V94-C
verbete: V94
tipo: infografico
posicao: pagina-inteira
---

# Visual V94-C: O paradoxo — o que exporta vs. o que falta

## 1. Briefing para designer
**O que e**: Infografico split-screen de pagina inteira. Lado esquerdo: "O QUE O MARANHAO EXPORTA" — minerio de ferro (icone de trem/navio), soja (icone de graos), energia eletrica (icone de torre), aluminio. Com valores em dolares/toneladas. Lado direito: "O QUE FALTA NO MARANHAO" — esgoto (3,92%), escolas (IDEB 4,1), hospitais (1,8 leitos/mil), empregos formais (60% informal). Separados por uma linha vertical no centro. Impacto visual maximo: riqueza de um lado, pobreza de indicadores do outro.
**Dados**: Exportacoes: ~US$ 15 bi em commodities via Itaqui. Energia: superavitario. Soja: milhoes de toneladas. Falta: 96% sem esgoto, 15,6% analfabetos, 50% abaixo da linha de pobreza.
**Paleta**: Lado esquerdo: fundo Verde-mata escuro (#1A3A2A), dados em dourado/branco. Lado direito: fundo Vermelho-bumba escuro (#5A1015), dados em branco. Linha central em Ocre (#C8952E).
**Tamanho**: Pagina inteira (23x28cm)

## 2. SVG simplificado
**Elementos**: Retangulo dividido ao meio verticalmente. Lado esquerdo verde escuro com lista de exportacoes. Lado direito vermelho escuro com lista de carencias. Titulo centralizado na linha divisoria.
**Layout**: Simetria perfeita. Mesmo numero de itens de cada lado. Impacto visual pela oposicao de cores.

## 3. Prompt para IA generativa
**Prompt**: "Split-screen infographic poster. Left half: dark green background showing wealth indicators of Maranhao state Brazil — cargo ship, train carrying iron ore, soybean fields, wind turbines, large numbers in gold text. Right half: dark red background showing poverty indicators — broken pipe (no sewage), empty classroom, small rural clinic, informal workers. Stark contrast between the two halves. Separated by a thin golden vertical line. Minimalist icons, no photographs, no people. Bold sans-serif typography. 23x28cm vertical format. Style: protest poster meets data visualization."
**Estilo**: Poster de dados com impacto visual — contraste dramatico
**Referencia**: Information is Beautiful awards; data journalism visuals
**NAO incluir**: fotografias de pessoas, imagens estereotipadas de pobreza, rostos, bandeiras
