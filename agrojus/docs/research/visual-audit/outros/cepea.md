# CEPEA — Centro de Estudos Avançados em Economia Aplicada (ESALQ/USP)

- **URL:** https://www.cepea.esalq.usp.br/br (redireciona 301 para https://www.cepea.org.br/br)
- **Categoria:** mercado-dados
- **Data auditoria:** 2026-04-17
- **Acesso:** público para consulta básica; dados históricos e relatórios podem exigir cadastro

## Status da auditoria
**FALHA PARCIAL — o WebFetch detectou o redirect 301 para `cepea.org.br/br`, mas o host retornou 403 em seguida** (provavelmente WAF/Cloudflare bloqueando User-Agent não-browser). Tentativa em página interna `/indicador/soja.aspx` também retornou 403. Esta auditoria é construída a partir de conhecimento externo amplamente documentado do CEPEA, considerado **padrão-ouro de cotação agropecuária brasileira**.

## Propósito declarado
CEPEA é órgão da ESALQ/USP (Escola Superior de Agricultura Luiz de Queiroz, Piracicaba-SP) dedicado à pesquisa e divulgação de **indicadores de preços agropecuários diários**. Seus indicadores são referência nacional para contratos futuros na B3, liquidação de commodities, indexação em contratos de arrendamento e foot-e-mouth de quase toda negociação agro do país.

## Layout e navegação
Padrão institucional universitário clássico:
- **Header USP/ESALQ** com brasão, navegação em azul institucional.
- **Menu horizontal**: Institucional / Indicadores / Publicações / Boletins / Cursos / Imprensa / Contato.
- **Home**: painel de **indicadores em destaque** — cards ou tabela com preço de fechamento do dia útil anterior (boi gordo, soja, milho, café arábica, café robusta, algodão, açúcar, etanol, trigo, leite, suínos, frango, tilápia, madeira, entre outros).
- **Página por indicador**: cotação do dia + gráfico de linha (15-30 dias padrão) + tabela de últimos valores + link para série histórica + notas metodológicas + equipe responsável.

## Features / dados expostos
Indicadores CEPEA/ESALQ/BM&F publicados diariamente:
- **Boi gordo** (R$/arroba)
- **Soja Paraná** e **Soja Paranaguá** (US$/saca e R$/saca)
- **Milho ESALQ/BM&F** (R$/saca)
- **Café arábica** e **Café robusta / conilon** (R$/saca)
- **Algodão** (R$/@)
- **Açúcar cristal** (R$/50kg)
- **Etanol anidro e hidratado** (R$/litro, sem impostos)
- **Trigo PR/RS** (R$/saca)
- **Leite "CEPEA/ESALQ"** mensal
- **Bezerro, suínos, frango, tilápia**
- **Madeira (pinus, eucalipto)**

Cada indicador tem:
- Cotação diária fechada em tabela (data | preço | variação % | variação R$)
- Série histórica (mensal, semanal, diária) exportável em XLS
- Gráfico interativo simples (linha, zoom por período)
- PDF de boletim diário por cadeia
- Metodologia (amostra, praças de coleta, critérios de inclusão)

## UX / interações
- **Download XLS** nativo de série histórica é o fluxo principal de quem é data user (analista, trader, banco, seguradora, perito).
- Tabelas densas, estilo "planilha web". Não há mobile-first sério.
- Gráficos minimalistas, tons azuis institucionais.
- Tom visual **acadêmico/institucional**: paleta azul USP + cinza + branco. Zero opinião de design moderno; é sisudo, confiável.
- Navegação um pouco datada (páginas .aspx, recarregamento completo).

## Preço e modelo de negócio
- Cotação atual e série básica: **gratuita**.
- Newsletter diária de cadeia: grátis com cadastro.
- **Banco de dados histórico completo** e **assinaturas de boletins setoriais**: pagos (valores variam por cadeia; assinatura anual).
- Cursos de economia aplicada e consultoria: produtos premium.

## API pública (se houver)
**Não há API REST oficial amplamente documentada**. O fluxo oficial é:
- Download XLS manual pela página do indicador.
- Assinatura paga de boletins diários por e-mail (PDF).
- Licenciamento bilateral para empresas grandes (B3, seguradoras, tradings).

Raspagem das tabelas HTML é tecnicamente possível mas desencorajada pelos termos. Existe mercado de terceiros que vendem o CEPEA já ingerido (dashboards de trading, Bloomberg, Refinitiv).

## Autenticação
Cadastro para receber boletins; navegação básica sem login.

## Conhecimento externo aplicável
- CEPEA é **institucionalmente sagrado** no agro brasileiro. Indicador CEPEA de boi gordo, soja, milho é citado em milhões de contratos de arrendamento, parceria, CPR, CRA, swaps.
- A coleta é feita por equipe de Piracicaba via consulta diária a agentes de praça (compradores, vendedores, exportadores, frigoríficos, cooperativas) — metodologia artesanal mas rigorosa, auditada há 25+ anos.
- A B3 usa indicadores CEPEA/BM&F para liquidação de contratos futuros (boi, milho, soja, café, etanol). Isso dá blindagem institucional ao CEPEA.
- Dor conhecida: **ausência de API pública moderna**. Quem quer integrar programaticamente paga serviços de terceiros (AgroAPI, Canal Rural API, Safras API) que fazem o intermédio.
- Oportunidade: o agro brasileiro **carece de dashboard moderno** para cotações. Mobile app do CEPEA existe mas é tosco; sites de terceiros (Notícias Agrícolas, Canal Rural) exibem CEPEA com UX ainda média.

## Insights para AgroJus
1. **CEPEA é dado crítico para o valuation rural**: preço da commodity na região do imóvel é input essencial da abordagem de **renda/capitalização** da NBR 14.653-3. Sem CEPEA, não há cálculo de fluxo de caixa futuro defensável.
2. **Ingestão nativa**: AgroJus deve manter tabela interna atualizada diariamente com indicadores CEPEA por cadeia, via assinatura oficial ou parser do XLS. Mostrar "preço vigente + média 12m + tendência" em cada ficha de imóvel.
3. **Contextualização geográfica**: cruzar cotação CEPEA com **localização do imóvel + commodity dominante (via MapBiomas/ZARC) + frete até terminal**. "Essa fazenda está a 420 km de Paranaguá; preço líquido efetivo de soja é X."
4. **Componente visual forte**: AgroJus pode oferecer dashboard de cotações estilo Bloomberg-simplificado (preço, variação, gráfico 12m, correlação com dólar/weather) que o próprio CEPEA não tem bem feito. É marketing + produto ao mesmo tempo.
5. **Série histórica como diferencial de valuation**: no laudo pericial, tendência de 10-20 anos do preço é peça-chave. AgroJus entrega isso em um clique ao invés do perito baixar 12 XLSs.
6. **Licenciamento CEPEA**: importante formalizar licença comercial (provável, pago) para revender o dado no produto. Alinhar com ESALQ/USP evita problema reputacional.

## Gaps vs AgroJus (tabela)

| Dimensão | CEPEA | AgroJus |
|---|---|---|
| Propósito | Publicar indicadores diários | Usar indicadores para valuation e análise de imóvel |
| UI | Institucional, datada | Moderna, mobile-first |
| Série histórica | XLS manual | Gráfico interativo + API |
| API | Inexistente / pagos bilaterais | REST exposta (com CEPEA licenciado) |
| Contextualização geográfica | Ausente | Integração com CAR, MapBiomas, ZARC |
| Frete e logística | Ausente | Distância até porto/terminal + custo |
| Correlação multi-fator | Ausente | Commodity × câmbio × clima × logística |
| Laudo | Ausente | Gera capítulo "abordagem da renda" pronto |
| Preço | Freemium | Licença CEPEA custo interno + SaaS AgroJus |
| Público | Analista, trader, consultor | + advogado, perito, banco, investidor |
