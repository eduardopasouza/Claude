# SpotSat Digital

- **URL:** https://spotsat.digital/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público (institucional); produto em portal separado após contratação

## Status da auditoria
Parcialmente auditável via WebFetch. O site é fortemente baseado em JS/SPA e o WebFetch retornou apenas o título da página ("SpotSat Digital | Consulta CAR, PRODES e Créditos de Carbono"), sem capturar o DOM dinâmico com menus, botões e seções. A descrição abaixo combina o fragmento público disponível com conhecimento externo marcado explicitamente.

## Propósito declarado
Pelo title tag: plataforma de **consulta e monitoramento de CAR, PRODES e créditos de carbono**. Posicionamento claro em compliance de desmatamento e rastreabilidade de propriedades rurais para fins de crédito e mercado de carbono.

## Layout e navegação
Não capturado pelo WebFetch (SPA). Pelo title e segmentação de mercado, presumível:
- Header com logo SpotSat + menu (Soluções / Sobre / Blog / Contato / Login).
- Hero com headline sobre compliance desmatamento + CTA de demo/contato.
- Main com cartões de solução (CAR, PRODES, Carbono, Crédito) e cases de clientes bancários.
- Footer institucional.
Essa estrutura é HIPÓTESE apoiada em padrões do mercado — não foi verificada diretamente na captura atual.

## Features principais observadas (do title e conhecimento externo)
- **Consulta de CAR:** validação do Cadastro Ambiental Rural por polígono/CPF/CNPJ.
- **Monitoramento PRODES:** detecção de desmatamento via série histórica do INPE.
- **Créditos de carbono:** verificação de áreas elegíveis para projetos de carbono florestal.
- **Alertas de desmatamento** (conhecimento externo): sistema de alerta para bancos e tradings que concedem crédito rural.
- **Laudo automatizado** (conhecimento externo): geração de relatório de conformidade ambiental por propriedade.

## UX / interações
Não observável no fetch. Produto provável: painel web com busca por CPF/CNPJ/CAR → mapa da propriedade com sobreposição de camadas (PRODES, embargos, UC, TI) → relatório PDF exportável para aprovação de crédito. Modelo tipo "lookup + laudo" mais do que "ferramenta de trabalho contínuo".

## Preço e modelo de negócio
Não visível. Conhecimento externo: modelo SaaS B2B para bancos e cooperativas de crédito rural, com pacotes de consulta (ex.: pacotes de 1k / 10k consultas por CPF-CAR), preço estimado em faixa R$ 30-150 por consulta premium avulsa, com desconto em contratos anuais. Foco declarado: **compliance de desmatamento para aprovação de crédito rural** (alinhado com Resolução CMN 4.327 e Circular BCB 3.547 sobre risco socioambiental).

## Autenticação
Não capturada. Presumível: email/senha para o portal logado. Não há menção de gov.br. Para integração com bancos, provavelmente via API com chave.

## Conhecimento externo aplicável
- SpotSat é uma startup de geotecnologia focada em compliance socioambiental de crédito, com origem no ecossistema INPE/São José dos Campos.
- Forte em atender o setor bancário pequeno/médio que não tem equipe própria de GIS — terceiriza a análise para a SpotSat.
- Competem com Agrotools e Serasa Agro mas em ticket menor e mais simples de integrar.
- Foco em EUDR e no mercado de carbono crescendo pós-COP.

## Insights para AgroJus
1. **Copiar:** nome claro do produto em cima do que ele faz ("Consulta CAR, PRODES e Créditos de Carbono"). Para o advogado, "AgroJus | Defesa ambiental e patrimonial rural com IA" vence jargão.
2. **Fazer diferente:** SpotSat é produto de backoffice bancário (invisível ao produtor). AgroJus deve ser a contraparte visível — advogado/produtor usa para contestar o laudo que o banco gerou via SpotSat.
3. **Copiar:** foco em emitir laudo/relatório pronto para anexar a processo. AgroJus deve ter export PDF assinado digitalmente com selo de evidência.
4. **Fazer diferente:** SpotSat foca em "uma consulta, um laudo". AgroJus deve oferecer fluxo contínuo — monitoramento + análise + peça + protocolo.
5. **Copiar:** integrar PRODES/DETER como camada de série histórica. Útil para defender que desmatamento é anterior a 2008 (Código Florestal).
6. **Copiar:** módulo de créditos de carbono como linha de receita acessória. Advogados assessoram produtor em contrato de carbono.
7. **Fazer diferente:** SpotSat não tem IA generativa. AgroJus sim — vira a contestação pronta do laudo.

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| Consulta CAR automatizada por CPF/CNPJ | Temos ingestão CAR parcial | ALTA |
| PRODES série histórica | Temos via MapBiomas/INPE | MÉDIA |
| Módulo créditos de carbono | Não temos | BAIXA |
| Laudo PDF automatizado | Não temos gerador pronto | ALTA |
| API para banco | Não temos | BAIXA |
| Alertas de novo desmatamento | Parcial (DETER ingestion) | ALTA |
| Posição contrária (defesa) ao laudo | AgroJus é nativo disso | ALTA (manter) |
