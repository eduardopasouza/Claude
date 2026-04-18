"""
Hub Jurídico-Agro — endpoints do módulo jurídico reposicionado.

Escopo MUITO além de "ferramenta para advogado": hub de informação para
agricultor, corretor, trading, investidor, consultor ambiental, produtor.

Endpoints:
  GET  /juridico/contratos[?categoria=...&q=...&publico=...]
  GET  /juridico/contratos/{slug}
  GET  /juridico/teses[?area=...&q=...]
  GET  /juridico/teses/{slug}
  GET  /juridico/legislacao[?uf=...&municipio_ibge=...&tema=...&esfera=...]
  GET  /juridico/legislacao/{slug}
  GET  /juridico/processos/{cpf_cnpj}/dossie   — resumo de processos, autos, sanções
  POST /juridico/monitoramento  — cadastra monitoramento contínuo de uma parte
  GET  /juridico/monitoramento
  DELETE /juridico/monitoramento/{id}
  POST /juridico/seed?force=true  — reexecuta seed (admin)
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import or_, text

from app.api.auth import get_current_user
from app.models.database import (
    ContratoAgroTemplate, TeseDefesaAgro, LegislacaoAgro,
    MonitoramentoParte,
    get_engine, get_session,
)

logger = logging.getLogger("agrojus.juridico")
router = APIRouter()


# ==========================================================================
# Contratos
# ==========================================================================


@router.get("/contratos")
def list_contratos(
    categoria: Optional[str] = None,
    publico: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 50,
):
    session = get_session()
    try:
        query = session.query(ContratoAgroTemplate)
        if categoria:
            query = query.filter(ContratoAgroTemplate.categoria == categoria)
        if q:
            like = f"%{q.lower()}%"
            query = query.filter(or_(
                ContratoAgroTemplate.titulo.ilike(like),
                ContratoAgroTemplate.sinopse.ilike(like),
            ))
        rows = query.order_by(ContratoAgroTemplate.titulo).limit(limit).all()
        results = []
        for r in rows:
            if publico and publico not in (r.publico_alvo or []):
                continue
            results.append({
                "id": r.id,
                "slug": r.slug,
                "titulo": r.titulo,
                "categoria": r.categoria,
                "subcategoria": r.subcategoria,
                "sinopse": r.sinopse,
                "aplicacao": r.aplicacao,
                "publico_alvo": r.publico_alvo,
                "n_campos": len(r.campos or []),
                "n_legislacao": len(r.legislacao_referencia or []),
                "versao": r.versao,
            })
        return {"total": len(results), "contratos": results}
    finally:
        session.close()


@router.get("/contratos/{slug}")
def get_contrato(slug: str):
    session = get_session()
    try:
        r = session.query(ContratoAgroTemplate).filter_by(slug=slug).first()
        if not r:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        return {
            "id": r.id,
            "slug": r.slug,
            "titulo": r.titulo,
            "categoria": r.categoria,
            "subcategoria": r.subcategoria,
            "sinopse": r.sinopse,
            "aplicacao": r.aplicacao,
            "publico_alvo": r.publico_alvo,
            "texto_markdown": r.texto_markdown,
            "campos": r.campos,
            "legislacao_referencia": r.legislacao_referencia,
            "cautelas": r.cautelas,
            "versao": r.versao,
        }
    finally:
        session.close()


# ==========================================================================
# Teses
# ==========================================================================


@router.get("/teses")
def list_teses(
    area: Optional[str] = None,
    q: Optional[str] = None,
    publico: Optional[str] = None,
    limit: int = 50,
):
    session = get_session()
    try:
        query = session.query(TeseDefesaAgro)
        if area:
            query = query.filter(TeseDefesaAgro.area == area)
        if q:
            like = f"%{q.lower()}%"
            query = query.filter(or_(
                TeseDefesaAgro.titulo.ilike(like),
                TeseDefesaAgro.situacao.ilike(like),
                TeseDefesaAgro.sumula_propria.ilike(like),
            ))
        rows = query.order_by(TeseDefesaAgro.area, TeseDefesaAgro.titulo).limit(limit).all()
        results = []
        for r in rows:
            if publico and publico not in (r.publico_alvo or []):
                continue
            results.append({
                "id": r.id,
                "slug": r.slug,
                "titulo": r.titulo,
                "area": r.area,
                "situacao": r.situacao,
                "sumula_propria": r.sumula_propria,
                "publico_alvo": r.publico_alvo,
                "n_argumentos": len(r.argumentos_principais or []),
                "n_precedentes": len(r.precedentes_sugeridos or []),
            })
        return {"total": len(results), "teses": results}
    finally:
        session.close()


@router.get("/teses/{slug}")
def get_tese(slug: str):
    session = get_session()
    try:
        r = session.query(TeseDefesaAgro).filter_by(slug=slug).first()
        if not r:
            raise HTTPException(status_code=404, detail="Tese não encontrada")
        return {
            "id": r.id,
            "slug": r.slug,
            "titulo": r.titulo,
            "area": r.area,
            "situacao": r.situacao,
            "sumula_propria": r.sumula_propria,
            "argumentos_principais": r.argumentos_principais,
            "precedentes_sugeridos": r.precedentes_sugeridos,
            "legislacao_aplicavel": r.legislacao_aplicavel,
            "aplicabilidade": r.aplicabilidade,
            "contra_argumentos": r.contra_argumentos,
            "proxima_acao": r.proxima_acao,
            "publico_alvo": r.publico_alvo,
        }
    finally:
        session.close()


# ==========================================================================
# Legislação
# ==========================================================================


@router.get("/legislacao")
def list_legislacao(
    esfera: Optional[str] = None,
    uf: Optional[str] = None,
    municipio_ibge: Optional[str] = None,
    tema: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 100,
):
    session = get_session()
    try:
        query = session.query(LegislacaoAgro)
        if esfera:
            query = query.filter(LegislacaoAgro.esfera == esfera)
        if uf:
            query = query.filter(or_(
                LegislacaoAgro.uf == uf.upper(),
                LegislacaoAgro.esfera == "federal",  # inclui federais
            ))
        if municipio_ibge:
            query = query.filter(or_(
                LegislacaoAgro.municipio_ibge == municipio_ibge,
                LegislacaoAgro.esfera == "federal",
            ))
        if q:
            like = f"%{q.lower()}%"
            query = query.filter(or_(
                LegislacaoAgro.titulo.ilike(like),
                LegislacaoAgro.ementa.ilike(like),
                LegislacaoAgro.resumo.ilike(like),
            ))
        rows = query.order_by(LegislacaoAgro.esfera, LegislacaoAgro.ano.desc()).limit(limit).all()
        results = []
        for r in rows:
            if tema and r.temas and tema not in r.temas:
                continue
            results.append({
                "id": r.id,
                "slug": r.slug,
                "titulo": r.titulo,
                "esfera": r.esfera,
                "uf": r.uf,
                "municipio": r.municipio,
                "tipo": r.tipo,
                "numero": r.numero,
                "ano": r.ano,
                "orgao": r.orgao,
                "temas": r.temas,
                "resumo": r.resumo,
                "situacao": r.situacao,
                "url_oficial": r.url_oficial,
            })
        return {"total": len(results), "legislacao": results}
    finally:
        session.close()


@router.get("/legislacao/{slug}")
def get_legislacao(slug: str):
    session = get_session()
    try:
        r = session.query(LegislacaoAgro).filter_by(slug=slug).first()
        if not r:
            raise HTTPException(status_code=404, detail="Legislação não encontrada")
        return {
            "id": r.id, "slug": r.slug, "titulo": r.titulo, "esfera": r.esfera,
            "uf": r.uf, "municipio": r.municipio, "tipo": r.tipo, "numero": r.numero,
            "ano": r.ano, "orgao": r.orgao, "ementa": r.ementa, "temas": r.temas,
            "publicacao": r.publicacao.isoformat() if r.publicacao else None,
            "situacao": r.situacao, "url_oficial": r.url_oficial,
            "url_lexml": r.url_lexml, "texto_integral_url": r.texto_integral_url,
            "resumo": r.resumo,
        }
    finally:
        session.close()


# ==========================================================================
# Dossiê de processos (terceiro ou próprio)
# ==========================================================================


@router.get("/processos/{cpf_cnpj}/dossie")
def processos_dossie(cpf_cnpj: str):
    """
    Varre todas as bases para trazer dossiê jurídico consolidado do CPF/CNPJ.
    Útil para monitoramento de terceiros (vendedor, fornecedor, vizinho).
    """
    clean = cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    engine = get_engine()
    d: dict = {"cpf_cnpj_mask": _mask_cpf_cnpj(clean)}

    with engine.connect() as conn:
        # DataJud / legal_records
        d["datajud_processos"] = [
            dict(r) for r in conn.execute(text("""
                SELECT record_type AS tipo, source AS tribunal, case_number AS numero,
                       description AS objeto, amount AS valor, status,
                       date_filed::text AS data_distribuicao,
                       municipality AS municipio, state AS uf
                FROM legal_records
                WHERE cpf_cnpj = :cpf
                ORDER BY date_filed DESC NULLS LAST
                LIMIT 50
            """), {"cpf": clean}).mappings().all()
        ]
        # DJEN (por CPF na raw_data)
        try:
            d["djen_publicacoes"] = [
                dict(r) for r in conn.execute(text("""
                    SELECT numero_processo, tribunal, orgao, tipo_comunicacao,
                           data_disponibilizacao::text AS data,
                           texto, link
                    FROM publicacoes_djen
                    WHERE raw_data::text ILIKE :cpf_pattern
                    ORDER BY data_disponibilizacao DESC
                    LIMIT 20
                """), {"cpf_pattern": f"%{clean}%"}).mappings().all()
            ]
        except Exception:
            d["djen_publicacoes"] = []
        # Autos IBAMA
        d["autos_ibama"] = [
            dict(r) for r in conn.execute(text("""
                SELECT numero_auto, data_auto::text AS data, uf, municipio,
                       valor_auto, status_debito, desc_infracao, enq_legal
                FROM ibama_autos_infracao
                WHERE cpf_cnpj_infrator = :cpf
                ORDER BY valor_auto DESC NULLS LAST LIMIT 30
            """), {"cpf": clean}).mappings().all()
        ]
        # CEIS + CNEP
        d["ceis"] = [
            dict(r) for r in conn.execute(text("""
                SELECT nome, tipo_sancao,
                       data_inicio_sancao::text AS data_inicio,
                       data_fim_sancao::text AS data_fim,
                       orgao_sancionador, processo
                FROM ceis_registros WHERE cpf_cnpj = :cpf
            """), {"cpf": clean}).mappings().all()
        ]
        d["cnep"] = [
            dict(r) for r in conn.execute(text("""
                SELECT nome, tipo_sancao, valor_multa,
                       data_inicio_sancao::text AS data_inicio,
                       orgao_sancionador, processo
                FROM cnep_registros WHERE cpf_cnpj = :cpf
            """), {"cpf": clean}).mappings().all()
        ]
        # Lista Suja
        d["lista_suja"] = [
            dict(r) for r in conn.execute(text("""
                SELECT alert_type, description, date_detected::text AS data, raw_data
                FROM environmental_alerts
                WHERE source='MTE' AND cpf_cnpj = :cpf
            """), {"cpf": clean}).mappings().all()
        ]

    # Totais para sumário
    d["sumario"] = {
        "processos_datajud": len(d["datajud_processos"]),
        "djen_publicacoes": len(d["djen_publicacoes"]),
        "autos_ibama": len(d["autos_ibama"]),
        "valor_autos_ibama": sum((a.get("valor_auto") or 0) for a in d["autos_ibama"]),
        "ceis": len(d["ceis"]),
        "cnep": len(d["cnep"]),
        "lista_suja_mte": len(d["lista_suja"]),
        "valor_processos": sum((p.get("valor") or 0) for p in d["datajud_processos"]),
    }
    d["risco_consolidado"] = _classificar_risco(d["sumario"])
    return d


def _classificar_risco(s: dict) -> str:
    pontos = 0
    if s.get("lista_suja_mte", 0) > 0:
        pontos += 50
    if s.get("ceis", 0) > 0:
        pontos += 30
    if s.get("cnep", 0) > 0:
        pontos += 25
    if s.get("autos_ibama", 0) >= 5:
        pontos += 20
    elif s.get("autos_ibama", 0) > 0:
        pontos += 10
    if (s.get("valor_autos_ibama") or 0) > 500_000:
        pontos += 15
    if s.get("processos_datajud", 0) >= 10:
        pontos += 10
    if pontos >= 50:
        return "CRITICO"
    if pontos >= 25:
        return "ALTO"
    if pontos >= 10:
        return "MEDIO"
    return "BAIXO"


# ==========================================================================
# Monitoramento de partes (CPF/CNPJ contínuo)
# ==========================================================================


class MonitoramentoPartePayload(BaseModel):
    cpf_cnpj: str
    nome_sugerido: Optional[str] = None
    contexto: Optional[str] = None
    tags: Optional[list[str]] = None
    eventos_monitorados: list[str] = [
        "datajud_novo_processo", "ibama_auto", "ceis", "cnep", "lista_suja", "djen",
    ]
    frequencia: str = "diaria"
    webhook_url: Optional[str] = None


@router.get("/monitoramento")
def list_monitoramento(user: Optional[dict] = Depends(get_current_user)):
    session = get_session()
    try:
        query = session.query(MonitoramentoParte)
        if user and user.get("user_id"):
            query = query.filter(or_(
                MonitoramentoParte.user_id == user["user_id"],
                MonitoramentoParte.user_id.is_(None),
            ))
        rows = query.order_by(MonitoramentoParte.created_at.desc()).all()
        return {
            "total": len(rows),
            "monitoramentos": [
                {
                    "id": r.id, "cpf_cnpj": _mask_cpf_cnpj(r.cpf_cnpj),
                    "nome_sugerido": r.nome_sugerido, "contexto": r.contexto,
                    "tags": r.tags, "eventos_monitorados": r.eventos_monitorados,
                    "frequencia": r.frequencia, "webhook_url": bool(r.webhook_url),
                    "active": r.active,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "last_checked_at": r.last_checked_at.isoformat() if r.last_checked_at else None,
                }
                for r in rows
            ],
        }
    finally:
        session.close()


@router.post("/monitoramento")
def create_monitoramento(
    payload: MonitoramentoPartePayload,
    user: Optional[dict] = Depends(get_current_user),
):
    clean = payload.cpf_cnpj.replace(".", "").replace("/", "").replace("-", "")
    if len(clean) not in (11, 14):
        raise HTTPException(status_code=400, detail="CPF/CNPJ inválido")
    session = get_session()
    try:
        row = MonitoramentoParte(
            user_id=user["user_id"] if user else None,
            cpf_cnpj=clean,
            nome_sugerido=payload.nome_sugerido,
            contexto=payload.contexto,
            tags=payload.tags or [],
            eventos_monitorados=payload.eventos_monitorados,
            frequencia=payload.frequencia,
            webhook_url=payload.webhook_url,
            active=True,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return {"id": row.id, "cpf_cnpj": _mask_cpf_cnpj(clean)}
    finally:
        session.close()


@router.delete("/monitoramento/{monit_id}")
def delete_monitoramento(
    monit_id: int,
    user: Optional[dict] = Depends(get_current_user),
):
    session = get_session()
    try:
        row = session.query(MonitoramentoParte).filter_by(id=monit_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Monitoramento não encontrado")
        session.delete(row)
        session.commit()
        return {"deleted": True}
    finally:
        session.close()


# ==========================================================================
# Seed admin
# ==========================================================================


@router.post("/seed")
def seed_juridico_endpoint(force: bool = Query(False)):
    from app.services.juridico_seeds import seed_juridico
    result = seed_juridico(force=force)
    return {"inserted": result, "message": "Seeds processadas com sucesso"}


def _mask_cpf_cnpj(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    if len(s) >= 11:
        return s[:3] + "." + "*" * (len(s) - 6) + s[-4:]
    return s
