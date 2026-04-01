---
id: VIS-V33
verbete: V33
tipo: infografico-multiplo
posicao: distribuido
---

# Visuais V33: Números da escravidão no Maranhão

---

## Visual V33-A: Gráfico de volume anual do tráfico (1680-1850)

### 1. Briefing para designer
**O que é**: Gráfico de barras empilhadas mostrando o volume anual estimado de africanos escravizados trazidos ao Maranhão, de 1680 a 1850. O elemento-chave é a ruptura de 1755 (Companhia de Pombal) — antes, quase nada; depois, explosão.
**Dados**:
- 1680-1755: ~34/ano (barra minúscula, quase invisível)
- 1755-1778: ~1.087/ano (Companhia — barra média, cor destacada)
- 1778-1815: ~1.500-2.000/ano estimados (tráfico livre, boom algodoeiro — barras altas)
- 1815-1842: decrescente (proibição do tráfico ao norte do Equador, tráfico ilegal)
- 1842-1850: residual (Lei Eusébio de Queirós encerra)
- Anotação vertical em 1755: "Companhia de Pombal" — marca o divisor
- Anotação vertical em 1815: "Congresso de Viena"
- Anotação vertical em 1850: "Lei Eusébio de Queirós"
**Formato**: Largura total da página (23 cm), altura ~12 cm
**Paleta**: Roxo-tambor (#5E3A7E) para barras, Preto-mangue (#1C1C1C) para eixos, Branco para fundo
**Referência de estilo**: gráficos do Trans-Atlantic Slave Trade Database (slavevoyages.org)

### 2. SVG simplificado

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="800" height="400" fill="#FAFAFA"/>

  <!-- Titulo -->
  <text x="400" y="30" text-anchor="middle" fill="#1C1C1C" font-size="16" font-weight="bold">Africanos escravizados trazidos ao Maranhão por ano (estimativa)</text>

  <!-- Eixo X -->
  <line x1="80" y1="340" x2="760" y2="340" stroke="#1C1C1C" stroke-width="1"/>
  <text x="120" y="365" fill="#666" font-size="10">1680</text>
  <text x="280" y="365" fill="#666" font-size="10">1755</text>
  <text x="440" y="365" fill="#666" font-size="10">1800</text>
  <text x="600" y="365" fill="#666" font-size="10">1842</text>
  <text x="700" y="365" fill="#666" font-size="10">1850</text>

  <!-- Eixo Y -->
  <line x1="80" y1="60" x2="80" y2="340" stroke="#1C1C1C" stroke-width="1"/>
  <text x="70" y="340" text-anchor="end" fill="#666" font-size="10">0</text>
  <text x="70" y="270" text-anchor="end" fill="#666" font-size="10">500</text>
  <text x="70" y="200" text-anchor="end" fill="#666" font-size="10">1.000</text>
  <text x="70" y="130" text-anchor="end" fill="#666" font-size="10">1.500</text>
  <text x="70" y="60" text-anchor="end" fill="#666" font-size="10">2.000</text>

  <!-- Barras: pre-Companhia (1680-1755) — quase invisivel -->
  <rect x="100" y="335" width="170" height="5" fill="#5E3A7E" opacity="0.3"/>
  <text x="185" y="332" text-anchor="middle" fill="#5E3A7E" font-size="9">~34/ano</text>

  <!-- Barras: Companhia (1755-1778) -->
  <rect x="280" y="190" width="80" height="150" fill="#5E3A7E" opacity="0.7"/>
  <text x="320" y="185" text-anchor="middle" fill="#5E3A7E" font-size="9">~1.087/ano</text>

  <!-- Barras: boom (1778-1815) -->
  <rect x="370" y="100" width="150" height="240" fill="#5E3A7E" opacity="0.9"/>
  <text x="445" y="90" text-anchor="middle" fill="#5E3A7E" font-size="9">~1.500-2.000/ano</text>

  <!-- Barras: declinio (1815-1842) -->
  <rect x="530" y="220" width="80" height="120" fill="#5E3A7E" opacity="0.5"/>
  <text x="570" y="215" text-anchor="middle" fill="#5E3A7E" font-size="9">decrescente</text>

  <!-- Barras: residual (1842-1850) -->
  <rect x="620" y="320" width="40" height="20" fill="#5E3A7E" opacity="0.2"/>

  <!-- Anotacoes verticais -->
  <line x1="280" y1="50" x2="280" y2="340" stroke="#BA4A00" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="282" y="48" fill="#BA4A00" font-size="9" font-weight="bold">Companhia de Pombal (1755)</text>

  <line x1="520" y1="50" x2="520" y2="340" stroke="#BA4A00" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="522" y="48" fill="#BA4A00" font-size="9">Congresso de Viena (1815)</text>

  <line x1="660" y1="50" x2="660" y2="340" stroke="#BA4A00" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="662" y="48" fill="#BA4A00" font-size="9">Eusébio de Queirós (1850)</text>

  <!-- Legenda -->
  <text x="400" y="390" text-anchor="middle" fill="#666" font-size="10">Fontes: Carreira (1983), Hawthorne (2010), Assunção (2015), Mota & Barroso (2017)</text>
</svg>
```

---

## Visual V33-B: Mapa de calor — concentração de escravizados no MA

### 1. Briefing para designer
**O que é**: Mapa do Maranhão com gradiente de cor mostrando a concentração de população escravizada por região no auge (c. 1800-1821). O Vale do Itapecuru é o epicentro (roxo escuro), litoral de Alcântara/São Luís em tom médio, sertão em tom claro.
**Dados**:
- Vale do Itapecuru (Itapecuru-Mirim, Caxias, Codó, Coroatá): 80-85% — roxo escuro
- Litoral (São Luís, Alcântara, Guimarães): 50-60% — roxo médio
- Baixada Maranhense: 40-50% — roxo claro
- Sertão (Pastos Bons, Carolina): 20-30% — roxo muito claro
- O rio Itapecuru deve ser visível como linha condutora
**Formato**: Meia página (11×14 cm)
**Paleta**: Gradiente de roxo-tambor — de #E8D5F5 (claro) a #2D1A3E (escuro)
**Referência**: mapas coropléticos do IBGE

### 2. SVG simplificado

```svg
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="500" height="500" fill="#FAFAFA"/>

  <!-- Titulo -->
  <text x="250" y="30" text-anchor="middle" fill="#1C1C1C" font-size="14" font-weight="bold">Concentração de escravizados no Maranhão (c. 1821)</text>

  <!-- Contorno simplificado do MA -->
  <path d="M100,80 L200,60 L320,70 L400,100 L430,160 L420,240 L380,320 L320,380 L240,420 L160,400 L100,340 L80,260 L90,180 Z" fill="#E8D5F5" stroke="#1C1C1C" stroke-width="1.5"/>

  <!-- Vale do Itapecuru — zona mais escura -->
  <path d="M200,120 L280,110 L340,150 L350,220 L320,280 L260,300 L200,260 L180,200 Z" fill="#2D1A3E" opacity="0.9"/>

  <!-- Litoral (São Luís, Alcântara) -->
  <path d="M100,80 L200,60 L220,100 L200,120 L180,160 L130,140 Z" fill="#5E3A7E" opacity="0.8"/>

  <!-- Baixada -->
  <path d="M100,140 L180,160 L200,200 L200,260 L160,300 L100,280 L80,200 Z" fill="#8B6BAE" opacity="0.7"/>

  <!-- Sertão -->
  <path d="M340,150 L400,100 L430,160 L420,240 L380,280 L350,220 Z" fill="#C9B3DB" opacity="0.5"/>

  <!-- Rio Itapecuru -->
  <path d="M160,120 L200,140 L240,180 L280,220 L310,270 L330,320" fill="none" stroke="#1B4F72" stroke-width="2.5" stroke-linecap="round"/>
  <text x="340" y="330" fill="#1B4F72" font-size="10" font-style="italic">Itapecuru</text>

  <!-- Labels -->
  <circle cx="150" cy="100" r="3" fill="white"/>
  <text x="155" y="95" fill="white" font-size="9" font-weight="bold">São Luís</text>

  <circle cx="120" cy="120" r="2" fill="white"/>
  <text x="100" y="115" fill="white" font-size="8">Alcântara</text>

  <circle cx="250" cy="180" r="3" fill="white"/>
  <text x="255" y="175" fill="white" font-size="9" font-weight="bold">Itapecuru-Mirim</text>

  <circle cx="310" cy="230" r="3" fill="white"/>
  <text x="315" y="225" fill="white" font-size="9">Caxias</text>

  <circle cx="290" cy="260" r="2" fill="white"/>
  <text x="295" y="255" fill="white" font-size="8">Codó</text>

  <!-- Legenda -->
  <rect x="30" y="430" width="20" height="10" fill="#2D1A3E"/>
  <text x="55" y="439" fill="#1C1C1C" font-size="9">80-85% escravizados</text>

  <rect x="170" y="430" width="20" height="10" fill="#5E3A7E"/>
  <text x="195" y="439" fill="#1C1C1C" font-size="9">50-60%</text>

  <rect x="270" y="430" width="20" height="10" fill="#8B6BAE"/>
  <text x="295" y="439" fill="#1C1C1C" font-size="9">40-50%</text>

  <rect x="370" y="430" width="20" height="10" fill="#C9B3DB"/>
  <text x="395" y="439" fill="#1C1C1C" font-size="9">20-30%</text>

  <text x="250" y="475" text-anchor="middle" fill="#666" font-size="9">Fontes: Pereira do Lago (1822), Viveiros (1954), Mota & Cunha (2017)</text>
</svg>
```

---

## Visual V33-C: Tabela comparativa — MA vs. Atlântico escravista

### 1. Briefing para designer
**O que é**: Tabela-infográfico comparando a proporção de escravizados no Maranhão (capitania e Itapecuru) com outras regiões do Atlântico escravista. Formato: barras horizontais proporcionais, com bandeiras ou ícones das regiões.
**Dados**:
- Saint-Domingue (Haiti): 89%
- Jamaica: 88%
- **Vale do Itapecuru (MA)**: 85%
- **Maranhão (capitania)**: 55,3%
- Virginia (EUA): 40%
- Bahia: 35-40%
- Rio de Janeiro: 35-40%
- Pernambuco: 30-35%
**Formato**: Meia página (11×10 cm)
**Paleta**: Roxo-tambor (#5E3A7E) para MA, cinza (#999) para demais, destaque em branco para texto
**Nota**: Itapecuru e MA em roxo; demais em cinza. Destaque visual que o Itapecuru estava na mesma faixa do Caribe.

### 2. SVG simplificado

```svg
<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="350" fill="#FAFAFA"/>

  <text x="300" y="25" text-anchor="middle" fill="#1C1C1C" font-size="14" font-weight="bold">Proporção de escravizados no auge — comparação atlântica</text>

  <!-- Barras -->
  <!-- Haiti -->
  <text x="140" y="62" text-anchor="end" fill="#666" font-size="11">Saint-Domingue (Haiti)</text>
  <rect x="150" y="50" width="400" height="22" fill="#999" rx="2"/>
  <text x="555" y="66" fill="#666" font-size="10">89%</text>

  <!-- Jamaica -->
  <text x="140" y="92" text-anchor="end" fill="#666" font-size="11">Jamaica</text>
  <rect x="150" y="80" width="395" height="22" fill="#999" rx="2"/>
  <text x="550" y="96" fill="#666" font-size="10">88%</text>

  <!-- Itapecuru -->
  <text x="140" y="122" text-anchor="end" fill="#5E3A7E" font-size="11" font-weight="bold">Vale do Itapecuru (MA)</text>
  <rect x="150" y="110" width="382" height="22" fill="#5E3A7E" rx="2"/>
  <text x="537" y="126" fill="#5E3A7E" font-size="10" font-weight="bold">85%</text>

  <!-- MA capitania -->
  <text x="140" y="152" text-anchor="end" fill="#5E3A7E" font-size="11" font-weight="bold">Maranhão (capitania)</text>
  <rect x="150" y="140" width="248" height="22" fill="#5E3A7E" opacity="0.7" rx="2"/>
  <text x="403" y="156" fill="#5E3A7E" font-size="10" font-weight="bold">55%</text>

  <!-- Virginia -->
  <text x="140" y="182" text-anchor="end" fill="#666" font-size="11">Virginia (EUA)</text>
  <rect x="150" y="170" width="180" height="22" fill="#999" rx="2"/>
  <text x="335" y="186" fill="#666" font-size="10">40%</text>

  <!-- Bahia -->
  <text x="140" y="212" text-anchor="end" fill="#666" font-size="11">Bahia</text>
  <rect x="150" y="200" width="170" height="22" fill="#999" rx="2"/>
  <text x="325" y="216" fill="#666" font-size="10">~38%</text>

  <!-- RJ -->
  <text x="140" y="242" text-anchor="end" fill="#666" font-size="11">Rio de Janeiro</text>
  <rect x="150" y="230" width="165" height="22" fill="#999" rx="2"/>
  <text x="320" y="246" fill="#666" font-size="10">~37%</text>

  <!-- PE -->
  <text x="140" y="272" text-anchor="end" fill="#666" font-size="11">Pernambuco</text>
  <rect x="150" y="260" width="145" height="22" fill="#999" rx="2"/>
  <text x="300" y="276" fill="#666" font-size="10">~32%</text>

  <!-- Nota -->
  <text x="300" y="310" text-anchor="middle" fill="#666" font-size="9">Dados referem-se ao pico de cada região. MA: censo de 1821 + estimativas do Itapecuru.</text>
  <text x="300" y="325" text-anchor="middle" fill="#666" font-size="9">Fontes: Pereira do Lago (1822), Viveiros (1954), Geggus (2001), Burnard (2004).</text>
</svg>
```

---

## Visual V33-D: Linha do tempo demográfica (para versão digital/web)

### 1. Briefing para designer
**O que é**: Timeline horizontal mostrando a evolução da proporção de escravizados no Maranhão, de 1680 a 2022. Cada ponto marca um evento ou dado demográfico. O arco visual é: quase zero → explosão → maioria → declínio → legado contemporâneo (78%).
**Dados-pontos**:
- 1680: ~5% (residual)
- 1755: Companhia de Pombal — início da transformação
- 1778: ~30-35% — fim da Companhia, tráfico livre
- 1800: ~45-50% — boom algodoeiro
- 1821: 55,3% — censo oficial, maioria absoluta
- 1835: Balaiada — revolta com forte participação de escravizados
- 1850: Lei Eusébio de Queirós — fim do tráfico atlântico
- 1888: Abolição
- 2022: 78,1% pretos + pardos (IBGE)
**Formato**: Horizontal, para spread dupla (46×10 cm) ou scroll digital
**Paleta**: Roxo-tambor (#5E3A7E) dominante, com gradiente de intensidade acompanhando a proporção
**Nota visual**: O ponto de 2022 (78%) é maior que todos os outros — o legado é o maior número.
