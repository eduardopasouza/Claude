"""
Sistema de jurisdição legal para imóveis rurais.

Cada estado brasileiro tem procedimentos diferentes para:
- Regularização fundiária
- Licenciamento ambiental
- Reserva Legal
- APP
- Outorga de água
- CAR estadual
- Órgão ambiental competente

Este módulo fornece as regras e procedimentos por estado,
permitindo que advogados e proprietários saibam exatamente
o que fazer em cada jurisdição.
"""

import logging
from typing import Optional

logger = logging.getLogger("agrojus")


# Base de dados de jurisdição por estado
JURISDICAO_POR_ESTADO = {
    "AC": {
        "estado": "Acre",
        "orgao_ambiental": "IMAC - Instituto de Meio Ambiente do Acre",
        "orgao_fundiario": "ITERACRE - Instituto de Terras do Acre",
        "sicar_estadual": "https://car.semas.pa.gov.br/",
        "legislacao_principal": "Lei Estadual 1.426/2001 (Política Estadual de Meio Ambiente)",
        "reserva_legal_percentual": "80% (Amazônia)",
        "bioma_predominante": "Amazônia",
        "particularidades": [
            "ZEE do Acre define áreas de uso e conservação",
            "Programa de Regularização Ambiental (PRA) via IMAC",
            "Estado com forte atuação em REDD+ e créditos de carbono",
        ],
        "procedimento_licenciamento": "Licenciamento via IMAC. LAR (Licença Ambiental Rural) para atividades agropecuárias. Dispensa para pequenas propriedades até 4 módulos fiscais.",
        "regularizacao_fundiaria": "ITERACRE faz titulação de terras estaduais. Imóveis em terras da União seguem procedimento federal via INCRA.",
    },
    "AL": {
        "estado": "Alagoas",
        "orgao_ambiental": "IMA/AL - Instituto do Meio Ambiente de Alagoas",
        "orgao_fundiario": "ITERAL - Instituto de Terras e Reforma Agrária de Alagoas",
        "legislacao_principal": "Lei Estadual 4.090/1979 (Política Estadual de Meio Ambiente)",
        "reserva_legal_percentual": "20% (Mata Atlântica/Cerrado)",
        "bioma_predominante": "Mata Atlântica",
        "particularidades": [
            "Área predominante de cana-de-açúcar",
            "Zona costeira com regras específicas de APP",
        ],
        "procedimento_licenciamento": "Licenciamento via IMA/AL. LP, LI e LO para atividades de impacto.",
        "regularizacao_fundiaria": "ITERAL atua na regularização de terras estaduais.",
    },
    "AM": {
        "estado": "Amazonas",
        "orgao_ambiental": "IPAAM - Instituto de Proteção Ambiental do Amazonas",
        "orgao_fundiario": "ITEAM - Instituto de Terras do Amazonas",
        "legislacao_principal": "Lei Complementar 53/2007 (Sistema Estadual de UCs)",
        "reserva_legal_percentual": "80% (Amazônia)",
        "bioma_predominante": "Amazônia",
        "particularidades": [
            "Maior estado em área, menor densidade demográfica rural",
            "Forte presença de Terras Indígenas e Unidades de Conservação",
            "ZEE do Amazonas em elaboração",
            "Programa Bolsa Floresta para comunidades tradicionais",
        ],
        "procedimento_licenciamento": "Licenciamento via IPAAM. RAP (Relatório Ambiental Preliminar) para atividades de baixo impacto.",
        "regularizacao_fundiaria": "ITEAM regulariza terras estaduais. Grande parte do território é federal (INCRA/FUNAI).",
    },
    "BA": {
        "estado": "Bahia",
        "orgao_ambiental": "INEMA - Instituto do Meio Ambiente e Recursos Hídricos",
        "orgao_fundiario": "CDA - Coordenação de Desenvolvimento Agrário",
        "legislacao_principal": "Lei Estadual 10.431/2006 (Política de Meio Ambiente)",
        "reserva_legal_percentual": "20% (Cerrado/Caatinga/Mata Atlântica), 35% no bioma Cerrado dentro da Amazônia Legal",
        "bioma_predominante": "Caatinga/Cerrado/Mata Atlântica",
        "particularidades": [
            "MATOPIBA: oeste baiano é fronteira agrícola de soja",
            "3 biomas diferentes exigem tratamento diferenciado",
            "CEFIR (Cadastro Estadual Florestal) integrado ao SICAR",
            "Forte produção de cacau no sul da Bahia",
        ],
        "procedimento_licenciamento": "Licenciamento via INEMA. CERFA (Certidão de Regularidade Florestal e Ambiental) para atividades rurais.",
        "regularizacao_fundiaria": "CDA atua na regularização. Programa Terra Legal para terras devolutas.",
    },
    "GO": {
        "estado": "Goiás",
        "orgao_ambiental": "SEMAD - Secretaria de Meio Ambiente e Desenvolvimento Sustentável",
        "orgao_fundiario": "IDAGO / AGRODEFESA",
        "legislacao_principal": "Lei Estadual 14.247/2002 (Política Florestal)",
        "reserva_legal_percentual": "20% (Cerrado), podendo ser 35% em áreas de transição para Amazônia",
        "bioma_predominante": "Cerrado",
        "particularidades": [
            "Forte produção de soja, milho e pecuária",
            "CAR-GO integrado ao SICAR nacional",
            "Programa de Regularização Ambiental (PRA-GO)",
            "Outorga de água é obrigatória para irrigação",
        ],
        "procedimento_licenciamento": "Licenciamento via SEMAD. LAU (Licença Ambiental Única) para atividades de baixo impacto agropecuário.",
        "regularizacao_fundiaria": "IDAGO regulariza terras devolutas estaduais.",
    },
    "MA": {
        "estado": "Maranhão",
        "orgao_ambiental": "SEMA-MA - Secretaria de Estado de Meio Ambiente e Recursos Naturais",
        "orgao_fundiario": "ITERMA - Instituto de Colonização e Terras do Maranhão",
        "legislacao_principal": "Lei Estadual 5.405/1992 (Código de Proteção Ambiental)",
        "reserva_legal_percentual": "80% (Amazônia no oeste), 35% (Cerrado na Amazônia Legal), 20% (demais)",
        "bioma_predominante": "Cerrado/Amazônia",
        "particularidades": [
            "MATOPIBA: sul do Maranhão é fronteira agrícola de soja",
            "Dupla jurisdição: parte Amazônia Legal (80% RL), parte fora",
            "Forte presença de comunidades quilombolas e TIs",
            "Conflitos fundiários históricos no sul e oeste",
            "Lei do Babaçu Livre em alguns municípios",
        ],
        "procedimento_licenciamento": "Licenciamento via SEMA-MA. LAR para atividades agropecuárias. Supressão de vegetação exige ASV da SEMA.",
        "regularizacao_fundiaria": "ITERMA regulariza terras estaduais. Alto índice de grilagem e sobreposição de títulos.",
    },
    "MG": {
        "estado": "Minas Gerais",
        "orgao_ambiental": "SEMAD/IEF-MG - Instituto Estadual de Florestas",
        "orgao_fundiario": "ITER-MG / Fundação Rural Minas",
        "sicar_estadual": "https://idesisema.meioambiente.mg.gov.br/",
        "legislacao_principal": "Lei Estadual 20.922/2013 (Política Florestal)",
        "reserva_legal_percentual": "20% (Cerrado/Mata Atlântica/Caatinga)",
        "bioma_predominante": "Cerrado/Mata Atlântica",
        "particularidades": [
            "IDE-SISEMA: portal de dados ambientais mais completo do país",
            "3 biomas: Cerrado, Mata Atlântica e Caatinga",
            "Forte produção de café (maior produtor nacional)",
            "SUPRAM: Superintendências Regionais de Regularização Ambiental",
            "AAF (Autorização Ambiental de Funcionamento) para baixo impacto",
        ],
        "procedimento_licenciamento": "Licenciamento trifásico (LP, LI, LO) via SUPRAM. AAF para atividades de baixo impacto. LAC para aquicultura.",
        "regularizacao_fundiaria": "Programa de Regularização Fundiária de Minas Gerais.",
    },
    "MS": {
        "estado": "Mato Grosso do Sul",
        "orgao_ambiental": "IMASUL - Instituto de Meio Ambiente de Mato Grosso do Sul",
        "orgao_fundiario": "AGRAER - Agência de Desenvolvimento Agrário",
        "legislacao_principal": "Lei Estadual 3.839/2009 (Política Estadual de Meio Ambiente)",
        "reserva_legal_percentual": "20% (Cerrado), 35% (Cerrado na Amazônia Legal, porção norte)",
        "bioma_predominante": "Cerrado/Pantanal/Mata Atlântica",
        "particularidades": [
            "Pantanal: regras especiais de uso (restrições severas)",
            "Forte produção de soja, milho e pecuária",
            "CAR-MS integrado ao SICAR",
            "Outorga de água obrigatória (IMASUL)",
        ],
        "procedimento_licenciamento": "Licenciamento via IMASUL. DAA (Declaração de Atividade Agropecuária) para atividades sem supressão.",
        "regularizacao_fundiaria": "AGRAER coordena regularização de assentamentos e terras estaduais.",
    },
    "MT": {
        "estado": "Mato Grosso",
        "orgao_ambiental": "SEMA-MT - Secretaria de Estado de Meio Ambiente",
        "orgao_fundiario": "INTERMAT - Instituto de Terras de Mato Grosso",
        "sicar_estadual": "https://monitoramento.sema.mt.gov.br/",
        "legislacao_principal": "Lei Complementar 592/2017 (Política Florestal)",
        "reserva_legal_percentual": "80% (Amazônia), 35% (Cerrado na Amazônia Legal), 20% (Cerrado fora da AL)",
        "bioma_predominante": "Amazônia/Cerrado/Pantanal",
        "particularidades": [
            "Maior produtor de soja e algodão do Brasil",
            "3 biomas com regras diferentes de RL no mesmo estado",
            "SEMA-MT tem sistema de monitoramento próprio avançado",
            "LAR (Licença Ambiental Rural) é obrigatória",
            "PRODES/DETER tem alta incidência de alertas",
            "Programa MT Legal para regularização ambiental",
        ],
        "procedimento_licenciamento": "Licenciamento via SEMA-MT. LAR obrigatória para todas as atividades agropecuárias. CAR-MT integrado ao SICAR. Supressão exige ASV com análise de imagem de satélite.",
        "regularizacao_fundiaria": "INTERMAT regulariza terras estaduais. Alto conflito em áreas de expansão agrícola na Amazônia.",
    },
    "PA": {
        "estado": "Pará",
        "orgao_ambiental": "SEMAS-PA - Secretaria de Estado de Meio Ambiente e Sustentabilidade",
        "orgao_fundiario": "ITERPA - Instituto de Terras do Pará",
        "sicar_estadual": "https://car.semas.pa.gov.br/",
        "legislacao_principal": "Lei Estadual 5.887/1995 (Política Estadual de Meio Ambiente)",
        "reserva_legal_percentual": "80% (Amazônia)",
        "bioma_predominante": "Amazônia",
        "particularidades": [
            "CAR-PA: sistema próprio (SICAR-PA) antes do SICAR nacional",
            "Maior número de embargos IBAMA do país",
            "Forte presença de TIs e UCs",
            "Programa Terra Legal Federal atuante",
            "Desmatamento: maior incidência de alertas DETER",
            "Frigoríficos TAC (compromisso contra desmatamento)",
        ],
        "procedimento_licenciamento": "Licenciamento via SEMAS-PA. LAR para atividades agropecuárias. Supressão exige ASV da SEMAS com análise geoespacial.",
        "regularizacao_fundiaria": "ITERPA regulariza terras estaduais. Terra Legal para terras federais. Alto índice de posses sem título.",
    },
    "PR": {
        "estado": "Paraná",
        "orgao_ambiental": "IAT - Instituto Água e Terra",
        "orgao_fundiario": "ITCG - Instituto de Terras, Cartografia e Geociências",
        "legislacao_principal": "Lei Estadual 20.507/2021 (Código Florestal Estadual)",
        "reserva_legal_percentual": "20% (Mata Atlântica)",
        "bioma_predominante": "Mata Atlântica",
        "particularidades": [
            "Alto nível de mecanização agrícola",
            "Forte produção de soja, milho, trigo e frango",
            "SISLEG substituído pelo CAR nacional",
            "Cooperativismo agrícola forte (Coamo, C.Vale, Cocamar)",
        ],
        "procedimento_licenciamento": "Licenciamento via IAT. LAS (Licença Ambiental Simplificada) para atividades de baixo impacto.",
        "regularizacao_fundiaria": "ITCG coordena cadastro e regularização de terras estaduais.",
    },
    "RS": {
        "estado": "Rio Grande do Sul",
        "orgao_ambiental": "FEPAM - Fundação Estadual de Proteção Ambiental",
        "orgao_fundiario": "SEAPI / DRF",
        "legislacao_principal": "Lei Estadual 15.434/2020 (Código Florestal Estadual)",
        "reserva_legal_percentual": "20% (Mata Atlântica/Pampa)",
        "bioma_predominante": "Mata Atlântica/Pampa",
        "particularidades": [
            "Bioma Pampa com regras específicas de conservação",
            "Forte produção de soja, arroz, uva e pecuária",
            "FEPAM tem licenciamento online (SOL)",
            "Outorga de água via DRHS/SEMA",
        ],
        "procedimento_licenciamento": "Licenciamento via FEPAM. LO online para atividades de baixo impacto. EIA/RIMA para alto impacto.",
        "regularizacao_fundiaria": "Programa Gaúcho de Regularização Fundiária.",
    },
    "SP": {
        "estado": "São Paulo",
        "orgao_ambiental": "CETESB / SMA",
        "orgao_fundiario": "ITESP - Fundação Instituto de Terras do Estado de São Paulo",
        "sicar_estadual": "https://datageo.ambiente.sp.gov.br/",
        "legislacao_principal": "Lei Estadual 15.684/2015 (PRA-SP)",
        "reserva_legal_percentual": "20% (Mata Atlântica/Cerrado)",
        "bioma_predominante": "Mata Atlântica/Cerrado",
        "particularidades": [
            "DataGEO: portal de dados ambientais mais acessível",
            "Maior produtor de cana-de-açúcar e laranja",
            "CETESB: licenciamento ambiental mais rigoroso do país",
            "PRA-SP: Programa de Regularização Ambiental avançado",
            "IEA: Instituto de Economia Agrícola com dados de preços de terra",
        ],
        "procedimento_licenciamento": "Licenciamento via CETESB (poluição) e SMA (recursos naturais). Processo mais rigoroso e documentado do país.",
        "regularizacao_fundiaria": "ITESP atua em assentamentos e regularização de terras devolutas estaduais.",
    },
    "TO": {
        "estado": "Tocantins",
        "orgao_ambiental": "NATURATINS - Instituto Natureza do Tocantins",
        "orgao_fundiario": "ITERTINS - Instituto de Terras do Tocantins",
        "legislacao_principal": "Lei Estadual 1.307/2002 (Política Estadual de Recursos Hídricos)",
        "reserva_legal_percentual": "35% (Cerrado na Amazônia Legal), 20% (Cerrado fora da AL)",
        "bioma_predominante": "Cerrado/Amazônia",
        "particularidades": [
            "MATOPIBA: estado inteiro é fronteira agrícola",
            "Parte do estado na Amazônia Legal (RL 35%)",
            "Forte expansão de soja e pecuária",
            "NATURATINS faz licenciamento e outorga de água",
        ],
        "procedimento_licenciamento": "Licenciamento via NATURATINS. LAR para atividades agropecuárias.",
        "regularizacao_fundiaria": "ITERTINS regulariza terras estaduais. Programa de titulação em andamento.",
    },
}

# Adicionar estados faltantes com dados mínimos
for uf in ["AP", "CE", "DF", "ES", "PB", "PE", "PI", "RJ", "RN", "RO", "RR", "SC", "SE"]:
    if uf not in JURISDICAO_POR_ESTADO:
        bioma = {
            "AP": "Amazônia", "CE": "Caatinga", "DF": "Cerrado", "ES": "Mata Atlântica",
            "PB": "Caatinga/Mata Atlântica", "PE": "Caatinga/Mata Atlântica",
            "PI": "Caatinga/Cerrado", "RJ": "Mata Atlântica", "RN": "Caatinga",
            "RO": "Amazônia", "RR": "Amazônia", "SC": "Mata Atlântica", "SE": "Mata Atlântica",
        }.get(uf, "")
        rl = "80%" if "Amazônia" in bioma and uf in ["AP", "RO", "RR"] else "20%"
        JURISDICAO_POR_ESTADO[uf] = {
            "estado": uf,
            "reserva_legal_percentual": rl,
            "bioma_predominante": bioma,
            "particularidades": [],
            "procedimento_licenciamento": "Consultar órgão ambiental estadual.",
            "regularizacao_fundiaria": "Consultar instituto de terras estadual.",
        }


def get_jurisdicao(uf: str) -> Optional[dict]:
    """Retorna informações de jurisdição para um estado."""
    return JURISDICAO_POR_ESTADO.get(uf.upper())


def get_all_jurisdicoes() -> dict:
    """Retorna jurisdição de todos os estados."""
    return JURISDICAO_POR_ESTADO


def get_reserva_legal_info(uf: str, bioma: str = None) -> dict:
    """
    Calcula o percentual de Reserva Legal obrigatória.

    Regras do Código Florestal (Lei 12.651/2012):
    - Amazônia (floresta): 80%
    - Cerrado na Amazônia Legal: 35%
    - Demais (Mata Atlântica, Caatinga, Pampa, Pantanal): 20%

    Estados da Amazônia Legal: AC, AM, AP, MA (oeste), MT (norte),
    PA, RO, RR, TO.
    """
    amazonia_legal = ["AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO"]
    uf = uf.upper()

    if bioma and "amazônia" in bioma.lower():
        return {
            "percentual": 80,
            "fundamento": "Art. 12, I, 'a' do Código Florestal (Lei 12.651/2012)",
            "detalhes": "Imóvel situado em área de florestas na Amazônia Legal",
        }

    if uf in amazonia_legal:
        if bioma and "cerrado" in bioma.lower():
            return {
                "percentual": 35,
                "fundamento": "Art. 12, I, 'b' do Código Florestal (Lei 12.651/2012)",
                "detalhes": "Imóvel situado em área de Cerrado na Amazônia Legal",
            }
        return {
            "percentual": 80,
            "fundamento": "Art. 12, I, 'a' do Código Florestal (Lei 12.651/2012)",
            "detalhes": "Imóvel na Amazônia Legal — percentual pode variar conforme bioma (80% floresta, 35% cerrado)",
        }

    return {
        "percentual": 20,
        "fundamento": "Art. 12, II do Código Florestal (Lei 12.651/2012)",
        "detalhes": "Imóvel fora da Amazônia Legal",
    }
