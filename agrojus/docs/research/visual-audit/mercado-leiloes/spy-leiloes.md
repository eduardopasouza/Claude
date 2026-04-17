# Spy Leilões

- **URL:** https://www.spyleiloes.com.br/
- **Categoria:** leilao
- **Data auditoria:** 2026-04-17
- **Acesso:** trial 14 dias sem cartão; depois assinatura paga

## Propósito declarado
"Nunca mais perca um leilão de imóvel no Brasil." Agregador nacional de leilões **judiciais + extrajudiciais + venda direta**, com cobertura de +900 leiloeiros integrados e escala declarada de **200 mil leilões ativos e encerrados** / **R$ 300 bilhões em leilões ativos monitorados**.

## Layout e navegação
- **Hero** de conversão direta: headline "Nunca mais perca um leilão..." + CTA "Quero ver isso na prática".
- **Menu superior** enxuto: Login, Planos, Teste Grátis, WhatsApp.
- **Social proof** forte: logos dos parceiros (Caixa, TJ-MG, TJ-SP, TJ-SC, Bradesco, Mega Leilões, Franco Leilões, Leffa, Alfa Leilões).
- **Seções sequenciais**: Oportunidades → Planos → Tecnologias → Cobertura → Depoimentos → FAQ. Padrão SaaS moderno de vendas.
- Paleta **verde + branco + preto**, tipografia sans-serif limpa. Tom agressivo, orientado a resultado ("Decolaram", "Surreal"), copy estilo infoproduto.

## Features / dados expostos
**Catálogo de leilões** em cards horizontais (carrossel de "Oportunidades"):
- Foto do imóvel
- Tipo (Apartamento, Casa, Comercial, Área Rural, Terreno, Outro)
- Preço atual + valor avaliado + **desconto em %**
- Localização com ícone
- Datas das praças (primeira / segunda)

**Filtros** (declarados):
- Preço (min/max livre, não buckets)
- Tipo de Imóvel: Apartamento, Casa, **Área Rural**, Terreno, Comercial, Outro
- Metragem
- Modalidade: Judicial, Extrajudicial, Venda Direta
- "Apenas com fotos" (flag)
- Data
- Leiloeiros (por nome)
- Bairros
- Processos (número CNJ)
- Palavras-chave
- Uma ou duas praças
- Descontos (%)

## UX / interações
- **Mapa** de imóveis (declarado como feature)
- **Alertas por WhatsApp** inteligentes (não por e-mail — escolha deliberada de canal)
- **Favoritos** (ícone de coração nos cards)
- **Comparação** não explicitada
- Login obrigatório para ver detalhes — típico estratégia de gatewall para forçar cadastro no trial
- CTAs embutidos em várias seções, estilo direct response

## Preço e modelo de negócio
Assinatura SaaS:
- **Mensal**: R$ 197/mês (listado com desconto de R$ 300)
- **Anual**: R$ 99/mês equivalente (listado com desconto de R$ 197)
- **50% OFF primeira mensalidade**, sem taxa de adesão
- **Teste grátis 14 dias sem cartão**

Posicionamento: ferramenta profissional para investidor/advogado que compra leilão recorrentemente, não consumidor único.

## API pública (se houver)
Não mencionada publicamente. Integração provavelmente bilateral com leiloeiros (scraping + parceria comercial). Sem endpoint aberto para terceiros.

## Autenticação
- Cadastro com e-mail + telefone
- Trial 14 dias sem cartão
- Pós-trial: assinatura obrigatória para continuar vendo detalhes

## Conhecimento externo aplicável
- Spy Leilões é o **player dominante no agregador SaaS de leilões brasileiros** em 2024-26. Supera (em escala) concorrentes como Resale, LeilãoVip, Sold, PortalLeilãoImovel em coverage e polish.
- Modelo foi inspirado em Zillow/Redfin + agregadores judiciais americanos (Auction.com, Hubzu).
- Integração com tribunais é parcial: alguns TJs (MG, SP, SC) publicam em padrão estruturado (JSON/XML), outros só em PDF — raspagem é o padrão para os demais.
- **+900 leiloeiros** é número declarado, mas a cobertura efetiva tem gaps em leiloeiros regionais pequenos e em leilões administrativos municipais.
- Dor conhecida: mesmo com Spy, o usuário ainda precisa **ler o edital em PDF** para detectar riscos (ocupação, dívidas de IPTU, matrícula bloqueada, conflito possessório). Spy não tem análise de risco automatizada.
- No segmento rural (crítico para AgroJus), Spy tem "Área Rural" como categoria mas o tratamento é genérico — sem CAR, sem análise de uso do solo, sem ZARC, sem contexto agronômico.

## Insights para AgroJus
1. **Benchmark de UX a seguir**: o padrão cards-horizontais + filtros facetados + favoritos + alertas WhatsApp é referência de conversão no segmento. AgroJus deve replicar e elevar.
2. **Canal WhatsApp como default de alerta**: Spy escolheu só WhatsApp, sem e-mail. Brasil é mobile-first; isso converte mais. AgroJus deve considerar mesmo — ou WhatsApp + e-mail como opcional.
3. **Preço referência**: R$ 197/mês ou ~R$ 99/mês no anual. Isso define o teto de SaaS em PT-BR para essa categoria. AgroJus SaaS deve mirar faixa similar para o módulo leilão.
4. **Vertical AgroJus = "Spy para rural com análise"**: Spy é horizontal (urbano domina); AgroJus verticaliza no rural e adiciona a camada que Spy não tem — **parse do edital + mapa CAR + estimativa VTN + ZARC**.
5. **Imitação + extensão**: replicar filtros (desconto %, praças, modalidade) e acrescentar facetas geo (bioma, raio até ferrovia, aptidão ZARC, uso MapBiomas atual).
6. **Transparência do desconto**: mostrar desconto % como Spy faz é cliente-magnet. Adicionar "desconto vs. VTN SIMET" (diferente de vs. valor avaliado do edital, que às vezes é inflado) seria diferencial único.

## Gaps vs AgroJus (tabela)

| Dimensão | Spy Leilões | AgroJus (agregador leilão rural) |
|---|---|---|
| Escopo | Horizontal (urbano + rural) | Vertical rural-first |
| Base | +200 mil leilões | Espelhar Spy + desapropriações + Caixa FCO/Pronaf |
| Categoria rural | "Área Rural" genérica | Faceted: soja / pecuária / silvicultura / café / cerrado / amazônia |
| Análise jurídica | Nenhuma (só link PDF edital) | Parser LLM extrai riscos do edital |
| Georreferenciamento | Mapa com pin | Polígono CAR + análise MapBiomas |
| Valuation | Valor avaliado vs. preço atual | + VTN SIMET + estimativa AgroJus + comparáveis |
| Contexto agro | Zero | ZARC, CEPEA, custo Conab, precipitação |
| Alertas | WhatsApp | WhatsApp + e-mail + webhook |
| Preço | R$ 197/mês ou R$ 99/mês anual | Faixa similar para tier leilão |
| Público-alvo | Investidor de leilão generalista | Investidor rural + advogado + perito + banco |
| API | Não tem | REST pública |
| Integrações | Caixa, alguns TJs, leiloeiros | Mesmo + sistemas judiciais + CAR + SIGEF |
| Histórico | Encerrados consultáveis | Mesmo + análise de quanto lote rural realmente fechou |
