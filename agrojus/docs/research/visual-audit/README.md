# Auditoria Visual Sistemática do Ecossistema AgroJus

**Início:** 2026-04-17
**Objetivo:** catalogar, site a site, o que concorrentes, fontes de dados e referências oferecem visualmente. Insights alimentam o design do frontend AgroJus v2 (mapa, ficha do imóvel, painéis).

## Método

1. Navegar em cada site via `claude-in-chrome` MCP (ou WebFetch fallback).
2. Extrair texto e estrutura interativa.
3. Escrever relatório `.md` padronizado em `visual-audit/{categoria}/{nome}.md`.
4. Atualizar este índice marcando ✅ concluído.
5. Nunca reler relatórios salvos — delegar análises agregadas a sub-agents.

## Template padrão de cada relatório

```markdown
# {Nome do serviço}

- **URL:** {url}
- **Categoria:** {concorrente|fonte-gov|mapbiomas|legal-tech|valuation|leilão}
- **Data auditoria:** YYYY-MM-DD
- **Acesso:** público|cadastro|pago

## Propósito declarado
...

## Layout e navegação
Header, sidebar, main, footer. Quais menus principais.

## Camadas/dados expostos
Lista de dados/camadas visíveis.

## Interações
Click, hover, drill-down, filtros, drawers, modais.

## Basemap(s) e tema
Claro/escuro/satélite.

## Ferramentas extras
Desenho, medição, export, compartilhamento, tour guiado.

## Dashboard/estatísticas
Agregados visuais (charts, KPIs, séries temporais).

## Inspector / detalhes on-click
O que aparece quando clica em uma feature.

## API e export
Endpoints, download, formatos.

## Autenticação
Tipo e nível exigido.

## Insights para AgroJus
Padrões que devemos incorporar, evitar, adaptar.
```

---

## Checklist de sites (48 total)

### A. Plataformas MapBiomas (6) — foco em **dashboard + legenda + árvore de temas** ✅

- [x] [`plataforma.brasil.mapbiomas.org`](mapbiomas/brasil-cobertura.md) — Cobertura LULC Coleção 10
- [x] [`plataforma.alerta.mapbiomas.org`](mapbiomas/alerta.md) — Alertas de desmatamento validados
- [x] [`plataforma.creditorural.mapbiomas.org`](mapbiomas/credito-rural.md) — Crédito × cobertura
- [x] [`plataforma.monitorfogo.mapbiomas.org`](mapbiomas/monitor-fogo.md) — Fogo mensal/anual (página não renderizou, análise por inferência)
- [x] [`plataforma.recuperacao.mapbiomas.org`](mapbiomas/recuperacao.md) — Vegetação secundária
- [x] [`plataforma.monitormineracao.mapbiomas.org`](mapbiomas/mineracao.md) — Mineração legal/ilegal

### B. Concorrentes diretos (10) ✅ — foco em **UX agro-jurídico, compliance, score**

- [x] [`softfocus.com.br`](concorrentes/softfocus.md) — MCR 2.9 (33% dos bancos BR)
- [x] [`advlabs.com.br`](concorrentes/advlabs.md) — 128 teses agro/ambiental
- [x] [`agrotools.com.br`](concorrentes/agrotools.md) — ~R$50k/mês, 1300 camadas
- [x] [`serasaagro.com.br`](concorrentes/serasa-agro.md) — Score multi-eixos
- [x] [`spotsat.digital`](concorrentes/spotsat.md) — Compliance crédito (parcial, SPA)
- [x] [`traive.ag`](concorrentes/traive.md) — IA crédito (bloqueado, externo)
- [x] [`buscaterra.com.br`](concorrentes/busca-terra.md) — ESG, LIF
- [x] [`sette.ag`](concorrentes/sette-ag.md) — Jornada crédito end-to-end
- [x] [`satelligence.com`](concorrentes/satelligence.md) — CAR + EUDR (holandeses)
- [x] [`registrorural.com.br`](concorrentes/registro-rural.md) — 16M CARs R$149/mês (bloqueado, externo)

### C. Legal tech (6) ✅ — foco em **monitoramento processual, busca, jurimetria**

- [x] [`escavador.com`](legal-tech/escavador.md) — 450M+ processos API v2 (parcial, 403 landing)
- [x] [`jusbrasil.com.br`](legal-tech/jusbrasil.md) — Jurisprudência, modelos (bloqueado, externo)
- [x] [`judit.io`](legal-tech/judit.md) — API on-demand
- [x] [`intima.ai`](legal-tech/intima-ai.md) — Automação PJe/e-SAJ (SPA mínima, externo)
- [x] [`docket.com.br`](legal-tech/docket.md) — OCR inteligente (parcial)
- [x] [`alerte.com.br`](legal-tech/alerte.md) — Monitoramento multi-sistema

### D. Fontes governamentais (12) ✅ — foco em **APIs, WFS, downloads**

- [x] [`car.gov.br`](fontes-gov/sicar.md) — Consulta pública CAR (SSL inválido registrado)
- [x] [`sigef.incra.gov.br`](fontes-gov/sigef.md) — Parcelas certificadas
- [x] [`portaldatransparencia.gov.br`](fontes-gov/portal-transparencia.md) — CEIS, CNEP, Garantia-Safra
- [x] [`consulta.ibama.gov.br`](fontes-gov/ibama-consulta.md) — Embargos (CAPTCHA registrado)
- [x] [`geo.anm.gov.br`](fontes-gov/sigmine.md) — Processos minerários
- [x] [`snirh.gov.br`](fontes-gov/ana-snirh.md) — Outorgas ANA, BHO (SPA registrada)
- [x] [`dadosabertos.web.stj.jus.br`](fontes-gov/stj-dados-abertos.md) — 13 datasets jurisprudência
- [x] [`cnj.jus.br/sistemas/datajud`](fontes-gov/datajud.md) — 88 tribunais (WAF 403 registrado)
- [x] [`comunica.pje.jus.br`](fontes-gov/djen.md) — Publicações/intimações (WAF 403 registrado)
- [x] [`lexml.gov.br`](fontes-gov/lexml.md) — Legislação (timeout registrado)
- [x] [`apitempo.inmet.gov.br`](fontes-gov/inmet.md) — Estações meteorológicas
- [x] [`sidra.ibge.gov.br`](fontes-gov/sidra-ibge.md) — PAM, PPM, Censo

### E. Valuation & avaliação (3) ✅

- [x] [`pellisistemas.com`](valuation/pelli-sisdea.md) — SisDEA desktop (WooCommerce 2008)
- [x] [`simet.incra.gov.br`](valuation/simet-incra.md) — VTI/VTN oficial (parcial)
- [x] [`ramt.incra.gov.br`](valuation/ramt-incra.md) — Relatório Análise Mercados de Terras

### F. Mercado/leilões (5) ✅

- [x] [`caixa.gov.br/leiloes`](mercado-leiloes/caixa-leiloes.md) — Leilões Caixa
- [x] [`reland.com.br`](mercado-leiloes/reland.md) — 2.600 propriedades (parcial)
- [x] [`spyleiloes.com.br`](mercado-leiloes/spy-leiloes.md) — 300k anúncios, benchmark conversion
- [x] [`portalleilaoimovel.com.br`](mercado-leiloes/portal-leilao.md) — 80k (ECONNREFUSED registrado)
- [x] [`agroterra.com.br`](mercado-leiloes/agroterra.md) — Agro especializado (falha registrada)

### G. Outros dados de mercado (6) ✅

- [x] [`cepea.esalq.usp.br`](outros/cepea.md) — Cotações (Cloudflare 403 registrado)
- [x] [`conab.gov.br`](outros/conab.md) — Safras, custos
- [x] [`bcb.gov.br`](outros/bcb-sicor.md) — SGS excelente (API ouro)
- [x] [`agroapi.cnptia.embrapa.br`](outros/embrapa-agroapi.md) — ZARC, SmartSolos (parcial)
- [x] [`dados.gov.br`](outros/dados-gov.md) — CKAN federal (estrutura)
- [x] [`map.onr.org.br`](outros/onr.md) — Mapa matrículas (offline, registrado)

---

## Progresso agregado

**Total:** 48 sites  |  **Concluído:** 48  |  **Em andamento:** 0  |  **Pendente:** 0

📄 **Síntese executiva consolidada:** [`SYNTHESIS.md`](SYNTHESIS.md)

## Insights acumulados — Onda 2 (Concorrentes, 10 sites)

**Top 5 padrões observados nos 10 concorrentes:**

1. **Opacidade de preço é regra.** 8/10 escondem preço (exigem contato comercial). Só AdvLabs (R$ 39/249) e Registro Rural (~R$ 149) publicam valores. **Gap comercial:** AgroJus pode ser transparente como diferencial real.

2. **Arquitetura modular por "motor"/"solução".** Softfocus (Credit/Zoom/Proagro/MQ/Smart/Assist), Sette (Motor Territorial/Agro/ESG/Financeiro), Serasa (Crédito Rural/Socioambiental/Inteligência). **Adotar no AgroJus:** vocabulário tipo "Motor Ambiental / Fundiário / Creditício / Jurídico".

3. **Todos atendem o CREDOR/COMPRADOR, nenhum o PRODUTOR em defesa.** Softfocus, Traive, Serasa, Agrotools, Satelligence, Sette, SpotSat. **Gap estratégico central do AgroJus.**

4. **Mapa como núcleo + drawer lateral** ao clicar em polígono (Registro Rural, Busca Terra, Agrotools, Sette, Satelligence). Confirma direção do AgroJus v2 (já implementado com LayerInspector).

5. **Sites institucionais escondem produto real** (placeholders SVG, sem screenshots). Fluxo padrão: landing → SDR → demo. AdvLabs e Registro Rural rompem isso com **trial auto-serviço** — e capturam advogados solo. **AgroJus deve ter demo pública + screenshots reais + trial sem cartão.**

**Bônus:** **IA generativa de peça jurídica é gap universal.** Zero dos 10 concorrentes oferece redação automatizada. **Moat direto do AgroJus.**

## Insights acumulados — Onda 3 (Legal Tech, 6 sites)

**Top 15 padrões observados nos 6 legal techs:**

1. **Single search bar polimórfica** (OAB/CPF/CNPJ/CNJ/Nome com detecção automática) — padrão universal.
2. **Tabs por status acima da lista** ("Todos | Novos | Em análise"). Replicável para DJEN com "Não lidas | Prazo crítico | Arquivadas".
3. **Badges coloridos de status** (cor + texto, nunca só cor).
4. **Contadores proeminentes no hero** ("250 processos encontrados", "+900k termos/dia") — prova social numérica.
5. **Monitoramento com 2 modos explícitos:** novas entidades vs já rastreadas.
6. **Webhooks como canal premium** (Judit, Escavador, Alerte). Diferencial viável.
7. **Trial curto + CTA visível** ("Teste Grátis", "10 dias").
8. **Sem preço público** é unânime; só Escavador sinaliza crédito por chamada.
9. **Cofre de certificado A1** para peticionamento (gating premium).
10. **Canais múltiplos de entrega** (email digest + webhook + repositório persistente).
11. **Resumo/extração IA tier superior** (Escavador Resumo Inteligente, Docket IA, Jusbrasil IA).
12. **Dashboards de prazos/condicionantes** (Docket Controle).
13. **Busca fuzzy tolerante a erro ortográfico** (Alerte headline) — fácil via `pg_trgm`.
14. **Pipeline visual tipo kanban** para oportunidades/leads (Judit Miner).
15. **Separação leitura (barato, Escavador/Judit) vs escrita (caro, Intima.ai)** — AgroJus deve posicionar-se como "leitura premium agro".

## Insights acumulados — Onda 4 (Fontes governamentais, 12 portais)

**Top 12 padrões dos portais gov BR:**

1. **Subdomínio de consulta separado do institucional** (SICAR, INMET, STJ, SIGEF) — split "marketing vs app".
2. **Design System Gov.br** como linguagem visual dominante (Rawline + azul institucional + cards grandes com ícones).
3. **Drill-down geográfico UF → Município** é o padrão universal de filtro — expectativa cultural.
4. **Código IBGE de município (7 dígitos)** é o identificador territorial canônico.
5. **APIs fragmentadas por paradigma:** ArcGIS REST (SIGMINE), Elasticsearch DSL (DataJud), SOAP (Hidroweb), OAI-PMH/SRU (LexML), CKAN (STJ), REST-path (SIDRA), REST JSON (INMET, Transparência). **Não existe padrão unificado — cada integração é artesanal.**
6. **Autenticação heterogênea e imatura:** maioria anônima ou token por e-mail; gov.br prata/ouro só em ações de escrita (SIGEF). Zero portal tem OAuth pleno.
7. **Rate limits raramente documentados** — exceção é Portal da Transparência (90/min diurno, 300/min madrugada). Resto bloqueia por CAPTCHA/WAF sem mensagem.
8. **Formatos legados persistem:** ODS (SIGEF), MDB Access (Hidroweb), SOAP XML (ANA), XML/RDF (LexML).
9. **SIRGAS2000 (EPSG:4674)** é o CRS brasileiro oficial — compatibilizar com WGS84 interno.
10. **"Mapa primeiro"** em portais geo — UI abre no mapa, busca vem depois.
11. **Permalink com parâmetros na URL** (SIDRA) — feature valorizada por pesquisador/advogado.
12. **Ausência quase universal de:** webhooks, alertas proativos, cruzamento entre bases, laudo PDF, dark mode, Swagger interativo, SDK moderno.

**Recomendações direto dos agents para AgroJus:**

- **Adotar Design System Gov.br como tema opcional** (toggle "modo gov.br") para usuários institucionais, default dark Forest/Onyx.
- **OAuth gov.br prata/ouro** como gate de ações sensíveis (geração de laudo oficial, compartilhamento de dossiê).
- **Documentar rate limits upfront** (`X-RateLimit-*` headers + página `/limits`).
- **Swagger/OpenAPI visível + playground "Try it"** desde dia 1 — diferencial contra o padrão gov.
- **Drill-down UF → Município → Imóvel** aceitando código IBGE-7.
- **CRS dual (SIRGAS2000 + WGS84)** negociáveis por query param.
- **Permalink total de estado na URL** (filtros, zoom, layer, data) — reusar cultura SIDRA.
- **Formatos de saída múltiplos:** CSV + Parquet + GeoJSON + **PDF laudo** (último é o artefato final que o advogado quer).
- **Killer features ausentes no gov:** webhook por imóvel/OAB/processo, laudo PDF automático, cruzamento CAR × SIGEF × SIGMINE × embargos, timeline temporal MapBiomas integrada, alerta de mudança normativa.

## Insights acumulados — Onda 5 (Valuation/Mercado/Leilões, 14 sites)

**Valuation (SisDEA + SIMET + RAMT):** mercado estagnado visualmente.
- SisDEA vende em 2026 como e-commerce WooCommerce de 2008, zero screenshot dinâmico
- SIMET e RAMT são "biblioteca digital gov.br" (listas de estados + PDFs + XLS manuais)
- NBR 14.653 vive em PDFs e manuais, **nunca como motor de validação inline**
- Defasagem de dados 2-4 anos é norma silenciosa

**Mercado/Leilões (Caixa/Reland/Spy/Portal/Agroterra):**
- Padrão UX: cards horizontais + filtros UF/tipo/valor + mapa com pin + alertas WhatsApp + SaaS R$ 99-197/mês + login gateway
- **Spy Leilões** é benchmark conversion (200k leilões, 900 leiloeiros)
- **Ninguém trata "rural" como primeira classe** — diluído em "Outros" ou "Área Rural" genérica
- **Ausência universal:** histórico de preço do lote, parser de edital, análise jurídica automatizada

**Outros dados (CEPEA/CONAB/BCB/Embrapa/dados.gov/ONR):**
- CEPEA é padrão-ouro de cotação mas sem API moderna
- **BCB SGS é exemplo raro de API pública excelente**
- Embrapa AgroAPI é marketplace API bem desenhado mas subutilizado
- dados.gov.br é CKAN funcional, metadados irregulares
- ONR fragmentado (map.onr.org.br offline em abril/2026)
- Todos entregam dado bruto, **ninguém entrega contexto aplicado ao imóvel rural específico**

**Ideias concretas capturadas para AgroJus:**

**Tela `/valuation`:**
1. Input CAR/SIGEF/matrícula/coordenada → tabs Comparativo/Renda/Evolutivo/Capitalização
2. Bloco "oficial baseline" topo: VTN SIMET + RAMT + data-base + defasagem explícita
3. Motor NBR 14.653-3 com Grau de Fundamentação + Grau de Precisão + IC 80% inline
4. Capítulo "renda" automático: Custo CONAB − Receita (CEPEA × ZARC) = margem → valor-terra capitalizado
5. Série histórica preço/ha 10+ anos (leilões + anúncios + SIMET) no mesmo gráfico
6. Export: PDF laudo com ART + capa + memorial + JSON auditável + permalink versionado

**Agregador de leilões:**
1. **Verticalizar rural como categoria primária** (soja/pasto/café/silvicultura/cerrado/amazônia) com ícones
2. Deduplicação Caixa + Spy + Portal Leilão + TJs via hash (matrícula + CAR + endereço)
3. **Parser LLM do edital:** ocupação, dívida IPTU/ITR, matrícula bloqueada, conflito possessório → red flags
4. Enriquecimento geo: polígono CAR + uso MapBiomas 10a + APP/RL + embargos IBAMA + ZARC aptidão
5. **Desconto vs. VTN SIMET** (não só vs. avaliado do edital — esse é inflado)
6. Alertas WhatsApp + email + webhook, facetas avançadas (bioma, raio até porto, aceita fin. Caixa)
7. **Histórico do lote:** primeira praça deserta → segunda → preço final. **Transparência que ninguém entrega.**

## Insights acumulados — Onda 1 (MapBiomas)

**Padrão visual dominante nas 6 plataformas:**

1. **Árvore temática lateral esquerda** em accordion hierárquico com 4 níveis (Cobertura), ou **tabs** (Filtros/Camadas/Mapa base) em algumas
2. **Dashboard inferior com estatísticas** (MapBiomas Brasil/Cobertura é referência-ouro)
3. **Slider temporal duplo** (início/fim) em mês-ano ou ano simples
4. **Legenda dinâmica** no painel direito com classes clicáveis ("Ver só esta")
5. **URL com estado serializado** — todos os filtros em query params para compartilhamento
6. **Seletor de região hierárquico** — Brasil → Bioma → Estado → Município → AOI customizada
7. **API documentada** exposta no header (Recuperação)
8. **Dialog de fontes** no primeiro acesso mostrando transparência das bases cruzadas (Mineração)
9. **Busca cross-field** aceitando código processo OU nome titular no mesmo campo
10. **Botões "Exportar" contextuais** por métrica, não genéricos

**Top 10 features prioritárias a incorporar no AgroJus (por ALTA prioridade):**

| # | Feature | Origem | AgroJus hoje |
|---|---|---|---|
| 1 | Painel lateral com **tabs** (Camadas/Filtros/Mapa base/Exportar) | Crédito Rural | só painel único |
| 2 | **Slider temporal duplo** YYYY-MM | Alerta | ❌ |
| 3 | **URL com estado serializado** | Todos | ❌ |
| 4 | **Dashboard inferior com KPIs + série temporal** | Brasil/Cobertura | parcial |
| 5 | **Múltiplos identificadores** no painel (CAR + Embargo + CNPJ + CNJ) | Recuperação | só OmniSearch único |
| 6 | **Legenda dinâmica painel direito** com "Ver só esta" | Brasil/Cobertura | ❌ |
| 7 | **Combos encadeados** (UF→município→bioma) | Recuperação | ❌ |
| 8 | **Lista de features visíveis** painel direito | Alerta | ❌ |
| 9 | **Opacidade por camada** | Alerta + Crédito | ❌ |
| 10 | **Régua + Histórico do ponto + Lat/Lon input** toolbar | Alerta + Mineração | ❌ |
