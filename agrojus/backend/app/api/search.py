"""Rotas de busca de imóveis e proprietários."""

from fastapi import APIRouter, HTTPException

from app.collectors.sicar import SICARCollector
from app.collectors.sigef import SIGEFCollector
from app.collectors.receita_federal import ReceitaFederalCollector
from app.models.schemas import PropertySearchRequest

router = APIRouter()


@router.post("/property")
async def search_property(request: PropertySearchRequest):
    """Busca um imóvel rural por código CAR, coordenadas ou município."""
    if request.car_code:
        sicar = SICARCollector()
        result = await sicar.get_property_by_car(request.car_code)
        if result:
            return {"source": "SICAR/CAR", "data": result}

    if request.latitude and request.longitude:
        sigef = SIGEFCollector()
        parcels = await sigef.search_parcels_by_location(
            request.latitude, request.longitude
        )
        if parcels:
            return {"source": "SIGEF/INCRA", "data": parcels}

    if request.municipality and request.state:
        sicar = SICARCollector()
        results = await sicar.search_by_municipality(
            request.municipality, request.state
        )
        if results:
            return {"source": "SICAR/CAR", "data": results}

    raise HTTPException(
        status_code=404,
        detail="Nenhum imovel encontrado com os parametros informados",
    )


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
    """Valida um CPF ou CNPJ."""
    receita = ReceitaFederalCollector()
    return await receita.validate_cpf_cnpj(document)
