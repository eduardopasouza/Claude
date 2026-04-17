"""
Endpoints REST expondo as 9 APIs Embrapa AgroAPI ao frontend AgroJus.

Todos prefix: /api/v1/embrapa/*
Auth: usa credenciais Consumer Key/Secret no .env

Paths corrigidos na sessão 7 (validados via Swagger + curl real):
  /agritec/v2       → culturas, municípios, zoneamento (ZARC), cultivares
  /agrofit/v1       → agrotóxicos MAPA (búsca por cultura/praga, titulares, detalhes)
  /bioinsumos/v2    → inoculantes, biológicos, pragas, plantas daninhas
  /agrotermos/v1    → glossário técnico (termo, parcial, com relações)
  /bovtrace/v1      → raças, protocolos, trânsitos GTA
  /respondeagro/v1  → Q&A busca na base Embrapa
  /smartsolos/expert/v1 → classificação SiBCS
  /plantannot/v2    → bioinfo (stub minimal)
  /sting/v1         → PDB proteico (stub minimal)

Eduardo (advogado) usa majoritariamente:
  - Agritec ZARC para opinar sobre sinistros climáticos
  - Agrofit para compliance de defensivos (perícia ambiental/tributária)
  - Bioinsumos para auditoria de rotulagem de insumos
  - BovTrace para cadeia bovina (compliance EUDR)
  - AgroTermos para uso em peças jurídicas
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.collectors.embrapa import EmbrapaCollector, EmbrapaAuth

router = APIRouter()


# ---------------------------------------------------------------------------
# Healthcheck / status
# ---------------------------------------------------------------------------
@router.get("/status")
async def embrapa_status():
    """Testa se as credenciais Embrapa estão válidas (tenta obter token)."""
    auth = EmbrapaAuth()
    token = await auth.get_token()
    if not token:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível obter token Embrapa. Verifique EMBRAPA_CONSUMER_KEY/SECRET no .env.",
        )
    return {
        "status": "authenticated",
        "token_preview": token[:8] + "…" + token[-4:],
        "gateway": "https://api.cnptia.embrapa.br",
        "apis_disponiveis": {
            "agritec": "/agritec/v2 (ZARC, cultivares, municípios)",
            "agrofit": "/agrofit/v1 (agrotóxicos MAPA)",
            "bioinsumos": "/bioinsumos/v2 (inoculantes/biológicos/pragas)",
            "agrotermos": "/agrotermos/v1 (glossário)",
            "bovtrace": "/bovtrace/v1 (rastreabilidade bovina)",
            "respondeagro": "/respondeagro/v1 (Q&A)",
            "smartsolos": "/smartsolos/expert/v1 (SiBCS)",
            "plantannot": "/plantannot/v2 (bioinformática)",
            "sting": "/sting/v1 (PDB)",
        },
    }


# ---------------------------------------------------------------------------
# Agritec v2
# ---------------------------------------------------------------------------
@router.get("/agritec/culturas")
async def agritec_culturas():
    """Lista 188 culturas catalogadas no Agritec."""
    c = EmbrapaCollector()
    return await c.agritec_culturas()


@router.get("/agritec/cultura/{id_cultura}")
async def agritec_cultura(id_cultura: int):
    """Detalhe de cultura por id."""
    c = EmbrapaCollector()
    return await c.agritec_cultura(id_cultura)


@router.get("/agritec/municipios")
async def agritec_municipios(uf: Optional[str] = Query(None, description="UF (ex: MA)")):
    """Municípios atendidos pelo Agritec (opcional filtrar por UF)."""
    c = EmbrapaCollector()
    return await c.agritec_municipios(uf)


@router.get("/agritec/municipio/{codigo_ibge}")
async def agritec_municipio(codigo_ibge: int):
    """Detalhe de município + regiões de zoneamento."""
    c = EmbrapaCollector()
    return await c.agritec_municipio(codigo_ibge)


@router.get("/agritec/municipio/{codigo_ibge}/culturas")
async def agritec_municipio_culturas(codigo_ibge: int):
    """Culturas disponíveis (com ZARC) para o município."""
    c = EmbrapaCollector()
    return await c.agritec_culturas_municipio(codigo_ibge)


@router.get("/agritec/zoneamento")
async def agritec_zoneamento(
    id_cultura: int = Query(..., description="Id da cultura (ver /agritec/culturas)"),
    codigo_ibge: int = Query(..., description="Código IBGE do município (7 dígitos)"),
    risco: str = Query("20", description="20, 30, 40 ou 'todos' (percentual de risco climático)"),
):
    """Janelas de plantio ZARC — usado em perícia de sinistro climático."""
    c = EmbrapaCollector()
    return await c.agritec_zoneamento(id_cultura, codigo_ibge, risco)


@router.get("/agritec/cultivares")
async def agritec_cultivares(
    safra: str = Query(..., description="Safra ex: 2024/2025"),
    id_cultura: int = Query(...),
    uf: str = Query(...),
    regiao: Optional[str] = None,
):
    """Cultivares recomendadas para a safra/cultura/UF."""
    c = EmbrapaCollector()
    return await c.agritec_cultivares(safra, id_cultura, uf, regiao)


# ---------------------------------------------------------------------------
# AGROFIT v1
# ---------------------------------------------------------------------------
@router.get("/agrofit/culturas")
async def agrofit_culturas():
    """Culturas registradas no AGROFIT."""
    c = EmbrapaCollector()
    return await c.agrofit_culturas()


@router.get("/agrofit/produtos")
async def agrofit_busca_produtos(
    cultura: Optional[str] = Query(None),
    praga: Optional[str] = Query(None),
    titular: Optional[str] = Query(None),
):
    """Agrotóxicos formulados por cultura+praga (MAPA)."""
    c = EmbrapaCollector()
    return await c.agrofit_busca_produtos_formulados(cultura, praga, titular)


@router.get("/agrofit/produto/{numero_registro}")
async def agrofit_produto_tecnico(numero_registro: str):
    """Detalhe técnico de produto pelo nº registro MAPA."""
    c = EmbrapaCollector()
    return await c.agrofit_produto_tecnico(numero_registro)


@router.get("/agrofit/titulares")
async def agrofit_titulares():
    """Titulares de registro (fabricantes)."""
    c = EmbrapaCollector()
    return await c.agrofit_titulares()


@router.get("/agrofit/pragas")
async def agrofit_pragas():
    """Pragas catalogadas (nomes comuns)."""
    c = EmbrapaCollector()
    return await c.agrofit_pragas_nomes_comuns()


# ---------------------------------------------------------------------------
# Bioinsumos v2
# ---------------------------------------------------------------------------
@router.get("/bioinsumos/inoculantes")
async def bioinsumos_inoculantes(cultura: Optional[str] = None):
    """Inoculantes registrados para cultura."""
    c = EmbrapaCollector()
    return await c.bioinsumos_busca_inoculantes(cultura)


@router.get("/bioinsumos/biologicos")
async def bioinsumos_biologicos(
    cultura: Optional[str] = None, praga: Optional[str] = None
):
    """Produtos biológicos para controle de pragas."""
    c = EmbrapaCollector()
    return await c.bioinsumos_busca_produtos_biologicos(cultura, praga)


@router.get("/bioinsumos/pragas")
async def bioinsumos_pragas_list():
    """Pragas catalogadas (com link AGROFIT)."""
    c = EmbrapaCollector()
    return await c.bioinsumos_pragas()


@router.get("/bioinsumos/plantas-daninhas")
async def bioinsumos_plantas_daninhas():
    """Plantas daninhas catalogadas."""
    c = EmbrapaCollector()
    return await c.bioinsumos_plantas_daninhas()


# ---------------------------------------------------------------------------
# AgroTermos v1
# ---------------------------------------------------------------------------
@router.get("/agrotermos/termo")
async def agrotermos_termo(descricao: str = Query(..., min_length=2)):
    """Glossário — busca exata por termo."""
    c = EmbrapaCollector()
    return await c.agrotermos_termo(descricao)


@router.get("/agrotermos/parcial")
async def agrotermos_parcial(descricao: str = Query(..., min_length=2)):
    """Glossário — busca parcial (autocomplete)."""
    c = EmbrapaCollector()
    return await c.agrotermos_termo_parcial(descricao)


@router.get("/agrotermos/relacoes")
async def agrotermos_relacoes():
    """Tipos de relações no vocabulário Agrovoc."""
    c = EmbrapaCollector()
    return await c.agrotermos_relacoes()


# ---------------------------------------------------------------------------
# BovTrace v1
# ---------------------------------------------------------------------------
@router.get("/bovtrace/racas")
async def bovtrace_racas():
    """Lista de raças bovinas reconhecidas."""
    c = EmbrapaCollector()
    return await c.bovtrace_racas()


@router.get("/bovtrace/protocolos")
async def bovtrace_protocolos():
    """Protocolos de rastreabilidade (SISBOV, Angus GO, etc)."""
    c = EmbrapaCollector()
    return await c.bovtrace_protocolos()


@router.get("/bovtrace/transito/{codigo}")
async def bovtrace_transito(codigo: str):
    """Detalhe de trânsito (GTA) por código."""
    c = EmbrapaCollector()
    return await c.bovtrace_transito(codigo)


# ---------------------------------------------------------------------------
# RespondeAgro v1
# ---------------------------------------------------------------------------
@router.get("/respondeagro/buscar")
async def respondeagro_buscar(
    q: str = Query(..., min_length=3),
    tamanho: int = Query(10, ge=1, le=50),
):
    """Q&A base Embrapa — busca semântica por palavras-chave."""
    c = EmbrapaCollector()
    return await c.respondeagro_buscar(q, template="query_all", tamanho=tamanho)


@router.get("/respondeagro/doc/{doc_id}")
async def respondeagro_doc(doc_id: str):
    """Par pergunta+resposta específico."""
    c = EmbrapaCollector()
    return await c.respondeagro_documento(doc_id)


# ---------------------------------------------------------------------------
# SmartSolosExpert v1
# ---------------------------------------------------------------------------
@router.get("/smartsolos/health")
async def smartsolos_health():
    """Healthcheck do SmartSolos."""
    c = EmbrapaCollector()
    return await c.smartsolos_health()


@router.post("/smartsolos/classify")
async def smartsolos_classify(profiles: list[dict]):
    """
    Classifica perfis de solo segundo SiBCS.

    Body: lista de objetos {ID_PONTO, DRENAGEM, HORIZONTES: [...]}
    """
    c = EmbrapaCollector()
    return await c.smartsolos_classify(profiles)


@router.post("/smartsolos/verify")
async def smartsolos_verify(profiles: list[dict]):
    """Verifica se os perfis são válidos (schema SiBCS)."""
    c = EmbrapaCollector()
    return await c.smartsolos_verify(profiles)
