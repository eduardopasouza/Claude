# AdvLabs

- **URL:** https://advlabs.com.br/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público para cadastro; aplicativo em app.advlabs.com.br após login (trial 7 dias + pago)

## Propósito declarado
"Solução definitiva para profissionais que atuam na área Ambiental." Tagline: "Simples de Usar. Poderoso para Atuar." Plataforma multi-perfil (advogados, servidores públicos, biólogos, engenheiros, gestores/consultores) focada em direito ambiental, unindo banco de teses, modelos de peças, monitoramento de autos de infração e gestão de escritório.

## Layout e navegação
- **Header:** logo AdvLabs, menu horizontal com "Recursos", "Dúvidas", "Manual", "Teses", "Modelos", "Contato", botão "Login" (leva para app.advlabs.com.br) e ícones sociais (Facebook, LinkedIn, YouTube, Instagram). Tem links secundários "Comunidade Ambiental" e "Direito Ambiental Experience 2026" — indício de que a marca monta evento presencial próprio.
- **Hero:** headline "Simples de Usar. Poderoso para Atuar." + descritivo + botão "Conheça" + formulário inline (Nome/Email/aceite) com CTA "Criar conta Grátis".
- **Main:** seções verticais por persona (Advogados, Servidores, Biólogos, Engenheiros, Gestores) + bloco de recursos + bloco de preços com dois planos + depoimentos.
- **Footer:** razão social ADV Ambiental – Tecnologia, Consultoria e Serviços LTDA, CNPJ, endereço em Florianópolis, links de privacidade/termos, ícones sociais, crédito "site por wjk marketing".
- Dentro do app logado (app.advlabs.com.br) a arquitetura é dashboard "Meu Escritório" + painéis de módulos.

## Features principais observadas
- **Radar de Autos de Infração:** monitoramento de APAs publicados pelo IBAMA/ICMBio, com alerta de novos autos.
- **Radar de Prospecção:** identificação de oportunidades de negócio (aparenta cruzar autos com dados dos infratores para advogado prospectar).
- **Biblioteca de Teses:** mais de 128 teses agro-ambientais (alegada externamente); identificação por IA da tese aplicável ao caso.
- **900+ modelos** em Word, editáveis (petições e teses).
- **Calculadora de Prescrição** com IA e relatório automatizado.
- **Monitoramento de processo administrativo** com alertas.
- **CRM + formulários customizáveis** para captar cliente.
- **Feed social interno** para networking entre usuários da plataforma.
- **Meu Escritório:** dashboard central de gestão do escritório.
- Conteúdo educacional: cursos, palestras, estudos de caso, lives.

## UX / interações
Fluxo típico: advogado cria conta grátis (7 dias) → dashboard "Meu Escritório" → escolhe módulo (Teses, Radar, Calculadora, CRM) → busca/filtra por tipo de auto/infração/tema → abre tese/modelo → edita em Word ou exporta. IA de "identificação de tese" sugere teses relevantes a partir dos dados do caso. Feed social é retenção comunitária. Alertas de IBAMA/ICMBio chegam como notificações no painel. Biblioteca de modelos é navegada por categoria + busca textual.

## Preço e modelo de negócio
Dois planos visíveis:
- **Comunidade Ambiental Pro:** R$ 39/mês (R$ 357/ano) — painel da comunidade, feed, cursos exclusivos, estudos de caso.
- **Pro + Meu Escritório:** R$ 249/mês (R$ 1.997/ano) — tudo do Pro + dashboard de escritório, formulários de prospecção, biblioteca de teses, monitoramento, alertas IBAMA/ICMBio, análise IA com cálculo de prescrição, 1.000 créditos IA.
Ambos com "7 dias grátis". Conhecimento externo cita tiers anuais R$ 997 – R$ 4.997, possivelmente variantes enterprise/consultor não expostas no site vitrine atual.

## Autenticação
Email + senha (sem gov.br, sem OAB-validate visível). Login leva ao subdomínio app.advlabs.com.br. Trial sem cartão ("Criar conta Grátis" + aceite de privacidade).

## Conhecimento externo aplicável
- AdvLabs é fundada por ambientalistas/advogados de SC (Florianópolis), com forte presença em eventos como "Direito Ambiental Experience".
- O banco de teses é curado e atualizado por advogados parceiros; o valor real está mais na curadoria do que na ferramenta.
- Há tração em advogados de escritórios boutique ambientais, não tanto em grandes bancas.
- Segmentação por persona (biólogo, engenheiro) é estratégia de ampliação de TAM para além do advogado.

## Insights para AgroJus
1. **Copiar:** segmentação clara por persona no landing (advogado / servidor / biólogo / engenheiro / gestor). AgroJus pode ter rotas separadas para advogado agro, produtor, consultor de crédito, perito.
2. **Copiar:** trial de 7 dias SEM cartão de crédito com formulário no hero. Reduz atrito de onboarding.
3. **Copiar:** preços visíveis e escalonados (R$ 39 vs R$ 249) — comunidade barata como funil, produto caro como conversão.
4. **Fazer diferente:** AdvLabs é forte em teses mas fraco em dados geográficos/satelitais. AgroJus deve ter mapa interativo + camadas (MapBiomas, CAR, embargos) como núcleo, não como anexo.
5. **Copiar:** Radar de Autos de Infração — monitorar publicações do IBAMA/ICMBio e alertar o advogado. Esse módulo é replicável com dados já conectados (MapBiomas, CAR, Ibama).
6. **Copiar:** Biblioteca de 900+ modelos Word editáveis. Pode ser diferencial reaproveitado com modelos específicos de agro (contestação Proagro, embargo CAR, etc.).
7. **Fazer diferente:** AdvLabs prende feed/comunidade como retenção. AgroJus pode usar dados compartilhados (ex.: watchlist de fazendas críticas, casos similares) como moat em vez de feed social.
8. **Copiar:** calculadora de prescrição com IA + relatório. AgroJus precisa de calculadoras (prescrição tributária, prescrição ambiental, ITR).
9. **Fazer diferente:** AdvLabs é só ambiental. AgroJus deve cobrir ambiental + crédito rural + possessório + tributário agro.

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| Radar de Autos de Infração (IBAMA/ICMBio) | Temos dados brutos mas não o alerta automatizado | ALTA |
| Biblioteca de 128+ teses agro-ambientais | Parcial (mIA-pesquisa tem base local) | ALTA |
| 900+ modelos Word editáveis | Não temos em volume | ALTA |
| Calculadora de Prescrição | Não temos | MÉDIA |
| CRM + formulários prospectivos | Não temos | MÉDIA |
| Dashboard "Meu Escritório" | Parcial (mIA kernel) | MÉDIA |
| Feed social / comunidade | Não temos, não é prioridade | BAIXA |
| Trial 7 dias sem cartão | Ainda não temos billing | ALTA (roadmap) |
| Segmentação por persona no marketing | Não temos site comercial | MÉDIA |
| IA de identificação de tese | mIA-pesquisa parcialmente cobre | MÉDIA |
