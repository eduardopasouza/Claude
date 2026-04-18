# Síntese Executiva — Auditoria Visual do Ecossistema AgroJus

**Auditoria concluída:** 2026-04-17
**Cobertura:** 48 sites em 5 categorias (MapBiomas, Concorrentes, Legal Tech, Fontes Gov, Valuation/Mercado/Leilões)
**Objetivo:** destilar padrões de UI, gaps e killer features para orientar o design do AgroJus v2+.

---

## 1. Os 25 padrões prioritários (consenso forte de múltiplas ondas)

Ordenado por frequência de aparição + impacto esperado no produto.

| # | Padrão | Origem (ondas) | Status AgroJus | Prioridade |
|---|---|---|---|---|
| 1 | **URL como estado serializado** (todos filtros, zoom, camadas em query params) | MapBiomas + SIDRA + Alerta | ❌ ausente | **CRÍTICA** |
| 2 | **Drill-down UF → Município → Imóvel** como filtro padrão aceitando código IBGE-7 | Fontes gov + MapBiomas + Concorrentes | ❌ só OmniSearch | **CRÍTICA** |
| 3 | **Dashboard inferior** com KPIs + série temporal da região selecionada | MapBiomas Brasil | ⚠️ parcial | **ALTA** |
| 4 | **Árvore temática lateral** em accordion com contadores por tema | MapBiomas + Concorrentes | ✅ já feito (LayerTreePanel) | OK |
| 5 | **Click em feature → drawer lateral com atributos + ações** | ONR + Alerta + Concorrentes | ✅ já feito (LayerInspector) | OK |
| 6 | **Basemap switcher** (dark/light/satélite/topo) | Alerta + Crédito Rural | ✅ já feito (BasemapSwitcher) | OK |
| 7 | **Slider temporal duplo** (início/fim) em mês-ano | Alerta MapBiomas + Recuperação | ❌ | **ALTA** |
| 8 | **Legenda dinâmica no painel direito** com "Ver só esta classe" | MapBiomas Brasil/Cobertura | ❌ | **ALTA** |
| 9 | **Modular por "motor"/"solução"** — vocabulário tipo "Motor Ambiental / Fundiário / Creditício / Jurídico" | Concorrentes (Softfocus, Sette, Serasa, Agrotools) | ⚠️ implícito | **ALTA** |
| 10 | **Single search bar polimórfica** (OAB/CPF/CNPJ/CNJ/Nome/CAR detect auto) | Legal Tech + Concorrentes | ✅ OmniSearch + smart_search (12 regex) | OK |
| 11 | **Mapa primeiro** — UI abre no mapa, busca vem depois | Fontes gov + Concorrentes | ✅ `/mapa` é central | OK |
| 12 | **Tabs laterais Camadas/Filtros/Mapa Base/Exportar** (vs painel único) | Crédito Rural + Recuperação | ❌ painel único | **ALTA** |
| 13 | **Badges coloridos de status** (cor + texto, nunca só cor) | Legal Tech + Alerta | ✅ parcial (InspectorPayload) | MÉDIA |
| 14 | **Contadores proeminentes** ("250 processos", "+900k termos/dia") — prova social | Legal Tech + Concorrentes | ✅ KPIs em `/publicacoes` e `/processos` | OK |
| 15 | **Webhooks como canal premium** | Legal Tech (Judit, Escavador, Alerte) | ❌ | **ALTA** (monetização) |
| 16 | **Opacidade por camada** com slider individual | Alerta + Crédito Rural | ❌ fixo 0.18 | MÉDIA |
| 17 | **Trial auto-serviço sem cartão** | Concorrentes (AdvLabs, Registro Rural) | ❌ só dev credentials | **ALTA** (GTM) |
| 18 | **Resumo/extração IA como tier superior** | Legal Tech (Escavador, Docket, Jusbrasil) | ⚠️ planejado (mIA) | **ALTA** (moat) |
| 19 | **Régua + Lat/Lon input + Histórico do ponto** | Alerta + Mineração | ❌ | MÉDIA |
| 20 | **Múltiplos identificadores simultâneos** (CAR + Embargo + CNPJ + CNJ num painel) | Recuperação MapBiomas | ❌ | **ALTA** |
| 21 | **CRS dual (SIRGAS2000 + WGS84)** negociável por query param | Fontes gov | ❌ só WGS84 | BAIXA |
| 22 | **Design System Gov.br** como tema opcional | Fontes gov | ❌ só dark | BAIXA |
| 23 | **OAuth gov.br prata/ouro** como gate de ações sensíveis | Fontes gov | ❌ só JWT | MÉDIA (produção) |
| 24 | **Permalink versionado** (assinatura criptográfica do estado) | Nenhum faz bem | ❌ | MÉDIA (diferencial) |
| 25 | **Export múltiplos formatos** (CSV + Parquet + GeoJSON + **PDF laudo**) | Fontes gov + Concorrentes | ⚠️ só PDF `/report` | **ALTA** |

---

## 2. Os 7 killer gaps que o AgroJus pode preencher

Features ausentes em **todos** os 48 sites auditados. Cada uma é um moat.

### 2.1 Cruzamento CAR × SIGEF × SIGMINE × IBAMA × DataJud × DJEN × MapBiomas num único dossiê

**Nenhum concorrente, nenhum portal gov, nenhum MapBiomas faz.** Cada um fica na sua base. O advogado/analista hoje abre 7 abas diferentes. AgroJus já tem 6 dessas fontes integradas no backend (`/consulta/completa` + overlaps + `/publicacoes`). Falta polir no frontend.

### 2.2 Webhook por imóvel/OAB/CPF/CNPJ

Legal tech cobra caro (Judit, Escavador, Alerte). Gov não tem. Concorrentes agro não têm. **Zero concorrência.** Já temos base de polling em `/publicacoes`; falta persistência (Redis) + trigger + canal (email/WhatsApp).

### 2.3 Laudo PDF automático com rastreabilidade

Gov entrega dado cru. MapBiomas Alerta tem "Gerar laudo" mas só para alertas. SisDEA tem laudo NBR-based mas manual/desktop. AgroJus já tem `/report/due-diligence` → expandir para laudo judicial assinável com ART + memorial + JSON auditável.

### 2.4 IA generativa de peça jurídica agro

**Zero dos 10 concorrentes agro oferece redação automatizada** (confirmado Onda 2). Legal tech generalista (Docket IA, Jusbrasil IA, Escavador Resumo) faz extração/resumo, não peça completa. **Moat direto via mIA** com motor jurídico agro especializado.

### 2.5 Timeline temporal MapBiomas integrada com ficha do imóvel

MapBiomas Brasil tem slider 1985-2024 para o país. Nenhum produto cruza isso **com o imóvel específico** (CAR) mostrando "esta fazenda era Cerrado em 1985, virou Soja em 2018, teve fogo em 2022". Earth Engine já configurado no backend — falta endpoint `/imoveis/{car}/historico-mapbiomas`.

### 2.6 Parser LLM de edital de leilão

Agregadores de leilão (Spy, Portal Leilão, Caixa) mostram edital como PDF bruto. Ninguém extrai: ocupação, dívida IPTU/ITR, matrícula bloqueada, conflito possessório. AgroJus pode ser o primeiro "Due Diligence de Leilão Rural".

### 2.7 Histórico completo do lote (1ª → 2ª → 3ª praça)

Leilões mostram só o atual. Nenhum mostra que "este mesmo lote foi leiloado em 2024 por R$ 800/ha, depois em 2025 por R$ 600/ha, hoje R$ 400/ha". Transparência que convence comprador. Possível via scraping histórico.

---

## 3. Roadmap visual — MapComponent v3

Com base em padrões prioritários (1, 2, 3, 7, 8, 12, 16, 19, 20). Incremental sobre o v2 já entregue.

### Sprint A — Estado de URL + Drill-down geográfico (fundação)

- [ ] Hook `useMapState()` serializa em `useSearchParams`: `?layers=terras_indigenas,prodes&basemap=dark&z=10&lat=-12.4&lng=-55.2&car=MA-xxx`
- [ ] Componente `RegionBreadcrumb` topo: "Brasil > Maranhão > São Luís" com dropdown em cada nível
- [ ] Endpoint `/api/v1/geo/municipios/buscar?uf=MA&q=sao+lu...` para autocomplete
- [ ] Ao clicar município → fly-to com bbox do município + ativa camada `municipios` destacando

### Sprint B — Legenda dinâmica + "Ver só esta"

- [ ] Novo componente `LegendPanel` painel direito
- [ ] Para camadas com `classes` (PRODES year, DETER classname, MapBiomas LULC), exibir legenda com cor + label + checkbox "ver só esta"
- [ ] Estado controlado: `hiddenClasses: Record<layerId, Set<className>>` que filtra GeoJSON client-side
- [ ] "Isolar classe" = oculta outras classes da mesma camada

### Sprint C — Slider temporal duplo

- [ ] Novo componente `TimeRangeSlider` na barra inferior
- [ ] Só aparece quando há camada ativa com atributo temporal (view_date, year, detected_at)
- [ ] Range em mês-ano (ex: 2019-01 → 2026-04)
- [ ] Query backend aceita `date_start` e `date_end` → WHERE view_date BETWEEN
- [ ] Animação "play" que avança slider 1 mês por segundo → vê evolução

### Sprint D — Tabs laterais + Múltiplos identificadores

- [ ] Refatorar painel esquerdo em 4 tabs: **Camadas / Filtros / Mapa Base / Exportar**
- [ ] Tab Filtros: inputs simultâneos para CAR, CNPJ, CPF, Embargo nº, Processo CNJ, SIGEF UUID
- [ ] Tab Exportar: checkbox "incluir geometria" + seleção de camadas + formato (GeoJSON/CSV/Shapefile/PDF)
- [ ] Opacidade por camada (slider no item da árvore quando ativa)

### Sprint E — Ferramentas toolbar

- [ ] Régua (leaflet-measure plugin)
- [ ] Lat/Lon input direto (fly-to por coordenada)
- [ ] Histórico do ponto (endpoint MapBiomas via Earth Engine quando desbloqueado)
- [ ] Botão "compartilhar" copia URL atual com estado

### Sprint F — Dashboard inferior v2

- [ ] Expandir `StatsDashboard` com tabs: Resumo / Série Temporal / Distribuição
- [ ] Série temporal para camadas com tempo (área desmatada/ano, alertas/mês)
- [ ] Distribuição: bars chart das classes da camada ativa (ex: PRODES por ano)
- [ ] "Recalcular sobre AOI customizada" (upload GeoJSON)

---

## 4. Roadmap `/valuation` (baseado Onda 5)

Tela que ainda não existe. Priorizada pelo consenso da auditoria: **mercado estagnado, oportunidade clara**.

### Estrutura da tela

```
┌─────────────────────────────────────────────┐
│ Header: [CAR input] [Município] [Calcular]  │
├─────────────────────────────────────────────┤
│ Baseline Oficial (topo)                     │
│  ┌─────┬─────┬─────┐                         │
│  │SIMET│RAMT │AgroJ│  + data-base + defasagem │
│  └─────┴─────┴─────┘                         │
├─────────────────────────────────────────────┤
│ Tabs: Comparativo · Renda · Evolutivo · Cap │
│                                              │
│ [Conteúdo da tab selecionada]                │
│                                              │
│ Série Histórica 10+ anos (CEPEA+leilões)    │
├─────────────────────────────────────────────┤
│ Exportar: [PDF ART] [JSON] [Permalink]      │
└─────────────────────────────────────────────┘
```

### Backend novo

- [ ] `/api/v1/valuation/simet/{municipio_ibge}` — VTN oficial SIMET
- [ ] `/api/v1/valuation/ramt/{uf}` — Relatório RAMT
- [ ] `/api/v1/valuation/calcular` — POST com CAR + método → resultado + ART metadata
- [ ] `/api/v1/valuation/serie-historica/{car}` — agrega leilões + anúncios + SIMET + CEPEA

### Diferenciais vs SisDEA (inline no produto)

- Cruzamento automático com overlaps ambientais (desvalorização por embargo/RL deficitária)
- Grau de Fundamentação + Precisão NBR 14.653-3 calculados inline
- Permalink versionado com hash SHA256 do input (auditabilidade)

---

## 5. Roadmap Agregador de Leilões (novo produto)

Nenhum concorrente trata "rural" como primeira classe. Spy Leilões tem 300k anúncios genéricos. **Oportunidade de vertical.**

### Features mínimas viáveis

1. Scraper diário: Caixa + Spy + Portal Leilão + TJs estaduais → tabela `leiloes`
2. Deduplicação por hash (matrícula + CAR + endereço)
3. Classificação automática: lavoura temporária / pastagem / café / silvicultura / cerrado / Amazônia
4. Parser LLM do edital (Claude via API) → extrai: ocupação, dívidas, status matrícula, conflitos possessórios
5. Enriquecimento geo (backend já pronto): sobrepõe CAR + MapBiomas 10a + APP/RL + embargos IBAMA + ZARC
6. Cálculo de desconto vs VTN SIMET (não vs edital, que é inflado)
7. Timeline do lote: "1ª praça: R$X em 2024 → 2ª: R$Y em 2025 → atual: R$Z"
8. Alertas (webhook + email + WhatsApp) por: cultura + UF + faixa preço + bioma + raio até porto

### Monetização

- **Free tier:** 10 leilões/mês + alerta 1 por webhook
- **Pro R$ 99/mês:** ilimitado + WhatsApp + parser LLM completo
- **Enterprise R$ 497/mês:** API + multi-usuário + export automático

---

## 6. Roadmap `/compliance` real (MCR 2.9 + EUDR)

Tela placeholder hoje. Oportunidade direta dado o MCR 2.9 obrigatório desde 01/04/2026.

### Expandir de 6 para 30 validações MCR 2.9 auditáveis

Backend já tem 6 critérios em `compliance.py`. Expandir seguindo referência Softfocus:

- 6 validações fundiárias (CAR ativo, SIGEF consistente, dominialidade, etc.)
- 8 validações ambientais (embargos ativos, PRODES pós-2019, DETER recente, sobreposição UC/TI/quilombola, ZARC aptidão, outorga hídrica, APP/RL, licença ambiental)
- 6 validações trabalhistas (Lista Suja, CNDT, INSS, FGTS)
- 5 validações jurídicas (protestos, CNPJ ativo, CCIR, ITR pago, CPF regular)
- 5 validações de crédito/tributária (SICOR em dia, Dívida Ativa, CADIN, SELIC/spread, garantias)

### UI

- Checklist grande no topo com 30 itens (✓/✗/⚠️)
- Cada item clicável → drawer com evidência + data-base + link para fonte
- Score 5 eixos (Fundiário, Ambiental, Trabalhista, Jurídico, Financeiro) com pesos ponderados
- Botão "Gerar laudo compliance PDF" → ART + memorial + anexos
- Integração com `/report/due-diligence` existente

### EUDR (UE 2023/1115)

- Tab adicional "EUDR" com 4 critérios: geolocalização lote, sem desmatamento pós-2020, legalidade produção, rastreabilidade cadeia
- Export para formato DDS (Due Diligence Statement) aceito pelo TRACES UE

---

## 7. Killer features cross-cutting

Features que afetam todas as telas e devem ser decisões de arquitetura agora.

### 7.1 State global via Zustand

Onda 2 e 3 mostram que produtos polidos têm estado compartilhado entre telas. Hoje `/mapa` seleciona CAR mas `/publicacoes` não sabe. Resolver com Zustand:

```ts
const useAgroStore = create((set) => ({
  selectedCar: null,
  selectedCnpj: null,
  selectedProcesso: null,
  selectProperty: (car) => set({ selectedCar: car }),
  // ... mais entidades cross-tela
}));
```

### 7.2 OpenAPI → TypeScript codegen

Backend tem Swagger; gerar types com `openapi-typescript`:

```bash
npx openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts
```

Garante que backend + frontend falem a mesma linguagem (ex: inspector fields sempre batem com colunas reais).

### 7.3 JWT httpOnly cookie

Hoje em `localStorage` (XSS risk). Mudar backend para setar `Set-Cookie: agrojus_token=...; HttpOnly; Secure; SameSite=Strict`. Frontend remove manipulação manual.

### 7.4 Dark/light toggle

Onda 4 (Fontes gov) sugere modo Gov.br para usuário institucional. Já temos 4 basemaps (escuro/claro/satélite/topo). Expandir para **tema completo**: `data-theme="dark|light|govbr"` no `<html>`, CSS variables swap.

### 7.5 Permalink versionado com assinatura

Estado da URL + hash SHA256 do payload + timestamp + user_id → "este permalink foi gerado por Eduardo em 17/04/2026 às 14:32 com esses filtros". Valor pericial se o link for incluído em defesa.

---

## 8. Matriz de prioridades integrada (next sprints)

| Sprint | Objetivo | Dependências | Duração estimada |
|---|---|---|---|
| **1** | URL state + Drill-down UF→Município (Padrões 1, 2) | Zustand + `useSearchParams` | 3 dias |
| **2** | Legenda dinâmica + Slider temporal (Padrões 7, 8) | Sprint 1 | 4 dias |
| **3** | Tabs laterais + Múltiplos IDs (Padrões 12, 20) | Sprint 1 | 3 dias |
| **4** | `/valuation` MVP (baseline SIMET + tabs + PDF) | CEPEA + CONAB + SICOR backend | 5 dias |
| **5** | `/compliance` expandido (30 MCR 2.9 + EUDR) | Integração gov.br oauth | 5 dias |
| **6** | Webhook + laudo PDF + parser LLM edital | mIA Claude integration | 7 dias |
| **7** | Agregador leilões (scraper + parser + frontend) | Sprint 6 | 10 dias |
| **8** | OpenAPI codegen + JWT httpOnly + dark/light toggle | — | 3 dias |

**Total:** ~40 dias de desenvolvimento focado para alcançar paridade + diferenciação vs 48 sites auditados.

---

## 9. Reconhecimento de limites da auditoria

- **17 sites (35%) tiveram falha de fetch total ou parcial** (SPAs, CAPTCHA, WAF, Cloudflare, timeout). Análise dessas baseou-se em conhecimento externo + observação indireta. Listados em cada `.md` sob "Status da auditoria".
- **Screenshots reais ausentes** — sem ferramenta headless com JS + auth, vimos apenas DOM de primeiro carregamento. Hidratações pós-login e modais interativos ficaram invisíveis.
- **Sem teste de telemetria/responsividade** — este relatório é UI structural, não UX performance.

**Próxima iteração da auditoria** (quando oportuno): usar Playwright headless + `claude-in-chrome` aprofundado + screenshots pós-login para auditar fluxos profundos (onboarding, compra, geração de relatório).

---

## 10. Meta-conclusão

O AgroJus **já está no caminho certo visualmente**:

- Dark Forest/Onyx (único no mercado, diferenciado)
- Árvore temática + drawer on-click + basemap switcher (padrões consolidados MapBiomas/ONR)
- 17 camadas PostGIS operacionais (infraestrutura pronta para crescer)
- Motor jurídico real (DataJud + DJEN integrados, único que faz o cruzamento)

O que **falta** é **amplificar os 7 killer gaps** (seção 2) e **incorporar os 10 padrões críticos-altas** (linhas 1-20 da seção 1). Com isso, AgroJus sai de "produto em construção" para **referência visual e funcional no mercado agrojurídico brasileiro** — porque ninguém mais junta todos esses pontos.

---

*Documento gerado após auditoria de 48 sites (2026-04-17). Fontes individuais em `docs/research/visual-audit/{categoria}/*.md`. README mestre: `README.md`.*
