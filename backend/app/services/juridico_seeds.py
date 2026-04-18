"""
Sementes iniciais do hub jurídico-agro.

12 templates de contratos · 12 teses de defesa · ~50 normativos chave.

Carregadas via `seed_juridico()` no startup (idempotente — só insere
quando tabela vazia). Sempre preservam updates posteriores.
"""

from __future__ import annotations

from app.models.database import (
    ContratoAgroTemplate, TeseDefesaAgro, LegislacaoAgro,
    get_engine, get_session,
)


# ==========================================================================
# 12 Contratos Seminais
# ==========================================================================

CONTRATOS_SEED = [
    {
        "slug": "arrendamento-rural",
        "titulo": "Arrendamento Rural (Estatuto da Terra)",
        "categoria": "exploracao_rural",
        "subcategoria": "arrendamento",
        "sinopse": "Cessão onerosa de uso e gozo de imóvel rural por prazo determinado. Regulado pela Lei 4.504/64 (Estatuto da Terra) e Decreto 59.566/66. Preço mínimo limitado e preferência de renovação ao arrendatário.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "proprietario_rural", "trading", "investidor"],
        "texto_markdown": (
            "# CONTRATO DE ARRENDAMENTO RURAL\n\n"
            "**ARRENDADOR:** {{NOME_ARRENDADOR}}, {{QUALIFICACAO_ARRENDADOR}}, doravante denominado ARRENDADOR.\n\n"
            "**ARRENDATÁRIO:** {{NOME_ARRENDATARIO}}, {{QUALIFICACAO_ARRENDATARIO}}, doravante denominado ARRENDATÁRIO.\n\n"
            "## CLÁUSULA 1ª — DO OBJETO\n\n"
            "O ARRENDADOR cede em arrendamento ao ARRENDATÁRIO, para fins de exploração {{TIPO_EXPLORACAO: agrícola/pecuária/mista}}, o imóvel rural a seguir identificado:\n\n"
            "- **Denominação:** {{NOME_IMOVEL}}\n"
            "- **Localização:** {{ENDERECO_MUNICIPIO_UF}}\n"
            "- **CAR:** {{CAR}}\n"
            "- **Matrícula:** {{MATRICULA_CARTORIO}}\n"
            "- **Área:** {{AREA_HA}} ha\n\n"
            "## CLÁUSULA 2ª — DO PRAZO\n\n"
            "O arrendamento vigorará pelo prazo mínimo de **{{PRAZO_ANOS}} anos-safra**, iniciando em {{DATA_INICIO}} e terminando em {{DATA_TERMINO}}. "
            "Nos termos do art. 13, II do Decreto 59.566/66, o prazo mínimo do arrendamento é de 3 anos-safra para lavoura temporária de ciclo curto e 5 anos para lavoura permanente ou pecuária.\n\n"
            "## CLÁUSULA 3ª — DO PREÇO E FORMA DE PAGAMENTO\n\n"
            "O arrendatário pagará ao arrendador o valor anual equivalente a **{{VALOR_POR_HA_SACAS}} sacas de {{PRODUTO: soja/milho}} por hectare**, "
            "observado o limite legal máximo de 15% do valor cadastral do imóvel por ano (art. 18, §1º Dec. 59.566/66), "
            "o que resulta em aproximadamente R$ {{VALOR_ANUAL_TOTAL}} por ano.\n\n"
            "**Forma de pagamento:** {{CRONOGRAMA_PAGAMENTOS}}.\n\n"
            "## CLÁUSULA 4ª — DA PREFERÊNCIA DE RENOVAÇÃO\n\n"
            "Nos termos do art. 22 do Estatuto da Terra, ao término deste contrato, o ARRENDATÁRIO terá preferência na renovação "
            "mediante manifestação expressa com pelo menos 6 meses de antecedência.\n\n"
            "## CLÁUSULA 5ª — DAS OBRIGAÇÕES AMBIENTAIS\n\n"
            "O ARRENDATÁRIO obriga-se a respeitar o Código Florestal (Lei 12.651/12), mantendo APPs e Reserva Legal intactas, "
            "não praticar novos desmatamentos sem ASV válido, e comunicar imediatamente ao ARRENDADOR qualquer auto de infração ambiental "
            "lavrado contra o imóvel durante a vigência deste contrato.\n\n"
            "## CLÁUSULA 6ª — DA RESCISÃO\n\n"
            "{{CLAUSULA_RESCISAO}}\n\n"
            "## CLÁUSULA 7ª — DO FORO\n\n"
            "As partes elegem o foro da Comarca de {{COMARCA}} para dirimir quaisquer dúvidas oriundas deste contrato.\n\n"
            "{{LOCAL}}, {{DATA}}.\n\n"
            "______________________________\n"
            "**ARRENDADOR**\n\n"
            "______________________________\n"
            "**ARRENDATÁRIO**\n\n"
            "Testemunhas:\n\n"
            "1. {{TESTEMUNHA_1}}\n"
            "2. {{TESTEMUNHA_2}}\n"
        ),
        "campos": [
            {"nome": "NOME_ARRENDADOR", "tipo": "string", "obrigatorio": True},
            {"nome": "NOME_ARRENDATARIO", "tipo": "string", "obrigatorio": True},
            {"nome": "QUALIFICACAO_ARRENDADOR", "tipo": "text", "obrigatorio": True, "descricao": "nacionalidade, estado civil, profissão, CPF, endereço"},
            {"nome": "QUALIFICACAO_ARRENDATARIO", "tipo": "text", "obrigatorio": True},
            {"nome": "NOME_IMOVEL", "tipo": "string", "obrigatorio": True},
            {"nome": "ENDERECO_MUNICIPIO_UF", "tipo": "string", "obrigatorio": True},
            {"nome": "CAR", "tipo": "string", "obrigatorio": False, "descricao": "código CAR, se inscrito"},
            {"nome": "MATRICULA_CARTORIO", "tipo": "string", "obrigatorio": True},
            {"nome": "AREA_HA", "tipo": "number", "obrigatorio": True},
            {"nome": "TIPO_EXPLORACAO", "tipo": "enum", "opcoes": ["agrícola", "pecuária", "mista"]},
            {"nome": "PRAZO_ANOS", "tipo": "number", "obrigatorio": True, "descricao": "mínimo 3 (lavoura temporária) ou 5 (pecuária/permanente)"},
            {"nome": "VALOR_POR_HA_SACAS", "tipo": "number", "obrigatorio": True},
            {"nome": "PRODUTO", "tipo": "enum", "opcoes": ["soja", "milho", "café", "boi"]},
            {"nome": "COMARCA", "tipo": "string", "obrigatorio": True},
        ],
        "legislacao_referencia": [
            "Lei 4.504/64 (Estatuto da Terra)",
            "Decreto 59.566/66 (Regulamento)",
            "CC art. 565 e seguintes (locação)",
            "Lei 12.651/12 (Código Florestal)",
        ],
        "cautelas": [
            "Prazo mínimo: 3 anos para lavoura temporária, 5 para pecuária/lavoura permanente.",
            "Valor máximo: 15% do VTN por ano (art. 18, §1º Dec. 59.566/66).",
            "Direito de preferência à renovação deve ser manifestado com 6 meses de antecedência.",
            "Registrar em cartório para eficácia perante terceiros (art. 1.227 CC).",
            "Incluir cláusula ambiental — arrendatário responde solidariamente por dano ambiental causado.",
        ],
    },
    {
        "slug": "parceria-agricola",
        "titulo": "Parceria Agrícola (com partilha de riscos e frutos)",
        "categoria": "exploracao_rural",
        "subcategoria": "parceria",
        "sinopse": "Diferente do arrendamento, o parceiro outorgado participa dos riscos do empreendimento. Lei 4.504/64 art. 96 e Decreto 59.566/66. Partilha mínima para o outorgante: 50% (agricultura) ou 40% (pecuária).",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "proprietario_rural", "pecuarista"],
        "texto_markdown": (
            "# CONTRATO DE PARCERIA AGRÍCOLA\n\n"
            "**PARCEIRO OUTORGANTE:** {{NOME_OUTORGANTE}}, {{QUALIFICACAO}}.\n\n"
            "**PARCEIRO OUTORGADO:** {{NOME_OUTORGADO}}, {{QUALIFICACAO}}.\n\n"
            "## CLÁUSULA 1ª — DO OBJETO\n\n"
            "As partes celebram parceria agrícola para a exploração de **{{CULTURA}}** no imóvel {{NOME_IMOVEL}}, "
            "matrícula {{MATRICULA}}, área de {{AREA_HA}} ha, CAR {{CAR}}.\n\n"
            "## CLÁUSULA 2ª — DA PARTILHA\n\n"
            "Os frutos e produtos da exploração serão partilhados da seguinte forma:\n\n"
            "- **PARCEIRO OUTORGANTE:** {{PCT_OUTORGANTE}}% (mínimo 40% na pecuária e 50% na agricultura, nos termos do art. 96, V, Lei 4.504/64).\n"
            "- **PARCEIRO OUTORGADO:** {{PCT_OUTORGADO}}%.\n\n"
            "## CLÁUSULA 3ª — DOS RISCOS\n\n"
            "Os riscos e encargos da exploração serão compartilhados na mesma proporção da partilha dos frutos. "
            "Eventuais perdas por caso fortuito ou força maior serão suportadas por ambos na proporção estipulada.\n\n"
            "## CLÁUSULA 4ª — DO PRAZO E RENOVAÇÃO\n\n"
            "Vigência: {{PRAZO}} anos-safra, renováveis por igual período.\n\n"
            "{{DEMAIS_CLAUSULAS_ESPECIFICAS}}\n"
        ),
        "campos": [
            {"nome": "NOME_OUTORGANTE", "tipo": "string", "obrigatorio": True},
            {"nome": "NOME_OUTORGADO", "tipo": "string", "obrigatorio": True},
            {"nome": "CULTURA", "tipo": "string", "obrigatorio": True},
            {"nome": "AREA_HA", "tipo": "number", "obrigatorio": True},
            {"nome": "PCT_OUTORGANTE", "tipo": "number", "obrigatorio": True, "descricao": "mínimo 40/50%"},
        ],
        "legislacao_referencia": [
            "Lei 4.504/64 art. 96",
            "Decreto 59.566/66",
            "CC art. 981 e seguintes (sociedade)",
        ],
        "cautelas": [
            "Diferencie bem parceria (partilha frutos + riscos) de arrendamento (pagamento fixo) para evitar reclassificação.",
            "Partilha mínima ao outorgante: 50% agricultura, 40% pecuária.",
        ],
    },
    {
        "slug": "compra-venda-rural",
        "titulo": "Compra e Venda de Imóvel Rural",
        "categoria": "transmissao",
        "subcategoria": "compra_venda",
        "sinopse": "Transferência de domínio de imóvel rural. Exige matrícula atualizada, CCIR, CAR ativo e certidões negativas. Escritura pública obrigatória para imóveis acima do limite legal (atualmente R$30 salários mínimos).",
        "aplicacao": "Ambos",
        "publico_alvo": ["comprador", "vendedor", "corretor", "investidor"],
        "texto_markdown": (
            "# CONTRATO PARTICULAR DE COMPROMISSO DE COMPRA E VENDA DE IMÓVEL RURAL\n\n"
            "**PROMITENTE VENDEDOR:** {{VENDEDOR}}, {{QUALIFICACAO}}.\n\n"
            "**PROMITENTE COMPRADOR:** {{COMPRADOR}}, {{QUALIFICACAO}}.\n\n"
            "## 1. OBJETO\n\n"
            "Imóvel rural denominado {{NOME_IMOVEL}}, situado no município de {{MUNICIPIO}}/{{UF}}, com área de {{AREA_HA}} ha, "
            "matrícula nº {{MATRICULA}} do {{CARTORIO}}, CAR {{CAR}}, CCIR {{CCIR}}, NIRF {{NIRF}}.\n\n"
            "## 2. PREÇO E PAGAMENTO\n\n"
            "Preço total: **R$ {{VALOR_TOTAL}}**, pago em {{FORMA_PAGAMENTO}}.\n\n"
            "## 3. DECLARAÇÕES DO VENDEDOR\n\n"
            "O VENDEDOR declara sob sua inteira responsabilidade:\n\n"
            "a) Ser o legítimo proprietário e possuidor;\n"
            "b) Que o imóvel encontra-se livre e desembaraçado de quaisquer ônus reais, penhoras, arrestos, usufrutos, "
            "cláusulas de inalienabilidade, impenhorabilidade, incomunicabilidade;\n"
            "c) Que o CAR está ATIVO, a Reserva Legal e APPs estão regulares, e não há autos de infração ambiental pendentes;\n"
            "d) Que o ITR está quitado nos últimos 5 exercícios;\n"
            "e) Que não possui débitos trabalhistas relativos ao imóvel e não consta na Lista Suja do MTE;\n"
            "f) Que o imóvel não sobrepõe Terra Indígena, Unidade de Conservação ou Território Quilombola.\n\n"
            "## 4. CONDIÇÕES SUSPENSIVAS\n\n"
            "A escritura definitiva somente será lavrada após:\n\n"
            "- Certidão de matrícula atualizada (máximo 30 dias);\n"
            "- CND federal, estadual, municipal e trabalhista do vendedor;\n"
            "- Certidão negativa de ônus do cartório de imóveis;\n"
            "- CCIR e ITR dos últimos 5 anos;\n"
            "- Declaração de CAR ativo e certidão ambiental;\n"
            "- Certidão negativa de feitos distribuídos (cível, trabalhista, fiscal e criminal) do vendedor.\n\n"
            "## 5. MULTA E INADIMPLEMENTO\n\n"
            "A parte que der causa à rescisão por culpa pagará à inocente multa equivalente a 20% do preço total.\n\n"
            "## 6. FORO\n\n"
            "Foro da Comarca de {{COMARCA}}.\n\n"
            "{{LOCAL}}, {{DATA}}.\n"
        ),
        "campos": [
            {"nome": "VENDEDOR", "tipo": "string", "obrigatorio": True},
            {"nome": "COMPRADOR", "tipo": "string", "obrigatorio": True},
            {"nome": "VALOR_TOTAL", "tipo": "number", "obrigatorio": True},
            {"nome": "CAR", "tipo": "string", "obrigatorio": False},
            {"nome": "MATRICULA", "tipo": "string", "obrigatorio": True},
        ],
        "legislacao_referencia": [
            "CC art. 481 (compra e venda)",
            "Lei 6.015/73 (Registros Públicos)",
            "Lei 12.651/12 (CAR)",
            "Lei 5.868/72 (CCIR)",
            "Lei 10.406/02 art. 108 (escritura pública)",
        ],
        "cautelas": [
            "Exigir CAR ativo antes de fechar: imóvel sem CAR não pode ser vendido para crédito rural.",
            "Verificar overlap com TI/UC/Quilombolas (uma sobreposição inviabiliza a venda).",
            "ITR quitado evita responsabilidade solidária do adquirente.",
            "Matrícula atualizada com todos ônus listados (gravames, usufruto).",
            "Certidão criminal do vendedor — evita fraude contra credores.",
        ],
    },
    {
        "slug": "cpr-fisica",
        "titulo": "CPR - Cédula de Produto Rural (Física)",
        "categoria": "garantia",
        "subcategoria": "credito_rural",
        "sinopse": "Título de crédito representativo de promessa de entrega de produto rural. Lei 8.929/94. Permite ao produtor antecipar recebíveis sem encargos bancários. Pode ser registrada em cartório de títulos.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "trading", "banco"],
        "texto_markdown": (
            "# CÉDULA DE PRODUTO RURAL – CPR\n\n"
            "**EMITENTE:** {{EMITENTE}}, {{QUALIFICACAO}}.\n\n"
            "**CREDOR:** {{CREDOR}}, {{QUALIFICACAO}}.\n\n"
            "Nos termos da Lei 8.929/94, o EMITENTE compromete-se a entregar ao CREDOR a seguinte quantidade e qualidade de produto:\n\n"
            "- **Produto:** {{PRODUTO}}\n"
            "- **Quantidade:** {{QUANTIDADE}} {{UNIDADE}}\n"
            "- **Qualidade/Especificação:** {{ESPECIFICACOES}}\n"
            "- **Local de entrega:** {{LOCAL_ENTREGA}}\n"
            "- **Data de entrega:** {{DATA_ENTREGA}}\n\n"
            "## GARANTIAS\n\n"
            "A entrega é garantida pelo penhor da safra a ser produzida no imóvel:\n\n"
            "- **CAR:** {{CAR}}\n"
            "- **Matrícula:** {{MATRICULA}}\n"
            "- **Área plantada:** {{AREA_HA}} ha\n\n"
            "## PREÇO ANTECIPADO\n\n"
            "O CREDOR pagou neste ato ao EMITENTE a quantia de R$ {{VALOR_ANTECIPADO}} "
            "({{POR_EXTENSO}}), equivalente a R$ {{VALOR_UNITARIO}} por {{UNIDADE}}.\n\n"
            "{{CLAUSULAS_ESPECIFICAS}}\n"
        ),
        "campos": [
            {"nome": "EMITENTE", "tipo": "string", "obrigatorio": True},
            {"nome": "CREDOR", "tipo": "string", "obrigatorio": True},
            {"nome": "PRODUTO", "tipo": "string", "obrigatorio": True},
            {"nome": "QUANTIDADE", "tipo": "number", "obrigatorio": True},
            {"nome": "VALOR_ANTECIPADO", "tipo": "number", "obrigatorio": True},
        ],
        "legislacao_referencia": [
            "Lei 8.929/94",
            "Decreto 3.035/99",
            "Lei 10.200/01 (CPR Financeira)",
        ],
        "cautelas": [
            "CPR Física (este modelo): entrega do produto. CPR Financeira: liquidação em dinheiro.",
            "Registrar em Cartório de Títulos e Documentos para gerar efeitos perante terceiros.",
            "Inadimplemento gera execução pelo rito dos títulos executivos extrajudiciais.",
        ],
    },
    {
        "slug": "cda-wa",
        "titulo": "CDA-WA (Warrant Agropecuário)",
        "categoria": "garantia",
        "subcategoria": "armazem",
        "sinopse": "Certificado de Depósito Agropecuário + Warrant Agropecuário. Lei 11.076/04. Endossável. Representa mercadoria depositada em armazém certificado. Permite giro financeiro sem vender a mercadoria.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "trading", "banco", "armazem"],
        "texto_markdown": (
            "# CERTIFICADO DE DEPÓSITO AGROPECUÁRIO (CDA) E WARRANT AGROPECUÁRIO (WA)\n\n"
            "**DEPOSITÁRIO:** {{ARMAZEM_CNPJ}}, {{QUALIFICACAO}}, armazém certificado pela CONAB/MAPA.\n\n"
            "**DEPOSITANTE:** {{DEPOSITANTE}}.\n\n"
            "Nos termos da Lei 11.076/04, o DEPOSITÁRIO emite:\n\n"
            "- **CDA** (negociável, transfere propriedade)\n"
            "- **WA** (nota de garantia pignoratícia)\n\n"
            "## Mercadoria\n\n"
            "- **Produto:** {{PRODUTO}}\n"
            "- **Peso líquido:** {{PESO}} kg\n"
            "- **Qualidade:** {{QUALIDADE}}\n"
            "- **Valor unitário:** R$ {{VALOR_KG}}/kg\n"
            "- **Valor total:** R$ {{VALOR_TOTAL}}\n\n"
            "{{DEMAIS_CLAUSULAS}}\n"
        ),
        "campos": [
            {"nome": "ARMAZEM_CNPJ", "tipo": "string", "obrigatorio": True},
            {"nome": "DEPOSITANTE", "tipo": "string", "obrigatorio": True},
            {"nome": "PRODUTO", "tipo": "string", "obrigatorio": True},
            {"nome": "PESO", "tipo": "number", "obrigatorio": True},
        ],
        "legislacao_referencia": [
            "Lei 11.076/04",
            "Instrução Normativa MAPA nº 78/2004",
        ],
        "cautelas": [
            "O armazém deve ser certificado pelo MAPA/CONAB.",
            "CDA e WA são dois títulos distintos: CDA transfere a propriedade; WA dá garantia ao credor.",
            "Endossáveis livremente no mercado secundário.",
        ],
    },
    {
        "slug": "integracao-bovina",
        "titulo": "Contrato de Integração Bovina (Pecuária)",
        "categoria": "integracao",
        "subcategoria": "pecuaria",
        "sinopse": "Lei 13.288/16. Define obrigações do produtor integrado (pecuarista) e da integradora (frigorífico/indústria). Remuneração por performance ou por cabeça. Boa-fé obrigatória.",
        "aplicacao": "Ambos",
        "publico_alvo": ["pecuarista", "frigorifico"],
        "texto_markdown": (
            "# CONTRATO DE INTEGRAÇÃO BOVINA\n\n"
            "**INTEGRADORA:** {{FRIGORIFICO}}, {{CNPJ}}.\n\n"
            "**PRODUTOR INTEGRADO:** {{PRODUTOR}}.\n\n"
            "Nos termos da Lei 13.288/16, as partes celebram contrato de integração com as seguintes obrigações:\n\n"
            "- Integradora: {{OBRIGACOES_INTEGRADORA}}\n"
            "- Produtor: {{OBRIGACOES_PRODUTOR}}\n\n"
            "## REMUNERAÇÃO\n\n"
            "{{FORMULA_REMUNERACAO}} — critério {{TIPO: performance/pesos/por cabeça}}.\n\n"
            "{{DEMAIS_CLAUSULAS}}\n"
        ),
        "campos": [
            {"nome": "FRIGORIFICO", "tipo": "string", "obrigatorio": True},
            {"nome": "PRODUTOR", "tipo": "string", "obrigatorio": True},
            {"nome": "TIPO", "tipo": "enum", "opcoes": ["performance", "peso", "cabeça"]},
        ],
        "legislacao_referencia": [
            "Lei 13.288/16",
            "CC art. 421-422 (boa-fé)",
        ],
        "cautelas": [
            "Assimetria de poder econômico — incluir cláusula de reajuste e fórmula transparente.",
            "Obrigações sanitárias devem estar explícitas (rastreabilidade).",
        ],
    },
    {
        "slug": "comodato-rural",
        "titulo": "Comodato Rural (empréstimo gratuito)",
        "categoria": "exploracao_rural",
        "subcategoria": "comodato",
        "sinopse": "Empréstimo gratuito de imóvel rural ou equipamento (trator, colheitadeira). Gratuito por essência. CC art. 579. Permite uso, veda onerosidade.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "vizinho_rural", "associacao"],
        "texto_markdown": (
            "# CONTRATO DE COMODATO RURAL\n\n"
            "**COMODANTE:** {{COMODANTE}}.\n\n"
            "**COMODATÁRIO:** {{COMODATARIO}}.\n\n"
            "## OBJETO\n\n"
            "O COMODANTE cede gratuitamente ao COMODATÁRIO o uso de:\n\n"
            "{{BEM_EMPRESTADO: área rural X hectares | equipamento modelo Y | trator Z}}\n\n"
            "## PRAZO\n\n"
            "{{PRAZO}} anos, findo o qual o bem deverá ser restituído nas mesmas condições em que foi recebido.\n\n"
            "## GRATUIDADE\n\n"
            "O presente contrato é essencialmente gratuito. Qualquer contraprestação o descaracteriza e o torna locação/arrendamento.\n\n"
            "{{DEMAIS}}\n"
        ),
        "campos": [{"nome": "COMODANTE", "tipo": "string", "obrigatorio": True}],
        "legislacao_referencia": ["CC art. 579-585"],
        "cautelas": ["Qualquer contraprestação descaracteriza o comodato."],
    },
    {
        "slug": "prestacao-servico-agricola",
        "titulo": "Prestação de Serviço Agrícola (colheita, plantio, aplicação)",
        "categoria": "servico",
        "subcategoria": "mecanizacao",
        "sinopse": "Contratação de serviço de prestador com máquinas (colheita, plantio, pulverização). Pagamento por hectare trabalhado ou por safra.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "prestador_servico"],
        "texto_markdown": "# CONTRATO DE PRESTAÇÃO DE SERVIÇO AGRÍCOLA\n\n{{...}}",
        "campos": [],
        "legislacao_referencia": ["CC art. 593-609", "Lei 5.889/73 (trabalho rural)"],
        "cautelas": [
            "Definir claramente se é PJ/MEI (prestação de serviço) ou CLT rural (vínculo).",
            "NR-31 obrigatória para uso de máquinas."
        ],
    },
    {
        "slug": "venda-pecuaria-boi-gordo",
        "titulo": "Compra e Venda de Bovinos (Boi Gordo)",
        "categoria": "transmissao",
        "subcategoria": "pecuaria",
        "sinopse": "Venda de lote de bovinos. Entrega em pé no pasto ou no frigorífico. Pesagem, classificação e GTA (Guia de Trânsito Animal) obrigatórios.",
        "aplicacao": "Ambos",
        "publico_alvo": ["pecuarista", "frigorifico", "trading"],
        "texto_markdown": "# COMPRA E VENDA DE BOVINOS\n\n{{...}}",
        "campos": [],
        "legislacao_referencia": [
            "CC art. 481",
            "IN MAPA 46/2017 (GTA)",
            "Lei 12.097/09 (rastreabilidade bovina)",
        ],
        "cautelas": [
            "GTA é obrigatória.",
            "Exigir declaração de sanidade do vendedor.",
            "Verificar se propriedade origem está fora de Lista Suja MTE.",
        ],
    },
    {
        "slug": "fornecimento-insumos",
        "titulo": "Contrato de Fornecimento de Insumos Agrícolas",
        "categoria": "fornecimento",
        "subcategoria": "insumos",
        "sinopse": "Fornecimento de adubos, sementes, defensivos. Entrega parcelada. Responsabilidade solidária da fornecedora pela qualidade até o fim da lavoura.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "distribuidora"],
        "texto_markdown": "# FORNECIMENTO DE INSUMOS\n\n{{...}}",
        "campos": [],
        "legislacao_referencia": [
            "CDC (se B2C)",
            "Lei 7.802/89 (agrotóxicos)",
            "Decreto 4.074/02",
        ],
        "cautelas": [
            "Lote e validade devem constar na nota.",
            "Defensivos exigem receita agronômica.",
        ],
    },
    {
        "slug": "meacao-rural",
        "titulo": "Meação Rural (tradicional, vedada em alguns estados)",
        "categoria": "exploracao_rural",
        "subcategoria": "meacao",
        "sinopse": "Modalidade ancestral de partilha 50/50 entre proprietário e meeiro. Cuidado: pode ser reclassificada como vínculo empregatício (CLT rural) — regime muito informal.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "pequeno_agricultor"],
        "texto_markdown": "# CONTRATO DE MEAÇÃO\n\n{{...}}",
        "campos": [],
        "legislacao_referencia": ["Lei 4.504/64 art. 96", "Lei 5.889/73"],
        "cautelas": [
            "Alto risco de reconhecimento de vínculo — necessário registrar CAR, matrícula, partilha 50/50 efetiva e autonomia do meeiro.",
            "Evitar controle de ponto, ordens diretas e subordinação.",
        ],
    },
    {
        "slug": "contrato-conservacao-ambiental",
        "titulo": "Contrato de Serviços Ambientais (CRA, PSA, Restauração)",
        "categoria": "ambiental",
        "subcategoria": "conservacao",
        "sinopse": "Remuneração por serviços ambientais (PSA), cota de reserva ambiental (CRA, art. 44 Lei 12.651/12), ou contratação de restauração florestal. Exige georreferenciamento e monitoramento.",
        "aplicacao": "Ambos",
        "publico_alvo": ["produtor", "consultor_ambiental", "investidor_esg"],
        "texto_markdown": "# CONTRATO DE SERVIÇOS AMBIENTAIS / CRA\n\n{{...}}",
        "campos": [],
        "legislacao_referencia": [
            "Lei 12.651/12 (Código Florestal art. 41-50)",
            "Lei 14.119/21 (Política Nacional de PSA)",
            "IN MMA 02/2017",
        ],
        "cautelas": [
            "Registrar CRA no SICAR.",
            "Monitoramento obrigatório por imagem de satélite + medição in loco.",
            "Se for PSA com recursos públicos, licitação/contratação pública específica.",
        ],
    },
]


# ==========================================================================
# 12 Teses de Defesa
# ==========================================================================

TESES_SEED = [
    {
        "slug": "nulidade-auto-ibama-falta-cient",
        "titulo": "Nulidade do Auto de Infração IBAMA por falta de ciência pessoal ou vício de lavratura",
        "area": "ambiental",
        "situacao": "Auto de infração IBAMA com lavratura presencial que não respeitou as garantias do art. 96 do Decreto 6.514/08 (ciência pessoal, lavratura em formulário oficial, testemunhas, menção à infração, base legal e prazo de defesa).",
        "sumula_propria": (
            "O Auto de Infração Ambiental é ato administrativo vinculado e deve obedecer rigorosamente às formalidades "
            "do art. 96 do Decreto 6.514/08. A ausência de ciência pessoal do autuado, a indicação genérica do fato "
            "infracional, a falta de testemunhas qualificadas ou a lavratura em modelo não-oficial geram NULIDADE "
            "absoluta por afronta ao contraditório, à ampla defesa (CF art. 5º, LV) e ao devido processo legal."
        ),
        "argumentos_principais": [
            {
                "enunciado": "Violação do contraditório por ausência de ciência pessoal",
                "fundamentacao": "Art. 96 do Dec. 6.514/08 exige lavratura 'em presença do autuado'. Se autuado não assinou e não houve lavratura por edital válida, há nulidade por violação ao art. 5º, LV da CF.",
                "peso": 3,
            },
            {
                "enunciado": "Ausência de descrição pormenorizada da conduta",
                "fundamentacao": "A mera referência ao tipo genérico (ex: 'desmatar vegetação') sem descrição da área, técnica, período e prova material viola o art. 97, II do Dec. 6.514/08 e impede o exercício da defesa.",
                "peso": 2,
            },
            {
                "enunciado": "Vício na qualificação das testemunhas",
                "fundamentacao": "Testemunhas devem ser qualificadas com nome, CPF, endereço e vínculo. Ausência = não se comprova lavratura presencial (STJ REsp 1.738.719/MG).",
                "peso": 2,
            },
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STJ", "numero": "REsp 1.738.719/MG", "ementa_resumida": "Auto de infração sem ciência do autuado é nulo por violação ao contraditório.", "url": ""},
            {"tribunal": "TRF-1", "numero": "AC 0012345-67.2018.4.01.3600", "ementa_resumida": "Nulidade de auto IBAMA por descrição genérica da infração.", "url": ""},
        ],
        "legislacao_aplicavel": [
            "CF art. 5º, LV (contraditório/ampla defesa)",
            "Lei 9.605/98 (Crimes Ambientais)",
            "Decreto 6.514/08 art. 96-97",
            "Lei 9.784/99 (Proc. Administrativo Federal)",
        ],
        "aplicabilidade": "Use quando o autuado não foi cientificado pessoalmente ou quando a lavratura do auto tem vícios formais.",
        "contra_argumentos": [
            "IBAMA sustentará que a lavratura por edital supriu a ciência — rebater com art. 26 da Lei 9.784/99 (só cabível quando o autuado está em local incerto ou recusou ciência comprovadamente).",
            "Argumento de 'fato continuado' — rebater com prova de encerramento da atividade antes da autuação.",
        ],
        "proxima_acao": "Protocolar Defesa Administrativa no IBAMA em 20 dias úteis (art. 113 Dec. 6.514/08). Caso negada, recurso administrativo ao Superintendente Regional, depois Presidente do IBAMA, depois ação anulatória.",
        "publico_alvo": ["produtor_autuado", "advogado", "consultor_ambiental"],
    },
    {
        "slug": "prescricao-intercorrente-auto-ibama",
        "titulo": "Prescrição intercorrente no processo administrativo do Auto IBAMA (paralisação >3 anos)",
        "area": "ambiental",
        "situacao": "Processo administrativo IBAMA parado por mais de 3 anos sem movimentação (art. 21 Lei 9.873/99).",
        "sumula_propria": (
            "A inércia do IBAMA por mais de 3 anos consecutivos no processo administrativo configura prescrição "
            "intercorrente nos termos do art. 21 da Lei 9.873/99, declarando-se a extinção da exigibilidade do crédito."
        ),
        "argumentos_principais": [
            {"enunciado": "Paralisação injustificada superior a 3 anos", "fundamentacao": "Lei 9.873/99 art. 21", "peso": 3},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STJ", "numero": "REsp 1.678.135/PR", "ementa_resumida": "Prescrição intercorrente administrativa aplicável aos autos IBAMA.", "url": ""},
        ],
        "legislacao_aplicavel": ["Lei 9.873/99 art. 21", "Lei 9.784/99 art. 24"],
        "aplicabilidade": "Processo administrativo parado > 3 anos por ato não imputável ao autuado.",
        "contra_argumentos": ["IBAMA tentará justificar a paralisação por 'complexidade do caso' ou 'necessidade de perícia' — rebater com juntada do andamento e demonstrando ausência de diligência nos últimos 3 anos."],
        "proxima_acao": "Peticionar ao presidente do processo solicitando declaração de prescrição intercorrente. Em caso de indeferimento, ação declaratória.",
        "publico_alvo": ["produtor_autuado", "advogado"],
    },
    {
        "slug": "embargos-execucao-fiscal-itr",
        "titulo": "Embargos à Execução Fiscal de ITR por erro no Valor da Terra Nua (VTN)",
        "area": "tributario",
        "situacao": "Execução fiscal do ITR baseada em arbitramento do VTN pela Receita Federal sem consideração da realidade fundiária.",
        "sumula_propria": (
            "O VTN arbitrado pela Receita deve refletir o valor real do imóvel sem considerar benfeitorias, "
            "culturas e gado. Imóveis com restrição ambiental (APP, RL, embargos) têm direito a redução. "
            "Laudo de avaliação oficial contestando o VTN é prova plena (STJ REsp 1.144.982/PR)."
        ),
        "argumentos_principais": [
            {"enunciado": "VTN arbitrado acima do valor de mercado — laudo comprova", "fundamentacao": "Lei 9.393/96 art. 10, §1º, II + STJ", "peso": 3},
            {"enunciado": "Não computo da área de Reserva Legal/APP", "fundamentacao": "Lei 9.393/96 art. 10, §1º, V + IN RFB 2.166/07", "peso": 3},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STJ", "numero": "REsp 1.144.982/PR", "ementa_resumida": "VTN deve refletir valor real, excluindo benfeitorias e culturas.", "url": ""},
        ],
        "legislacao_aplicavel": ["Lei 9.393/96 (ITR)", "Lei 6.830/80 (Exec. Fiscal)", "CF art. 153, VI"],
        "aplicabilidade": "ITR executado com VTN manifestamente acima do valor de mercado.",
        "contra_argumentos": [
            "Fazenda exigirá laudo por perito oficial — contratar engenheiro agrônomo com ART.",
        ],
        "proxima_acao": "Apresentar embargos à execução em 30 dias úteis a contar da intimação da penhora.",
        "publico_alvo": ["produtor", "advogado"],
    },
    {
        "slug": "usucapiao-rural-especial",
        "titulo": "Usucapião Especial Rural (CF art. 191) — área <=50ha, posse ininterrupta 5 anos",
        "area": "fundiario",
        "situacao": "Posseiro rural de área de até 50 ha, sem proprietário de outro imóvel, que produza e torne a terra produtiva por 5 anos.",
        "sumula_propria": (
            "Nos termos do art. 191 da CF/88 e art. 1.239 do CC, ao possuidor de área rural até 50 ha, "
            "não proprietário de outro imóvel rural, que a torne produtiva por trabalho próprio/família por 5 anos ininterruptos, "
            "é conferida a propriedade, independente de justo título ou boa-fé."
        ),
        "argumentos_principais": [
            {"enunciado": "Posse mansa e pacífica", "fundamentacao": "CF art. 191 + CC art. 1.239", "peso": 3},
            {"enunciado": "Área rural até 50 ha", "fundamentacao": "Comprovada por laudo de medição", "peso": 3},
            {"enunciado": "Não ser proprietário de outro imóvel rural", "fundamentacao": "Certidão INCRA + RGI", "peso": 2},
            {"enunciado": "Produção pelo trabalho próprio/família", "fundamentacao": "Notas fiscais, testemunhas, DAP/CAF", "peso": 2},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STJ", "numero": "REsp 1.165.894/MG", "ementa_resumida": "Usucapião especial rural dispensa justo título e boa-fé.", "url": ""},
        ],
        "legislacao_aplicavel": ["CF art. 191", "CC art. 1.239", "Lei 6.969/81"],
        "aplicabilidade": "Posse rural até 50 ha por 5 anos sem propriedade de outro imóvel.",
        "contra_argumentos": ["Alegação de precariedade da posse — rebater com testemunhas, notas de produção, fotos datadas."],
        "proxima_acao": "Ação de usucapião em varas da justiça comum. Ingressar também com pedido administrativo no INCRA para reconhecimento simplificado (Lei 13.465/17).",
        "publico_alvo": ["posseiro", "pequeno_agricultor", "advogado"],
    },
    {
        "slug": "previdencia-rural-segurado-especial",
        "titulo": "Aposentadoria do Segurado Especial Rural (CF art. 201, §7º, II)",
        "area": "previdenciario",
        "situacao": "Agricultor familiar, pescador, indígena ou quilombola que pleiteia aposentadoria sem contribuição prévia.",
        "sumula_propria": (
            "O segurado especial rural (CF art. 201, §7º, II) tem direito à aposentadoria por idade (60h/55m) "
            "mediante comprovação da atividade rural em regime de economia familiar por no mínimo 15 anos "
            "(art. 39, Lei 8.213/91), dispensada contribuição prévia."
        ),
        "argumentos_principais": [
            {"enunciado": "Atividade rural em economia familiar (≥15 anos)", "fundamentacao": "Lei 8.213/91 art. 11, VII + art. 39", "peso": 3},
            {"enunciado": "Início de prova material + testemunhas", "fundamentacao": "Súmula 577 STJ", "peso": 3},
        ],
        "precedentes_sugeridos": [{"tribunal": "STJ", "numero": "Súmula 577", "ementa_resumida": "Admite-se prova documental em nome de terceiro para comprovar atividade rural.", "url": ""}],
        "legislacao_aplicavel": ["CF art. 201, §7º", "Lei 8.213/91 art. 11, VII", "Decreto 3.048/99"],
        "aplicabilidade": "Trabalhador rural familiar sem contribuição prévia.",
        "contra_argumentos": ["INSS exigirá início de prova material em nome próprio — Súmula 577 STJ permite nome de cônjuge/familiar."],
        "proxima_acao": "Pedido administrativo no INSS. Se negado, ação judicial.",
        "publico_alvo": ["agricultor_familiar", "advogado_previdenciario"],
    },
    {
        "slug": "retirada-lista-suja-mte",
        "titulo": "Retirada da Lista Suja do Trabalho Escravo por vício na fiscalização",
        "area": "trabalhista",
        "situacao": "Empregador incluído na Lista de Transparência (Portaria MTE 1.293/17) que contesta os achados da fiscalização.",
        "sumula_propria": (
            "A inclusão na Lista Suja só é válida após processo administrativo com contraditório e ampla "
            "defesa. Havendo vício na fiscalização — ausência de autuado, descrição genérica, falta de "
            "qualificação de trabalhadores resgatados — cabe Mandado de Segurança para exclusão imediata."
        ),
        "argumentos_principais": [
            {"enunciado": "Violação do contraditório", "fundamentacao": "Portaria 1.293/17 + CF art. 5º, LV", "peso": 3},
            {"enunciado": "Ausência de descrição da 'condição análoga à de escravo'", "fundamentacao": "CP art. 149 exige elementos específicos: trabalhos forçados, jornada exaustiva, servidão por dívida ou condições degradantes.", "peso": 3},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STF", "numero": "ADPF 742", "ementa_resumida": "Validou a Lista Suja como instrumento de política pública.", "url": ""},
        ],
        "legislacao_aplicavel": [
            "CP art. 149",
            "CF art. 5º, LV",
            "Portaria MTE 1.293/17",
        ],
        "aplicabilidade": "Empregador que contesta inclusão na Lista com base em vícios formais ou mérito.",
        "contra_argumentos": ["MTE sustentará presunção de veracidade — rebater com contraprova documental e depoimentos."],
        "proxima_acao": "Recurso administrativo ao MTE. Em paralelo, MS em Justiça Federal. Bloqueio da Lista é automático (efeito suspensivo da liminar).",
        "publico_alvo": ["empregador_rural", "advogado_trabalhista"],
    },
    {
        "slug": "nulidade-embargo-ibama-desproporcional",
        "titulo": "Nulidade do embargo IBAMA por desproporcionalidade (área embargada > área degradada)",
        "area": "ambiental",
        "situacao": "IBAMA embarga toda a fazenda quando a degradação ocorreu em apenas parte da área.",
        "sumula_propria": (
            "O embargo ambiental é medida cautelar administrativa, devendo ser proporcional ao dano. "
            "Embargar toda a propriedade quando a degradação ocorreu em fração mínima viola o princípio da "
            "proporcionalidade (CF art. 5º, LIV) e a razoabilidade (Lei 9.784/99 art. 2º)."
        ),
        "argumentos_principais": [
            {"enunciado": "Desproporção entre área embargada e área degradada", "fundamentacao": "Laudo + medição", "peso": 3},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STJ", "numero": "REsp 1.456.332/MT", "ementa_resumida": "Embargo total quando degradação é parcial configura desproporção.", "url": ""},
        ],
        "legislacao_aplicavel": ["Dec. 6.514/08", "CF art. 5º, LIV"],
        "aplicabilidade": "Embargo abrangente sobre área produtiva sem relação causal com degradação.",
        "contra_argumentos": ["IBAMA alegará risco de continuidade — rebater com plano de manejo e TAC."],
        "proxima_acao": "Defesa administrativa + pedido de levantamento parcial do embargo.",
        "publico_alvo": ["produtor", "consultor_ambiental"],
    },
    {
        "slug": "compensacao-rl-cra",
        "titulo": "Compensação de Reserva Legal via CRA (Lei 12.651/12 art. 44-50)",
        "area": "ambiental",
        "situacao": "Imóvel com déficit de Reserva Legal — regularização via aquisição de Cotas de Reserva Ambiental.",
        "sumula_propria": (
            "Havendo déficit de RL na propriedade, o Código Florestal (Lei 12.651/12) permite a compensação por "
            "meio de: (a) CRA — aquisição de cotas de propriedade superavitária no mesmo bioma; (b) arrendamento "
            "de área sob regime de servidão ambiental; (c) doação ao poder público de área em UC pendente de regularização."
        ),
        "argumentos_principais": [
            {"enunciado": "Déficit de RL comprovado por CAR", "fundamentacao": "Lei 12.651/12 art. 12 + CAR", "peso": 2},
            {"enunciado": "Direito à compensação por CRA", "fundamentacao": "Lei 12.651/12 art. 44-50", "peso": 3},
        ],
        "precedentes_sugeridos": [],
        "legislacao_aplicavel": ["Lei 12.651/12 art. 44-50", "Dec. 7.830/12"],
        "aplicabilidade": "Imóvel com déficit de RL que busca alternativa à recomposição in loco.",
        "contra_argumentos": ["Órgão ambiental pode exigir recomposição in loco se a área for crítica — verificar PRADA."],
        "proxima_acao": "Aderir ao PRADA do estado. Identificar CRAs disponíveis (SICAR).",
        "publico_alvo": ["produtor", "consultor_ambiental"],
    },
    {
        "slug": "defesa-lista-suja-mte",
        "titulo": "Defesa da Inclusão na Lista Suja por via administrativa + MS",
        "area": "trabalhista",
        "situacao": "Proposta de inclusão na Lista Suja após fiscalização. Prazo de defesa administrativa.",
        "sumula_propria": (
            "Há 3 fases: (1) fiscalização; (2) instauração do contencioso administrativo com 10 dias de defesa "
            "escrita; (3) decisão de inclusão publicada em DOU. Em qualquer fase cabe contraditório pleno e, "
            "havendo violação, Mandado de Segurança com pedido de liminar para impedir publicação."
        ),
        "argumentos_principais": [
            {"enunciado": "Ausência de elementos do art. 149 CP", "fundamentacao": "Trabalho forçado, jornada exaustiva, servidão por dívida, condições degradantes", "peso": 3},
            {"enunciado": "Vícios no relatório de fiscalização", "fundamentacao": "Depoimentos não qualificados, laudos incompletos", "peso": 2},
        ],
        "precedentes_sugeridos": [],
        "legislacao_aplicavel": ["Portaria MTE 1.293/17", "CP art. 149"],
        "aplicabilidade": "Fiscalização em curso ou concluída com inclusão pendente.",
        "contra_argumentos": [],
        "proxima_acao": "Defesa escrita em 10 dias + MS preventivo/liminar se publicação iminente.",
        "publico_alvo": ["empregador_rural", "advogado_trabalhista"],
    },
    {
        "slug": "dissidio-rural-enquadramento",
        "titulo": "Enquadramento do trabalhador rural (Lei 5.889/73) vs CLT urbana",
        "area": "trabalhista",
        "situacao": "Trabalhador reclamando vínculo CLT urbano, quando o correto é rural (Lei 5.889/73).",
        "sumula_propria": (
            "Trabalhador rural tem regime próprio (Lei 5.889/73) com jornada, horas extras e adicional noturno "
            "distintos. O enquadramento depende da atividade preponderante do empregador e do labor efetivo — "
            "não da localização (imóvel urbano pode ser rural se destinado à atividade agrícola)."
        ),
        "argumentos_principais": [
            {"enunciado": "Preponderância da atividade rural no empregador", "fundamentacao": "CF art. 7, XXIX; Lei 5.889/73 art. 2º", "peso": 3},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "TST", "numero": "RR-10245-25", "ementa_resumida": "Fazendas de agropecuária devem aplicar Lei 5.889/73.", "url": ""},
        ],
        "legislacao_aplicavel": ["Lei 5.889/73", "Dec. 73.626/74", "NR-31"],
        "aplicabilidade": "Defesa em reclamação trabalhista em que o autor alega regime urbano indevidamente.",
        "contra_argumentos": ["Autor alegará que desempenhava função auxiliar/urbana — rebater com atividade preponderante."],
        "proxima_acao": "Contestação trabalhista com prova testemunhal e CNAE do empregador.",
        "publico_alvo": ["empregador_rural", "advogado_trabalhista"],
    },
    {
        "slug": "reclassificacao-parceria-arrendamento",
        "titulo": "Defesa contra reclassificação de Parceria para Arrendamento (tributário + trabalhista)",
        "area": "trabalhista",
        "situacao": "Fiscalização do trabalho ou Receita tentando reclassificar parceria agrícola como arrendamento (e/ou vínculo empregatício).",
        "sumula_propria": (
            "A parceria é válida quando há real partilha de RISCOS e FRUTOS (art. 96 Lei 4.504/64). "
            "Reclassificar como arrendamento (pagamento fixo) ou vínculo (subordinação) exige prova clara de "
            "descaracterização — partilha insignificante, subordinação hierárquica ou assunção total do risco "
            "pelo suposto parceiro outorgante."
        ),
        "argumentos_principais": [
            {"enunciado": "Partilha efetiva de frutos e riscos", "fundamentacao": "Contrato + movimentação bancária + prova testemunhal", "peso": 3},
            {"enunciado": "Autonomia do parceiro outorgado", "fundamentacao": "Ausência de controle de jornada, regras diretas, uniformes", "peso": 2},
        ],
        "precedentes_sugeridos": [],
        "legislacao_aplicavel": ["Lei 4.504/64", "CC art. 981"],
        "aplicabilidade": "Autuação fiscal ou reclamação trabalhista que tenta descaracterizar parceria.",
        "contra_argumentos": [],
        "proxima_acao": "Defesa com cálculo real de partilha e demonstração de autonomia operacional.",
        "publico_alvo": ["proprietario_rural", "advogado"],
    },
    {
        "slug": "revisao-contrato-credito-rural-pronaf",
        "titulo": "Revisão de contrato de crédito rural (PRONAF/PRONAMP) por onerosidade excessiva",
        "area": "tributario",
        "situacao": "Contrato de crédito rural subsidiado cuja taxa reajustada excede o teto legal ou descumpre a Res. CMN 5.193/24.",
        "sumula_propria": (
            "Contratos de crédito rural subsidiado estão sujeitos a tetos legais (MCR 2.9). Aplicação de juros "
            "acima do permitido, encargos abusivos ou descumprimento da Resolução 5.193/24 geram direito à revisão "
            "(CC art. 317-478 — onerosidade excessiva) e à repetição do indébito."
        ),
        "argumentos_principais": [
            {"enunciado": "Taxa acima do teto MCR 2.9", "fundamentacao": "Res. CMN 5.193/24 + MCR", "peso": 3},
        ],
        "precedentes_sugeridos": [
            {"tribunal": "STJ", "numero": "Súmula 379", "ementa_resumida": "Limitação de juros aplicável ao crédito rural.", "url": ""},
        ],
        "legislacao_aplicavel": ["CC art. 317-478", "Lei 4.829/65", "Res. CMN 5.193/24"],
        "aplicabilidade": "Contrato PRONAF/PRONAMP/PCA com encargos superiores ao legal.",
        "contra_argumentos": ["Banco sustentará validade contratual — rebater com laudo de perito financeiro."],
        "proxima_acao": "Ação revisional + repetição do indébito.",
        "publico_alvo": ["pequeno_agricultor", "produtor", "advogado"],
    },
]


# ==========================================================================
# Legislação Agro — sementes (50+ normativos federais/estaduais)
# ==========================================================================

LEGISLACAO_SEED = [
    # --- FEDERAIS — Ambiental ---
    {"slug": "cf-1988", "titulo": "Constituição Federal de 1988", "esfera": "federal", "ano": 1988, "tipo": "constituicao", "orgao": "ANC", "ementa": "Constituição Federal — arts. 5º, 23, 170, 184-191, 225, 231.", "temas": ["fundiario", "ambiental", "tributario", "trabalhista"], "url_oficial": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm", "resumo": "Base constitucional agrária (art. 184 desapropriação para reforma agrária), ambiental (art. 225), indígena (art. 231).", "situacao": "vigente"},
    {"slug": "lei-12651-2012", "titulo": "Código Florestal (Lei 12.651/12)", "esfera": "federal", "ano": 2012, "tipo": "lei", "numero": "12.651", "orgao": "Congresso", "ementa": "Dispõe sobre a proteção da vegetação nativa.", "temas": ["reserva_legal", "app", "cra", "car"], "url_oficial": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12651.htm", "resumo": "Novo Código Florestal — define APPs, Reserva Legal, CAR, CRA, PRADA.", "situacao": "vigente"},
    {"slug": "lei-9605-1998", "titulo": "Lei de Crimes Ambientais (9.605/98)", "esfera": "federal", "ano": 1998, "tipo": "lei", "numero": "9.605", "orgao": "Congresso", "ementa": "Sanções penais e administrativas por condutas lesivas ao meio ambiente.", "temas": ["penal_agro", "ambiental"], "url_oficial": "https://www.planalto.gov.br/ccivil_03/leis/l9605.htm", "resumo": "Criminaliza desmate, incêndio, caça ilegal. Responsabilidade da PJ.", "situacao": "vigente"},
    {"slug": "decreto-6514-2008", "titulo": "Decreto 6.514/08 (regulamento infrações ambientais)", "esfera": "federal", "ano": 2008, "tipo": "decreto", "numero": "6.514", "orgao": "Executivo", "ementa": "Infrações e sanções administrativas ao meio ambiente.", "temas": ["ambiental"], "url_oficial": "", "resumo": "Regulamenta art. 70 Lei 9.605/98 — processo administrativo IBAMA, multas, embargos.", "situacao": "vigente"},
    {"slug": "lei-9985-2000", "titulo": "SNUC — Sistema Nacional de Unidades de Conservação (Lei 9.985/00)", "esfera": "federal", "ano": 2000, "tipo": "lei", "numero": "9.985", "orgao": "Congresso", "ementa": "Institui o SNUC.", "temas": ["ambiental", "uc"], "url_oficial": "", "resumo": "Define categorias de UC (proteção integral vs uso sustentável).", "situacao": "vigente"},
    {"slug": "lei-9784-1999", "titulo": "Lei do Processo Administrativo Federal (9.784/99)", "esfera": "federal", "ano": 1999, "tipo": "lei", "numero": "9.784", "orgao": "Congresso", "ementa": "Regula o processo administrativo no âmbito da Adm Pública Federal.", "temas": ["administrativo", "ambiental"], "resumo": "Fundamenta defesa em processo IBAMA, INCRA etc.", "situacao": "vigente"},
    # --- FEDERAIS — Fundiário ---
    {"slug": "lei-4504-1964", "titulo": "Estatuto da Terra (Lei 4.504/64)", "esfera": "federal", "ano": 1964, "tipo": "lei", "numero": "4.504", "orgao": "Congresso", "ementa": "Dispõe sobre o Estatuto da Terra.", "temas": ["fundiario", "arrendamento", "parceria"], "resumo": "Base para arrendamento, parceria, reforma agrária e ITR.", "situacao": "vigente"},
    {"slug": "decreto-59566-1966", "titulo": "Decreto 59.566/66 (Regulamento do Estatuto da Terra)", "esfera": "federal", "ano": 1966, "tipo": "decreto", "numero": "59.566", "orgao": "Executivo", "ementa": "Regulamenta o Estatuto da Terra.", "temas": ["fundiario", "arrendamento"], "resumo": "Detalha prazos mínimos, valor limite e preferência em arrendamento/parceria.", "situacao": "vigente"},
    {"slug": "lei-5868-1972", "titulo": "Lei 5.868/72 (SNCR)", "esfera": "federal", "ano": 1972, "tipo": "lei", "numero": "5.868", "orgao": "Congresso", "ementa": "Sistema Nacional de Cadastro Rural.", "temas": ["fundiario", "incra", "ccir"], "resumo": "Cria SNCR, CCIR e NIRF. Base da tributação e transmissão.", "situacao": "vigente"},
    {"slug": "lei-10267-2001", "titulo": "Lei do Georreferenciamento (10.267/01)", "esfera": "federal", "ano": 2001, "tipo": "lei", "numero": "10.267", "orgao": "Congresso", "ementa": "Altera dispositivos sobre registro de imóveis rurais.", "temas": ["fundiario", "sigef"], "resumo": "Base do SIGEF — georreferenciamento obrigatório para imóveis >=100 ha.", "situacao": "vigente"},
    {"slug": "lei-13465-2017", "titulo": "Lei 13.465/17 (Regularização Fundiária Urbana e Rural)", "esfera": "federal", "ano": 2017, "tipo": "lei", "numero": "13.465", "orgao": "Congresso", "ementa": "Dispõe sobre regularização fundiária rural e urbana.", "temas": ["fundiario", "regularizacao"], "resumo": "Facilita titulação de terras públicas federais e urbanas.", "situacao": "vigente"},
    # --- FEDERAIS — ITR / Tributário ---
    {"slug": "lei-9393-1996", "titulo": "Lei do ITR (9.393/96)", "esfera": "federal", "ano": 1996, "tipo": "lei", "numero": "9.393", "orgao": "Congresso", "ementa": "Dispõe sobre o Imposto sobre a Propriedade Territorial Rural.", "temas": ["tributario", "itr"], "resumo": "Fato gerador, base de cálculo (VTN), alíquotas e isenções.", "situacao": "vigente"},
    # --- FEDERAIS — Trabalhista ---
    {"slug": "lei-5889-1973", "titulo": "Lei do Trabalho Rural (5.889/73)", "esfera": "federal", "ano": 1973, "tipo": "lei", "numero": "5.889", "orgao": "Congresso", "ementa": "Normas reguladoras do trabalho rural.", "temas": ["trabalhista", "rural"], "resumo": "Regime próprio do trabalhador rural — jornada, férias, aviso prévio.", "situacao": "vigente"},
    {"slug": "portaria-mte-1293-2017", "titulo": "Portaria MTE 1.293/17 (Lista Suja)", "esfera": "federal", "ano": 2017, "tipo": "portaria", "numero": "1.293", "orgao": "MTE", "ementa": "Procedimento para divulgação do Cadastro de Empregadores (Lista Suja).", "temas": ["trabalhista", "lista_suja"], "resumo": "Detalha fluxo administrativo para inclusão na Lista Suja.", "situacao": "vigente"},
    # --- FEDERAIS — Crédito Rural ---
    {"slug": "lei-4829-1965", "titulo": "Lei do Crédito Rural (4.829/65)", "esfera": "federal", "ano": 1965, "tipo": "lei", "numero": "4.829", "orgao": "Congresso", "ementa": "Institui o crédito rural.", "temas": ["credito_rural"], "resumo": "Base do SNCR — financiamento a custeio, investimento e comercialização.", "situacao": "vigente"},
    {"slug": "res-cmn-5193-2024", "titulo": "Resolução CMN 5.193/24 (MCR 2.9 - Impedimentos)", "esfera": "federal", "ano": 2024, "tipo": "resolucao", "numero": "5.193", "orgao": "CMN", "ementa": "Impedimentos socioambientais para crédito rural.", "temas": ["credito_rural", "mcr29", "compliance"], "resumo": "32 critérios de elegibilidade MCR 2.9: CAR, desmate, embargo, lista suja etc.", "situacao": "vigente"},
    {"slug": "lei-8929-1994", "titulo": "Lei da CPR (8.929/94)", "esfera": "federal", "ano": 1994, "tipo": "lei", "numero": "8.929", "orgao": "Congresso", "ementa": "Cédula de Produto Rural.", "temas": ["credito_rural", "cpr"], "resumo": "Título executivo extrajudicial para antecipação de receitas.", "situacao": "vigente"},
    {"slug": "lei-11076-2004", "titulo": "Lei dos Títulos Agro (11.076/04)", "esfera": "federal", "ano": 2004, "tipo": "lei", "numero": "11.076", "orgao": "Congresso", "ementa": "CDA, WA, CRA, LCA, CDCA.", "temas": ["credito_rural", "cda_wa", "cra"], "resumo": "Cria CDA/WA — instrumentos de garantia em armazém.", "situacao": "vigente"},
    # --- FEDERAIS — ESG/EUDR ---
    {"slug": "ue-2023-1115", "titulo": "Regulamento UE 2023/1115 (EUDR)", "esfera": "federal", "ano": 2023, "tipo": "regulamento", "numero": "2023/1115", "orgao": "União Europeia", "ementa": "Regulamenta commodities livres de desmatamento.", "temas": ["eudr", "exportacao"], "resumo": "Commodities (soja, carne, café, cacau, óleo palma, borracha, madeira) precisam provar desmate-zero pós-31/12/2020.", "situacao": "vigente"},
    # --- ESTADUAIS — destaque por UF (amostra) ---
    {"slug": "mt-lei-estadual-ambiental-10106", "titulo": "Política Estadual Ambiental — MT (Lei 10.106/14)", "esfera": "estadual", "uf": "MT", "ano": 2014, "tipo": "lei", "numero": "10.106", "orgao": "SEMA/MT", "temas": ["ambiental", "licenciamento"], "resumo": "Licenciamento ambiental rural estadual MT — LAU.", "situacao": "vigente"},
    {"slug": "ma-lei-licenciamento-rural", "titulo": "Lei Estadual de Licenciamento Rural — MA", "esfera": "estadual", "uf": "MA", "ano": 2022, "tipo": "lei", "orgao": "SEMA/MA", "temas": ["ambiental", "licenciamento"], "situacao": "vigente"},
    {"slug": "ba-reg-fundiaria", "titulo": "Regularização Fundiária — BA", "esfera": "estadual", "uf": "BA", "ano": 2018, "tipo": "lei", "orgao": "INTERBA", "temas": ["fundiario", "regularizacao"], "situacao": "vigente"},
    {"slug": "pr-zee-2024", "titulo": "ZEE Paraná", "esfera": "estadual", "uf": "PR", "ano": 2024, "tipo": "decreto", "orgao": "SEDEST/PR", "temas": ["zee", "planejamento"], "situacao": "vigente"},
    {"slug": "ms-fogo-2024", "titulo": "Plano Estadual de Prevenção a Incêndios — MS", "esfera": "estadual", "uf": "MS", "ano": 2024, "tipo": "decreto", "orgao": "IMASUL/MS", "temas": ["ambiental", "fogo"], "situacao": "vigente"},
    # --- MAPA / ANVISA / AGROFIT ---
    {"slug": "lei-7802-1989", "titulo": "Lei dos Agrotóxicos (7.802/89)", "esfera": "federal", "ano": 1989, "tipo": "lei", "numero": "7.802", "orgao": "Congresso", "ementa": "Pesquisa, produção, comercialização e uso de agrotóxicos.", "temas": ["agrotoxico", "agrofit"], "situacao": "vigente"},
    {"slug": "decreto-4074-2002", "titulo": "Decreto 4.074/02 (regulamento agrotóxicos)", "esfera": "federal", "ano": 2002, "tipo": "decreto", "numero": "4.074", "orgao": "Executivo", "temas": ["agrotoxico"], "situacao": "vigente"},
    {"slug": "in-mapa-46-2017", "titulo": "IN MAPA 46/17 (GTA)", "esfera": "federal", "ano": 2017, "tipo": "instrucao_normativa", "numero": "46", "orgao": "MAPA", "temas": ["pecuaria", "gta"], "resumo": "Guia de Trânsito Animal — obrigatória para deslocamento de animais.", "situacao": "vigente"},
    # --- Outros ---
    {"slug": "lei-13288-2016", "titulo": "Lei da Integração (13.288/16)", "esfera": "federal", "ano": 2016, "tipo": "lei", "numero": "13.288", "orgao": "Congresso", "temas": ["integracao", "pecuaria", "suinos", "aves"], "resumo": "Relação entre integrador e produtor integrado (aves, suínos, bovinos).", "situacao": "vigente"},
    {"slug": "lei-14119-2021", "titulo": "Política Nacional de PSA (14.119/21)", "esfera": "federal", "ano": 2021, "tipo": "lei", "numero": "14.119", "orgao": "Congresso", "temas": ["psa", "ambiental"], "resumo": "Pagamento por Serviços Ambientais.", "situacao": "vigente"},
    {"slug": "lei-9433-1997", "titulo": "Lei das Águas (9.433/97)", "esfera": "federal", "ano": 1997, "tipo": "lei", "numero": "9.433", "orgao": "Congresso", "temas": ["recursos_hidricos", "outorga"], "resumo": "Política Nacional de Recursos Hídricos — base das outorgas ANA.", "situacao": "vigente"},
    {"slug": "lei-13465-2017-rf", "titulo": "Lei da Regularização Fundiária (13.465/17)", "esfera": "federal", "ano": 2017, "tipo": "lei", "numero": "13.465", "orgao": "Congresso", "temas": ["fundiario", "regularizacao"], "resumo": "REURB, ReflorAmazônia, titulação INCRA.", "situacao": "vigente"},
    {"slug": "lei-12097-2009", "titulo": "Lei da Rastreabilidade Bovina (12.097/09)", "esfera": "federal", "ano": 2009, "tipo": "lei", "numero": "12.097", "orgao": "Congresso", "temas": ["pecuaria", "rastreabilidade"], "situacao": "vigente"},
    {"slug": "lei-8171-1991", "titulo": "Lei da Política Agrícola (8.171/91)", "esfera": "federal", "ano": 1991, "tipo": "lei", "numero": "8.171", "orgao": "Congresso", "temas": ["politica_agricola"], "situacao": "vigente"},
    {"slug": "cc-art-1196", "titulo": "Código Civil art. 1.196 (Posse)", "esfera": "federal", "ano": 2002, "tipo": "codigo", "orgao": "Congresso", "temas": ["fundiario", "posse"], "situacao": "vigente"},
    {"slug": "lei-8213-1991", "titulo": "Lei dos Benefícios Previdenciários (8.213/91)", "esfera": "federal", "ano": 1991, "tipo": "lei", "numero": "8.213", "orgao": "Congresso", "temas": ["previdenciario"], "resumo": "Segurado especial rural, aposentadoria por idade rural.", "situacao": "vigente"},
    {"slug": "dec-3048-1999", "titulo": "Decreto 3.048/99 (RPS)", "esfera": "federal", "ano": 1999, "tipo": "decreto", "numero": "3.048", "orgao": "Executivo", "temas": ["previdenciario"], "situacao": "vigente"},
    {"slug": "in-mapa-78-2004", "titulo": "IN MAPA 78/04 (Armazenagem)", "esfera": "federal", "ano": 2004, "tipo": "instrucao_normativa", "numero": "78", "orgao": "MAPA", "temas": ["armazenagem", "cda_wa"], "situacao": "vigente"},
    {"slug": "nr-31-2020", "titulo": "NR-31 Atualizada (2020)", "esfera": "federal", "ano": 2020, "tipo": "norma_regulamentadora", "numero": "31", "orgao": "MTE", "temas": ["trabalhista", "nr31"], "resumo": "Segurança e saúde no trabalho rural.", "situacao": "vigente"},
    {"slug": "lei-12440-2011", "titulo": "Lei da CNDT (12.440/11)", "esfera": "federal", "ano": 2011, "tipo": "lei", "numero": "12.440", "orgao": "Congresso", "temas": ["trabalhista", "cndt"], "situacao": "vigente"},
    {"slug": "lei-12846-2013", "titulo": "Lei Anticorrupção (12.846/13)", "esfera": "federal", "ano": 2013, "tipo": "lei", "numero": "12.846", "orgao": "Congresso", "temas": ["compliance", "ceis", "cnep"], "resumo": "CEIS/CNEP — sanções administrativas contra PJ.", "situacao": "vigente"},
    {"slug": "lei-6830-1980", "titulo": "Lei de Execução Fiscal (6.830/80)", "esfera": "federal", "ano": 1980, "tipo": "lei", "numero": "6.830", "orgao": "Congresso", "temas": ["tributario", "execucao_fiscal"], "situacao": "vigente"},
    {"slug": "lei-9873-1999", "titulo": "Lei da Prescrição Administrativa (9.873/99)", "esfera": "federal", "ano": 1999, "tipo": "lei", "numero": "9.873", "orgao": "Congresso", "temas": ["administrativo", "prescricao"], "resumo": "Prescrição administrativa de 5 anos + intercorrente de 3.", "situacao": "vigente"},
    {"slug": "lei-6969-1981", "titulo": "Lei do Usucapião Especial Rural (6.969/81)", "esfera": "federal", "ano": 1981, "tipo": "lei", "numero": "6.969", "orgao": "Congresso", "temas": ["fundiario", "usucapiao"], "situacao": "vigente"},
    {"slug": "cdc-agronegocio", "titulo": "CDC aplicado ao Agronegócio", "esfera": "federal", "ano": 1990, "tipo": "lei", "numero": "8.078", "orgao": "Congresso", "temas": ["consumidor"], "resumo": "Quando o produtor é destinatário final de insumos, aplica-se CDC.", "situacao": "vigente"},
    {"slug": "lei-4947-1966", "titulo": "Lei dos Distritos de Irrigação (4.947/66)", "esfera": "federal", "ano": 1966, "tipo": "lei", "numero": "4.947", "orgao": "Congresso", "temas": ["irrigacao"], "situacao": "vigente"},
    # --- Alguns específicos estaduais ---
    {"slug": "rs-dec-irrigacao", "titulo": "Dec. Estadual Irrigação RS", "esfera": "estadual", "uf": "RS", "ano": 2020, "tipo": "decreto", "orgao": "SEMA/RS", "temas": ["irrigacao"], "situacao": "vigente"},
    {"slug": "go-lei-fogo", "titulo": "Lei Estadual de Queima Controlada — GO", "esfera": "estadual", "uf": "GO", "ano": 2021, "tipo": "lei", "orgao": "SEMAD/GO", "temas": ["fogo", "queima_controlada"], "situacao": "vigente"},
    {"slug": "mg-pda", "titulo": "Programa Desenvolvimento Agrícola — MG", "esfera": "estadual", "uf": "MG", "ano": 2019, "tipo": "decreto", "orgao": "Seapa/MG", "temas": ["politica_agricola"], "situacao": "vigente"},
    {"slug": "to-incentivo-fiscal-agro", "titulo": "Incentivos Fiscais Agro TO", "esfera": "estadual", "uf": "TO", "ano": 2023, "tipo": "lei", "orgao": "SEFAZ/TO", "temas": ["tributario", "icms"], "situacao": "vigente"},
    {"slug": "pa-fundo-amazonia-car", "titulo": "PA — Integração CAR estadual", "esfera": "estadual", "uf": "PA", "ano": 2022, "tipo": "decreto", "orgao": "SEMAS/PA", "temas": ["car", "ambiental"], "situacao": "vigente"},
    {"slug": "mt-procar", "titulo": "PROCAR MT (programa estadual de regularização CAR)", "esfera": "estadual", "uf": "MT", "ano": 2020, "tipo": "decreto", "orgao": "SEMA/MT", "temas": ["car"], "situacao": "vigente"},
]


def seed_juridico(force: bool = False) -> dict:
    """Insere sementes se tabelas vazias (ou se force=True)."""
    session = get_session()
    result = {"contratos": 0, "teses": 0, "legislacao": 0}
    try:
        # Contratos
        n = session.query(ContratoAgroTemplate).count()
        if n == 0 or force:
            if force and n > 0:
                session.query(ContratoAgroTemplate).delete()
            for data in CONTRATOS_SEED:
                session.add(ContratoAgroTemplate(**data))
            session.commit()
            result["contratos"] = len(CONTRATOS_SEED)

        # Teses
        n = session.query(TeseDefesaAgro).count()
        if n == 0 or force:
            if force and n > 0:
                session.query(TeseDefesaAgro).delete()
            for data in TESES_SEED:
                session.add(TeseDefesaAgro(**data))
            session.commit()
            result["teses"] = len(TESES_SEED)

        # Legislação
        n = session.query(LegislacaoAgro).count()
        if n == 0 or force:
            if force and n > 0:
                session.query(LegislacaoAgro).delete()
            for data in LEGISLACAO_SEED:
                session.add(LegislacaoAgro(**data))
            session.commit()
            result["legislacao"] = len(LEGISLACAO_SEED)
    finally:
        session.close()
    return result
