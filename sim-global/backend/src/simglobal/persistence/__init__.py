"""Camada de persistência: SQLAlchemy 2.x ORM + Alembic.

Re-exporta os pontos de entrada usados pelo resto do backend
(repositórios, modelos ORM e helpers de DB). Não importa nada
específico de FastAPI — é puramente domínio + acesso ao banco.
"""
from __future__ import annotations

from . import models, repositories
from .db import (
    drop_db,
    get_session,
    init_db,
    make_engine,
    make_session_factory,
)
from .models import (
    Base,
    Battalion,
    Campaign,
    ConsolidatedSummary,
    DiplomaticLogEntry,
    DiplomaticRelation,
    Doctrine,
    Event,
    InternalTension,
    PendingAction,
    Polity,
    Region,
    ScheduledEventFire,
)
from .repositories import (
    CampaignAlreadyExistsError,
    CampaignNotFoundError,
    append_diplomatic_log,
    append_event_log_entries,
    apply_turn_buffer,
    delete_campaign,
    events_since_summary,
    export_game_state,
    import_game_state,
    list_campaigns,
    record_scheduled_event_fired,
)

__all__ = [
    "Base",
    "Battalion",
    "Campaign",
    "CampaignAlreadyExistsError",
    "CampaignNotFoundError",
    "ConsolidatedSummary",
    "DiplomaticLogEntry",
    "DiplomaticRelation",
    "Doctrine",
    "Event",
    "InternalTension",
    "PendingAction",
    "Polity",
    "Region",
    "ScheduledEventFire",
    "append_diplomatic_log",
    "append_event_log_entries",
    "apply_turn_buffer",
    "delete_campaign",
    "drop_db",
    "events_since_summary",
    "export_game_state",
    "get_session",
    "import_game_state",
    "init_db",
    "list_campaigns",
    "make_engine",
    "make_session_factory",
    "models",
    "record_scheduled_event_fired",
    "repositories",
]
