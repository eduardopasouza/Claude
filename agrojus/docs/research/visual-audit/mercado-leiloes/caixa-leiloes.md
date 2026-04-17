# Caixa — Imóveis à Venda (SFI e Leilão)

- **URL original:** https://www.caixa.gov.br/voce/seu-imovel/imoveis-a-venda-imovel-usados/
- **URL efetiva (após redirects):** https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp
- **Categoria:** leilao
- **Data auditoria:** 2026-04-17
- **Acesso:** público para busca; cadastro exigido para ofertar/participar

## Status da auditoria
A URL institucional informada (caixa.gov.br/voce/seu-imovel/...) retornou loop de redirects (>10). A auditoria foi feita contra o sistema efetivo onde a Caixa lista e leiloa imóveis: `venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp`. Os resultados de busca em si não foram inspecionados em profundidade pelo fetch — o HTML retornado foca no formulário de busca inicial.

## Propósito declarado
"Experiência personalizada, feita para facilitar sua busca" de imóveis vendidos pela Caixa nas diversas modalidades (SFI, licitação aberta, venda direta, venda online). É o canal oficial da maior carteira de imóveis retomados do país.

## Layout e navegação
- **Breadcrumb**: Início › Produtos › Imóveis › Busca.
- **Menu lateral esquerdo**: acesso a "Minha conta", "Ex-mutuário", "Disputas", "Favoritos", "Painel do leiloeiro" — reforça que há fluxos autenticados além da busca.
- **Corpo central**: formulário progressivo em 4 etapas que refina a busca (localização → modalidade → características → valor).
- **Design**: visual antigo, típico de sistema ASP clássico da Caixa. Header com logo Caixa, paleta azul institucional #005CA9 com acentos amarelo/laranja. Não usa o design system moderno "Caixa 360".

## Features / dados expostos
Filtros disponíveis:
- **Estado** (27 UFs)
- **Cidade** (dependente da UF)
- **Modalidade de venda**: Leilão SFI - Edital Único; Licitação Aberta; Venda Online; Venda Direta Online; Exercício de Direito de Preferência.
- **Aceita financiamento Caixa?** Sim / Não / Indiferente.
- **Tipo de imóvel**: Casa / Apartamento / Outros.
- **Quartos**: 1 / 2 / 3+.
- **Vagas de garagem**.
- **Área útil**: 7 faixas.
- **Faixa de valor**: 6 faixas até R$ 750k+.

Ausências notáveis:
- Não tem filtro por bairro (só cidade).
- Sem range de valor customizável (apenas buckets fixos).
- **Sem filtro "imóvel rural"** explícito — ficam diluídos no bucket "Outros".

## UX / interações
- Formulário em 4 passos, linear (não é busca facetada tipo Airbnb).
- Resultados retornam em listagem HTML tradicional; cada imóvel abre ficha PDF com foto única, matrícula, valor mínimo, descrição do imóvel, edital completo baixável.
- Para ofertar: cadastro obrigatório (CPF + telefone + e-mail + aceite de LGPD), assinatura digital do edital, depósito de garantia quando aplicável.
- Pagamento parcelável quando o imóvel aceita financiamento Caixa (diferencial enorme vs. leilão judicial comum).
- Experiência data-dense mas visualmente pobre — um lote pode ter só uma foto granulada e texto denso.

## Preço e modelo de negócio
- Sistema gratuito para busca.
- Comissão do leiloeiro: **5% sobre o valor arrematado**, pago pelo arrematante.
- Imóveis são vendidos nas modalidades SFI (Sistema Financeiro Imobiliário) com descontos que chegam a 60-70% do valor de avaliação. Foco em residencial urbano.

## API pública (se houver)
**Não tem API oficial**. A Caixa publica periodicamente listas em PDF/XLSX por edital — esses arquivos costumam ser raspados por agregadores (Resale, Leilão Imóvel, Venda Judicial Online). Raspagem é frágil porque a URL do formulário varia por estado e o HTML é inconsistente.

## Autenticação
- **Busca**: pública.
- **Favoritos, ofertar, acompanhar disputa**: cadastro Caixa.
- **Painel do leiloeiro**: login específico para profissionais cadastrados.

## Conhecimento externo aplicável
- A Caixa é o **maior vendedor de imóveis retomados do Brasil** (estimado 10-15 mil imóveis ativos a qualquer momento). Dominância histórica em residencial urbano, minoria rural.
- Imóveis rurais na Caixa vêm do **Pronaf e FCO inadimplentes** — estoque pequeno mas existente. Costumam ser fazendas de pequeno/médio porte (50-500 ha) no Nordeste, Sul, MT.
- O modelo "Venda Direta Online" permite compra instantânea por valor fixado — similar a "buy it now" do eBay, sem lance.
- O maior diferencial da Caixa vs. leilão judicial privado: **financiamento próprio disponível**, inclusive com FGTS para imóvel residencial. Isso explica boa parte da liquidez.
- Dor conhecida do usuário: interface datada, ficha PDF pobre em fotos, sem mapa, edital com juridiquês denso. Oportunidade para agregador que traduza, geocodifique e exiba.

## Insights para AgroJus
1. **Ingerir sistematicamente os imóveis rurais da Caixa**: há goldmine diluído no bucket "Outros". AgroJus pode ser o primeiro agregador a separar "rural / urbano / industrial" e mostrar os rurais com CAR sobreposto, uso do solo MapBiomas e análise de ZARC automática.
2. **Ficha de imóvel Caixa enriquecida**: hoje o usuário vê PDF com foto ruim. Nossa tela ingeriria o mesmo lote e mostraria: foto (se houver) + mapa com polígono CAR + análise de APP/RL + precipitação histórica + histórico de uso (pasto/lavoura) + preço por ha vs. VTN SIMET do município. Isso é diferenciação pura.
3. **Modalidades como filtro de primeira classe**: leilão SFI (com financiamento) vs. venda direta (sem financiamento) vs. licitação aberta — afeta diretamente estratégia do comprador. Agregador atual ignora essa nuance.
4. **Alertas de novos lotes rurais**: usuário cadastra critério (UF + bioma + área min/max + aceita financiamento) e recebe push quando Caixa publica imóvel que bate. Matador.
5. **Risco jurídico pré-avaliado**: parsing automatizado do edital para extrair "ocupação irregular", "dívida de IPTU/ITR", "matrícula bloqueada". Hoje comprador faz isso a mão, muitas vezes erra.

## Gaps vs AgroJus (tabela)

| Dimensão | Caixa Imóveis | AgroJus (agregador de leilões futuro) |
|---|---|---|
| Público-alvo | Compradores residenciais majoritariamente | Investidores e advogados de mercado rural |
| UI | ASP clássico, 4 passos lineares | Mapa + facetas, UX 2026 |
| Separação rural vs. urbano | Inexistente (rural diluído em "Outros") | Primeira classe |
| Georreferenciamento | Endereço texto no edital | Polígono CAR/SIGEF + mapa interativo |
| Análise de imóvel | PDF estático | Enriquecimento automático (MapBiomas, ZARC, APP/RL) |
| Filtros | Buckets fixos | Faceted search, range livre |
| Alertas | Inexistente | Push/email baseado em critério |
| Análise de risco | Manual, via edital | Parser LLM do edital + red flags |
| Financiamento | Nativo Caixa | Indicado + simulador |
| Fonte de dados | Só imóveis Caixa | Caixa + BB + judicial + privado (multi-origem) |
| Comissão | 5% ao leiloeiro | Modelo SaaS + potencial revenue share com leiloeiro |
| Série histórica | Inexistente | Histórico do lote (primeira praça desértica, segunda, preço final) |
