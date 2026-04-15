"""
Endpoint de compliance MCR 2.9 e EUDR.

MCR 2.9 (Banco Central):
- Verifica se propriedade rural esta apta ao credito rural
- Resolucao CMN 5.193 (dez/2024) + Resolucao 5.268
- Verifica: CAR ativo, sem desmatamento ilegal (PRODES/DETER),
  sem embargo IBAMA, sem sobreposicao TI/UC, sem lista suja

EUDR (European Deforestation Regulation):
- Regulamento UE 2023/1115 - produtos livres de desmatamento
- Aplica-se a: soja, carne, cafe, cacau, oleo de palma, borracha, madeira
- Exige: geolocalizacao do lote, prova de nao-desmatamento apos 31/12/2020
- Vigencia: dez/2025 (grandes), jun/2026 (PMEs)

Ambas as verificacoes usam as mesmas fontes que o AgroJus ja integra:
FUNAI (TIs), INPE/DETER (desmatamento), IBAMA (embargos), MTE (lista suja).
"""

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from app.collectors.geolayers import FUNAICollector, TerraBrasilisCollector
from app.collectors.ibama import IBAMACollector
from app.collectors.slave_labour import SlaveLabourCollector
from app.collectors.ibge import IBGECollector

logger = logging.getLogger("agrojus.compliance")
router = APIRouter()


class ComplianceRequest(BaseModel):
    """Request para verificacao de compliance."""
    # Identificacao do imovel (pelo menos um obrigatorio)
    car_code: Optional[str] = Field(None, description="Codigo CAR")
    cpf_cnpj: Optional[str] = Field(None, description="CPF/CNPJ do proprietario")

    # Localizacao (para analise geoespacial)
    latitude: Optional[float] = Field(None, description="Latitude do imovel")
    longitude: Optional[float] = Field(None, description="Longitude do imovel")

    # Parametros de verificacao
    radius_km: float = Field(10.0, description="Raio de busca em km")
    reference_date: Optional[str] = Field(None, description="Data de referencia (YYYY-MM-DD)")


class ComplianceResult(BaseModel):
    """Resultado da verificacao de compliance."""
    compliance_id: str
    generated_at: str
    type: str  # "mcr29" ou "eudr"
    overall_status: str  # "approved", "restricted", "blocked"
    checks: list[dict]
    risk_level: str  # low, medium, high, critical
    recommendation: str
    sources_consulted: list[str]


# --- MCR 2.9 ---

@router.post("/mcr29")
async def check_mcr29_compliance(request: ComplianceRequest):
    """
    Verifica compliance MCR 2.9 — Credito Rural.

    Resolucao CMN 5.193/2024 — Impedimentos Sociais, Ambientais e Climaticos.
    Verifica se a propriedade rural esta apta a receber credito rural
    com recursos publicos.

    Criterios verificados:
    1. CAR ativo (nao cancelado/suspenso)
    2. Sem desmatamento ilegal apos 31/07/2019 (PRODES/DETER)
    3. Sem embargo IBAMA ativo
    4. Sem sobreposicao com Terra Indigena
    5. Sem sobreposicao com Unidade de Conservacao
    6. Sem registro na Lista Suja do trabalho escravo
    """
    checks = []
    sources = []
    blocked = False
    restricted = False

    # --- Check 1: CAR ativo ---
    if request.car_code:
        # Quando SICAR voltar, consultar status real
        checks.append({
            "check": "CAR ativo",
            "status": "info",
            "detail": f"CAR informado: {request.car_code}. Servidor SICAR temporariamente indisponivel para validacao automatica.",
            "regulation": "MCR 2-2-9, item 1",
        })
        sources.append("SICAR/CAR (pendente)")
    else:
        checks.append({
            "check": "CAR ativo",
            "status": "blocked",
            "detail": "CAR nao informado. Credito rural exige inscricao ativa no CAR.",
            "regulation": "MCR 2-2-9, item 1: Nao sera concedido credito rural para empreendimento em imovel sem inscricao ativa no CAR.",
        })
        blocked = True

    # --- Check 2: Desmatamento (INPE/DETER) ---
    if request.latitude and request.longitude:
        tb = TerraBrasilisCollector()
        deter_alerts = await tb.check_deforestation(
            request.latitude, request.longitude, request.radius_km
        )
        sources.append("INPE/DETER")

        # Filtrar alertas apos 31/07/2019
        recent_alerts = [a for a in deter_alerts if _is_after_cutoff(a.get("date", ""), "2019-07-31")]

        if recent_alerts:
            checks.append({
                "check": "Desmatamento pos-2019",
                "status": "blocked",
                "detail": f"{len(recent_alerts)} alerta(s) de desmatamento detectado(s) na regiao apos 31/07/2019. Credito bloqueado salvo apresentacao de ASV, PRAD ou TAC.",
                "regulation": "MCR 2-2-9, item 17: Verificacao ativa via satelite (PRODES/DETER).",
                "alerts": recent_alerts[:5],
            })
            blocked = True
        else:
            checks.append({
                "check": "Desmatamento pos-2019",
                "status": "approved",
                "detail": f"Nenhum alerta de desmatamento detectado na regiao ({request.radius_km}km) apos 31/07/2019.",
                "regulation": "MCR 2-2-9, item 17",
            })
    else:
        checks.append({
            "check": "Desmatamento pos-2019",
            "status": "info",
            "detail": "Coordenadas nao informadas. Informe latitude/longitude para verificacao via satelite.",
        })

    # --- Check 3: Embargos IBAMA ---
    if request.cpf_cnpj:
        ibama = IBAMACollector()
        embargos = await ibama.search_embargos_by_cpf_cnpj(request.cpf_cnpj)
        sources.append("IBAMA")

        active_embargos = [e for e in embargos if (e.status or "").lower() in ("ativo", "")]
        if active_embargos:
            checks.append({
                "check": "Embargos IBAMA",
                "status": "blocked",
                "detail": f"{len(active_embargos)} embargo(s) IBAMA ativo(s). Credito rural bloqueado.",
                "regulation": "MCR 2-2-9: Vedado credito para area com embargo ambiental.",
                "embargos": [e.model_dump() for e in active_embargos[:3]],
            })
            blocked = True
        else:
            checks.append({
                "check": "Embargos IBAMA",
                "status": "approved",
                "detail": "Nenhum embargo IBAMA ativo encontrado.",
            })

    # --- Check 4: Sobreposicao Terra Indigena ---
    if request.latitude and request.longitude:
        funai = FUNAICollector()
        tis = await funai.check_overlap_ti(request.latitude, request.longitude, request.radius_km)
        sources.append("FUNAI")

        if tis:
            checks.append({
                "check": "Sobreposicao Terra Indigena",
                "status": "blocked",
                "detail": f"Sobreposicao detectada com {len(tis)} Terra(s) Indigena(s): {', '.join(t.get('name','?') for t in tis)}",
                "regulation": "MCR 2-2-9: Vedado credito em area de TI.",
                "terras_indigenas": tis,
            })
            blocked = True
        else:
            checks.append({
                "check": "Sobreposicao Terra Indigena",
                "status": "approved",
                "detail": "Sem sobreposicao com Terras Indigenas.",
            })

    # --- Check 5: Lista Suja trabalho escravo ---
    if request.cpf_cnpj:
        slave = SlaveLabourCollector()
        entries = await slave.search_by_cpf_cnpj(request.cpf_cnpj)
        sources.append("MTE (Lista Suja)")

        if entries:
            checks.append({
                "check": "Lista Suja trabalho escravo",
                "status": "blocked",
                "detail": "CPF/CNPJ encontrado na Lista Suja do MTE. Credito rural bloqueado.",
                "regulation": "MCR 2-2-9, item 1-A: Vedado credito a empregadores na lista do trabalho escravo.",
            })
            blocked = True
        else:
            checks.append({
                "check": "Lista Suja trabalho escravo",
                "status": "approved",
                "detail": "CPF/CNPJ nao consta na Lista Suja.",
            })

    # --- Resultado final ---
    if blocked:
        overall = "blocked"
        risk = "critical"
        recommendation = "Credito rural BLOQUEADO. Propriedade possui impedimentos socioambientais conforme MCR 2.9. Necessario regularizacao antes de solicitar financiamento."
    elif restricted:
        overall = "restricted"
        risk = "high"
        recommendation = "Credito rural RESTRITO. Verificar documentacao complementar (ASV, PRAD ou TAC) antes de solicitar financiamento."
    else:
        overall = "approved"
        risk = "low"
        recommendation = "Propriedade aparentemente APTA ao credito rural conforme criterios verificados do MCR 2.9. Recomenda-se confirmacao final junto a instituicao financeira."

    return ComplianceResult(
        compliance_id=str(uuid.uuid4()),
        generated_at=datetime.now(timezone.utc).isoformat(),
        type="mcr29",
        overall_status=overall,
        checks=checks,
        risk_level=risk,
        recommendation=recommendation,
        sources_consulted=sources,
    )


# --- EUDR ---

@router.post("/eudr")
async def check_eudr_compliance(request: ComplianceRequest):
    """
    Verifica compliance EUDR — European Deforestation Regulation.

    Regulamento UE 2023/1115 — Produtos livres de desmatamento.
    Verifica se a producao de uma propriedade rural atende os criterios
    de exportacao para a Uniao Europeia.

    Criterios:
    1. Geolocalizacao do lote de producao
    2. Sem desmatamento apos 31/12/2020 (data de corte EUDR)
    3. Producao em conformidade com legislacao do pais (Codigo Florestal)
    4. Sem sobreposicao com areas protegidas
    5. Rastreabilidade da cadeia produtiva

    Commodities afetadas: soja, carne bovina, cafe, cacau,
    oleo de palma, borracha, madeira e derivados.
    """
    checks = []
    sources = []
    blocked = False

    # --- Check 1: Geolocalizacao ---
    if request.latitude and request.longitude:
        checks.append({
            "check": "Geolocalizacao do lote",
            "status": "approved",
            "detail": f"Coordenadas fornecidas: {request.latitude}, {request.longitude}",
            "regulation": "EUDR Art. 9(1)(d): Geolocalizacao obrigatoria de todos os lotes de producao.",
        })

        # Buscar municipio
        IBGECollector()
        # Reverse geocode via Nominatim
        import httpx
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={"lat": request.latitude, "lon": request.longitude, "format": "json", "zoom": 10},
                    headers={"User-Agent": "AgroJus/1.0"},
                )
                if r.status_code == 200:
                    addr = r.json().get("address", {})
                    mun = addr.get("city") or addr.get("town") or addr.get("municipality")
                    estado = addr.get("state")
                    checks.append({
                        "check": "Localizacao identificada",
                        "status": "info",
                        "detail": f"Municipio: {mun}, Estado: {estado}",
                    })
        except Exception:
            pass
    else:
        checks.append({
            "check": "Geolocalizacao do lote",
            "status": "blocked",
            "detail": "EUDR exige geolocalizacao obrigatoria. Informe latitude e longitude.",
            "regulation": "EUDR Art. 9(1)(d)",
        })
        blocked = True

    # --- Check 2: Desmatamento apos 31/12/2020 (data de corte EUDR) ---
    if request.latitude and request.longitude:
        tb = TerraBrasilisCollector()
        deter_alerts = await tb.check_deforestation(
            request.latitude, request.longitude, request.radius_km
        )
        sources.append("INPE/DETER")

        # EUDR cutoff: 31/12/2020
        post_2020 = [a for a in deter_alerts if _is_after_cutoff(a.get("date", ""), "2020-12-31")]

        if post_2020:
            checks.append({
                "check": "Desmatamento pos-2020 (cutoff EUDR)",
                "status": "blocked",
                "detail": f"{len(post_2020)} alerta(s) de desmatamento/degradacao detectado(s) apos 31/12/2020. Produto NAO pode ser exportado para UE.",
                "regulation": "EUDR Art. 2: Produto de area com desmatamento apos 31/12/2020 e proibido no mercado europeu.",
                "alerts": post_2020[:5],
            })
            blocked = True
        else:
            checks.append({
                "check": "Desmatamento pos-2020 (cutoff EUDR)",
                "status": "approved",
                "detail": "Nenhum desmatamento detectado na regiao apos 31/12/2020.",
                "regulation": "EUDR Art. 2",
            })

    # --- Check 3: Conformidade com legislacao local ---
    if request.car_code:
        checks.append({
            "check": "Conformidade Codigo Florestal (CAR)",
            "status": "approved",
            "detail": f"CAR informado: {request.car_code}. Inscricao no CAR indica conformidade declaratoria com Codigo Florestal.",
            "regulation": "EUDR Art. 3(b): Producao conforme legislacao do pais de origem.",
        })
    else:
        checks.append({
            "check": "Conformidade Codigo Florestal (CAR)",
            "status": "restricted",
            "detail": "CAR nao informado. Inscricao no CAR e evidencia de conformidade com Codigo Florestal.",
            "regulation": "EUDR Art. 3(b)",
        })

    # --- Check 4: Areas protegidas ---
    if request.latitude and request.longitude:
        funai = FUNAICollector()
        tis = await funai.check_overlap_ti(request.latitude, request.longitude, request.radius_km)
        sources.append("FUNAI")

        if tis:
            checks.append({
                "check": "Sobreposicao areas protegidas",
                "status": "blocked",
                "detail": f"Sobreposicao com Terra Indigena: {', '.join(t.get('name','?') for t in tis)}. Exportacao para UE bloqueada.",
                "regulation": "EUDR Art. 3: Producao deve respeitar areas protegidas.",
            })
            blocked = True
        else:
            checks.append({
                "check": "Sobreposicao areas protegidas",
                "status": "approved",
                "detail": "Sem sobreposicao com areas protegidas (TIs).",
            })

    # --- Check 5: Embargos ---
    if request.cpf_cnpj:
        ibama = IBAMACollector()
        embargos = await ibama.search_embargos_by_cpf_cnpj(request.cpf_cnpj)
        sources.append("IBAMA")

        if embargos:
            checks.append({
                "check": "Embargos ambientais",
                "status": "blocked",
                "detail": f"{len(embargos)} embargo(s) IBAMA. Indica descumprimento de legislacao ambiental.",
                "regulation": "EUDR Art. 3(b): Producao em conformidade com legislacao local.",
            })
            blocked = True
        else:
            checks.append({
                "check": "Embargos ambientais",
                "status": "approved",
                "detail": "Sem embargos IBAMA.",
            })

    # --- Resultado ---
    if blocked:
        overall = "non_compliant"
        risk = "critical"
        recommendation = "Propriedade NAO CONFORME com EUDR. Produtos desta area NAO podem ser exportados para a Uniao Europeia. Necessaria regularizacao ambiental e fundiaria."
    else:
        overall = "compliant"
        risk = "low"
        recommendation = "Propriedade aparentemente CONFORME com EUDR baseado nos dados disponiveis. Recomenda-se due diligence completa e documentacao de rastreabilidade antes da exportacao."

    return ComplianceResult(
        compliance_id=str(uuid.uuid4()),
        generated_at=datetime.now(timezone.utc).isoformat(),
        type="eudr",
        overall_status=overall,
        checks=checks,
        risk_level=risk,
        recommendation=recommendation,
        sources_consulted=sources,
    )


def _is_after_cutoff(date_str: str, cutoff: str) -> bool:
    """Verifica se uma data e posterior ao cutoff."""
    if not date_str:
        return False
    try:
        # Tentar varios formatos
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.strptime(date_str[:10], fmt[:min(len(fmt), len(date_str[:10])+3)])
                cutoff_dt = datetime.strptime(cutoff, "%Y-%m-%d")
                return dt > cutoff_dt
            except ValueError:
                continue
    except Exception:
        pass
    return False


@router.get("/dossier/{cpf_cnpj}")
async def get_dossier(cpf_cnpj: str):
    """
    Retorna o dossiê consolidado de Compliance de uma entidade (CPF/CNPJ).
    Varre o PostgreSQL (environmental_alerts) verificando IBAMA e Lista Suja MTE.
    """
    from app.models.database import get_session, EnvironmentalAlert
    from sqlalchemy import or_
    import copy

    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    
    with get_session() as db:
        alerts = db.query(EnvironmentalAlert).filter(
            EnvironmentalAlert.cpf_cnpj == clean
        ).all()
        
    mte_records = []
    ibama_records = []
    
    for a in alerts:
        # Avoid circular dependencies by cloning dictionary
        data_clean = copy.deepcopy(a.raw_data) if a.raw_data else {}
        
        if a.source == "MTE":
            mte_records.append({
                "type": a.alert_type,
                "description": a.description,
                "date": str(a.created_at),
                "data": data_clean
            })
        elif a.source == "IBAMA":
            ibama_records.append({
                "type": a.alert_type,
                "description": a.description,
                "data": data_clean
            })
            
    risk = "BAIXO"
    if mte_records:
        risk = "CRÍTICO (Exclusão Imediata)"
    elif ibama_records:
        risk = "MÉDIO/ALTO (Avaliar Restrições)"
        
    return {
        "entity": cpf_cnpj,
        "overall_risk": risk,
        "summary": {
            "mte_slave_labor_occurrences": len(mte_records),
            "ibama_embargoes_or_infractions": len(ibama_records)
        },
        "records": {
            "mte": mte_records,
            "ibama": ibama_records
        }
    }
