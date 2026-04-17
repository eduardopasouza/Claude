# MapBiomas Brasil — Cobertura LULC (Coleção 10)

- **URL:** https://plataforma.brasil.mapbiomas.org/
- **Categoria:** mapbiomas (referência de dashboard temático)
- **Data auditoria:** 2026-04-17
- **Acesso:** público, sem cadastro

## Propósito declarado

Plataforma de visualização da Coleção 10 (1985-2024) de uso e cobertura do solo do Brasil, resolução 30m Landsat + 10m Sentinel (9 anos), 34 classes hierárquicas. Renderiza raster via MapLibre + Google Earth Engine.

## Layout e navegação

**Estrutura em 3 colunas + rodapé expandido:**

```
┌────────┬──────────────────────────────────────┬──────────┐
│ Árvore │                                       │ Legenda  │
│ Temas  │           MAPA (MapLibre)             │ dinâmica │
│ Lateral│                                       │ por tema │
│  Esq   │                                       │          │
│        │                                       │          │
├────────┴──────────────────────────────────────┴──────────┤
│  DASHBOARD inferior: números + série temporal            │
│  "506.710.630 ha (59,6%) Floresta"                       │
│  Gráfico 1985-2024                                       │
└──────────────────────────────────────────────────────────┘
```

- **Header:** Brasil · Temas · MapBiomas IA (beta)
- **Sidebar esquerda (árvore):** Temas em accordion
- **Sidebar direita:** Legenda dinâmica do tema ativo + "Agrupar por Bioma"
- **Rodapé:** Dashboard com estatísticas agregadas da região selecionada

## Árvore temática (crítica para AgroJus)

**Níveis hierárquicos de 4 profundidades.** Temas mestres:

1. **Cobertura** 30m (40 anos) — Cobertura, Transições, Nº classes, Nº mudanças, Áreas estáveis
2. **Cobertura** 10m (9 anos) — beta Sentinel
3. **Desmatamento** — Anual, Acumulado, Frequência, Último ano
4. **Vegetação Secundária** — Anual, Idade
5. **Agricultura** — Uso agrícola, 2ª safra, Sistemas de irrigação, Frequência anual, Frequência média
6. **Pastagem** — Idade, Condição de vigor, Transição, Biomassa
7. **Fogo** — Anual, Mensal, Acumulado, Frequência, Último ano, Tamanho cicatriz + link **Acessar Monitor do fogo**
8. **Mineração** — Substância minerada + link **Acessar Monitor da mineração**
9. **Água** — Dados anuais, mensais + link **Bacias Hidrográficas**
10. **Solo** (beta) — Carbono orgânico, Fração areia/silte/argila, Grupo textural, Subgrupo, Classe textural, Pedregosidade
11. **Degradação** (beta) — Tamanho borda, Tamanho fragmento, Frequência fogo, Vegetação secundária, Cruzamento vetores
12. **Recifes costeiros** (beta)
13. **Urbano** — Urbanização anual, Períodos, Vegetação urbana, Declividade, Altura drenagem
14. **Análises Ambientais** (ext.) — Regiões Fitoecológicas IBGE 2026, Pedologia IBGE, Geomorfologia, Hipsometria, Declividade, Orientação de vertente
15. **Atmosfera** (beta) — Temperatura, Precipitação & Água, Pressão de vapor, Qualidade do ar
16. **Risco climático** (beta) — Deslizamentos, Inundação/alagamento, Índice segurança hídrica
17. **Criar análise** (beta) — AOI customizada
18. **Downloads** — Exportar dados

## Sub-legenda: classes hierárquicas

Para **Cobertura**, expande em 4 níveis clicáveis com **"Ver só esta"** em cada classe:

- Nível 1: Natural vs Antrópico
- Nível 2: Floresta / Veg. Não Florestal / Agropecuária / Não Vegetada / Água
- Nível 3-4: Formação Florestal, Formação Savânica, Mangue, Restinga, Formação Campestre, Campo Alagado, Apicum, Aquicultura, Floresta Alagável, Pastagem, Lavoura Temporária (Soja, Cana, Arroz, Algodão, Outras), Lavoura Perene (Café, Citrus, Dendê, Outras), Silvicultura, Mosaico de Usos, Mineração, Praia/Duna/Areal, Área Urbanizada, Usina Fotovoltaica, Rio/Lago/Oceano, Não Observado

## Dashboard inferior (fundamental para AgroJus)

**"Visualizado no mapa"** para a região selecionada (Brasil / Bioma / Estado / Município / AOI):

**Cards de classes principais com:**
- valor absoluto (ha)
- percentual
- cor da classe
- exemplo: *"506.710.630 ha (59,6%) · Floresta"*, *"273.169.329 ha (32,1%) · Agropecuária"*, *"46.595.174 ha (5,5%) · Veg. Herbácea"*

**Série temporal** abaixo — gráfico 1985-2024 mostrando evolução da cobertura. Clique em ano → mapa salta para aquele ano.

## Interações

- **Click classe na legenda:** "Ver só esta" → filtra mapa visual
- **Click em ano** na timeline → muda raster
- **Zoom/pan:** revela detalhes (limite de zoom baseado na resolução 30m)
- **Região:** dropdown Brasil → Bioma → Estado → Município → **Minha geometria** (upload/desenho)
- **Idioma:** pt/en

## Basemap e tema

- Interface **clara** (fundo branco)
- Tile de fundo neutro (Google Earth Engine)
- **MapLibre** (não Leaflet) — permite raster GPU

## Ferramentas extras

- **Criar análise** — definir AOI customizada (upload geoJSON/shapefile)
- **Downloads** — exportar: estatísticas CSV, mapa PNG, raster GeoTIFF
- **CAR** na sidebar de região — inserir código CAR para filtrar
- **Compartilhar** — URL contém estado serializado (todos os filtros em query params)

## Inspector / detalhes on-click

Click no mapa não abre popup rico — a experiência é orientada a **área selecionada** (região → dashboard). O que equivaleria a "inspector" é o dashboard inferior recalculado ao trocar AOI.

## API e export

- Dashboards chamam APIs internas (não documentadas publicamente como REST pública)
- Datasets oficiais via **Earth Engine public assets**: `projects/mapbiomas-public/assets/brazil/lulc/collection10/...`
- ATBDs (metodologia) em PDF

## Autenticação

Nenhuma para consulta. Cadastro só para salvar análises customizadas.

## Insights para AgroJus (MUITO IMPORTANTE)

1. **Árvore temática em níveis hierárquicos** — replicar em `LayerTreePanel` com accordion dobrável e contador de ativas por tema (feito já parcialmente).

2. **Legenda dinâmica no painel direito** — quando camada com classes é ativada (ex: PRODES, MapBiomas LULC), abrir painel à direita com legenda interativa. **Ainda não implementado no AgroJus.**

3. **Dashboard inferior com estatísticas agregadas do viewport** — padrão ouro. Replicar:
   - KPIs grandes com valor/percentual
   - Série temporal para camadas que tem tempo (PRODES, DETER, MapBiomas)
   - Recalcular ao mover mapa ou trocar região
   - ✅ Já está começado em `StatsDashboard.tsx`, mas falta série temporal e cores por classe.

4. **Seletor de região (Brasil → Bioma → Estado → Município → AOI customizada)** — breadcrumb navegável.

5. **"Ver só esta" por classe** — utilíssimo. Quando o usuário quer isolar ex: "apenas Soja" em MapBiomas Agricultura. Fazer para camadas com múltiplas classes.

6. **URL como estado serializado** — todos os filtros e seleções codificados na URL para compartilhamento permalink. Essencial para colaboração (advogado manda link pro cliente).

7. **"Criar análise" = AOI customizada** — funcionalidade premium: upload de shapefile/GeoJSON e o sistema calcula todas as estatísticas dentro daquela AOI. No contexto AgroJus, equivale a "colar CAR → calcular tudo para aquele polígono".

8. **Links de "saída" para plataformas especializadas** — "Acessar Monitor do fogo" é um link para outra plataforma. Nosso mapa pode fazer o mesmo: link "Ver ficha completa" → `/imoveis/[car]`.

9. **Nível de zoom define resolução visível** — não mostrar camadas abaixo do zoom útil. Mensagem "aumente zoom para ver detalhes". ✅ Já fazemos isso com `minZoom`.

10. **Temporal (slider de anos)** — para camadas com série temporal, incluir slider. Ex: PRODES 1985-2024. DETER dia-a-dia. ❌ Não temos ainda.

## Gaps vs AgroJus

| Feature MapBiomas | AgroJus hoje | Prioridade |
|---|---|---|
| Árvore temática hierárquica | ✅ implementado (LayerTreePanel) | — |
| Legenda dinâmica painel direito | ❌ ausente | ALTA |
| Dashboard inferior KPIs | ⚠️ parcial (sem charts) | ALTA |
| Série temporal no dashboard | ❌ ausente | MÉDIA |
| "Ver só esta classe" | ❌ ausente | MÉDIA |
| URL com estado serializado | ❌ ausente | ALTA (colaboração) |
| AOI customizada (upload) | ❌ ausente | MÉDIA |
| Seletor de região breadcrumb | ❌ ausente (temos só CAR search) | MÉDIA |
| Slider temporal | ❌ ausente | ALTA (PRODES/DETER) |
| Links para plataformas externas | ⚠️ parcial (LayerInspector tem ações) | BAIXA |
