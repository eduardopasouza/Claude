# MapBiomas — Exploração Detalhada para AgroJus

**Complemento ao DATA_CATALOG.md** — foco em agricultura e infraestrutura

---

## 1. AGRICULTURA — Classes MapBiomas Coleção 10

O MapBiomas classifica **cada pixel do Brasil** (30m ou 10m de resolução) em classes de uso. Para agricultura, temos granularidade até o tipo de cultura:

### Hierarquia completa de classes agrícolas

| Código | Classe | Nível | O que o AgroJus pode extrair |
|--------|--------|-------|------------------------------|
| **3** | Agropecuária (macro) | 1 | Área total agrícola de qualquer coord. |
| **15** | Pastagem | 3 | Área de pasto — compliance pecuária |
| **18** | Agricultura | 3 | Toda área de lavoura |
| **19** | Lavoura Temporária | 4 | Grãos e anuais |
| **39** | **Soja** | 5 | Mapeamento de safra soja — EUDR |
| **20** | **Cana-de-açúcar** | 5 | Usinas, etanol, biocombustível |
| **40** | **Arroz** | 5 | Arroz irrigado (irrigação detectada!) |
| **62** | **Algodão** (beta) | 5 | Commodity exportação |
| **41** | Outras Lavouras Temp. | 5 | Milho, feijão, trigo, etc. |
| **36** | Lavoura Perene | 4 | Frutas, café, cacau |
| **46** | **Café** | 5 | EUDR commodity regulada |
| **47** | **Citrus** | 5 | Laranja |
| **48** | Outras Lavouras Perenes | 5 | Cacau, dendê, seringueira |
| **9** | Silvicultura (Florestas Plantadas) | 3 | Eucalipto, pinus |
| **21** | Mosaico de Usos | 3 | Pequenas propriedades misturadas |

### Módulos especiais de agricultura

#### Vigor da Pastagem (pixel a pixel)
| Código | Nível de Vigor |
|--------|---------------|
| 1 | Baixo (pasto degradado) |
| 2 | Médio |
| 3 | Alto (pasto produtivo) |

**Aplicação AgroJus:** Avaliar qualidade da pastagem de uma propriedade — pasto degradado = risco de produtividade baixa = risco de crédito. Operações de recuperação podem gerar créditos de carbono.

#### Irrigação (detectada por satélite!)
| Código | Tipo de Irrigação |
|--------|------------------|
| 1 | **Irrigação por Pivô Central** |
| 2 | **Arroz Irrigado** |
| 3 | Outros sistemas de irrigação |

**Aplicação AgroJus:** Detectar pivôs centrais por satélite permite estimar valor da terra, produtividade potencial, e conformidade com outorga de água (ANA). Propriedades irrigadas valem 3-5× mais.

### Google Earth Engine Assets (acesso programático)

```
# Cobertura e Uso — Coleção 10.1
projects/mapbiomas-public/assets/brazil/lulc/collection10_1/mapbiomas_brazil_collection10_1_coverage_v1

# Desmatamento e Vegetação Secundária
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_deforestation_secondary_vegetation_v1

# Fogo — Coleção 4
projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_brazil_fire_collection4_annual_burned_v1
projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_brazil_fire_collection4_monthly_burned_v1

# Vigor da Pastagem
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_vigor_v1

# Irrigação
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_irrigation_v1
```

### Download de Estatísticas (CSV por município)
Na [Plataforma MapBiomas Estatísticas](https://plataforma.brasil.mapbiomas.org/), é possível exportar **tabela de áreas por município e por classe** para todos os anos (1985-2023). Isso gera CSVs riquíssimos como:

```
MUNICÍPIO | ANO | SOJA_ha | PASTAGEM_ha | FLORESTA_ha | CANA_ha | CAFÉ_ha | ...
```

**Aplicação AgroJus:** Análise de tendências — município que perdeu floresta e ganhou soja nos últimos 5 anos = alto risco EUDR.

---

## 2. INFRAESTRUTURA — Downloads Diretos (Shapefiles)

O MapBiomas compila dados de IBGE, ANTT, EPE, ONS, MME, ANAC e disponibiliza **cada camada como shapefile individualizado**. Todas as URLs abaixo são download direto:

### Transportes

| Camada | URL Download |
|--------|-------------|
| **Aeródromos Públicos** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Aerodromos_publicos.zip) |
| **Aeródromos Privados** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Aerodromos_Privados.zip) |
| **Helipontos** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Helipontos.zip) |
| **Hidrovias** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/hidrovia.zip) |
| **Ferrovias** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/ferrovia.zip) |
| **Rodovias Federais** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/rodovia-federal.zip) |
| **Rodovias Estaduais** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/rodovia-estadual.zip) |
| **Portos Organizados** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Porto-organizado.zip) |
| **Terminais de Uso Privado** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/terminal_de_uso_privado.zip) |
| **Eclusas** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/eclusa.zip) |
| **Estações de Transbordo** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/estacao_transbordo_de_cargas.zip) |

### Energia

| Camada | URL Download |
|--------|-------------|
| **Linhas de Transmissão** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/LT_EXISTENTE.zip) |
| **Subestações** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/SE_EXISTENTE.zip) |
| **Usinas Hidrelétricas (UHE)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Usinas_Hidreletricas_UHE.zip) |
| **PCH (Pequenas Centrais Hidrel.)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Pequenas_Centrais_Hidreletricas_PCH.zip) |
| **CGH (Centrais Geradoras Hidrel.)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Centrais_Geradoras_Hidreletricas_CGH.zip) |
| **Usinas Eólicas** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Usina-Eolica.zip) |
| **Usinas Fotovoltaicas** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Usina_Fotovoltaica_UFV.zip) |
| **Termelétricas Biomassa** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Usinas_Termeletricas_UTE_Biomassa.zip) |
| **Termelétricas Fóssil** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Usinas_Termeletricas_UTE_Fossil.zip) |
| **Termonuclear** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/termonuclear.zip) |
| **Usinas de Etanol** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/usina_etanol.zip) |
| **Usinas de Biodiesel** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/usina_biodiesel.zip) |
| **Usinas de Biogás** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/usina_biogas.zip) |

### Dutos e Oleodutos

| Camada | URL Download |
|--------|-------------|
| **Gasoduto Transporte** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/gasoduto-transporte.zip) |
| **Gasoduto Distribuição** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/gasoduto-distribuicao.zip) |
| **Gasoduto Escoamento** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/gasoduto-escoamento.zip) |
| **Oleoduto** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/oleoduto.zip) |
| **Mineroduto** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/mineroduto.zip) |
| **Aqueduto** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/aquaduto.zip) |

### Mineração

| Camada | URL Download |
|--------|-------------|
| **Minas (Energéticos)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/MinaEnergeticos.zip) |
| **Minas (Metálicos)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/MinaMetalicos.zip) |
| **Minas (Outros Produtos)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/MinaOutrosProdutos.zip) |
| **Barragens** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Barragens.zip) |

### Agronegócio

| Camada | URL Download |
|--------|-------------|
| **Armazéns e Silos** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/armazens-silos.zip) |
| **Frigoríficos** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/frigorificos.zip) |

### Telecomunicações

| Camada | URL Download |
|--------|-------------|
| **ERBs (Torres de Celular)** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/ERB.zip) |

### Especial — Pistas de Pouso na Amazônia

| Camada | URL Download |
|--------|-------------|
| **Pistas de Pouso** | [ZIP](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Pistas_de_Pouso_27_Mar_2023_v1.2.zip) |

**Aplicação AgroJus (infraestrutura):**
- **Armazéns + Silos**: Distância do imóvel a silos = custo logístico = valor da terra
- **Frigoríficos**: Rastreabilidade pecuária — qual frigorífico é mais próximo? Tem embargo?
- **Rodovias + Ferrovias**: Acesso logístico, rota de escoamento
- **Portos**: Distância ao porto de exportação (Santos, Paranaguá, etc.)
- **Pistas de Pouso na Amazônia**: Risco — pistas ilegais = garimpo/desmatamento clandestino

---

## 3. MONITOR DO CRÉDITO RURAL

| | |
|---|---|
| **Plataforma** | [plataforma.creditorural.mapbiomas.org](https://plataforma.creditorural.mapbiomas.org) |
| **Download Vetoriais** | [Google Drive (ZIP)](https://drive.google.com/file/d/1tO0-qYUAQKRHJWrbYxO7VsUmwHLEn-TS/view?usp=sharing) |
| **Última atualização** | Sicor: 16/10/2024, CAR: 01/2024 |
| **Conteúdo** | Polígonos de financiamentos do Sicor cruzados com alertas de desmatamento, imóveis CAR, SIGEF, SNCI |
| **Nota** | Nem todas as operações têm coordenadas (sigilo bancário parcial) |

**ESTE É O DADO MAIS EXCLUSIVO DO AGROJUS** — nenhum concorrente usa esse cruzamento. Mostra literalmente onde o dinheiro público do crédito rural foi parar e se há desmatamento na área.

---

## 4. MAPAS DE TRANSIÇÃO (Histórico de Mudanças)

O MapBiomas gera mapas de transição que codificam **o que cada pixel era → o que virou**:

| Código | Significado |
|--------|------------|
| 303 | Floresta → Floresta (sem mudança) |
| **315** | **Floresta → Pastagem** (desmatamento p/ pecuária) |
| **318** | **Floresta → Agricultura** (desmatamento p/ lavoura) |
| **339** | **Floresta → Soja** (desmatamento p/ soja = alarme EUDR) |
| 1515 | Pastagem → Pastagem (sem mudança) |
| **1518** | **Pastagem → Agricultura** (conversão produtiva) |
| **1524** | **Pastagem → Infraestrutura Urbana** (urbanização) |

**Aplicação AgroJus:** Mapas de transição são a **prova cabal para EUDR**. Se pixel mudou de floresta para soja após dez/2020 = desmatamento ilegal pela regulação europeia. Nenhum concorrente oferece isso automatizado.

---

## 5. LEGENDA OFICIAL

- [Códigos da Legenda Coleção 10 (PDF)](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/08/Legenda-Colecao-10-Legend-Code.pdf)
- [Descrição Detalhada (PDF)](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/08/Legenda-Colecao-10-Descricao-Detalhada-PDF_PT-BR_EN.pdf)
- [CSV de Códigos + Paleta de Cores](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/08/Codigos-da-legenda-colecao-10.zip)
- [Estilo QGIS (Coleção 10)](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/08/ESTILO_QGIS_COL10_PT_EN.zip)

---

*Este apêndice complementa o DATA_CATALOG.md principal com o detalhamento profundo do MapBiomas.*
