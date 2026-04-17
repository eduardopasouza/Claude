# Judit

- **URL:** https://judit.io/
- **Categoria:** legal-tech
- **Data auditoria:** 2026-04-17
- **Acesso:** freemium (teste grátis + planos pagos, preços sob cotação)

## Propósito declarado

Tagline literal: **"Sua infraestrutura completa de dados Jurídicos"**.

Posicionamento: plataforma modular (API + UI) para centralizar acesso a dados processuais dos tribunais brasileiros. Casos de uso explicitados: análise de risco, compliance, crédito, gestão jurídica. +300 clientes corporativos declarados.

Diferencial anunciado: **"A única do mercado com monitoramento por webhook"** (afirmação de marketing da própria empresa).

## Layout e navegação

**Header** (menu principal, aparece repetido em múltiplas âncoras):
- Início | Soluções | Quem somos | Produtos (API, Miner, Plataforma, Relatório) | Planos e Preços | Cobertura | Documentação API | Ajuda | Blog | CTA "Teste Grátis" | "Entrar"

**Hero:**
- Headline grande: "Sua infraestrutura completa de dados Jurídicos"
- Dois CTAs lado a lado: "Ver Produtos" (primário) e "Agendar uma reunião" (secundário)

**Seções abaixo do fold (na ordem):**
1. Clientes — faixa com +300 empresas
2. Produtos — 4 cards (API, Plataforma, Miner, Relatório)
3. Setores atendidos
4. Depoimentos
5. FAQ
6. Contato

**Footer:** logo + endereço físico (Barra da Tijuca, RJ) + email de atendimento + links de navegação + políticas + redes sociais + CNPJ.

**Navegação secundária:** âncoras (#produtos, #contato).

## Features principais observadas

1. **Consulta em Tempo Real** — "Os resultados são retornados diretamente dos sistemas dos tribunais, sem intermediários"
2. **Histórico processual completo** — "todo o histórico judicial de pessoas físicas e jurídicas — incluindo processos arquivados e encerrados"
3. **Background Check** — inclui processos criminais, execuções penais e "mandados de prisão ativos pelo BNMP"
4. **Monitoramento contínuo** de CPFs, CNPJs e OABs — "alertas em tempo quase real"
5. **API com Webhooks** — push de eventos em vez de polling
6. **Integração em massa** — lotes de CPFs/CNPJs automatizados
7. **Cofre de Credenciais** — armazena certificado do advogado para acessar processos em segredo de justiça
8. **Dados normalizados CNJ** — seguindo tabelas processuais oficiais
9. **Cache inteligente + on-demand** — dois modos: cache rápido ou fetch fresco sob demanda
10. **JUDIT Miner** — vertical de precatórios com pipeline visual (funil Entrada → Análise → Lead → Excluídos)

## UX / interações

**Busca:** critérios múltiplos explícitos — *"Realize consultas por CPF, CNPJ, CNJ, OAB, NOME, TERMOS"*. Seis tipos de identificador aceitos.

**Resultados:**
- Lista de processos com contagem total: "250 processos encontrados"
- Cada linha exibe: número do processo + tribunal (TRF1, TJSP, TST, TRF4, TJRJ) + status badge (Nova movimentação, Monitorado, Em análise)
- **Abas de filtragem:** "Todos | Novos | Em análise" — segmentação por status direto
- **Filtros laterais:** tribunal, estado, classe, assunto, polo
- Dados estruturados por resultado: "Partes, polos, classes, assuntos, tribunal e status processual"

**Pipeline visual (Miner):** contadores por coluna (Entradas: 180, Em análise: 40, Leads: 12) — padrão kanban para tracking de oportunidades.

**Alertas:** notificação in-app tipo "Alerta enviado para 3 processos monitorados" + push via webhook.

**Histórico de consultas** fica exposto na plataforma — auditoria e reuso.

**Exportação** de resultados disponível (não detalhado formato).

## Preço e modelo de negócio

- **Sem tabela pública** no site. CTA é "Entenda qual a melhor solução para o seu negócio" → conversão via contato.
- Três produtos com planos distintos: **JUDIT API**, **JUDIT Miner**, **JUDIT Plataforma**
- **Teste Grátis** disponível no header (freemium para qualificação)
- Modelo B2B enterprise com venda consultiva (depoimentos + agendamento)

## API pública (se houver)

**Sim, API v1 documentada em `docs.judit.io/introduction`.**

Exemplo de endpoint mostrado na landing:
```
POST /v1/requests
{
  "search": {
    "search_type": "cpf",
    "search_key": "999.999.999-99"
  }
}
```

**Response:** `total_processos`, `tribunais`, `polo_passivo`, `status`

Características:
- **Sem necessidade de token de advogado** para consultas públicas: *"Retornamos todos os processos sem precisar do token"*
- **Cofre de Credenciais** opcional para processos sob segredo
- Webhook-first para monitoramento (diferencial declarado)
- Cache inteligente + modo on-demand

## Autenticação

- **API:** Token de acesso gerado no portal após criação de conta (*"ao criar uma conta no portal crie seu token e acesse a documentação da API"*)
- **Plataforma web:** login convencional (botão "Entrar" no header)
- **Cofre de Credenciais:** upload do certificado A1/A3 do advogado para acessar segredo de justiça — mesma categoria do Escavador

## Conhecimento externo aplicável

*(marcado como conhecimento externo)*

- Judit é startup mais recente (fundada ~2020-2021, RJ) posicionando-se como alternativa "developer-first" ao Escavador
- Modelo pay-per-consulta é comum no setor; Judit tende a oferecer planos híbridos (assinatura base + overage)
- Segmento preferido: fintechs e empresas de crédito (background check), não necessariamente escritórios pequenos
- Webhook como diferencial é coerente — Escavador também oferece, mas Judit posiciona mais agressivamente

## Insights para AgroJus (pelo menos 5 concretos)

1. **Abas por status direto acima do feed:** "Todos | Novos | Em análise" é UX minimalista e imediatamente legível. No `/publicacoes` podemos ter abas "Todas | Não lidas | Marcadas | Arquivadas" (ou similar por status processual: "Intimações | Decisões | Despachos").

2. **Contagem total sempre visível:** "250 processos encontrados" como subtítulo da listagem. Nosso feed deve mostrar "X publicações encontradas" de forma proeminente — sinaliza confiança na cobertura.

3. **Badges de status em cada linha:** Nova movimentação, Monitorado, Em análise. Aplicar no AgroJus com estados como "Não lida", "Prazo crítico", "Já processada". Cor + texto, não apenas cor.

4. **Pipeline visual para precatórios:** o Miner tem kanban com contadores de funil. Para AgroJus, mesmo fora de precatórios, podemos montar kanban de "oportunidades detectadas" (ex: publicações que sinalizam desapropriação ambiental com prazo para manifestação = lead para o escritório).

5. **Modo cache + on-demand explícito:** Judit deixa usuário escolher entre resposta rápida (cache) e fresca (consulta em tempo real). No AgroJus, botão "Atualizar agora" ao lado de cada publicação para forçar refresh do DJEN em vez de esperar o cron.

6. **Filtros laterais hierárquicos:** tribunal → estado → classe → assunto → polo. Podemos estruturar filtros do `/publicacoes` em árvore (Tribunal > Órgão > Tipo), não só lista plana.

7. **Single search aceitando 6 tipos (CPF, CNPJ, CNJ, OAB, Nome, Termos):** reforça padrão também visto no Escavador. Implementar detecção por regex + sugestão tipo "parece um CNJ — buscar como processo?".

8. **Cofre de credenciais para segredo de justiça:** se AgroJus quiser entrar em processos ambientais sigilosos (ex: autos administrativos com sigilo), precisamos aceitar upload de certificado A1.

9. **Histórico de consultas persistido:** usuário vê o que já pesquisou. Barato de implementar, alto valor (reusabilidade + auditoria interna do escritório).

10. **Webhook como diferencial premium:** oferecer no AgroJus webhook de "nova publicação capturada" para integradores (CRMs jurídicos). Diferencia do polling que a maioria dos concorrentes força.

## Gaps vs AgroJus (tabela markdown)

| Aspecto | Judit | AgroJus (atual) | Gap / Oportunidade |
|---|---|---|---|
| Busca polimórfica | 6 tipos (CPF, CNPJ, CNJ, OAB, Nome, Termos) | Parcial | Detecção automática por regex + placeholder rotativo |
| Tabs por status | Todos / Novos / Em análise | Inferido filtros simples | Implementar tabs primárias por estado |
| Contagem total | "X processos encontrados" proeminente | Inferido | Adicionar subtítulo com count |
| Badges de status | Monitorado, Nova movimentação | Básico | Taxonomia formal de badges |
| Pipeline kanban | Miner tem funil | Não aplicável diretamente | Kanban para leads/oportunidades detectadas |
| Cache + on-demand | Dois modos explícitos | Cache implícito | Botão "Atualizar agora" inline |
| Cobertura criminal | BNMP incluído | Fora do escopo (agro/ambiental) | Não replicar |
| Webhook | Core do produto | Não implementado | Diferencial viável |
| Background check | Pacote dedicado | Não | Pode virar vertical "due diligence rural" |
| API pay-per-call | Sim, com teste grátis | N/A | Considerar quando abrir API externa |
| Cofre credenciais | Sim | Não | Só se entrarmos em sigilo |
| Histórico consultas | Persistido | Não | Fácil de adicionar |
