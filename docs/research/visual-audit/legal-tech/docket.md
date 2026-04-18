# Docket

- **URL:** https://www.docket.com.br/
- **Categoria:** legal-tech
- **Data auditoria:** 2026-04-17
- **Acesso:** pago (trial disponível; preços sob cotação)

## Propósito declarado

Taglines literais confirmadas:
- **Home:** *"O novo padrão para lidar com documentos"*
- **Docket IA:** *"O leitor de documentos que agiliza a análise"*
- **Hub:** *"A plataforma para solicitar documentos"* — foco em velocidade corporativa

**Posicionamento:** plataforma de **automação documental com IA**, não puramente OCR. Três produtos:
1. **Docket IA** — leitor/analisador de documentos (contratos, petições, laudos)
2. **Hub** — solicitação automatizada de documentos em órgãos públicos
3. **Controle** — gestão centralizada do acervo documental com dashboards

Números declarados: **+35.000 órgãos públicos conectados**, **22 milhões+ de documentos processados**, **5.500+ municípios**, **32.000+ horas de trabalho manual economizadas**, **61% dos documentos entregues em 24h**.

## Layout e navegação

**Header:** logo + toggle de idioma (EN/BR) + menu principal + CTA "Teste agora nossa IA"

**Hero:** proposta de valor com três taglines rotativas/alternadas

**Seções abaixo do fold:**
1. Showcase dos três produtos (Hub, Docket IA, Controle)
2. Casos de uso (contratos, petições, laudos)
3. Métricas de resultados (70% de melhoria em saúde regulatória, 10k horas poupadas em 2 anos, 2 dias médios de implementação)
4. Cases de sucesso
5. Blog / Parcerias / Sobre / Recursos

**Footer:** links categorizados + redes sociais (YouTube, LinkedIn, Instagram) + copyright 2026 + política de privacidade

**Navegação principal:** Produtos · Soluções · Casos de Sucesso · Blog · Parcerias · Sobre · Recursos

## Features principais observadas

**Docket IA (leitor de documentos):**
- Análise de documentos em segundos
- Processa: contratos, petições, laudos
- "Teste agora nossa IA" como CTA primário (trial acessível)

**Hub (solicitação de documentos):**
- Conexão com ~35.000 órgãos públicos
- "Encontre todos os documentos públicos em poucos cliques"
- Elimina deslocamento físico
- Rastreamento de entrega com "total visibilidade"
- SLA implícito: 61% entrega em 24h

**Controle (gestão):**
- Armazenamento centralizado de documentos
- Controle total de acesso com níveis personalizados por usuário
- Automatização de tarefas, condicionantes e processos
- Controle absoluto de prazos dos documentos
- Dashboards intuitivos com relatórios em tempo real
- Implementação média: 2 dias

## UX / interações

**Busca de documentos (Hub):** interface de request — o usuário pede um documento (certidão, registro, etc.) e a plataforma roteia para o órgão competente, acompanha o trâmite e entrega digitalmente. UX tipo "one-click request + tracking".

**Visualização de documentos (IA):** leitor que destaca campos extraídos. Conteúdo específico não retornado (fetch trouxe binário JPEG na página dedicada), mas padrão da categoria é side-by-side PDF + painel de campos extraídos.

**Dashboards (Controle):** tempo real, centralizados, com foco em prazos e condicionantes (termo jurídico-regulatório importante para agro/ambiental).

## Preço e modelo de negócio

- **Sem pricing público.**
- CTA principal: "Teste agora nossa IA" → trial gratuito para qualificação
- Modelo B2B enterprise (as métricas de caso falam em "anos", "horas economizadas em 2 anos" — compra corporativa, não autoservice)
- Três produtos vendidos separadamente ou como suíte

## API pública (se houver)

**Não documentada nas páginas testadas.** Provavelmente existe para integração enterprise, mas não é tier de produto público. Contato comercial requerido.

## Autenticação

**Não detalhado nas páginas.** Padrão inferido: email/senha + SSO enterprise (Google/Microsoft) dado o perfil corporativo.

## Conhecimento externo aplicável

> *Marcado como conhecimento externo, não confirmado no fetch.*

- Docket (fundada ~2016, SP) atende principalmente área **imobiliária** e **cartorária** — solicitação automatizada de matrículas, certidões, IPTU, habite-se
- Atualmente expandindo para compliance regulatório, due diligence e contratos
- Investimento: recebeu rodadas de venture (Series A/B) e é considerada scale-up madura no legal-tech BR
- "Condicionantes" é termo-chave para licenciamento ambiental — indica que Docket mira **compliance regulatório**, inclusive ambiental
- Concorrentes diretos: Neoway (due diligence), CertDoc, Solvi (certidões)

## Insights para AgroJus (pelo menos 5 concretos)

1. **"Condicionantes" como conceito de produto:** em licenciamento ambiental, condicionante = obrigação com prazo. O Controle do Docket trata isso explicitamente. O AgroJus pode montar um módulo `/condicionantes` com timeline de obrigações vinculadas a licenças ambientais rurais (LP, LI, LO, CAR, outorga) — rastrear prazos como publicações DJEN.

2. **Dashboard de prazos como produto-raiz:** Controle vende "controle absoluto dos prazos dos seus documentos" — visão centralizada com semáforo. Nosso `/publicacoes` pode evoluir para `/prazos` unificando intimações + condicionantes + vencimentos.

3. **Métricas sociais no hero:** Docket exibe "22M+ documentos", "35k órgãos", "61% em 24h", "70% melhoria regulatória". Aumenta confiança. AgroJus pode exibir "X publicações DJEN processadas hoje", "Y advogados monitoram Z estados", "tempo médio de detecção: N minutos".

4. **Solicitação one-click + tracking:** Hub transforma burocracia ("preciso do documento X do órgão Y") em fluxo de request com entrega rastreada. Para AgroJus: feature de "solicitar CAR", "solicitar certidão de inteiro teor", "solicitar licença ambiental" — um botão, entrega assíncrona, status ao vivo.

5. **Trial acessível como CTA primário:** "Teste agora nossa IA" é botão claro, sem fricção de "fale com especialista". Para `/publicacoes` público: "Teste grátis com sua OAB" como primeiro contato.

6. **Controle de acesso por níveis de usuário:** Docket vende controle granular. Escritórios grandes têm sócios, associados, estagiários com níveis distintos. AgroJus precisa RLS Supabase + UI de roles (Admin / Advogado / Estagiário / Leitura) para escalar.

7. **"Implementação em 2 dias" como promessa:** promessa numérica curta é mais concreta que "fácil de usar". AgroJus pode prometer "primeiro monitoramento em 5 minutos" como equivalente low-touch.

8. **Docket IA como camada de valor agregado:** leitor que extrai campos vira diferencial. Para AgroJus, um leitor que extrai campos de publicações DJEN (processo, intimado, prazo, tipo de ato, órgão) em JSON estruturado + resumo LLM é feature central.

## Gaps vs AgroJus (tabela markdown)

| Aspecto | Docket | AgroJus (atual) | Gap / Oportunidade |
|---|---|---|---|
| Foco | Documentos (request + análise) | Publicações DJEN | Complementar — Docket é input, AgroJus é sinal |
| Cobertura de órgãos | 35.000 | Só DJEN (agregador) | Roadmap: adicionar fontes próprias |
| IA em documentos | Docket IA extrai campos | Não implementado | Aplicar ao texto de publicação DJEN |
| Dashboard de prazos | Core do Controle | Inferido básico | Consolidar "central de prazos" |
| Métricas sociais | Agressivas no hero | Ausentes | Adicionar counters reais |
| Solicitação de docs | Hub é one-click | Não | Feature futura (request CAR/SIGEF/CRF) |
| Trial CTA | "Teste agora" acessível | Inferido | Destacar trial sem fricção |
| Multi-usuário / RBAC | Níveis personalizados | Inferido parcial | Formalizar roles |
| Internacionalização | EN/BR toggle | Somente BR | Baixa prioridade |
| Condicionantes como entidade | Conceito de produto | Não modelado | Modelar no schema para agro/ambiental |
| Chat/suporte | Provável | ? | Adicionar Intercom ou similar |
| Implementação rápida | "2 dias" promessa | Não comunicada | Definir SLA onboarding |
