# SIMET — Sistema de Informações de Mercado de Terras (INCRA)

- **URL:** https://simet.incra.gov.br/
- **Categoria:** valuation
- **Data auditoria:** 2026-04-17
- **Acesso:** público (site institucional), mas com conteúdo dinâmico que não renderiza via fetch estático

## Status da auditoria
**PARCIAL — conteúdo HTML retornado pelo WebFetch veio praticamente vazio** (apenas título "SIMET" sem corpo). A página parece ser SPA ou com renderização server-side dependente de sessão/JavaScript. Dois fetches a páginas-pai no gov.br/incra também não trouxeram material descritivo suficiente (404 em uma, menção indireta em outra). Esta auditoria combina: (a) o pouco extraído; (b) conhecimento externo sobre o programa SIMET; (c) padrão visual gov.br.

## Propósito declarado
O SIMET é o sistema oficial do INCRA para **publicar Valor da Terra Nua (VTN) e Valor da Terra Nua para Imissão (VTI) por município**, base legal de:
- Desapropriações por interesse social para reforma agrária (art. 12 da Lei 8.629/93).
- Indenização em ações possessórias e reintegrações.
- Referência técnica para RAMT (Relatório de Análise de Mercados de Terras).
- Parametro de atualização do VTN/ITR federal.

## Layout e navegação (inferido + padrão gov.br)
- Header institucional gov.br (barra azul superior com selo federal, busca, acessibilidade, contraste).
- Menu lateral típico INCRA: "Consultas", "Planilhas", "Metodologia", "Contato".
- Corpo provavelmente com filtros por UF → Mesorregião → Microrregião → Município.
- Tabela-resultado com ano-base, VTN R$/ha por aptidão (lavoura, pastagem, silvicultura, preservação), fonte amostral.
- Exportação de planilhas XLS/XLSX é o padrão do SIMET histórico.

## Features / dados expostos (inferido)
Estrutura típica do SIMET:
- **Por município**: VTN médio, mediana, amostra (nº de transações coletadas), período.
- **Por aptidão de uso** (conforme Instrução Especial INCRA):
  - Lavoura aptidão boa
  - Lavoura aptidão regular
  - Lavoura aptidão restrita
  - Pastagem plantada
  - Silvicultura / pastagem natural
  - Preservação / restrição de uso
- **Benfeitorias reprodutivas e não-reprodutivas** (VTI componentes).
- Histórico por ano-base (o SIMET costuma publicar a cada 2-3 anos, com defasagem significativa).

## UX / interações
Padrão gov.br (Design System do governo federal):
- Tipografia Rawline/Raleway institucional, paleta azul #1351B4.
- Botões sólidos de contraste AA.
- Acessibilidade-first (alto contraste, tecla-atalho, libras).
- Experiência funcional mas engessada; sem mapa interativo, sem gráficos sparkline, sem comparação lado-a-lado. Usuário extrai dado em planilha e trabalha fora do sistema.

## Preço e modelo de negócio
Gratuito, público (dado oficial produzido com recurso federal).

## API pública (se houver)
**Não conhecida publicamente.** Historicamente SIMET só oferece download de planilhas XLS por UF/ano. Não há endpoint REST/JSON documentado.
Alternativas para ingestão programática:
- Raspar a planilha publicada a cada ciclo (PDF/XLSX).
- Usar proxy via "dados.gov.br" se o INCRA catalogar o dataset.
- Combinar com **CNIR** e **Acervo Fundiário** para cruzar VTN com imóveis.

## Autenticação
Consulta é pública. Edição/alimentação é restrita a servidores INCRA via gov.br login (SSO unificado do governo federal).

## Conhecimento externo aplicável
- O SIMET é **peça central de qualquer laudo de desapropriação**: STF e STJ exigem que o VTN seja ancorado em SIMET ou em laudo NBR 14.653-3 com amostra equivalente.
- A **defasagem de publicação** (ciclos de 2-3 anos) é a principal crítica do mercado: em regiões de valorização rápida (MATOPIBA, oeste baiano, fronteira agrícola MA/PI/TO), o VTN SIMET fica muito aquém do valor real de mercado. Advogados usam essa defasagem a favor ou contra conforme o polo.
- A metodologia SIMET segue a Instrução Especial INCRA nº 60/2003 e atualizações. Separa VTN por aptidão de uso definida pelos levantamentos do próprio INCRA.
- **Gap histórico**: não existe API pública sólida; todos os sistemas de valuation (SisDEA, peritos autônomos) baixam planilha à mão.

## Insights para AgroJus
1. **Ingestão do SIMET como baseline obrigatório**: nossa tela `/valuation` deve abrir com o VTN SIMET do município + ano-base ao digitar o código IBGE. É o "preço de referência oficial" que todo laudo precisa citar.
2. **Mostrar defasagem explicitamente**: "VTN SIMET 2022 do município X = R$ 9.800/ha. Estimativa AgroJus (comparáveis 2025-26): R$ 24.500/ha. Diferença: +150%." Isso agrega valor imediato e diferencia do SisDEA.
3. **Série histórica**: plotar VTN SIMET × estimativa AgroJus ao longo de 10 anos. Gráfico que nenhum concorrente mostra.
4. **RAMT como output**: gerar automaticamente relatório compatível com a estrutura do RAMT/INCRA para uso em desapropriações.
5. **API nossa como produto**: AgroJus pode oferecer `/api/vtn?municipio=IBGECODE&ano=2025` retornando SIMET + AgroJus estimado. Bancos e seguradoras pagariam por isso.

## Gaps vs AgroJus (tabela)

| Dimensão | SIMET/INCRA | AgroJus |
|---|---|---|
| Abrangência | Nacional por município | Nacional por município + polígono (CAR/SIGEF) |
| Granularidade | Município x aptidão | Polígono georreferenciado + uso real MapBiomas |
| Atualização | 2-3 anos de defasagem | Mensal (leilões + anúncios + ITRs) |
| Método | Amostragem INCRA em campo | Hedônico + ML + comparáveis em tempo real |
| UI | Planilhas e tabelas estáticas | Mapa interativo + série temporal + comparáveis |
| API | Ausente | REST + webhooks versionados |
| Diferencial | Autoridade legal (RAMT) | Velocidade + precisão + georreferência |
| Custo usuário | Gratuito | SaaS (mas exibe SIMET sempre) |
| Exportação | XLSX | XLSX + PDF laudo + link web + JSON |
