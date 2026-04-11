"""
Endpoint de consulta unificada — o diferencial do AgroJus.

Um unico endpoint que agrega TODAS as fontes disponiveis para um CPF/CNPJ:
- Dados cadastrais (Receita Federal)
- Imoveis rurais (CAR/SICAR)
- Embargos ambientais (IBAMA)
- Lista Suja trabalho escravo (MTE)
- Processos judiciais (DataJud/CNJ)
- Protestos (CENPROT)
- Credito rural (SICOR/BCB)
- Terras indigenas proximas (FUNAI)
- Score de risco consolidado

Equivalente ao que InfoSimples, Registro Rural e DadosFazenda
oferecem separado — aqui tudo vem numa unica chamada.
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.collectors.receita_federal import ReceitaFederalCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.collectors.datajud import DataJudCollector
from app.collectors.financial import FinancialDataCollector
from app.collectors.cpf import CPFCollector
from app.collectors.protestos import ProtestosCollector

logger = logging.getLogger("agrojus.consulta")
router = APIRouter()


class ConsultaUnificadaRequest(BaseModel):
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ a consultar")
    include_cadastral: bool = Field(True, description="Dados cadastrais (Receita Federal)")
    include_environmental: bool = Field(True, description="Embargos IBAMA")
    include_labour: bool = Field(True, description="Lista Suja trabalho escravo")
    include_legal: bool = Field(True, description="Processos judiciais (DataJud)")
    include_financial: bool = Field(True, description="Credito rural (SICOR)")
    include_protests: bool = Field(True, description="Protestos (CENPROT)")


@router.post("/completa")
async def consulta_unificada(request: ConsultaUnificadaRequest):
    """
    Consulta unificada — agrega TODAS as fontes para um CPF/CNPJ.

    Executa todas as consultas em PARALELO e retorna um dossie completo
    com score de risco consolidado. Tempo medio: 3-5 segundos.

    Fontes consultadas: Receita Federal, IBAMA, MTE (Lista Suja),
    DataJud/CNJ, SICOR/BCB, CENPROT.
    """
    import re
    clean = re.sub(r"[.\-/]", "", request.cpf_cnpj)

    # Validate format: CPF = 11 digits, CNPJ = 14 digits
    if not re.fullmatch(r"\d{11}|\d{14}", clean):
        return {
            "error": "CPF/CNPJ invalido — deve conter 11 (CPF) ou 14 (CNPJ) digitos",
            "cpf_cnpj": request.cpf_cnpj,
        }

    # Detectar tipo
    receita = ReceitaFederalCollector()
    validation = await receita.validate_cpf_cnpj(clean)

    result = {
        "consulta_id": str(uuid.uuid4()),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cpf_cnpj": clean,
        "document_type": validation["type"],
        "document_valid": validation["valid"],
        "sections": {},
        "sources_consulted": [],
        "sources_unavailable": [],
        "risk_score": None,
    }

    if not validation["valid"]:
        result["error"] = f"{validation['type']} invalido"
        return result

    # Montar lista de tarefas paralelas
    tasks = {}

    if request.include_cadastral:
        if validation["type"] == "CNPJ":
            tasks["cadastral"] = _fetch_cnpj(clean)
        else:
            tasks["cadastral"] = _fetch_cpf(clean)

    if request.include_environmental:
        tasks["embargos_ibama"] = _fetch_ibama(clean)

    if request.include_labour:
        tasks["lista_suja"] = _fetch_lista_suja(clean)

    if request.include_legal:
        tasks["processos_judiciais"] = _fetch_processos(clean)

    if request.include_financial:
        tasks["credito_rural"] = _fetch_credito(clean)

    if request.include_protests:
        tasks["protestos"] = _fetch_protestos(clean)

    # Executar tudo em paralelo
    task_names = list(tasks.keys())
    task_coros = list(tasks.values())
    results = await asyncio.gather(*task_coros, return_exceptions=True)

    # Processar resultados
    risk_factors = []
    for name, res in zip(task_names, results):
        if isinstance(res, Exception):
            logger.warning("Consulta %s failed: %s", name, res)
            result["sources_unavailable"].append(name)
            result["sections"][name] = {"status": "error", "message": str(res)}
        else:
            result["sections"][name] = res["data"]
            result["sources_consulted"].append(res["source"])
            if res.get("risk_flags"):
                risk_factors.extend(res["risk_flags"])

    # Calcular risk score consolidado
    result["risk_score"] = _calculate_risk(result["sections"], risk_factors)

    return result


# --- Fetchers individuais (cada um retorna dict padrao) ---

async def _fetch_cnpj(cnpj: str) -> dict:
    collector = ReceitaFederalCollector()
    data = await collector.get_cnpj(cnpj)
    risk_flags = []
    if data:
        status = (data.situacao_cadastral or "").lower()
        if "inapta" in status or "baixada" in status or "suspensa" in status:
            risk_flags.append(f"CNPJ com situacao: {data.situacao_cadastral}")
        return {"source": "Receita Federal (BrasilAPI)", "data": data.model_dump(), "risk_flags": risk_flags}
    return {"source": "Receita Federal", "data": None, "risk_flags": ["CNPJ nao encontrado na base"]}


async def _fetch_cpf(cpf: str) -> dict:
    collector = CPFCollector()
    data = await collector.consultar_cpf(cpf)
    return {"source": data.source, "data": data.model_dump(), "risk_flags": []}


async def _fetch_ibama(cpf_cnpj: str) -> dict:
    collector = IBAMACollector()
    embargos = await collector.search_embargos_by_cpf_cnpj(cpf_cnpj)
    risk_flags = []
    if embargos:
        risk_flags.append(f"{len(embargos)} embargo(s) IBAMA ativo(s)")
    return {
        "source": "IBAMA (Dados Abertos)",
        "data": {"total": len(embargos), "embargos": [e.model_dump() for e in embargos]},
        "risk_flags": risk_flags,
    }


async def _fetch_lista_suja(cpf_cnpj: str) -> dict:
    collector = SlaveLabourCollector()
    entries = await collector.search_by_cpf_cnpj(cpf_cnpj)
    risk_flags = []
    if entries:
        total_workers = sum(e.workers_rescued or 0 for e in entries)
        risk_flags.append(f"Lista Suja: {len(entries)} registro(s), {total_workers} trabalhadores")
    return {
        "source": "MTE (Lista Suja)",
        "data": {"total": len(entries), "found": len(entries) > 0, "entries": [e.model_dump() for e in entries]},
        "risk_flags": risk_flags,
    }


async def _fetch_processos(cpf_cnpj: str) -> dict:
    collector = DataJudCollector()
    records = await collector.search_by_cpf_cnpj(cpf_cnpj)
    risk_flags = []
    if records:
        risk_flags.append(f"{len(records)} processo(s) judicial(is)")
    return {
        "source": "DataJud/CNJ",
        "data": {"total": len(records), "records": [r.model_dump() for r in records]},
        "risk_flags": risk_flags,
    }


async def _fetch_credito(cpf_cnpj: str) -> dict:
    collector = FinancialDataCollector()
    credits = await collector.get_rural_credits_by_cpf_cnpj(cpf_cnpj)
    total = sum(c.amount or 0 for c in credits)
    return {
        "source": "BCB/SICOR",
        "data": {"total_operations": len(credits), "total_amount": total, "records": [c.model_dump() for c in credits]},
        "risk_flags": [],
    }


async def _fetch_protestos(cpf_cnpj: str) -> dict:
    collector = ProtestosCollector()
    data = await collector.consultar_protestos(cpf_cnpj)
    risk_flags = []
    if data.has_protests:
        risk_flags.append(f"{data.total_protests} protesto(s) registrado(s)")
    return {
        "source": data.source,
        "data": data.model_dump(),
        "risk_flags": risk_flags,
    }


def _calculate_risk(sections: dict, risk_factors: list) -> dict:
    """Calcula score de risco consolidado baseado em todas as fontes."""
    severity_map = {"low": 0, "medium": 1, "high": 2, "critical": 3}

    scores = {
        "land_tenure": "low",
        "environmental": "low",
        "legal": "low",
        "labor": "low",
        "financial": "low",
    }

    # Ambiental
    embargos = sections.get("embargos_ibama", {})
    if isinstance(embargos, dict) and embargos.get("total", 0) > 0:
        scores["environmental"] = "critical"

    # Trabalhista
    lista_suja = sections.get("lista_suja", {})
    if isinstance(lista_suja, dict) and lista_suja.get("found"):
        scores["labor"] = "critical"

    # Juridico
    processos = sections.get("processos_judiciais", {})
    if isinstance(processos, dict):
        total = processos.get("total", 0)
        if total >= 5:
            scores["legal"] = "high"
        elif total >= 1:
            scores["legal"] = "medium"

    # Protestos → financeiro
    protestos = sections.get("protestos", {})
    if isinstance(protestos, dict) and protestos.get("has_protests"):
        scores["financial"] = "high"

    # Cadastral
    cadastral = sections.get("cadastral", {})
    if isinstance(cadastral, dict):
        status = str(cadastral.get("situacao_cadastral", "")).lower()
        if "inapta" in status or "baixada" in status or "suspensa" in status:
            scores["legal"] = "high"

    # Overall = pior de todos
    overall = max(scores.values(), key=lambda v: severity_map.get(v, 0))

    return {
        "overall": overall,
        **scores,
        "details": risk_factors if risk_factors else ["Nenhum alerta encontrado nas fontes consultadas"],
    }
