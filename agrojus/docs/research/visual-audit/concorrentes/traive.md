# Traive

- **URL:** https://traive.ag/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público (institucional); produto B2B enterprise

## Status da auditoria
Não foi possível capturar o site via WebFetch no momento da auditoria. Tentativas em `https://traive.ag/`, `https://www.traive.ag` e `https://traive.com/` retornaram ECONNREFUSED. Pode ser bloqueio de user-agent, geofencing do DNS ou instabilidade pontual. A descrição abaixo é baseada em **conhecimento externo** sobre a empresa, explicitamente marcada, e deve ser revalidada com captura manual/screenshot antes de virar decisão de produto.

## Propósito declarado (conhecimento externo)
Traive é uma fintech com foco em **motor de inteligência artificial para crédito rural e seguro agrícola**. Posiciona-se como infraestrutura de originação e underwriting para bancos, cooperativas, tradings e insumo-financiadores. Tagline histórica: "Originação inteligente de crédito para o agro".

## Layout e navegação (conhecimento externo)
Site corporativo típico de fintech SaaS, com:
- Header: logo Traive + menu "Platform / Solutions / Customers / Company / Blog / Login".
- Hero bilingue (PT/EN), headline sobre transformar dados do agro em decisão de crédito.
- Seções por persona (bank, cooperative, insurer, input provider).
- Cases de clientes (Banco do Brasil, OCB, Yara, Stone Agro entre outros mencionados na imprensa).
- Footer com endereços em São Paulo e nos EUA, LinkedIn, Twitter.
NÃO VERIFICADO neste fetch — revalidar.

## Features principais observadas (conhecimento externo)
- **Motor de IA de análise de crédito rural** — combina dados financeiros, comportamentais, climáticos, de produtividade e geoespaciais.
- **Originação digital de operações** — fluxo do produtor cadastra, envia docs, assina.
- **Score de risco agrícola** — específico para ciclo agrícola, safras, risco climático.
- **Monitoramento pós-contratação** (provável, baseado em estágio de fintechs do setor).
- **API para parceiros** — integração com core bancário e plataforma de tradings/insumos.
- **Plataforma whitelabel** para cooperativas e bancos menores sem estrutura de crédito rural própria.

## UX / interações (conhecimento externo)
Produto provável: jornada do analista de crédito no banco. Tela de "novo caso" → carrega CPF/CNPJ → Traive puxa dados e gera score + relatório → analista aprova/rejeita/pede info adicional. Produtor tem sub-portal para enviar documentos e acompanhar. Dashboard de carteira para gestor do banco.

## Preço e modelo de negócio (conhecimento externo)
- B2B enterprise, contrato anual + taxa por operação analisada (revenue share ou per-file).
- Captou USD 41M em rodada Series B (reportado na imprensa, 2022-2023) com apoio estratégico do Banco do Brasil.
- Clientes enterprise: bancos de médio porte, cooperativas, tradings internacionais.
- Sem preço público.

## Autenticação (conhecimento externo)
Produto logado para funcionários do banco cliente e para produtores. Autenticação provável via email/senha + 2FA; integração SSO para clientes enterprise. Não usa gov.br.

## Conhecimento externo aplicável
- Fundada por brasileiros com base dupla São Paulo / Boston, forte DNA técnico (ML + dados agrícolas).
- Rodada USD 41M liderada pelo BB investimentos e fundos americanos — virou "queridinha" agtech.
- Concorre com Softfocus (no segmento analítico), Serasa Agro (em inteligência) e algumas fintechs menores.
- Foco muito forte em originação e score, fraco em assessoria ao produtor/advogado.

## Insights para AgroJus
1. **Fazer diferente:** Traive resolve o problema do BANCO (decidir se concede crédito). AgroJus resolve o problema do ADVOGADO/PRODUTOR (contestar negativa, renegociar, levar a juízo). Posição complementar, não concorrente direta.
2. **Copiar:** captação robusta (USD 41M) traduzida em UI premium. AgroJus deve ter padrão visual de fintech madura, não de ferramenta interna.
3. **Copiar:** uso de IA como core do produto, não como feature. AgroJus deve mesmo posicionar IA como motor (mIA kernel) e não como plugin.
4. **Fazer diferente:** Traive é opaco sobre metodologia do score. AgroJus pode ser explicável — mostra ao advogado QUAIS dados, QUAIS pesos, QUAIS fontes deram a decisão ambiental/creditícia, para permitir contestação.
5. **Copiar:** bilíngue PT/EN desde o dia 1 se quiser investidor/parceiro internacional.
6. **Fazer diferente:** Traive precisa de integração técnica pesada com banco (6-12 meses). AgroJus deve ter onboarding self-service em minutos.
7. **Copiar:** posicionar dados + IA + workflow como "sistema operacional" de uma função (no caso deles, crédito). AgroJus pode ser "SO da defesa agro".

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| Motor de IA de score de crédito rural | Não temos (não é foco) | BAIXA |
| Originação digital de crédito | Não temos | BAIXA |
| Relatório automatizado para banco | Parcial | MÉDIA |
| Integração SSO enterprise | Não temos | BAIXA |
| Captação/marca premium | Em construção | MÉDIA |
| Posicionamento fintech enterprise | AgroJus é prof-liberal first | ALTA (diferencial) |
| Explicabilidade do modelo IA | AgroJus pode virar diferencial | ALTA |
| API whitelabel para cooperativa | Não temos | BAIXA |

## Observação
Este arquivo deve ser revalidado com uma captura manual de https://traive.ag/ assim que o site estiver acessível, para marcar quais itens são LITERAL vs INFERIDO.
