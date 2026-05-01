"""Endpoints REST do sim-global.

Conecta persistência (SQLAlchemy) com agente (Claude Agent SDK) e o
motor determinístico (simengine).
"""
from __future__ import annotations

import asyncio
import logging
from datetime import date as date_cls
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.orm import Session

from simengine.engine import (
    apply_turn_buffer as apply_turn_buffer_engine,
    check_state_invariants,
    check_turn_invariants,
)
from simengine.schemas import (
    ConsolidatedSummary,
    Event,
    GameState,
    TurnBuffer,
)

from ..persistence import (
    CampaignAlreadyExistsError,
    CampaignNotFoundError,
    all_summaries,
    apply_turn_buffer,
    append_diplomatic_log,
    delete_campaign,
    diplomatic_history,
    export_game_state,
    get_campaign_lore,
    import_game_state,
    list_campaigns,
    recent_events,
)
from ..scenarios import filter_in_window, load_scheduled_events_raw
from ..state_loader import load_example, list_examples

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["sim-global"])


# ---------- dependências ----------

def get_db(request: Request) -> Session:
    """Sessão SQLAlchemy injetada pelo lifespan da app."""
    factory = request.app.state.session_factory
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_agent(request: Request):
    """Devolve AgentRunner ou levanta 503 com instrução."""
    runner = getattr(request.app.state, "agent_runner", None)
    if runner is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Claude Agent SDK não inicializado. Instale com "
                "`pip install -e .[agent]` e exporte "
                "CLAUDE_CODE_OAUTH_TOKEN."
            ),
        )
    return runner


# ---------- payloads ----------

class ImportExamplePayload(BaseModel):
    example: str = Field(..., description="ex.: brasil-vargas-1930")
    campaign_name: str = Field(..., description="nome da campanha (slug)")


class NewCampaignPayload(BaseModel):
    name: str
    year: int = Field(ge=1500, le=2100)
    nation: str
    granularity: dict[str, Any] | None = None  # ex.: {"regioes":8,"polities":10}


class TurnRequest(BaseModel):
    months: int = Field(default=6, ge=1, le=120)


class AdviseRequest(BaseModel):
    question: str


class DiplomaticMessage(BaseModel):
    counterparty: str
    message: str


# ---------- endpoints ----------

@router.get("/campaigns")
def api_list_campaigns(db: Session = Depends(get_db)) -> list[dict]:
    return [
        {
            "name": c.name,
            "current_date": c.current_date.isoformat(),
            "player_polity": c.player_polity_name,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }
        for c in list_campaigns(db)
    ]


@router.get("/examples")
def api_list_examples() -> list[str]:
    return list_examples()


@router.post("/campaigns/import-example", status_code=201)
def api_import_example(
    payload: ImportExamplePayload, db: Session = Depends(get_db)
) -> dict:
    try:
        state = load_example(payload.example)
    except FileNotFoundError as exc:
        raise HTTPException(404, f"exemplo não encontrado: {payload.example}") from exc

    lore_md = _bundle_example_lore(payload.example)
    try:
        c = import_game_state(db, payload.campaign_name, state, lore_md=lore_md)
    except CampaignAlreadyExistsError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {"name": c.name, "imported": True, "polities": len(state.polities)}


@router.post("/campaigns/new", status_code=202)
async def api_new_campaign(
    payload: NewCampaignPayload,
    db: Session = Depends(get_db),
    runner=Depends(get_agent),
) -> dict:
    """Invoca scenario_builder para gerar estado procedural."""
    prompt = _prompt_path("scenario_builder.md")
    builder_payload = {
        "year": payload.year,
        "nation": payload.nation,
        "granularity": payload.granularity or {"regioes": 8, "polities": 10},
    }
    try:
        result = await runner.run_subagent(
            prompt, builder_payload, json_output=True, max_retries=3
        )
    except Exception as exc:
        logger.exception("scenario_builder falhou")
        raise HTTPException(502, f"scenario_builder falhou: {exc}") from exc

    try:
        state = GameState.model_validate(result["game_state"])
    except (KeyError, ValidationError) as exc:
        raise HTTPException(502, f"output inválido do builder: {exc}") from exc

    violations = check_state_invariants(state)
    if violations:
        raise HTTPException(
            502, f"estado gerado com violações de invariante: {violations}"
        )

    lore_md = result.get("lore_md")
    try:
        c = import_game_state(db, payload.name, state, lore_md=lore_md)
    except CampaignAlreadyExistsError as exc:
        raise HTTPException(409, str(exc)) from exc
    return {
        "name": c.name,
        "year": payload.year,
        "nation": payload.nation,
        "polities": len(state.polities),
        "regions": len(state.regions),
        "scheduled_events": len(result.get("scheduled_events", [])),
    }


@router.delete("/campaigns/{name}", status_code=204)
def api_delete_campaign(name: str, db: Session = Depends(get_db)) -> None:
    try:
        delete_campaign(db, name)
    except CampaignNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/campaigns/{name}/state")
def api_state(name: str, db: Session = Depends(get_db)) -> dict:
    try:
        state = export_game_state(db, name)
    except CampaignNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {
        "campaign": name,
        "state": state.model_dump(mode="json"),
        "invariant_violations": check_state_invariants(state),
    }


@router.post("/campaigns/{name}/turn")
async def api_turn(
    name: str,
    req: TurnRequest,
    db: Session = Depends(get_db),
    runner=Depends(get_agent),
) -> dict:
    try:
        state = export_game_state(db, name)
    except CampaignNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc

    from datetime import timedelta
    window_end = state.current_date + timedelta(days=30 * req.months)
    sched_raw = load_scheduled_events_raw(name)
    sched_window = filter_in_window(sched_raw, state.current_date, window_end)
    payload = {
        "current_state": state.model_dump(mode="json"),
        "pending_actions": [a.model_dump(mode="json") for a in state.pending_actions],
        "n_months": req.months,
        "scheduled_events_in_window": sched_window,
        "recent_event_log": [
            e.model_dump(mode="json") for e in recent_events(db, name, limit=20)
        ],
        "summaries": [
            s.model_dump(mode="json") for s in all_summaries(db, name)
        ],
    }

    try:
        raw = await runner.run_subagent(
            _prompt_path("game_master.md"),
            payload,
            json_output=True,
            max_retries=3,
        )
    except Exception as exc:
        logger.exception("game_master falhou")
        raise HTTPException(502, f"game_master falhou: {exc}") from exc

    try:
        buffer = TurnBuffer.model_validate(raw)
    except ValidationError as exc:
        raise HTTPException(502, f"turn_buffer inválido: {exc}") from exc

    violations = check_turn_invariants(state, buffer)
    if violations:
        raise HTTPException(
            502, f"invariantes de turno violados: {violations}"
        )

    apply_turn_buffer(db, name, buffer)
    return {
        "campaign": name,
        "turn_end_date": buffer.turn_end_date.isoformat(),
        "events": [e.model_dump(mode="json") for e in buffer.events],
        "deltas_applied": len(buffer.deltas),
        "narrative": buffer.narrative,
    }


@router.post("/campaigns/{name}/advise")
async def api_advise(
    name: str,
    req: AdviseRequest,
    db: Session = Depends(get_db),
    runner=Depends(get_agent),
) -> dict:
    try:
        state = export_game_state(db, name)
    except CampaignNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc

    payload = {
        "state": state.model_dump(mode="json"),
        "question": req.question,
        "recent_events": [
            e.model_dump(mode="json") for e in recent_events(db, name, limit=10)
        ],
        "summaries": [
            s.model_dump(mode="json") for s in all_summaries(db, name)
        ],
        "lore_md": get_campaign_lore(db, name),
    }
    try:
        text = await runner.run_subagent(
            _prompt_path("advisor.md"), payload, json_output=False
        )
    except Exception as exc:
        logger.exception("advisor falhou")
        raise HTTPException(502, f"advisor falhou: {exc}") from exc
    return {"campaign": name, "answer": text}


@router.post("/campaigns/{name}/dm")
async def api_dm(
    name: str,
    msg: DiplomaticMessage,
    db: Session = Depends(get_db),
    runner=Depends(get_agent),
) -> dict:
    try:
        state = export_game_state(db, name)
    except CampaignNotFoundError as exc:
        raise HTTPException(404, str(exc)) from exc

    if msg.counterparty not in state.polities:
        raise HTTPException(400, f"polity inexistente: {msg.counterparty}")
    if msg.counterparty == state.player_polity:
        raise HTTPException(400, "não há diplomacia consigo mesmo")

    full_lore = get_campaign_lore(db, name) or ""
    payload = {
        "state": state.model_dump(mode="json"),
        "counterparty": msg.counterparty,
        "lore_for_counterparty": _extract_polity_lore(full_lore, msg.counterparty),
        "bilateral_history": diplomatic_history(db, name, msg.counterparty),
        "message_in": msg.message,
    }
    try:
        result = await runner.run_subagent(
            _prompt_path("diplomat.md"), payload, json_output=True
        )
    except Exception as exc:
        logger.exception("diplomat falhou")
        raise HTTPException(502, f"diplomat falhou: {exc}") from exc

    entry = {
        "date": state.current_date.isoformat(),
        "from_polity": state.player_polity,
        "to_polity": msg.counterparty,
        "message_in": msg.message,
        "message_out": result.get("message_out", ""),
        "proposed_deltas": result.get("proposed_deltas", []),
    }
    append_diplomatic_log(db, name, msg.counterparty, entry)
    return {
        "campaign": name,
        "counterparty": msg.counterparty,
        "message_out": entry["message_out"],
        "proposed_deltas": entry["proposed_deltas"],
    }


# ---------- helpers ----------

def _prompt_path(name: str) -> Path:
    base = Path(__file__).parent.parent / "prompts"
    p = base / name
    if not p.exists():
        raise HTTPException(500, f"prompt ausente: {name}")
    return p


def _extract_polity_lore(lore_md: str, polity_name: str) -> str:
    """Tenta extrair a seção do lore_md correspondente a uma polity.

    Heurística simples: olha para um cabeçalho `# <name>` ou `## <name>`
    e devolve até o próximo cabeçalho de mesmo nível, OU concatena
    arquivos cujo path no comentário-marker bate com o nome.
    """
    if not lore_md:
        return ""
    needle_low = polity_name.lower()
    chunks: list[str] = []
    current_chunk: list[str] = []
    keep = False
    current_level: int | None = None
    for line in lore_md.splitlines():
        marker_match = line.startswith("<!--") and needle_low in line.lower()
        header_match = line.startswith("#") and needle_low in line.lower()
        if marker_match or header_match:
            if current_chunk and keep:
                chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            keep = True
            current_level = (
                len(line) - len(line.lstrip("#")) if line.startswith("#") else None
            )
            continue
        if (
            keep
            and line.startswith("#")
            and current_level is not None
            and (len(line) - len(line.lstrip("#"))) <= current_level
        ):
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            keep = False
            current_level = None
            continue
        if keep:
            current_chunk.append(line)
    if current_chunk and keep:
        chunks.append("\n".join(current_chunk))
    return "\n\n".join(chunks).strip()


def _bundle_example_lore(example_name: str) -> str | None:
    """Concatena lore_md/*.md do exemplo num único string. Devolve None se ausente."""
    from .. import config as cfg_module

    base = cfg_module.project_root() / "examples" / example_name / "lore"
    if not base.exists():
        return None
    chunks = []
    for path in sorted(base.rglob("*.md")):
        chunks.append(f"<!-- {path.relative_to(base)} -->\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks) if chunks else None
