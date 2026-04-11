"""
Catalogo mestre de TODAS as camadas geoespaciais disponiveis.

Organiza e cataloga cada fonte publica de dados geoespaciais do Brasil,
indicando URL, formato, status e se requer autenticacao.

Este modulo serve como referencia para o frontend montar o painel de
camadas do mapa e para o backend saber onde buscar cada dado.
"""

import logging
from typing import Optional

logger = logging.getLogger("agrojus")


# Catalogo completo de camadas disponiveis
LAYER_CATALOG = {
    # === FUNDIARIO ===
    "terras_indigenas": {
        "name": "Terras Indigenas",
        "category": "fundiario",
        "source": "FUNAI",
        "wfs_url": "https://geoserver.funai.gov.br/geoserver/Funai/ows",
        "layer_name": "Funai:tis_poligonais",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "active",
        "description": "655+ Terras Indigenas demarcadas com poligonos",
        "update_frequency": "mensal",
    },
    "assentamentos": {
        "name": "Assentamentos da Reforma Agraria",
        "category": "fundiario",
        "source": "INCRA",
        "wfs_url": "https://geoserver.incra.gov.br/geoserver/wfs",
        "layer_name": "acervo:assentamentos",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "blocked_proxy",
        "description": "Projetos de assentamento do INCRA",
        "alternative_url": "https://certificacao.incra.gov.br/csv_shp/export_shp.py",
    },
    "quilombolas": {
        "name": "Territorios Quilombolas",
        "category": "fundiario",
        "source": "INCRA/Palmares",
        "wfs_url": "https://geoserver.incra.gov.br/geoserver/wfs",
        "layer_name": "acervo:quilombolas",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "blocked_proxy",
        "description": "Comunidades quilombolas tituladas e em processo",
    },
    "sigef_parcelas": {
        "name": "Parcelas Certificadas SIGEF",
        "category": "fundiario",
        "source": "INCRA/SIGEF",
        "wfs_url": "https://acervofundiario.incra.gov.br/geoserver/wfs",
        "layer_name": "acervo:sigef_parcelas_certificadas",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "offline_404",
        "description": "Parcelas com georreferenciamento certificado",
    },
    "car_imoveis": {
        "name": "Imoveis CAR",
        "category": "fundiario",
        "source": "SICAR/MMA",
        "wfs_url": "https://geoserver.car.gov.br/geoserver/sicar/wfs",
        "layer_name": "sicar:sicar_imoveis",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "offline_503",
        "description": "6M+ imoveis rurais cadastrados no CAR com poligonos",
    },
    "terras_uniao": {
        "name": "Terras da Uniao (SPU)",
        "category": "fundiario",
        "source": "SPU/ME",
        "download_url": "https://www.gov.br/economia/pt-br/assuntos/patrimonio-da-uniao/a-spu",
        "format": "Shapefile (download)",
        "auth_required": False,
        "status": "available_download",
        "description": "Imoveis da Uniao (terrenos de marinha, varzeas, etc)",
    },
    "faixa_fronteira": {
        "name": "Faixa de Fronteira (150km)",
        "category": "fundiario",
        "source": "IBGE",
        "format": "Shapefile (download)",
        "auth_required": False,
        "status": "available_download",
        "description": "Faixa de 150km ao longo das fronteiras terrestres",
    },

    # === AMBIENTAL ===
    "desmatamento_deter": {
        "name": "Alertas DETER (Desmatamento)",
        "category": "ambiental",
        "source": "INPE/TerraBrasilis",
        "wfs_url": "https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/wfs",
        "layer_name": "deter-amz:deter_amz",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "active",
        "description": "Alertas de desmatamento em tempo real (Amazonia e Cerrado)",
    },
    "unidades_conservacao": {
        "name": "Unidades de Conservacao",
        "category": "ambiental",
        "source": "ICMBio/MMA",
        "wfs_url": "https://geoserver.icmbio.gov.br/geoserver/wfs",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "blocked_proxy",
        "description": "UCs federais e estaduais (parques, APAs, reservas)",
        "alternative_url": "https://dados.gov.br/dados/conjuntos-dados/unidades-de-conservacao",
    },
    "biomas": {
        "name": "Biomas Brasileiros",
        "category": "ambiental",
        "source": "INPE/TerraBrasilis",
        "wfs_url": "https://terrabrasilis.dpi.inpe.br/geoserver/prodes-brasil-nb/wfs",
        "layer_name": "prodes-brasil-nb:biomas_brasil",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "active",
        "description": "Limites dos 6 biomas brasileiros",
    },
    "embargos_ibama": {
        "name": "Areas Embargadas IBAMA",
        "category": "ambiental",
        "source": "IBAMA",
        "download_url": "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/",
        "format": "CSV (download)",
        "auth_required": False,
        "status": "active",
        "description": "Areas embargadas por infracoes ambientais",
    },

    # === ADMINISTRATIVO ===
    "municipios": {
        "name": "Limites Municipais",
        "category": "administrativo",
        "source": "IBGE",
        "api_url": "https://servicodados.ibge.gov.br/api/v3/malhas",
        "format": "API REST/GeoJSON",
        "auth_required": False,
        "status": "active",
        "description": "Contornos de todos os 5.570 municipios",
    },
    "estados": {
        "name": "Limites Estaduais",
        "category": "administrativo",
        "source": "IBGE",
        "api_url": "https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR",
        "format": "API REST/GeoJSON",
        "auth_required": False,
        "status": "active",
        "description": "Contornos dos 27 estados + DF",
    },

    # === INFRAESTRUTURA ===
    "rodovias": {
        "name": "Rodovias Federais",
        "category": "infraestrutura",
        "source": "DNIT",
        "wfs_url": "https://servicos.dnit.gov.br/geoserver/wfs",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "timeout",
        "alternative_url": "https://dados.gov.br/dados/conjuntos-dados/snv-rodovias",
        "description": "Malha rodoviaria federal (BRs)",
    },
    "ferrovias": {
        "name": "Ferrovias",
        "category": "infraestrutura",
        "source": "DNIT/ANTT",
        "download_url": "https://dados.gov.br/dados/conjuntos-dados/malha-ferroviaria",
        "format": "Shapefile (download)",
        "auth_required": False,
        "status": "available_download",
        "description": "Malha ferroviaria brasileira",
    },
    "mineracao": {
        "name": "Areas de Mineracao (SIGMINE)",
        "category": "infraestrutura",
        "source": "ANM",
        "api_url": "https://geo.anm.gov.br/arcgis/rest/services",
        "format": "ArcGIS REST",
        "auth_required": False,
        "status": "active",
        "description": "Processos minerarios, areas de concessao",
    },

    # === HIDROGRAFIA ===
    "hidrografia": {
        "name": "Hidrografia (rios, lagos)",
        "category": "hidrografia",
        "source": "ANA",
        "wfs_url": "https://metadados.snirh.gov.br/geoserver/wfs",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "blocked_proxy",
        "alternative_url": "https://dados.gov.br/dados/conjuntos-dados/base-hidrografica-ottocodificada-da-ana",
        "description": "Rede hidrografica Otto-codificada",
    },

    # === SOLO ===
    "solos": {
        "name": "Mapa de Solos do Brasil",
        "category": "solo",
        "source": "EMBRAPA",
        "wfs_url": "https://geoinfo.cnps.embrapa.br/geoserver/wfs",
        "format": "WFS/GeoJSON",
        "auth_required": False,
        "status": "blocked_proxy",
        "alternative_url": "https://www.embrapa.br/solos/sibcs/mapa-de-solos",
        "description": "Tipos de solo, aptidao agricola",
    },
    "aptidao_agricola": {
        "name": "Aptidao Agricola das Terras",
        "category": "solo",
        "source": "EMBRAPA/IBGE",
        "download_url": "https://geoftp.ibge.gov.br/informacoes_ambientais/pedologia/",
        "format": "Shapefile (download)",
        "auth_required": False,
        "status": "available_download",
        "description": "Zoneamento de aptidao agricola (classes 1-6)",
    },
    "zee_estados": {
        "name": "Zoneamento Ecologico-Economico (ZEE)",
        "category": "solo",
        "source": "Governos estaduais",
        "format": "Shapefile/WFS (por estado)",
        "auth_required": False,
        "status": "available_download",
        "description": "ZEE define zonas de uso e restricao por estado. Disponiveis: DF, PA, BA, PR, AC, MT, MA, RO",
        "urls_por_estado": {
            "DF": "https://zee.df.gov.br/mapas/",
            "PA": "https://www.semas.pa.gov.br/diretorias/digeo/zee/",
            "BA": "https://zee.ba.gov.br/",
            "PR": "https://www.iat.pr.gov.br/Pagina/Zoneamento-Ecologico-Economico-ZEE",
            "AC": "http://www.zee.ac.gov.br/",
        },
    },

    # === CLIMA ===
    "estacoes_meteorologicas": {
        "name": "Estacoes Meteorologicas",
        "category": "clima",
        "source": "INMET",
        "api_url": "https://apitempo.inmet.gov.br",
        "format": "API REST/JSON",
        "auth_required": False,
        "status": "intermittent_503",
        "description": "~600 estacoes automaticas com dados de temperatura, chuva, umidade",
    },
    "clima_nasa_power": {
        "name": "Dados Climaticos NASA POWER",
        "category": "clima",
        "source": "NASA",
        "api_url": "https://power.larc.nasa.gov/api/temporal",
        "format": "API REST/JSON",
        "auth_required": False,
        "status": "active",
        "description": "Temperatura, precipitacao, radiacao solar, umidade, vento — qualquer coordenada do planeta",
    },

    # === FINANCEIRO ===
    "indicadores_bcb": {
        "name": "Indicadores Economicos (BCB)",
        "category": "financeiro",
        "source": "Banco Central do Brasil",
        "api_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs",
        "format": "API REST/JSON",
        "auth_required": False,
        "status": "active",
        "description": "SELIC, dolar, IPCA, IGP-M, CDI, TR — dados em tempo real",
    },
    "credito_rural_sicor": {
        "name": "Credito Rural SICOR",
        "category": "financeiro",
        "source": "Banco Central do Brasil",
        "api_url": "https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata",
        "format": "OData/JSON",
        "auth_required": False,
        "status": "active",
        "description": "Operacoes de credito rural por municipio, cultura, modalidade",
    },
    "producao_agricola_pam": {
        "name": "Producao Agricola Municipal (PAM)",
        "category": "financeiro",
        "source": "IBGE/SIDRA",
        "api_url": "https://apisidra.ibge.gov.br/values",
        "format": "API REST/JSON",
        "auth_required": False,
        "status": "active",
        "description": "Area plantada, area colhida, quantidade produzida, valor — por municipio e cultura",
    },

    # === MINERACAO ===
    "mineracao_anm": {
        "name": "Processos Minerarios (SIGMINE)",
        "category": "mineracao",
        "source": "ANM",
        "api_url": "https://geo.anm.gov.br/arcgis/rest/services",
        "format": "ArcGIS REST/JSON",
        "auth_required": False,
        "status": "active",
        "description": "Areas de pesquisa, lavra, concessao mineral — poligonos e status",
    },

    # === ENERGIA ===
    "energia_aneel": {
        "name": "Infraestrutura Energetica",
        "category": "energia",
        "source": "ANEEL",
        "api_url": "https://dadosabertos.aneel.gov.br/api",
        "format": "API REST/JSON",
        "auth_required": False,
        "status": "active",
        "description": "Usinas, linhas de transmissao, subestacoes, areas de distribuicao",
    },
}


def get_active_layers() -> list[dict]:
    """Retorna apenas camadas com status 'active'."""
    return [
        {"id": k, **{kk: vv for kk, vv in v.items() if kk != "wfs_url"}}
        for k, v in LAYER_CATALOG.items()
        if v.get("status") == "active"
    ]


def get_all_layers() -> list[dict]:
    """Retorna todas as camadas catalogadas."""
    return [{"id": k, **v} for k, v in LAYER_CATALOG.items()]


def get_layers_by_category(category: str) -> list[dict]:
    """Retorna camadas filtradas por categoria."""
    return [
        {"id": k, **v}
        for k, v in LAYER_CATALOG.items()
        if v.get("category") == category
    ]
