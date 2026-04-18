# Softfocus

- **URL:** https://www.softfocus.com.br/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público (site institucional); produtos são B2B com acesso restrito

## Propósito declarado
Empresa sediada em Pato Branco/PR, com 22 anos de atuação, que se define como "especialista em aprimorar o ciclo do crédito com soluções tecnológicas" para instituições financeiras e cooperativas de crédito. O foco é crédito rural (agro) e integrações com Proagro, Sicor e BNDES.

## Layout e navegação
- **Header:** logo "Softfocus" + tagline "Soluções tecnológicas para crédito". Menu horizontal com dropdown "Soluções" (MQ, Zoom, Proagro, Credit, Smart, Assist, Fábrica de Software), além de "Blog", "Vagas", "Softfocus", "Quem Somos", "Contato".
- **Hero:** headline grande "Especialistas em aprimorar o ciclo do crédito com soluções tecnológicas" + subheadline descrevendo os 22 anos + botão "CONHEÇA NOSSAS SOLUÇÕES".
- **Main:** grid com os 5-6 produtos em cartões (cada um com imagem mockup do produto e métrica de vaidade — "130 mil pessoas beneficiadas", "2 MI de notas fiscais", "1º produto nacional a se comunicar com BNDES").
- **Footer:** contato telefônico (46 2604-0935), e-mail, endereço no Parque Tecnológico de Pato Branco, ícones sociais (Facebook/Instagram/YouTube/LinkedIn) e links jurídicos (Privacidade, Segurança, Termos).
- Não há sidebar nem área logada visível no site público.

## Features principais observadas
- **Credit:** análise de risco de crédito, mencionando "inteligente, rápida e simplificada".
- **Zoom:** monitoramento pós-contratação de operações de crédito rural (fiscalização de projetos).
- **Proagro:** automação do enquadramento e sinistros do programa Proagro.
- **MQ:** módulo de comunicação online com BNDES.
- **Smart:** consulta automatizada de notas fiscais (verificação de destinação de crédito).
- **Assist:** solução gratuita integrada para gestão de crédito rural.
- **Fábrica de Software:** desenvolvimento sob demanda para clientes.
- Em alto nível: automação de fluxo de crédito, APIs para consumo de dados, integração com Sicor, verificação de perdas.

## UX / interações
Site é vitrine institucional puramente informacional. O fluxo é: hero → cartões de produtos → "Conheça" → página de detalhe com mockups e descrição → formulário de contato/orçamento. Nenhum trial, nenhuma demo interativa pública. Interações limitadas a scroll e click em cartão.

## Preço e modelo de negócio
Sem preços publicados. Modelo B2B enterprise com venda consultiva para bancos, cooperativas e instituições financeiras. Apenas "Assist" é declarado como gratuito. Conhecimento externo: a Softfocus é dona/operadora do MCR 2.9 e tem participação estimada em cerca de 33% dos bancos brasileiros que concedem crédito rural — mas essa métrica não aparece no site público.

## Autenticação
Nenhum login visível no site institucional. Os produtos são entregues via integração direta (API/whitelabel) ao ambiente do banco-cliente, então a autenticação real roda dentro do core bancário do cliente.

## Conhecimento externo aplicável
- Softfocus domina o nicho de software para MCR 2.9 (Manual de Crédito Rural) em cooperativas e bancos médios.
- Produtos são integrados como módulos no core bancário do cliente (não é SaaS autosserviço).
- Vende para Sicoob, Sicredi, Cresol, Unicred e parte dos bancos privados médios.
- Estratégia é "estar debaixo do capô" do banco, não ser produto de advogado/produtor rural.

## Insights para AgroJus
1. **Copiar:** a clareza de dividir o produto em módulos nomeados (Credit / Zoom / Proagro / MQ / Smart / Assist) — cada um responde a uma etapa do ciclo de crédito. AgroJus pode imitar nomeando módulos (ex.: Análise, Monitor, Compliance, Cartório, Precedentes).
2. **Fazer diferente:** Softfocus vende PARA o banco. AgroJus pode se posicionar como contra-peça — vende para advogado/produtor que OPERA COM o banco, preenchendo o gap de quem quer contestar decisão do banco.
3. **Copiar:** vitrine de métricas de vaidade no cartão do produto ("130 mil beneficiados", "2 MI de notas").
4. **Fazer diferente:** Softfocus é opaca (sem demo, sem preço, sem login público). AgroJus deve ter demo pública + preço visível para advogados que chegam sozinhos.
5. **Copiar:** integração com órgãos públicos como diferencial (BNDES, Sicor, Proagro). AgroJus pode replicar com CAR/SNCR/Sicor/MapBiomas/INCRA.
6. **Fazer diferente:** stack aparentemente WordPress institucional + entrega .NET on-prem no banco. AgroJus nasce cloud-native, multi-tenant, usável sem integração.
7. **Fazer diferente:** Softfocus trata monitoramento como "pós-contratação do banco". AgroJus pode tratar monitoramento como "pré e pós-litígio do advogado" (monitora auto ambiental, DOU, publicações).

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| Módulo de análise de risco de crédito (Credit) | Não temos scoring de crédito | BAIXA (não é foco jurídico) |
| Monitoramento pós-contrato (Zoom) | Não temos monitoramento contínuo automatizado | ALTA |
| Automação de consulta de NF-e (Smart) | Não consumimos NF-e | MÉDIA |
| Integração BNDES/Sicor (MQ) | Não temos | MÉDIA |
| Módulo Proagro | Não temos, mas é vizinho a sinistro ambiental | MÉDIA |
| Modelo institucional sem autoatendimento | AgroJus pretende ter autoatendimento | ALTA (diferencial a manter) |
| Produto posicionado PARA o banco | AgroJus posiciona para advogado/produtor | ALTA (diferencial) |
