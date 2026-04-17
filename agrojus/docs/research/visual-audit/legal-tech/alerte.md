# Alerte

- **URL:** https://www.alerte.com.br/
- **Categoria:** legal-tech
- **Data auditoria:** 2026-04-17
- **Acesso:** pago (trial gratuito de 10 dias)

## Propósito declarado

**Tagline literal:** *"Soluções jurídicas automatizadas para advogados, escritórios e empresas"*.

**Posicionamento:** plataforma de **monitoramento multi-sistema** integrando clipping de diários oficiais, intimações eletrônicas em portais (PJe, e-Proc, e-SAJ, Projudi) e novos marcos como DJE (Domicílio Judicial Eletrônico) e DET (Domicílio Eletrônico Trabalhista). Foco central: **não perder publicação/prazo**.

Números declarados: **+400 Diários Oficiais cobertos**, **+900.000 termos pesquisados diariamente**, **+210.000 recortes diários**.

## Layout e navegação

**Header fixo:**
- Logo
- Menu horizontal: Home · A Alerte · Serviços (7 sub-itens) · Parcerias · Blog · Contato
- CTA de teste gratuito
- Atalho "Disco Virtual" (entrega de arquivos)

**Hero:** destaque do "sistema exclusivo de busca com detecção de erros tipográficos" — feature chamada como diferencial principal.

**Seções abaixo do fold:**
1. Apresentação das 8 soluções
2. Diferenciadores
3. Depoimentos de clientes
4. Blog
5. Footer (contatos, endereço no Rio de Janeiro, links úteis)

**Estilo visual:** corporativo, minimalista, **tons de azul predominantes** (padrão do setor jurídico), ícones numerados para enumerar features.

## Features principais observadas

1. **Clipping de +400 Diários Oficiais** — DJs estaduais, federais, DOU
2. **Busca fuzzy / tolerante a erros de digitação** — diferencial de marketing ("erros de digitação imprevisíveis")
3. **Monitoramento de novas distribuições** — captura **antes da publicação** no diário (via varredura de portais)
4. **Intimações eletrônicas** em PJe, e-Proc, e-SAJ, Projudi (multi-sistema, integração profunda)
5. **DJE (Domicílio Judicial Eletrônico)** — monitoramento do novo canal obrigatório CNJ
6. **DET (Domicílio Eletrônico Trabalhista)** — monitoramento do canal trabalhista
7. **Robôs de extração** — automação de consultas em portais
8. **Entrega via API** — opcional, para integradores
9. **Entrega via email** — modo tradicional, digest
10. **Disco Virtual** — repositório de arquivos entregues pela plataforma
11. **Filtros personalizáveis** nos resultados de busca
12. **Teste gratuito de 10 dias** como funil de entrada

## UX / interações

- **Busca com correção ortográfica embutida** — evita falsos negativos por erro de digitação no nome do cliente ou advogado (problema real: nomes compostos, acentos, variações)
- **Resultados filtráveis** — o próprio material diz "personalização do resultado das pesquisas, com possibilidade de aplicação de filtros"
- **Canais de notificação múltiplos:** email + API + "Disco Virtual"
- **Cobertura de dois momentos:** antes da publicação (distribuição detectada em portal) e depois (clipping de DJ) — redundância proposital

Detalhes de layout de listagem/timeline **não foram expostos pelo fetch**.

## Preço e modelo de negócio

- **Sem tabela pública.** Declaração: "preço competitivo"
- **Trial gratuito de 10 dias** — curto e qualificador
- Modelo B2B: advogados individuais, escritórios, departamentos jurídicos corporativos
- Venda consultiva implícita (contato direto)

## API pública (se houver)

**Mencionada como canal de entrega**, mas sem documentação pública visível. A entrega por API é oferecida como alternativa a email/Disco Virtual, o que sugere endpoints limitados a push de alertas — não uma API de consulta aberta ao estilo Judit/Escavador.

## Autenticação

**Duas vias apresentadas** para os portais judiciais que a Alerte acessa em nome do cliente:
- Login e senha
- **Certificado digital** (A1/A3 — inferido)

A autenticação na própria plataforma Alerte é login/senha convencional (não confirmado explicitamente, mas padrão).

## Conhecimento externo aplicável

> *Marcado como conhecimento externo.*

- Alerte é empresa tradicional do setor (>15 anos), modelo **clipping jurídico** legado que evoluiu para multi-sistema
- Concorre com LexML, Megalaw, Publicações Online, Hermes — mercado maduro com pouca diferenciação
- DJE (Domicílio Judicial Eletrônico) é mandato CNJ obrigatório desde 2024-2025: toda empresa com CNPJ ativo recebe intimações via DJE. Virou categoria nova de monitoramento.
- DET (Domicílio Eletrônico Trabalhista) é equivalente na Justiça do Trabalho
- Clipping tradicional é commodity; diferenciação hoje é: (a) DJE/DET, (b) UX, (c) IA/resumo, (d) integração API

## Insights para AgroJus (pelo menos 5 concretos)

1. **Busca fuzzy é feature vendável:** "sistema que detecta erros de digitação" vira headline. No AgroJus, usar `pg_trgm` ou similar no Supabase para busca tolerante por nome de parte, advogado e órgão. Exibir no UI: "quis dizer 'José da Silva'?".

2. **Monitoramento pré-publicação:** Alerte capta distribuição antes do diário sair. AgroJus depende do DJEN que é posterior. Ganho estratégico: adicionar fontes de *distribuição* (consulta direta PJe / e-SAJ, via Intima.ai ou integração própria) para antecipar.

3. **DJE / DET como categorias explícitas no UI:** não são apenas "mais um diário" — são canais obrigatórios CNJ com prazo contando do recebimento. No `/publicacoes` criar filtro/aba dedicada: "DJEN | DJE | DET | Outros". Advogados vão buscar exatamente por isso.

4. **Canais múltiplos de entrega (email + API + repositório):** Alerte oferece três modos. Podemos oferecer: email digest, webhook, painel web, e eventual **Google Drive sync** ou **S3 bucket** para clientes grandes.

5. **"Disco Virtual" como repositório persistente:** cada publicação capturada fica salva num drive do cliente. No AgroJus, `/publicacoes/{id}` deve ter URL permanente, download PDF, histórico de versões. Cada publicação é um ativo, não um evento efêmero.

6. **Contadores em tempo real como prova social:** "+900k termos pesquisados hoje", "+210k recortes diários" — números grandes legitimam. AgroJus pode exibir "X publicações agro capturadas esta semana" num strip na landing.

7. **Detecção de erros tipográficos como proteção do cliente:** advogados cadastram nomes e esquecem acentos, hífens, variações de grafia. Implementar: ao cadastrar termo de monitoramento, sugerir variações ("você quis cadastrar também: 'Jose', 'José', 'José da Silva', 'J. Silva'?").

8. **Trial curto (10 dias) > free tier indefinido:** força decisão rápida. Melhor que freemium arrastado. Bom default para AgroJus quando abrir a comercialização.

## Gaps vs AgroJus (tabela markdown)

| Aspecto | Alerte | AgroJus (atual) | Gap / Oportunidade |
|---|---|---|---|
| Cobertura de diários | +400 | DJEN (1 fonte agregadora) | Adicionar DJs estaduais individuais |
| DJE / DET | Categoria dedicada | Não diferenciado | Criar filtros/abas por canal CNJ |
| Busca fuzzy | Destaque de marketing | Não implementado | `pg_trgm` + sugestões |
| Monitoramento pré-publicação | Sim (portais) | Não | Integração via API de tribunal |
| Canais de entrega | Email + API + Disco | Painel web | Adicionar email digest + webhook |
| Repositório persistente | "Disco Virtual" | Inferido básico | Garantir URL estável + download PDF |
| Robôs de extração | Multi-sistema | Não | Fora do roadmap próximo |
| Filtros personalizáveis | Sim | Inferido | Formalizar interface de filtros |
| Trial | 10 dias gratuitos | Inferido | Adotar modelo trial curto |
| Foco setorial | Horizontal | Agro/ambiental | Diferencial único do AgroJus |
| Prova social | Contadores grandes no site | Ausente | Adicionar counters reais |
| Autenticação | Login + certificado A1 | Só login (inferido) | Cofre A1 só se expandirmos para escrita |
