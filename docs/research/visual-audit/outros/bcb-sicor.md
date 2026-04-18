# BCB — Crédito Rural e SICOR

- **URL:** https://www.bcb.gov.br/estabilidadefinanceira/credrural
- **Categoria:** mercado-dados
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Status da auditoria
**PARCIAL — WebFetch retornou apenas o header "Banco Central do Brasil"** sem conteúdo substantivo do corpo da página (provavelmente SPA/Angular do BCB com hydration client-side). Testes em URL alternativa `/estabilidadefinanceira/micrrural` também retornaram HTML mínimo. Auditoria consolidada com base em conhecimento externo público do sistema SICOR e padrões BCB.

## Propósito declarado
Página institucional do BCB reunindo:
- **Normas e manuais** do Crédito Rural (MCR — Manual de Crédito Rural).
- **Estatísticas e microdados** do **SICOR — Sistema de Operações de Crédito Rural e do Proagro**.
- Plano Safra vigente (governo federal) e taxas subvencionadas.

O SICOR é a base de dados oficial em que **todas as operações de crédito rural do Brasil são registradas** — cada contrato de custeio, investimento, comercialização, industrialização, Pronaf, Pronamp, Moderfrota, Inovagro, etc. Base censitária.

## Layout e navegação
Padrão BCB: header institucional azul/amarelo/verde (cores BCB), menu lateral com seções (Normas / Dados e Estatísticas / Manuais / Proagro / Plano Safra). Páginas com muito texto corrido + links para datasets. Design utilitário, zero concessão ao "marketing".

## Features / dados expostos
- **Painel SICOR** (dashboard Power BI ou Tableau dependendo da versão): volume contratado por UF, modalidade, programa, mês, fonte de recursos, produto (soja, milho, café...), porte (pequeno/médio/grande).
- **Microdados SICOR** (downloadable CSV por ano-safra) — nível contrato: UF, município, CNPJ agente, finalidade, valor, taxa, prazo, garantia, cultura, área/cabeças.
- **Séries temporais** (SGS — Sistema Gerenciador de Séries Temporais): código numérico por série, download CSV/XLSX/JSON/XML via parâmetros na URL.
- **Relatórios Proagro** (seguro rural obrigatório em operações com recursos controlados).

## UX / interações
- **SGS** é o grande diferencial BCB — tem API REST real e documentada: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.<CODIGO>/dados?formato=json&dataInicial=...&dataFinal=...`. Esse endpoint é usado por todo o mercado financeiro.
- **Microdados SICOR**: download manual do ZIP por ano. Arquivo grande (milhões de linhas). Formato CSV estável.
- Painéis embedados (Power BI) são visualização cumulativa; o mais valioso é o CSV bruto.
- Paleta sóbria BCB (azul #003D7C + dourado/amarelo + verde bandeira).

## Preço e modelo de negócio
100% gratuito.

## API pública (se houver)
- **SGS API**: documentada, estável, JSON/CSV/XML, sem chave, sem rate limit declarado. Excelente.
- **SICOR microdados**: ZIP/CSV por ano, sem API REST direta, mas catalogado em **dados.gov.br** como dataset.
- **Open Banking BCB**: APIs para dados de produtos financeiros (não foco SICOR).

## Autenticação
Nenhuma para leitura pública. Operação de SICOR (alimentar a base) é acesso restrito às instituições financeiras cadastradas.

## Conhecimento externo aplicável
- SICOR é **padrão-ouro para análise de crédito rural** no Brasil. Pesquisas acadêmicas, bancos, tradings e AgTechs usam SICOR para entender fluxos, inadimplência, concentração por região.
- A base SICOR **não identifica o produtor pelo CPF/CNPJ** (proteção LGPD), mas tem: UF, município, cultura, área financiada, valor, taxa, prazo, fonte de recurso. Permite análise agregada por célula geo+cultura.
- **Inadimplência Proagro** é tracker importante de risco climático real na região — onde chove mal, aciona Proagro; agregando, mapeia risco sistêmico.
- Plano Safra 2025/26 tem **~R$ 516 bi** em crédito controlado — base de dados gigante.
- Dor conhecida: SICOR é rico mas **difícil de usar sem esforço de engenharia de dados** (CSVs pesados, dicionário de variáveis complexo, joins manuais entre tabelas). AgTechs pagam analistas para pré-processar. Oportunidade para AgroJus.

## Insights para AgroJus
1. **Contratar o SICOR como camada de sinal financeiro**: cruzar AgroJus com SICOR revela "nesse município, R$ X bi foram contratados para custeio de soja em 2024/25; taxa média X%; inadimplência Proagro Y%". Isso é **sinal macro de saúde do mercado** na região do imóvel.
2. **SGS API para indicadores macro**: câmbio USD/BRL, Selic, IPCA, IGPM, IC-BR (Índice de Commodities Brasil). Tudo via SGS, trivial de ingerir. Essencial para cálculos de valor presente e capitalização em valuation.
3. **Risco climático via Proagro**: heatmap de sinistros Proagro por município revela onde seca/chuva afetam mais. Input direto pro score de risco do imóvel.
4. **"Crédito rural na região" como bloco de contexto**: na ficha do imóvel, AgroJus mostra "Crédito rural contratado em 2024/25 neste município: R$ X bi | Produto dominante: soja | Inadimplência Proagro: 3,2%".
5. **Normalização de taxas do Plano Safra**: AgroJus pode oferecer calculadora "quanto custaria custear essa fazenda pelo Pronamp a taxa X? quanto pelo custeio livre a Selic+3? Qual o break-even de rentabilidade?".

## Gaps vs AgroJus (tabela)

| Dimensão | BCB/SICOR | AgroJus |
|---|---|---|
| Acesso | CSV anual, painel Power BI, SGS API | Ingere tudo, reexpõe por imóvel/região |
| Granularidade | Município + cultura + modalidade | Mesmo, aplicado a polígono do imóvel |
| UX | Técnica, data analyst oriented | Traduzida para advogado/perito/investidor |
| SGS API | Excelente para indicadores macro | Consumida nativamente |
| Risco climático | Sinistros Proagro brutos | Heatmap visual por município |
| Laudo | Dado bruto | Capítulo "conjuntura financeira" gerado |
| Plano Safra | Norma + números | Calculadora interativa por cenário |
| Atualização | Anual (microdados) + diária (SGS) | Mesma cadência espelhada |
| Público | Analista de crédito, acadêmico | + advogado, perito, banco, seguradora, investidor |
