---
id: VIS-V17-A
verbete: V17
tipo: mapa
posicao: página-inteira
---

# Visual V17-A: Territórios Awá no noroeste maranhense

## 1. Briefing para designer
**O que é**: Mapa do noroeste do Maranhão mostrando as quatro Terras Indígenas onde vivem os Awá, o traçado da Ferrovia Carajás e as áreas de desmatamento. Página inteira.
**Dados**:
- TI Awá: 116.582 ha (exclusiva dos Awá) — cor principal
- TI Caru: 172.667 ha (compartilhada com Guajajara)
- TI Alto Turiaçu: 530.525 ha (compartilhada com Ka'apor)
- TI Arariboia: ~413.000 ha (compartilhada com Guajajara, com registros de Awá isolados)
- Ferrovia Carajás: traçado cortando a região (linha vermelha/preta)
- Rios: Pindaré, Caru, Turiaçu, Gurupi
- Áreas de desmatamento: manchas nas bordas das TIs
- Cidades de referência: Santa Inês, Pindaré-Mirim, Zé Doca, Centro Novo do Maranhão
- Indicação de grupos isolados: ícone discreto (ponto com interrogação) nas áreas de registro
**Referência de estilo**: Mapa editorial moderno, estilo National Geographic / DK Atlas. Fundo verde-floresta para TIs, manchas marrom-terra para desmatamento, linha vermelha para ferrovia.
**Paleta**: Verde-floresta (#1E5631) para TIs com cobertura, Terracota (#B5533E) para destaques e título, Marrom-desmatamento (#8B6914) para áreas degradadas, Azul-rio (#1B4F72) para hidrografia, Vermelho-ferrovia (#C0392B) para Carajás
**Tamanho**: Página inteira (23x28 cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect x="0" y="0" width="600" height="500" fill="#F5F0E8"/>

  <!-- TI Alto Turiaçu (maior, noroeste) -->
  <ellipse cx="200" cy="170" rx="130" ry="90" fill="#1E5631" opacity="0.35" stroke="#1E5631" stroke-width="2"/>
  <text x="150" y="155" fill="#1E5631" font-size="11" font-weight="bold">TI ALTO TURIAÇU</text>
  <text x="160" y="170" fill="#1E5631" font-size="9">530.525 ha</text>
  <text x="155" y="183" fill="#1E5631" font-size="8" font-style="italic">(Awá + Ka'apor)</text>

  <!-- TI Caru (centro) -->
  <ellipse cx="340" cy="250" rx="80" ry="60" fill="#1E5631" opacity="0.4" stroke="#1E5631" stroke-width="2"/>
  <text x="305" y="240" fill="#1E5631" font-size="11" font-weight="bold">TI CARU</text>
  <text x="300" y="255" fill="#1E5631" font-size="9">172.667 ha</text>
  <text x="295" y="268" fill="#1E5631" font-size="8" font-style="italic">(Awá + Guajajara)</text>

  <!-- TI Awá (centro-sul, exclusiva) -->
  <ellipse cx="260" cy="330" rx="65" ry="50" fill="#1E5631" opacity="0.5" stroke="#B5533E" stroke-width="3"/>
  <text x="225" y="320" fill="#B5533E" font-size="11" font-weight="bold">TI AWÁ</text>
  <text x="220" y="335" fill="#B5533E" font-size="9">116.582 ha</text>
  <text x="225" y="348" fill="#B5533E" font-size="8" font-style="italic">(exclusiva)</text>

  <!-- TI Arariboia (leste) -->
  <ellipse cx="450" cy="340" rx="90" ry="70" fill="#1E5631" opacity="0.3" stroke="#1E5631" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="410" y="330" fill="#1E5631" font-size="11" font-weight="bold">TI ARARIBOIA</text>
  <text x="415" y="345" fill="#1E5631" font-size="9">~413.000 ha</text>
  <text x="410" y="358" fill="#1E5631" font-size="8" font-style="italic">(Guajajara + Awá isolados)</text>

  <!-- Rios -->
  <path d="M80,200 Q200,280 350,250 Q420,240 550,220" fill="none" stroke="#1B4F72" stroke-width="2.5" opacity="0.7"/>
  <text x="350" y="215" fill="#1B4F72" font-size="10" font-style="italic">Rio Pindaré</text>

  <path d="M150,100 Q220,200 300,300 Q340,370 380,450" fill="none" stroke="#1B4F72" stroke-width="2" opacity="0.6"/>
  <text x="170" y="240" fill="#1B4F72" font-size="9" font-style="italic">Rio Caru</text>

  <path d="M50,80 Q100,150 130,250 Q150,350 160,450" fill="none" stroke="#1B4F72" stroke-width="2" opacity="0.6"/>
  <text x="55" y="130" fill="#1B4F72" font-size="9" font-style="italic">Rio Turiaçu</text>

  <!-- Ferrovia Carajás -->
  <path d="M580,80 Q450,180 300,280 Q200,350 50,450" fill="none" stroke="#C0392B" stroke-width="3" stroke-dasharray="8,4"/>
  <text x="480" y="120" fill="#C0392B" font-size="10" font-weight="bold">FERROVIA CARAJÁS</text>
  <text x="490" y="135" fill="#C0392B" font-size="8">(890 km, inaugurada 1985)</text>

  <!-- Áreas de desmatamento (manchas nas bordas) -->
  <ellipse cx="380" cy="180" rx="30" ry="20" fill="#8B6914" opacity="0.4"/>
  <ellipse cx="180" cy="390" rx="25" ry="15" fill="#8B6914" opacity="0.4"/>
  <ellipse cx="320" cy="380" rx="20" ry="25" fill="#8B6914" opacity="0.4"/>
  <ellipse cx="470" cy="270" rx="35" ry="18" fill="#8B6914" opacity="0.35"/>

  <!-- Grupos isolados (indicação) -->
  <circle cx="230" cy="300" r="5" fill="none" stroke="#B5533E" stroke-width="1.5"/>
  <text x="225" y="298" fill="#B5533E" font-size="8" text-anchor="middle">?</text>
  <circle cx="430" cy="310" r="5" fill="none" stroke="#B5533E" stroke-width="1.5"/>
  <text x="425" y="308" fill="#B5533E" font-size="8" text-anchor="middle">?</text>

  <!-- Cidades de referência -->
  <rect x="420" y="195" width="4" height="4" fill="#333"/>
  <text x="430" y="200" fill="#333" font-size="8">Santa Inês</text>
  <rect x="350" y="215" width="4" height="4" fill="#333"/>
  <text x="360" y="220" fill="#333" font-size="8">Pindaré-Mirim</text>
  <rect x="130" y="280" width="4" height="4" fill="#333"/>
  <text x="100" y="290" fill="#333" font-size="8">Zé Doca</text>

  <!-- Legenda -->
  <rect x="420" y="400" width="170" height="95" fill="white" stroke="#333" stroke-width="0.5" rx="3"/>
  <text x="430" y="415" fill="#333" font-size="9" font-weight="bold">LEGENDA</text>
  <rect x="430" y="422" width="12" height="8" fill="#1E5631" opacity="0.4"/>
  <text x="448" y="430" fill="#333" font-size="8">Terras Indígenas</text>
  <rect x="430" y="435" width="12" height="8" fill="#1E5631" opacity="0.5" stroke="#B5533E" stroke-width="1.5"/>
  <text x="448" y="443" fill="#333" font-size="8">TI Awá (exclusiva)</text>
  <line x1="430" y1="452" x2="442" y2="452" stroke="#C0392B" stroke-width="2" stroke-dasharray="4,2"/>
  <text x="448" y="456" fill="#333" font-size="8">Ferrovia Carajás</text>
  <rect x="430" y="462" width="12" height="8" fill="#8B6914" opacity="0.4"/>
  <text x="448" y="470" fill="#333" font-size="8">Desmatamento</text>
  <circle cx="436" cy="482" r="4" fill="none" stroke="#B5533E" stroke-width="1"/>
  <text x="432" y="484" fill="#B5533E" font-size="6">?</text>
  <text x="448" y="486" fill="#333" font-size="8">Grupos isolados (registro)</text>

  <!-- Título -->
  <text x="20" y="30" fill="#B5533E" font-size="16" font-weight="bold">Territórios Awá — noroeste do Maranhão</text>
  <text x="20" y="48" fill="#333" font-size="10">Quatro Terras Indígenas, uma ferrovia, uma floresta ameaçada</text>
</svg>
```

## 3. Dados para o designer
- Todas as áreas em hectares conforme portarias de homologação (FUNAI/ISA)
- Traçado da Ferrovia Carajás: simplificado, indicando direção Serra dos Carajás (PA) → Porto de Itaqui (São Luís)
- Desmatamento: concentrado nas bordas das TIs e ao longo da ferrovia
- Grupos isolados: posição aproximada, sem precisão (proteção dos isolados)

---

---
id: VIS-V17-B
verbete: V17
tipo: infografico
posicao: meia-pagina
---

# Visual V17-B: Os Awá em números

## 1. Briefing para designer
**O que é**: Infográfico comparativo mostrando a escala dos Awá — quantos são, o que representa em relação a outros povos e a outras referências populacionais. Meia página.
**Dados**:
- Awá: 520-600 pessoas (total)
- Awá isolados: 60-100 pessoas
- Comparações: Guajajara ~27.000 | Ka'apor ~2.200 | Yanomami ~28.000
- Referência urbana: lotação de um avião comercial (~550 pessoas) | uma escola de samba (~4.000) | um prédio residencial grande (~600)
- TI Awá: 116.582 ha para ~520 pessoas = ~224 ha por pessoa
- Operação Awá: 1.300 famílias invasoras removidas (2014)
**Referência de estilo**: Infográfico editorial, dados humanizados (ícones de pessoas, não só barras). Estilo The Guardian / National Geographic data viz.
**Paleta**: Terracota (#B5533E) para Awá, Verde-floresta (#1E5631) para contexto, Cinza (#666) para comparações
**Tamanho**: Meia página (23x14 cm)

## 2. Elementos visuais
- Ícones de pessoa (estilizados) representando populações — escala visual
- Awá: 520 ícones terracota agrupados (ou 1 ícone = 10 pessoas → 52 ícones)
- Guajajara: barra muito maior ao lado (27.000)
- Círculo central: "520 pessoas — todo o povo Awá cabe num avião"
- Destaque: "60-100 isolados" em ícones com interrogação
- Linha do tempo lateral: 1973 (primeiro contato) → 1985 (Ferrovia) → 2005 (TI homologada) → 2012 (campanha Survival) → 2014 (Operação Awá)

## 3. Texto do infográfico
**Título**: "520 pessoas. Todo um povo."
**Subtítulo**: "Os Awá-Guajá são o menor e mais ameaçado povo nômade do Brasil"
**Dado de impacto**: "Para cada Awá, existem 52 Guajajara e 54 Yanomami."
**Dado territorial**: "116.582 hectares de terra demarcada — mas a floresta ao redor encolhe todo ano."
**Dado operacional**: "Em 2014, a maior operação da FUNAI removeu 1.300 famílias invasoras da TI Awá."
