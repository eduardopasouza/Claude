"""
Endpoints de publicações judiciais via DJEN / Comunica.PJe.

Fluxo típico:
  GET  /api/v1/publicacoes/oab/{uf}/{numero}    — busca publicações por OAB
  GET  /api/v1/publicacoes/processo/{numero}     — publicações de um processo
  GET  /api/v1/publicacoes/texto?q=...            — busca textual livre
  POST /api/v1/publicacoes/sync-oab              — sincroniza e salva no banco
  GET  /api/v1/publicacoes                       — lista persistida no banco
  PATCH /api/v1/publicacoes/{id}/lida             — marca como lida
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.collectors.djen import (
    DJENCollector,
    classificar_urgencia,
    extrair_resumo,
)
from app.models.database import Publicacao, get_db

logger = logging.getLogger("agrojus")

router = APIRouter()


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def _enriquecer_item(item: dict) -> dict:
    """Adiciona urgência e resumo a um item do DJEN."""
    data_disp = item.get("data_disponibilizacao") or item.get("datadisponibilizacao")
    item["urgencia"] = classificar_urgencia(data_disp) if data_disp else "desconhecida"
    item["resumo"] = extrair_resumo(item.get("texto", ""), max_chars=280)
    return item


def _parse_iso_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Data inválida '{s}'. Use formato ISO: YYYY-MM-DD.",
        )


# ----------------------------------------------------------------------
# GET /api/v1/publicacoes/oab/{uf}/{numero}
# ----------------------------------------------------------------------
@router.get("/oab/{uf}/{numero}")
async def publicacoes_por_oab(
    uf: str,
    numero: str,
    data_inicio: Optional[str] = Query(
        None, description="YYYY-MM-DD (default: 30 dias atrás)"
    ),
    data_fim: Optional[str] = Query(None, description="YYYY-MM-DD (default: hoje)"),
    itens_por_pagina: int = Query(50, ge=1, le=200),
    pagina: int = Query(1, ge=1),
):
    """
    Busca publicações do DJEN para uma OAB (advogado).

    Exemplo:
        GET /api/v1/publicacoes/oab/MA/12147
        GET /api/v1/publicacoes/oab/MA/12147?data_inicio=2026-01-01
    """
    collector = DJENCollector()
    dt_ini = _parse_iso_date(data_inicio)
    dt_fim = _parse_iso_date(data_fim)

    data = await collector.buscar_por_oab(
        numero_oab=numero,
        uf_oab=uf,
        data_inicio=dt_ini,
        data_fim=dt_fim,
        itens_por_pagina=itens_por_pagina,
        pagina=pagina,
    )

    # Enriquece cada item com urgência e resumo
    items = [_enriquecer_item(dict(it)) for it in data.get("items", [])]

    return {
        "status": data.get("status", "success"),
        "count": data.get("count", len(items)),
        "pagina": pagina,
        "itens_por_pagina": itens_por_pagina,
        "oab": {"numero": numero, "uf": uf.upper()},
        "periodo": {
            "inicio": (dt_ini or (date.today() - timedelta(days=30))).isoformat(),
            "fim": (dt_fim or date.today()).isoformat(),
        },
        "items": items,
    }


# ----------------------------------------------------------------------
# GET /api/v1/publicacoes/processo/{numero}
# ----------------------------------------------------------------------
@router.get("/processo/{numero}")
async def publicacoes_por_processo(
    numero: str,
    itens_por_pagina: int = Query(100, ge=1, le=200),
    pagina: int = Query(1, ge=1),
):
    """Lista todas as publicações de um processo CNJ."""
    collector = DJENCollector()
    data = await collector.buscar_por_processo(numero, itens_por_pagina, pagina)
    items = [_enriquecer_item(dict(it)) for it in data.get("items", [])]
    return {
        "status": data.get("status", "success"),
        "count": data.get("count", len(items)),
        "pagina": pagina,
        "processo": numero,
        "items": items,
    }


# ----------------------------------------------------------------------
# GET /api/v1/publicacoes/texto
# ----------------------------------------------------------------------
@router.get("/texto")
async def publicacoes_por_texto(
    q: str = Query(..., min_length=3, description="Texto a buscar"),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
    itens_por_pagina: int = Query(50, ge=1, le=200),
    pagina: int = Query(1, ge=1),
):
    """Busca textual livre em publicações do DJEN."""
    collector = DJENCollector()
    data = await collector.buscar_por_texto(
        texto=q,
        data_inicio=_parse_iso_date(data_inicio),
        data_fim=_parse_iso_date(data_fim),
        itens_por_pagina=itens_por_pagina,
        pagina=pagina,
    )
    items = [_enriquecer_item(dict(it)) for it in data.get("items", [])]
    return {
        "status": data.get("status", "success"),
        "count": data.get("count", len(items)),
        "pagina": pagina,
        "query": q,
        "items": items,
    }


# ----------------------------------------------------------------------
# POST /api/v1/publicacoes/sync-oab
# ----------------------------------------------------------------------
@router.post("/sync-oab")
async def sincronizar_oab(
    uf: str,
    numero: str,
    dias: int = Query(30, ge=1, le=365, description="Quantos dias atrás sincronizar"),
    db: Session = Depends(get_db),
):
    """
    Busca publicações no DJEN para uma OAB e persiste no banco local.

    Usa upsert por djen_id: rodadas repetidas são idempotentes (não duplica).
    Retorna contadores: novas, atualizadas, total.
    """
    collector = DJENCollector()
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)

    total_api = 0
    pagina = 1
    itens_por_pagina = 100
    novas = 0
    atualizadas = 0

    # Paginação: DJEN devolve até 200 itens/request; continuamos até esgotar
    while True:
        resp = await collector.buscar_por_oab(
            numero_oab=numero,
            uf_oab=uf,
            data_inicio=data_inicio,
            data_fim=data_fim,
            itens_por_pagina=itens_por_pagina,
            pagina=pagina,
        )
        items = resp.get("items", [])
        if not items:
            break
        total_api = resp.get("count", 0)

        for it in items:
            registro = _normalizar_para_db(it, numero, uf)
            existing = db.query(Publicacao).filter(
                Publicacao.djen_id == registro["djen_id"]
            ).first()
            if existing:
                # Atualiza campos mutáveis (status, texto pode ser editado)
                for k, v in registro.items():
                    if k not in ("id", "djen_id", "created_at"):
                        setattr(existing, k, v)
                atualizadas += 1
            else:
                db.add(Publicacao(**registro))
                novas += 1

        # Se retornou menos que itens_por_pagina, chegou no fim
        if len(items) < itens_por_pagina:
            break
        pagina += 1
        # Safety: limita a 50 páginas (5k itens) por sync
        if pagina > 50:
            logger.warning("djen.sync.max_pages oab=%s/%s", numero, uf)
            break

    db.commit()

    return {
        "status": "success",
        "oab": {"numero": numero, "uf": uf.upper()},
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat(),
            "dias": dias,
        },
        "total_api": total_api,
        "processadas": novas + atualizadas,
        "novas": novas,
        "atualizadas": atualizadas,
    }


# ----------------------------------------------------------------------
# GET /api/v1/publicacoes  (lista local persistida)
# ----------------------------------------------------------------------
@router.get("")
async def listar_publicacoes_persistidas(
    uf: Optional[str] = None,
    numero_oab: Optional[str] = None,
    numero_processo: Optional[str] = None,
    tribunal: Optional[str] = None,
    apenas_nao_lidas: bool = False,
    urgencia: Optional[str] = Query(
        None, pattern="^(critico|alto|medio|baixo)$"
    ),
    dias: Optional[int] = Query(None, ge=1, le=365),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Lista publicações já persistidas no banco, com filtros e paginação."""
    q = db.query(Publicacao)

    if uf:
        q = q.filter(Publicacao.oab_uf == uf.upper())
    if numero_oab:
        q = q.filter(Publicacao.oab_numero == str(numero_oab).lstrip("0"))
    if numero_processo:
        clean = numero_processo.replace("-", "").replace(".", "")
        q = q.filter(Publicacao.numero_processo == clean)
    if tribunal:
        q = q.filter(Publicacao.tribunal == tribunal.upper())
    if apenas_nao_lidas:
        q = q.filter(Publicacao.lida == False)  # noqa: E712
    if urgencia:
        q = q.filter(Publicacao.urgencia == urgencia)
    if dias:
        cutoff = date.today() - timedelta(days=dias)
        q = q.filter(Publicacao.data_disponibilizacao >= cutoff)

    total = q.count()
    items = (
        q.order_by(desc(Publicacao.data_disponibilizacao), desc(Publicacao.id))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "status": "success",
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [_serialize(p) for p in items],
    }


# ----------------------------------------------------------------------
# GET /api/v1/publicacoes/{id}
# ----------------------------------------------------------------------
@router.get("/{publicacao_id}")
async def obter_publicacao(publicacao_id: int, db: Session = Depends(get_db)):
    """Retorna publicação completa (incluindo texto inteiro + raw_data)."""
    p = db.query(Publicacao).filter(Publicacao.id == publicacao_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    return _serialize(p, incluir_texto=True, incluir_raw=True)


# ----------------------------------------------------------------------
# PATCH /api/v1/publicacoes/{id}/lida
# ----------------------------------------------------------------------
@router.patch("/{publicacao_id}/lida")
async def marcar_lida(
    publicacao_id: int,
    lida: bool = True,
    db: Session = Depends(get_db),
):
    """Marca publicação como lida/não lida."""
    p = db.query(Publicacao).filter(Publicacao.id == publicacao_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    p.lida = lida
    db.commit()
    return {"status": "success", "id": publicacao_id, "lida": lida}


# ----------------------------------------------------------------------
# GET /api/v1/publicacoes/stats/oab/{uf}/{numero}
# ----------------------------------------------------------------------
@router.get("/stats/oab/{uf}/{numero}")
async def stats_oab(uf: str, numero: str, db: Session = Depends(get_db)):
    """Agregados rápidos para dashboard: total, por urgência, por tribunal."""
    from sqlalchemy import func

    numero_clean = str(numero).lstrip("0")
    uf_upper = uf.upper()

    base = db.query(Publicacao).filter(
        Publicacao.oab_uf == uf_upper,
        Publicacao.oab_numero == numero_clean,
    )

    total = base.count()
    nao_lidas = base.filter(Publicacao.lida == False).count()  # noqa: E712
    criticas = base.filter(Publicacao.urgencia == "critico").count()

    por_tribunal_rows = (
        db.query(Publicacao.tribunal, func.count(Publicacao.id))
        .filter(
            Publicacao.oab_uf == uf_upper,
            Publicacao.oab_numero == numero_clean,
        )
        .group_by(Publicacao.tribunal)
        .all()
    )
    por_tribunal = {t or "—": c for t, c in por_tribunal_rows}

    return {
        "status": "success",
        "oab": {"numero": numero, "uf": uf_upper},
        "total": total,
        "nao_lidas": nao_lidas,
        "criticas": criticas,
        "por_tribunal": por_tribunal,
    }


# ----------------------------------------------------------------------
# Normalização DJEN → row do banco
# ----------------------------------------------------------------------
def _normalizar_para_db(item: dict, oab_numero: str, oab_uf: str) -> dict:
    """Converte item DJEN no formato esperado pelo modelo Publicacao."""
    data_disp = item.get("data_disponibilizacao")
    if isinstance(data_disp, str):
        try:
            data_disp = date.fromisoformat(data_disp[:10])
        except ValueError:
            data_disp = None
    urgencia = (
        classificar_urgencia(item.get("data_disponibilizacao") or "")
        if item.get("data_disponibilizacao")
        else "desconhecida"
    )
    return {
        "djen_id": item.get("id"),
        "djen_hash": item.get("hash"),
        "data_disponibilizacao": data_disp,
        "tribunal": item.get("siglaTribunal"),
        "orgao": item.get("nomeOrgao"),
        "id_orgao": item.get("idOrgao"),
        "tipo_comunicacao": item.get("tipoComunicacao"),
        "tipo_documento": item.get("tipoDocumento"),
        "classe": item.get("nomeClasse"),
        "codigo_classe": str(item.get("codigoClasse") or ""),
        "meio": item.get("meio"),
        "numero_comunicacao": item.get("numeroComunicacao"),
        "numero_processo": item.get("numero_processo"),
        "numero_processo_mascarado": item.get("numeroprocessocommascara"),
        "texto": item.get("texto"),
        "link": item.get("link"),
        "oab_numero": str(oab_numero).lstrip("0"),
        "oab_uf": oab_uf.upper(),
        "urgencia": urgencia,
        "raw_data": item,
        "updated_at": datetime.now(timezone.utc),
    }


def _serialize(p: Publicacao, incluir_texto: bool = False, incluir_raw: bool = False) -> dict:
    """Serializa Publicacao para JSON, com texto/raw opcionais."""
    d = {
        "id": p.id,
        "djen_id": p.djen_id,
        "djen_hash": p.djen_hash,
        "data_disponibilizacao": p.data_disponibilizacao.isoformat() if p.data_disponibilizacao else None,
        "tribunal": p.tribunal,
        "orgao": p.orgao,
        "tipo_comunicacao": p.tipo_comunicacao,
        "tipo_documento": p.tipo_documento,
        "classe": p.classe,
        "codigo_classe": p.codigo_classe,
        "meio": p.meio,
        "numero_processo": p.numero_processo,
        "numero_processo_mascarado": p.numero_processo_mascarado,
        "link": p.link,
        "oab_numero": p.oab_numero,
        "oab_uf": p.oab_uf,
        "lida": p.lida,
        "urgencia": p.urgencia,
        "resumo": extrair_resumo(p.texto or "", max_chars=280),
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }
    if incluir_texto:
        d["texto"] = p.texto
    if incluir_raw:
        d["raw_data"] = p.raw_data
    return d
