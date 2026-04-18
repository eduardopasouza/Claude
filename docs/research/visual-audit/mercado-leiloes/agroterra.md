# Agroterra

- **URL:** https://www.agroterra.com.br/
- **Categoria:** leilao (marketplace rural especializado)
- **Data auditoria:** 2026-04-17
- **Acesso:** indeterminado (fetch falhou)

## Status da auditoria
**FALHA DE ACESSO — WebFetch retornou `ERR_TLS_CERT_ALTNAME_INVALID`** em `https://www.agroterra.com.br/` e variantes. O certificado TLS do domínio não cobre o hostname usado, o que indica ou problema de infra não resolvido no lado do host, ou bloqueio a fetchers headless via SNI. Tentativa em agrofy.com.br deu 403. Esta auditoria é integralmente baseada em conhecimento externo público do segmento.

## Propósito declarado
Agroterra Brasil é parte do grupo Agroterra (espanhol, origem ibérica) adaptado ao Brasil como **marketplace especializado em propriedades rurais**. Posicionamento: "maior portal ibero-americano de terras rurais". Foco em fazendas produtivas, sítios, áreas de expansão e reflorestamento. Menos "instituicional", mais "Zillow rural ibérico".

## Layout e navegação (inferido por conhecimento externo)
- Hero com busca por país / UF / tipo.
- Grid de destaques com foto aérea + nome da propriedade + área + preço + localização.
- Categorias por uso (pecuária, lavoura, café, olivais/vinhas na versão ibérica, silvicultura).
- Internacionalização (PT-BR, ES, PT-PT) — indicativo de presença Brasil + Espanha + Portugal + Cone Sul.
- Header e footer com seletor de país.

## Features / dados expostos (inferido)
Estrutura típica:
- Cards: foto, nome, país/UF, município, **área (ha)**, **preço total**, ícones de amenidade (água, energia, sede).
- Ficha detalhada: galeria, descrição, mapa embed (Google Maps), documentação listada, corretor responsável, telefone/WhatsApp.
- Filtros: país, UF, município, faixa de área (ha), faixa de preço, atividade principal, características (tem água, tem casa, aceita permuta, tem irrigação).

## UX / interações (inferido)
- Favoritos, alertas por e-mail.
- Contato direto com anunciante / corretor via formulário ou WhatsApp.
- Padrão marketplace com corretor humano no loop — não é leilão, é venda direta.

## Preço e modelo de negócio
- Consulta gratuita para comprador.
- Anúncio pago para vendedor (planos básico / destaque / premium) + comissão em casos de transação assistida.
- Ticket de anúncio estimado em R$ 100-500/mês na Espanha; Brasil ajustado.

## API pública (se houver)
Não conhecida.

## Autenticação
Cadastro para salvar favoritos, receber alertas, contatar anunciante.

## Conhecimento externo aplicável
- Agroterra nasceu na Espanha em 2006-2007 como portal de fincas rurais e expandiu para América Latina ~2015-2018.
- No Brasil concorre com **Reland**, **Terras Brasil**, **Agrofy Imóveis**, **FazendasBR**, seções agro de **ZAP/OLX**.
- Diferencial histórico: **inventário internacional** (mostrar fazenda brasileira para investidor europeu). Isso atrai estrangeiro procurando ativo rural na América Latina.
- Fraqueza comum do segmento: baixo rigor em dado técnico (matrícula, CAR, aptidão, ZARC, uso real). Foco é **visual + contato com corretor**, não transparência analítica.
- Base estimada Brasil: 500-2.000 anúncios ativos (ordem de grandeza menor que Reland). Pode variar bastante conforme momento.

## Insights para AgroJus
1. **Não precisamos ser marketplace** — mesmo raciocínio de Reland. AgroJus pode ser a camada de análise sobre marketplaces como Agroterra.
2. **Audiência internacional**: Agroterra traz investidor europeu para América Latina. AgroJus com **versão PT/EN/ES** + métricas padronizadas (USD/ha, R$/ha, EUR/ha) pode capturar esse público diretamente — oferecer "relatório independente" para deal cross-border.
3. **Due diligence automatizada**: investidor ibérico que nunca pisou no Cerrado precisa confiar em algo além do corretor. AgroJus pode emitir **relatório de due diligence em 1 clique**: CAR, matrícula, embargos IBAMA, histórico MapBiomas, aptidão ZARC, série de preço/ha. Isso vende.
4. **Integração potencial**: Agroterra pode virar cliente — consumir API AgroJus para enriquecer fichas com badge "Análise AgroJus" (como Carfax faz com carros usados).
5. **Padronização de métricas**: Agroterra e similares misturam preço em R$ total, R$/ha, USD/ha inconsistentemente. AgroJus pode ser referência de normalização.

## Gaps vs AgroJus (tabela)

| Dimensão | Agroterra | AgroJus |
|---|---|---|
| Modelo | Marketplace com corretor | Plataforma de análise |
| Escala Brasil | 500-2.000 anúncios estimados | Todos marketplaces agregados |
| Internacional | Sim (Espanha, Portugal, LatAm) | Potencial (PT/EN/ES) via API |
| Enriquecimento técnico | Baixo | CAR + MapBiomas + ZARC + SIMET |
| Due diligence | Manual pelo comprador | Relatório automático em PDF |
| Histórico de preço | Não exposto | Série histórica do lote |
| Validação documental | Corretor afirma | Cruzamento com SIGEF/INCRA/cartório |
| UX | Clássico marketplace imobiliário | Analítica + mapa + filtro geo |
| Incentivo | Corretor quer fechar venda | Análise independente |
| Público-alvo | Investidor + produtor | + banco, seguradora, advogado, perito |
| Monetização | Anúncio + comissão | SaaS + API |
| Normalização preço | Inconsistente | R$/ha + USD/ha + EUR/ha padronizados |
