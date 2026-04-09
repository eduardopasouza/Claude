"""
Endpoint de busca inteligente.

Recebe texto livre e detecta automaticamente o tipo de input:
CAR, CPF, CNPJ, coordenadas, município, nome, nº processo, etc.
"""

import re
from fastapi import APIRouter
from pydantic import BaseModel

from app.models.schemas import PropertySearchRequest

router = APIRouter()


class SmartSearchRequest(BaseModel):
    query: str


class SmartSearchResponse(BaseModel):
    detected_type: str
    confidence: str
    parsed: dict
    search_request: PropertySearchRequest


STATES = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS",
    "SC", "SE", "SP", "TO",
]


def detect_input_type(query: str) -> tuple[str, dict]:
    """Detecta o tipo de input e faz o parse."""
    q = query.strip()

    # CNPJ: 14 dígitos ou formato XX.XXX.XXX/XXXX-XX
    cnpj_pattern = r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$"
    if re.match(cnpj_pattern, q):
        clean = re.sub(r"[./-]", "", q)
        return "cnpj", {"cpf_cnpj": clean}

    # CPF: 11 dígitos ou formato XXX.XXX.XXX-XX
    cpf_pattern = r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"
    if re.match(cpf_pattern, q):
        clean = re.sub(r"[.-]", "", q)
        return "cpf", {"cpf_cnpj": clean}

    # Código CAR: UF-CODIBGE-HASH (ex: MT-5107925-ABC123...)
    car_pattern = r"^[A-Z]{2}-\d{7}-[A-Z0-9]"
    if re.match(car_pattern, q.upper()):
        return "car", {"car_code": q.upper()}

    # Coordenadas: lat,lon ou lat lon (decimais)
    coord_pattern = r"^(-?\d{1,3}[.,]\d+)[,;\s]+(-?\d{1,3}[.,]\d+)$"
    match = re.match(coord_pattern, q)
    if match:
        lat = float(match.group(1).replace(",", "."))
        lon = float(match.group(2).replace(",", "."))
        # Validar range Brasil
        if -35 <= lat <= 6 and -75 <= lon <= -30:
            return "coordinates", {"latitude": lat, "longitude": lon}
        # Talvez invertido
        if -35 <= lon <= 6 and -75 <= lat <= -30:
            return "coordinates", {"latitude": lon, "longitude": lat}

    # Número de processo judicial (CNJ): NNNNNNN-DD.AAAA.J.TR.OOOO
    cnj_pattern = r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$"
    if re.match(cnj_pattern, q):
        return "lawsuit", {"case_number": q}

    # Número de auto de infração IBAMA (6-7 dígitos puros)
    if re.match(r"^\d{6,7}$", q):
        return "ibama_auto", {"auto_number": q}

    # Número de processo ANM (NNN.NNN/AAAA)
    anm_pattern = r"^\d{3}\.\d{3}/\d{4}$"
    if re.match(anm_pattern, q):
        return "anm_process", {"process_number": q}

    # UUID (possível código SIGEF)
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    if re.match(uuid_pattern, q.lower()):
        return "sigef", {"sigef_code": q.lower()}

    # Município/UF: "Sorriso/MT" ou "Sorriso - MT" ou "Sorriso, MT"
    mun_pattern = r"^(.+?)[/\-,]\s*([A-Z]{2})$"
    match = re.match(mun_pattern, q.strip(), re.IGNORECASE)
    if match:
        mun = match.group(1).strip()
        uf = match.group(2).strip().upper()
        if uf in STATES:
            return "municipality", {"municipality": mun, "state": uf}

    # Matrícula: "matrícula 12345" ou "mat. 12345"
    mat_pattern = r"^(?:matr[ií]cula|mat\.?)\s*(\d+)$"
    match = re.match(mat_pattern, q, re.IGNORECASE)
    if match:
        return "matricula", {"matricula": match.group(1)}

    # NIRF: "nirf 1234567" ou "NIRF: 1234567"
    nirf_pattern = r"^nirf[:\s]*(\d+)$"
    match = re.match(nirf_pattern, q, re.IGNORECASE)
    if match:
        return "nirf", {"nirf": match.group(1)}

    # CCIR: "ccir 1234567890"
    ccir_pattern = r"^ccir[:\s]*(\d+)$"
    match = re.match(ccir_pattern, q, re.IGNORECASE)
    if match:
        return "ccir", {"ccir": match.group(1)}

    # Default: trata como nome de proprietário
    return "owner_name", {"owner_name": q}


@router.post("/smart")
async def smart_search(request: SmartSearchRequest) -> SmartSearchResponse:
    """
    Busca inteligente: detecta automaticamente o tipo de input.

    Aceita: CNPJ, CPF, código CAR, coordenadas, código SIGEF, município/UF,
    nº processo judicial (CNJ), nº auto IBAMA, nº processo ANM,
    matrícula, NIRF, CCIR, ou nome do proprietário.
    """
    detected_type, parsed = detect_input_type(request.query)

    search_request = PropertySearchRequest(**parsed)

    return SmartSearchResponse(
        detected_type=detected_type,
        confidence="high" if detected_type != "owner_name" else "low",
        parsed=parsed,
        search_request=search_request,
    )
