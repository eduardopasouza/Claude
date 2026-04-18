# MapBiomas Alerta

- **URL:** https://plataforma.alerta.mapbiomas.org/mapa
- **Categoria:** mapbiomas (referência de UX de alertas + laudos)
- **Data auditoria:** 2026-04-17
- **Acesso:** público; cadastro opcional para API/download massivo

## Propósito declarado

Sistema de **alertas validados de desmatamento** integrando múltiplas fontes (DETER/INPE, SAD/Imazon, GLAD) com cruzamento automático contra CAR, UCs, TIs, embargos IBAMA, assentamentos INCRA. Cada alerta gera um **laudo individual georreferenciado** (PDF) utilizável como prova pericial.

## Layout e navegação

**Baseado em Leaflet** (não MapLibre como o Brasil). 3 zonas principais:

```
┌───────────────┬─────────────────────────────┬──────────────┐
│ FILTROS (esq) │                              │              │
│ - Vetor pres. │         MAPA                 │ LISTA        │
│ - Fonte orig. │                              │ ALERTAS      │
│ - Autoria     │   Controles à direita:       │ (dir)        │
│ - Fiscaliz.   │     - Zoom +/-               │              │
│ - Território  │     - Régua                  │ Cards dos    │
│ - Localização │     - Hist. do ponto         │ alertas      │
│               │     - Opacidade              │ visíveis     │
│ Slider data   │     - Centralizar            │              │
│ 01/2019 →     │     - Compartilhar           │ Ordem: data  │
│ 12/2025       │                              │              │
└───────────────┴─────────────────────────────┴──────────────┘
```

- **Header:** link "Alertas e Laudos" (ativo) | "Monitor da Fiscalização" | Downloads | Plugins | API | Login
- **Botão "Leia nossa nota informativa"** + **"Iniciar tour guiado"** no topo
- **Painel lateral esquerdo recolhível** ("Esconder painel")
- **Painel lateral direito recolhível** (lista de alertas)

## Filtros expostos (crítico)

Todos implementados como dropdowns/botões no painel esquerdo:

1. **Intervalo de datas** (2 sliders): 01/2019 → 12/2025
2. **Intervalo de área** (2 sliders): min-max ha
3. **Vetor de Pressão** — Todos / Agropecuária / Mineração / etc. (permite múltipla escolha)
4. **Fonte Original do Alerta** — Todas / SAD / GLAD / DETER
5. **Autorização** — Todos / Com autorização / Sem autorização (cruza com IBAMA)
6. **Embargo** — Todos / Embargados / Não embargados
7. **Território** — Todos / TIs / UCs / Assentamentos / CAR
8. **Código do alerta** — busca textual direta

## Basemap e tema

- Parâmetro `activeBaseMap=1` na URL indica sistema de **múltiplos basemaps**
- Interface **clara** predominantemente (fundo branco nos painéis, basemap claro)
- Leaflet padrão

## Ferramentas (toolbar flutuante direita)

1. **Ampliar zoom / Reduzir zoom** (+/-)
2. **Régua** — medição de distância/área
3. **Histórico do Ponto** — mostra mudanças naquela coordenada ao longo do tempo
4. **Opacidade** — slider para transparência da camada de alertas
5. **Centralizar em um ponto** — ir para lat/lon ou endereço
6. **Compartilhar** — URL com estado (observado: todos filtros em query params)

## Interações / inspector on-click

Clicar num alerta abre **popup/drawer** com:

- ID do alerta
- Data de detecção
- Fonte original (SAD/GLAD/DETER)
- Área (ha)
- Classe / vetor de pressão
- Município, UF, bioma
- Sobreposições: CAR, UC, TI, assentamento, embargo
- **Imagens antes/depois** (Landsat/Sentinel)
- **Botão "Gerar laudo"** — PDF técnico downloadável (referência CRÍTICA)
- Link "Publicado em DD/MM/AAAA"

## Lista de Alertas (painel direito)

Cards rolável com:
- Thumbnail do alerta
- Data
- Área
- Município
- Vetor de pressão
- Click → zoom ao alerta + abre popup/drawer

## URL como estado (observado)

```
/mapa?monthRange[0]=2019-01&monthRange[1]=2025-12
     &sources[0]=All
     &territoryType=all
     &authorization=all
     &embargoed=all
     &locationType=alert_code
     &activeBaseMap=1
     &map=-14.39,-56.25,4
```

Tudo serializado. Link compartilhável.

## API e export

- **API pública GraphQL** (endpoint `plataforma.alerta.mapbiomas.org/api/v2/graphql`)
- JWT bearer após login
- Queries: `allPublishedAlerts`, `alertReport`, filtros por `territoryId`, `cityId`, `startDetectedAt`
- Downloads bulk via tela "Downloads" (shapefile, CSV, GeoJSON)

## Autenticação

- Consulta: pública
- API massiva: cadastro gratuito → JWT

## Insights para AgroJus

### Padrões que devemos copiar

1. **Slider temporal duplo (início-fim)** em YYYY-MM — essencial para camadas com histórico (PRODES, DETER, MapBiomas alertas). AgroJus ❌
2. **Slider de área (min-max ha)** — filtro genial para achar "alertas > 100ha" direto. AgroJus ❌
3. **Filtros de cruzamento** ("com/sem autorização", "embargados/não embargados") — operam **em colunas já calculadas no backend**. Para AgroJus: expandir `LAYER_REGISTRY` com atributos de cruzamento.
4. **"Gerar laudo" individual por alerta** → PDF com marca d'água, metadata, imagens, mapa. Para AgroJus: botão equivalente no inspector chamando `/report/due-diligence`.
5. **Histórico do ponto** — ao clicar em qualquer coordenada, mostra timeline. Para AgroJus: botão "mostrar histórico MapBiomas deste pixel" usando Earth Engine.
6. **Opacidade por camada** — slider individual. Atualmente nosso `<GeoJSON fillOpacity=0.15>` é fixo. Adicionar controle.
7. **Lista de features no painel direito** (alternativa ao inspector) — navegar pelos alertas visíveis.
8. **URL como estado completo** — replicar com `useSearchParams` do Next.js.
9. **Régua nativa** — `leaflet-measure` ou plugin. Prioridade MÉDIA.
10. **Tour guiado** — "Iniciar tour" abre overlay passo-a-passo. Plugin `intro.js` ou similar. Prioridade BAIXA mas grande para onboarding.

### O que AgroJus faz melhor potencialmente

- Integra **MapBiomas Alerta + DataJud + DJEN + IBAMA** numa única plataforma. O MapBiomas Alerta é monotemático (só alertas); nosso mapa é multi-domínio.
- **Links diretos para ficha de imóvel** com motor jurídico + valuation. MapBiomas para no "laudo PDF".

## Gaps vs AgroJus

| Feature Alerta | AgroJus hoje | Prioridade |
|---|---|---|
| Slider temporal duplo | ❌ | ALTA |
| Slider área (min-max) | ❌ | MÉDIA |
| Filtros de cruzamento pré-calculados | ⚠️ só via overlaps por CAR | ALTA |
| Gerar PDF/laudo individual | ✅ (rota /report já existe) | integrar no inspector |
| Histórico do ponto (timeline GEE) | ❌ | MÉDIA |
| Opacidade por camada | ❌ | BAIXA |
| Lista de features no painel | ❌ | MÉDIA |
| URL como estado | ❌ | ALTA |
| Régua | ❌ | MÉDIA |
| Tour guiado onboarding | ❌ | BAIXA |
