"""
Endpoints de jurisdição legal — regras por estado.

Cada imóvel rural está sujeito a regras diferentes dependendo do estado.
Este módulo informa ao usuário:
- Qual órgão ambiental é competente
- Qual o percentual de Reserva Legal obrigatório
- Procedimento de licenciamento específico
- Particularidades da regularização fundiária
"""

from fastapi import APIRouter
from typing import Optional

from app.services.jurisdicao import (
    get_jurisdicao,
    get_all_jurisdicoes,
    get_reserva_legal_info,
)

router = APIRouter()


@router.get("/estado/{uf}")
async def get_jurisdicao_estado(uf: str):
    """
    Retorna regras de jurisdição para um estado.

    Inclui: órgão ambiental, órgão fundiário, legislação principal,
    percentual de Reserva Legal, procedimento de licenciamento,
    regularização fundiária, particularidades.
    """
    data = get_jurisdicao(uf)
    if not data:
        return {"error": f"Estado '{uf}' não encontrado"}
    return {"uf": uf.upper(), "jurisdicao": data}


@router.get("/estados")
async def list_all_jurisdicoes():
    """Retorna jurisdição de todos os 27 estados."""
    all_data = get_all_jurisdicoes()
    return {
        "total": len(all_data),
        "estados": all_data,
    }


@router.get("/reserva-legal")
async def get_reserva_legal(uf: str, bioma: Optional[str] = None):
    """
    Calcula o percentual de Reserva Legal obrigatório.

    Regras do Código Florestal (Lei 12.651/2012):
    - Amazônia (floresta): 80%
    - Cerrado na Amazônia Legal: 35%
    - Demais biomas: 20%

    Parâmetros:
    - uf: sigla do estado
    - bioma: amazonia, cerrado, mata_atlantica, caatinga, pampa, pantanal
    """
    info = get_reserva_legal_info(uf, bioma)
    return {
        "uf": uf.upper(),
        "bioma": bioma,
        "reserva_legal": info,
    }


@router.get("/comparar")
async def comparar_jurisdicoes(uf1: str, uf2: str):
    """
    Compara regras de jurisdição entre dois estados.

    Útil para advogados que atuam em mais de um estado.
    """
    j1 = get_jurisdicao(uf1)
    j2 = get_jurisdicao(uf2)

    if not j1 or not j2:
        return {"error": "Estado não encontrado"}

    diferencas = []

    # Comparar Reserva Legal
    rl1 = j1.get("reserva_legal_percentual", "")
    rl2 = j2.get("reserva_legal_percentual", "")
    if rl1 != rl2:
        diferencas.append({
            "aspecto": "Reserva Legal",
            uf1.upper(): rl1,
            uf2.upper(): rl2,
        })

    # Comparar bioma
    b1 = j1.get("bioma_predominante", "")
    b2 = j2.get("bioma_predominante", "")
    if b1 != b2:
        diferencas.append({
            "aspecto": "Bioma predominante",
            uf1.upper(): b1,
            uf2.upper(): b2,
        })

    # Orgao ambiental
    oa1 = j1.get("orgao_ambiental", "")
    oa2 = j2.get("orgao_ambiental", "")
    diferencas.append({
        "aspecto": "Órgão ambiental",
        uf1.upper(): oa1,
        uf2.upper(): oa2,
    })

    # Licenciamento
    l1 = j1.get("procedimento_licenciamento", "")
    l2 = j2.get("procedimento_licenciamento", "")
    diferencas.append({
        "aspecto": "Licenciamento",
        uf1.upper(): l1,
        uf2.upper(): l2,
    })

    return {
        "comparacao": f"{uf1.upper()} vs {uf2.upper()}",
        "diferencas": diferencas,
        uf1.upper(): j1,
        uf2.upper(): j2,
    }
