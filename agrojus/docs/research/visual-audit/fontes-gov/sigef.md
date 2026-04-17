# SIGEF — Sistema de Gestão Fundiária (INCRA)

- **URL:** https://sigef.incra.gov.br/
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (consulta de parcelas); ações requerem gov.br prata/ouro

## Propósito declarado
"Recepção, validação, organização, regularização e disponibilização das informações georreferenciadas" de imóveis rurais certificados pelo INCRA. É o sistema que **certifica** o georreferenciamento conforme exigência da Lei 10.267/2001 e IN INCRA 77/2013. Diferentemente do CAR (declaratório), SIGEF produz dado **certificado** com rastreabilidade de credenciamento profissional.

## Layout e navegação
- **Header:** marca gov.br + logo INCRA + menu enxuto ("Documentos", "Sobre", "Entrar").
- **Área central:** cards para ações principais — "Consultar Parcelas", "Requerimento de Atualização", "Requerimento de Desmembramento".
- **Footer institucional:** logos gov.br + INCRA + Ministério da Agricultura, links para redes sociais (Facebook, Instagram, Twitter).
- Identidade visual segue o **padrão Design System Gov.br** (azul institucional, tipografia Rawline, layout centralizado com largura máxima fixa).

O portal é discreto, orientado a ação e com baixa densidade informacional — contrasta com o SICAR, que é mais exploratório.

## Dados e funcionalidades expostas
- **Consultar Parcelas:** busca de imóveis rurais certificados (parcelas com vértices georreferenciados validados).
- **Requerimento de Atualização de Parcela:** permite alterar códigos de vértice e altitude preservando a certificação.
- **Requerimento de Desmembramento:** divisão de parcela certificada em parcelas menores.
- **Documentos:** manuais técnicos, IN 77/2013, Portarias, e templates em planilha ODS para submissão.

## UX / interações (consulta, busca, filtros, download)
- Fluxo primário é **requerimento**, não consulta — o SIGEF é sistema de produção/submissão, a consulta é secundária.
- Templates obrigatórios em **formato ODS** (LibreOffice) sugerem herança acadêmica/técnica do INCRA — incomum em portais mais modernos.
- Downloads diretos: apenas normativos e manuais. A consulta de parcelas individuais exige navegação autenticada (dependendo do nível de detalhe).
- Não observado, na página raiz, um mapa interativo embutido; a visualização geográfica fica em subaplicação específica.

## API pública (endpoints, auth, formatos)
Nenhuma menção a API REST, Swagger ou documentação de endpoints na página raiz auditada.

**Conhecimento externo aplicável:**
- O INCRA disponibiliza **WFS público** com a camada de parcelas certificadas (`https://acervofundiario.incra.gov.br/...`) consumível por QGIS/ArcGIS.
- Existe endpoint de download em massa de shapefile por UF na Certificação — atualização semanal/mensal.
- Não há API JSON documentada; integrações são feitas via WFS GetFeature ou dumps shapefile.

## Rate limits / cotas conhecidas
Não declarados. WFS público historicamente tem limite implícito de `maxFeatures` por requisição (tipicamente 1000), exigindo paginação com `startIndex`.

## Autenticação
- **Consulta básica:** parece aberta (link "Consultar Parcelas" visível sem login no front).
- **Requerimentos e ações de escrita:** exigem **gov.br nível prata ou ouro** (biometria ou certificado digital).
- Integração gov.br completa é destaque — o SIGEF é um dos sistemas mais "modernos" do INCRA nesse quesito.

## Conhecimento externo aplicável
- Parcela certificada SIGEF é a única base com **precisão cartográfica validada** em imóveis rurais brasileiros — ao contrário do CAR.
- Sobreposição de parcela certificada × CAR declarado é prova documental frequente em disputas possessórias.
- Lei 10.267/2001 obriga georreferenciamento de imóveis > 25 ha em transferência/divisão — SIGEF é a base de compliance.
- Dados são públicos (Lei 12.527/2011), mas o front esconde WFS do cidadão leigo.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Design System Gov.br** é o padrão visual que o usuário público espera de portais fundiários — AgroJus deve oferecer "modo gov.br" opcional para usuários habituados.
2. **Cards de ação verbais** ("Consultar", "Requerer", "Atualizar") é a UX padrão — não usar jargão técnico.
3. **Integração gov.br prata/ouro** como gate para escrita é o padrão público — AgroJus pode diferenciar níveis (consulta livre, ações certificadas via gov.br).
4. **Templates ODS** expõe um gap: advogados querem **upload de KML/shapefile/GeoJSON**, não planilha. AgroJus deve aceitar formatos nativos de GIS.
5. **Documentação técnica (IN 77/2013) linkada visivelmente** constrói confiança — AgroJus deve citar normativos em cada módulo.

## Gaps vs AgroJus (tabela)

| Dimensão | SIGEF | AgroJus (alvo) |
|---|---|---|
| Propósito | Certificação georreferenciada | Inteligência jurídica + integração |
| Dado nativo | Parcela certificada INCRA | Multi-fonte (CAR, SIGEF, MapBiomas, ANM) |
| API REST JSON | Inexistente | Documentada (OpenAPI) |
| WFS/WMS | Disponível (não divulgado) | Sim + tiles Mapbox/MapLibre |
| Sobreposição automática | Não | Detecção CAR × SIGEF em background |
| Formato de upload | ODS obrigatório | KML, SHP, GeoJSON, CSV |
| Dark mode | Não | Sim |
| Consulta por CPF/CNPJ | Parcial | Completa e cruzada |
| Integração gov.br | Prata/ouro | OAuth + tier free |
| Cruzamento com jurisprudência | Nenhum | Core (STJ/CNJ/TJ ligado ao imóvel) |
| Alerta de conflito documental | Manual | Proativo (base interna) |
