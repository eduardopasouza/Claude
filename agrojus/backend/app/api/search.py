"""
Rotas de busca universal.

Aceita qualquer identificador de imóvel ou pessoa e retorna dados cruzados.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from app.collectors.sicar import SICARCollector
from app.collectors.sigef import SIGEFCollector
from app.collectors.receita_federal import ReceitaFederalCollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.models.schemas import PropertySearchRequest, PersonSearchRequest, RegionSearchRequest

router = APIRouter()


@router.post("/property")
async def search_property(request: PropertySearchRequest):
    """
    Busca universal de imóvel rural.

    Aceita qualquer identificador: CAR, matrícula, SNCR, NIRF, CCIR,
    ITR, SIGEF, coordenadas, município ou nome do proprietário.
    """
    results = {"found": False, "identifiers_used": [], "data": {}}

    # Try each identifier in order of specificity
    if request.car_code:
        sicar = SICARCollector()
        car_data = await sicar.get_property_by_car(request.car_code)
        if car_data:
            results["found"] = True
            results["identifiers_used"].append("CAR")
            results["data"]["car"] = car_data

    if request.sigef_code:
        sigef = SIGEFCollector()
        sigef_data = await sigef.get_parcel_by_code(request.sigef_code)
        if sigef_data:
            results["found"] = True
            results["identifiers_used"].append("SIGEF")
            results["data"]["sigef"] = sigef_data

    if request.latitude and request.longitude:
        sigef = SIGEFCollector()
        parcels = await sigef.search_parcels_by_location(
            request.latitude, request.longitude
        )
        if parcels:
            results["found"] = True
            results["identifiers_used"].append("Coordenadas")
            results["data"]["sigef_parcels"] = parcels

    if request.cpf_cnpj:
        receita = ReceitaFederalCollector()
        validation = await receita.validate_cpf_cnpj(request.cpf_cnpj)
        results["data"]["document_validation"] = validation

        if validation["type"] == "CNPJ" and validation["valid"]:
            cnpj_data = await receita.get_cnpj(request.cpf_cnpj)
            if cnpj_data:
                results["found"] = True
                results["identifiers_used"].append("CNPJ")
                results["data"]["owner"] = cnpj_data

    if request.municipality and request.state:
        sicar = SICARCollector()
        properties = await sicar.search_by_municipality(
            request.municipality, request.state
        )
        if properties:
            results["found"] = True
            results["identifiers_used"].append("Municipio")
            results["data"]["properties_in_municipality"] = properties[:20]

    # Track identifiers that were provided but not yet queryable
    pending = []
    if request.matricula:
        pending.append({"type": "matricula", "value": request.matricula, "status": "Consulta a cartorios em desenvolvimento"})
    if request.sncr_code:
        pending.append({"type": "SNCR", "value": request.sncr_code, "status": "Consulta ao SNCR/CNIR em desenvolvimento"})
    if request.nirf:
        pending.append({"type": "NIRF", "value": request.nirf, "status": "Consulta ao CAFIR em desenvolvimento"})
    if request.ccir:
        pending.append({"type": "CCIR", "value": request.ccir, "status": "Consulta ao SNCR em desenvolvimento"})
    if request.itr_number:
        pending.append({"type": "ITR", "value": request.itr_number, "status": "Consulta a Receita Federal em desenvolvimento"})

    if pending:
        results["pending_identifiers"] = pending

    if not results["found"] and not pending:
        raise HTTPException(
            status_code=404,
            detail="Nenhum imovel encontrado. Informe ao menos um identificador valido.",
        )

    return results


@router.get("/cnpj/{cnpj}")
async def search_cnpj(cnpj: str):
    """Busca dados cadastrais de um CNPJ na Receita Federal."""
    receita = ReceitaFederalCollector()
    result = await receita.get_cnpj(cnpj)
    if result:
        return {"source": "Receita Federal (BrasilAPI)", "data": result}
    raise HTTPException(status_code=404, detail="CNPJ nao encontrado")


@router.get("/validate/{document}")
async def validate_document(document: str):
    """Valida um CPF ou CNPJ e retorna tipo."""
    receita = ReceitaFederalCollector()
    return await receita.validate_cpf_cnpj(document)


@router.get("/lista-suja/{cpf_cnpj}")
async def search_slave_labour(cpf_cnpj: str):
    """Busca um CPF/CNPJ na Lista Suja do Trabalho Escravo (MTE)."""
    collector = SlaveLabourCollector()
    results = await collector.search_by_cpf_cnpj(cpf_cnpj)
    return {
        "source": "MTE (Lista Suja)",
        "cpf_cnpj": cpf_cnpj,
        "found": len(results) > 0,
        "total": len(results),
        "records": results,
    }


@router.get("/lista-suja")
async def list_slave_labour(
    municipality: Optional[str] = None,
    state: Optional[str] = None,
    name: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    """Lista registros da Lista Suja, com filtros opcionais."""
    collector = SlaveLabourCollector()

    if name:
        results = await collector.search_by_name(name)
    elif state:
        results = await collector.search_by_municipality(municipality or "", state)
    else:
        results = await collector.get_all()

    total = len(results)
    page = results[skip:skip + limit]
    return {
        "source": "MTE (Lista Suja)",
        "total": total,
        "skip": skip,
        "limit": limit,
        "records": page,
    }
