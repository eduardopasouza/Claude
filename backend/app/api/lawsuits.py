"""
Rotas de consulta de processos judiciais via DataJud/CNJ.

Permite buscar processos por CPF/CNPJ ou por assunto em tribunais específicos.
"""

from fastapi import APIRouter
from typing import Optional

from app.collectors.datajud import DataJudCollector, TRIBUNAIS, ASSUNTOS_AGRO

router = APIRouter()


@router.get("/search/{cpf_cnpj}")
async def search_lawsuits_by_document(
    cpf_cnpj: str,
    tribunais: Optional[str] = None,
    max_results: int = 20,
):
    """
    Busca processos judiciais por CPF/CNPJ.

    Por padrão busca nos TRFs (Justiça Federal). Informe tribunais
    separados por vírgula para expandir (ex: TRF1,TRF3,TJSP).

    Fonte: DataJud/CNJ (API pública).
    """
    collector = DataJudCollector()

    tribunal_list = None
    if tribunais:
        tribunal_list = [t.strip().upper() for t in tribunais.split(",")]

    results = await collector.search_by_cpf_cnpj(
        cpf_cnpj, tribunais=tribunal_list, max_results=max_results
    )

    return {
        "source": "DataJud/CNJ",
        "cpf_cnpj": cpf_cnpj,
        "total": len(results),
        "records": results,
    }


@router.get("/subject/{subject_code}")
async def search_lawsuits_by_subject(
    subject_code: str,
    tribunal: str = "TRF1",
    municipality: Optional[str] = None,
    max_results: int = 20,
):
    """
    Busca processos judiciais por assunto (código TPU do CNJ).

    Assuntos relevantes para agro: usucapião (10432), desapropriação (10445),
    posse (10455), dano ambiental (10673), trabalho rural (11793),
    contratos agrários (14045), arrendamento (14046), parceria rural (14047).
    """
    collector = DataJudCollector()
    results = await collector.search_by_subject(
        subject_code, tribunal, municipality, max_results
    )

    subject_name = ASSUNTOS_AGRO.get(subject_code, subject_code)
    return {
        "source": "DataJud/CNJ",
        "subject": subject_name,
        "subject_code": subject_code,
        "tribunal": tribunal,
        "total": len(results),
        "records": results,
    }


@router.get("/tribunais")
async def list_tribunais():
    """Lista tribunais disponíveis no DataJud e assuntos relevantes para agro."""
    return {
        "tribunais": TRIBUNAIS,
        "assuntos_agro": ASSUNTOS_AGRO,
    }
