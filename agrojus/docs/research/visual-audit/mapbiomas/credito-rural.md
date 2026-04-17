# MapBiomas Monitor do Crédito Rural

- **URL:** https://plataforma.creditorural.mapbiomas.org/
- **Categoria:** mapbiomas (referência compliance crédito + ESG)
- **Data auditoria:** 2026-04-17
- **Acesso:** público, sem cadastro

## Propósito declarado

Monitor do **crédito rural brasileiro** cruzado com cobertura/uso MapBiomas. Identifica operações em áreas com desmatamento pós-concessão, sobreposição com UCs/TIs/embargos. Alimenta fiscalização do BCB e diligência de bancos.

## Layout e navegação

**3 abas laterais esquerdas + mapa Leaflet:**

- Aba **Filtros** (default) — combinação de filtros para isolar operações
- Aba **Camadas** — gerenciamento de camadas sobrepostas
- Aba **Mapa base** — seletor de basemap (3+ opções)

Header horizontal:
- Logo MapBiomas Crédito Rural
- **Destaques** (narrativas/case studies)
- **Downloads** (dados agregados CSV/XLSX)
- **Nota Informativa** (metodologia, notas de uso)

Footer aside:
- Link para Remap Geo (parceiro)
- Link externo para MapBiomas Alerta
- Banner "Concordo" (termos de uso)

## Filtros expostos (Abordagem diferente do Alerta)

Dois modos disponíveis via botões tab:

1. **Selecionáveis** — combo boxes para categorias fixas
2. **Pesquisáveis** — busca por texto livre

**Campos observados:**
- 5-6 comboboxes com "Selecione" (categorias, bancos, finalidades, culturas, UF)
- **Date range** (De / Até) com calendários — observado: inicia 01/01/2019
- Busca sobre os combos (autocomplete)
- Botões **Resetar** e **Buscar** na base do painel

## Aba "Camadas"

Controles:
- **Opacidade dos Financiamentos** — slider
- **Quantidade** — visualizar mapa colorido por nº de contratos
- **Área** — visualizar por área agregada
- **Volume de Crédito** — visualizar por R$ agregado

Cada métrica tem botão **Exportar** ao lado (CSV/XLSX).

## Aba "Mapa base"

Seletor de basemap (múltiplas opções implícitas — não detalhado mas presente).

## Basemap e tema

- Interface predominantemente clara
- Leaflet

## Interações / inspector

Click numa célula/cluster/município abre popup com agregados de crédito naquela região + link para detalhes.

## API e export

- Downloads bulk pela aba **Downloads**
- Por métrica: Exportar (Quantidade, Área, Volume)
- Datas e filtros codificados em URL (observado: `?date_start=2019-01-01`)

## Autenticação

Nenhuma.

## Insights para AgroJus

### Padrão diferenciado de UI (diferente do Alerta)

1. **3 abas laterais: Filtros / Camadas / Mapa base** — organização mais limpa que o Alerta que mistura tudo em um painel. **Adotar no AgroJus.**

2. **Modo "Selecionáveis" vs "Pesquisáveis"** — dar ao usuário 2 jeitos de filtrar:
   - avançado: combos encadeados
   - rápido: busca texto livre
   - Implementação: toggle no topo do painel de filtros.

3. **Visualização por métrica (Quantidade / Área / Volume)** — mesmo dado, 3 lentes. Para AgroJus, fazer equivalente em camadas:
   - DETER: por Nº alertas / por área total / por data mais recente
   - SICOR: por Nº contratos / por R$ total / por safra
   - Cada métrica → estilo de renderização diferente (cor, tamanho de bolha).

4. **Opacidade por camada** — slider dedicado (Alerta também tem). **Adicionar para cada camada ativa.**

5. **Botão Exportar por métrica** — download contextual, não genérico. **Replicar.**

6. **Date range com calendário nativo** — melhor UX que 2 sliders (como o Alerta tem). Usar componente de calendário.

7. **"Destaques"** — aba editorial/narrativa que mostra casos emblemáticos. Para AgroJus: poderia ser "Casos de impacto" (ex: "fazendas em Sorriso/MT com embargo ativo", "alertas em TIs em 2026").

### Padrão de tabs na esquerda (vs accordion)

O MapBiomas Alerta usa **painel único esquerdo** com todos os filtros empilhados.
O MapBiomas Crédito Rural usa **tabs** (Filtros / Camadas / Mapa base).

**Escolha AgroJus:** tabs é melhor para 48 camadas. Organizar:
- Tab 1: **Camadas** (árvore temática — atual `LayerTreePanel`)
- Tab 2: **Filtros** (busca, data, área)
- Tab 3: **Mapa** (basemap, opacidade global)
- Tab 4: **Exportar** (PDF, GeoJSON, CSV)

## Gaps vs AgroJus

| Feature Crédito Rural | AgroJus hoje | Prioridade |
|---|---|---|
| 3 abas laterais (Filtros/Camadas/Mapa base) | ❌ só um painel | ALTA |
| Modo Selecionáveis vs Pesquisáveis | ❌ | MÉDIA |
| Métricas alternativas (Qtd/Área/Volume) | ❌ | BAIXA |
| Opacidade por camada | ❌ | MÉDIA |
| Exportar contextual por métrica | ❌ | MÉDIA |
| Date range com calendário | ❌ | ALTA |
| Destaques editoriais | ❌ | BAIXA |
