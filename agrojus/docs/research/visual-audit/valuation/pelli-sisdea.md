# Pelli SisDEA

- **URL:** https://pellisistemas.com/produto/software-sisdea/
- **Categoria:** valuation
- **Data auditoria:** 2026-04-17
- **Acesso:** público (página de venda); software comprado sob licença

## Propósito declarado
Software desktop para "avaliação de imóveis urbanos, rurais, máquinas e equipamentos pelo **método comparativo direto de dados de mercado**, conforme preconiza a NBR 14.653 da ABNT". É o produto histórico de referência do mercado brasileiro de engenharia de avaliações — nasceu como ferramenta acadêmica e virou standard de escritórios de perícia.

## Layout e navegação
- **Header**: logo Pelli Sistemas + menu horizontal com dropdowns (Pelli Sistemas, Software, Cursos, Suporte, Contato, Blog).
- **Hero**: bloco de e-commerce clássico — imagem do produto à esquerda, ficha/preço/CTA à direita.
- **Corpo**: abas/seções verticais de "Descrição do produto", "FAQ", "Produtos relacionados".
- **Footer**: contatos, links de dicas, newsletter, widget de WhatsApp flutuante.
- Tom geral: página de **e-commerce WooCommerce** padrão, sem landing page moderna. Baixa densidade visual, sem screenshots vivos do software em funcionamento.

## Features / dados expostos
Técnicas matemáticas citadas (em lista textual, sem demonstração):
- Regressão linear e não-linear
- Análise de envoltória de dados (DEA) — daí o nome SisDEA
- Redes neurais artificiais
- Inferência estatística
- Avaliação pelo método comparativo direto

**Não mostra**: componentes NBR 14.653 (grau de fundamentação, grau de precisão, intervalo de confiança, saneamento amostral, homogeneização), fluxo de trabalho, exportação de laudo, tela de cadastro de dados de mercado, mapa de dados comparativos. Tudo isso está no software, mas a página não expõe.

## UX / interações
- CTA primário: "Adicionar ao carrinho" (fluxo de loja).
- Formulário de contato no final (Nome/Email/Telefone/Mensagem).
- Link para playlist de tutoriais no YouTube como "demo" (sem trial in-browser, sem sandbox).
- Newsletter signup no footer.
- Widget WhatsApp flutuante para atendimento comercial.
- Imagens carregam como placeholders GIF — screenshots do SisDEA não aparecem de forma funcional.

## Preço e modelo de negócio
- **Licença permanente: R$ 1.986,00** (com frete grátis do token).
- Alternativas: assinatura **mensal, semestral, anual** (valores não estampados no hero; precisam ser consultados na loja).
- Modelo desktop tradicional: o engenheiro/perito compra, instala na máquina, entrega laudos em DOCX/PDF para cliente final.

## API pública (se houver)
Nenhuma. SisDEA é fechado, desktop-only, base local — não há API documentada, webhook ou integração declarada na página. É ponto de dor histórico do mercado: dados comparativos ficam presos no computador do perito.

## Autenticação
Não há login web. Habilitação de produto via **Token USB** (dongle físico) ou código de habilitação vinculado à máquina. Modelo pré-SaaS.

## Conhecimento externo aplicável
- SisDEA é **line-of-business tool** dominante em avaliação imobiliária brasileira desde os anos 2000; concorre com SISREG (urbano), SISPEMA, e planilhões Excel artesanais.
- A NBR 14.653 tem partes específicas: **14.653-1** (procedimentos gerais), **14.653-2** (imóveis urbanos), **14.653-3** (imóveis rurais, nosso foco), **14.653-4** (empreendimentos), etc. Um laudo rural precisa reportar: grau de fundamentação (I, II, III), grau de precisão (I, II, III), intervalo de confiança 80%, análise de outliers, tratamento por fatores ou inferência.
- O mercado de perícia rural no Brasil usa SisDEA + Excel + dados coletados em campo (anúncios, entrevistas com corretores, IPTU/ITR). Não existe base unificada de transações rurais reais — esse é o grande gap que AgroJus pode preencher.

## Insights para AgroJus
1. **Gap gritante na apresentação visual**: SisDEA vende em 2026 como se fosse 2008. Zero screenshots dinâmicos, zero demo in-browser, zero storytelling de laudo. AgroJus pode ganhar no "ver antes de comprar".
2. **Comparativo direto = núcleo do valuation rural**: qualquer tela `/valuation` nossa tem que começar por "encontre imóveis comparáveis" (com filtros: raio, uso do solo, CAR similar, infraestrutura). Isso é o que o perito faz no Excel hoje.
3. **NBR 14.653-3 como checklist nativo**: o laudo precisa produzir automaticamente grau de fundamentação + precisão + IC 80%. Isso é diferencial enorme vs. SisDEA desktop.
4. **Exportação é subestimada**: peritos entregam DOCX/PDF para clientes. A tela precisa gerar laudo PDF com capa, ART, memorial, anexos — não só mostrar número na tela.
5. **Modelo SaaS anual vs. licença eterna**: R$ 1.986 único é o ticket que o mercado aceita. SaaS a R$ 199/mês ou R$ 1.990/ano cabe nesse range e entrega dados vivos (satélite, comparáveis atualizados, ZARC) que justifiquem a recorrência.

## Gaps vs AgroJus (tabela)

| Dimensão | SisDEA (2026) | AgroJus (planejado) |
|---|---|---|
| Plataforma | Desktop Windows, token USB | Web SaaS, multi-device |
| Dados de mercado | Inseridos manualmente pelo perito | Agregador automático (leilões + anúncios + CAR + MapBiomas + CEPEA) |
| Comparáveis | Base local do usuário | Base nacional compartilhada com filtros geoespaciais |
| Método | Só comparativo + DEA/regressão | Comparativo + evolutivo + renda + capitalização + múltiplos |
| Georreferenciamento | Inexistente / manual | CAR+SIGEF+INCRA nativos, sobreposição MapBiomas |
| NBR 14.653 check automático | Manual, o perito valida | Motor valida GF/GP, IC, outliers automaticamente |
| Laudo de saída | DOCX/PDF via templates | DOCX/PDF automatizado + link web auditável |
| API | Não tem | REST + webhooks para ERPs e bancos |
| Preço | R$ 1.986 licença perpétua + update | SaaS R$ 199/mês ou enterprise negociado |
| Onboarding | Manual + cursos presenciais/EAD | Autoserviço com laudo-modelo em 15 min |
| Auditabilidade | Arquivo .sis local | Cadeia de custódia versionada no cloud |
| Colaboração | Monousuário | Multi-perito + revisor + cliente com permissões |
