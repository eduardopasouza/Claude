"""Schemas Pydantic do estado de jogo."""
from __future__ import annotations

from .action import PlayerAction
from .common import (
    BattalionStatusType,
    BattalionType,
    DiplomaticStatusType,
    EffectOpType,
    EventCategoryType,
    EventCauseType,
    EventSeverityType,
    MapFeatureType,
    RegionGeoType,
    TriggerKind,
)
from .delta import (
    BattalionCreate,
    BattalionDestroy,
    BattalionMove,
    DiplomaticOpinionChange,
    DiplomaticStatusChange,
    PolityDoctrineAdd,
    PolityDoctrineRemove,
    PolityLeaderChange,
    PolityTensionAdd,
    PolityTensionRemove,
    RegionOwnerChange,
    StateDelta,
)
from .diplomatic import DiplomaticRelation
from .event import ConsolidatedSummary, Event
from .polity import Battalion, Polity, PolityAttributes
from .region import MapFeature, Region
from .scenario import CancelCondition, EffectSpec, ScheduledEvent, Trigger
from .state import GameState
from .turn import TurnBuffer

__all__ = [
    "Battalion",
    "BattalionCreate",
    "BattalionDestroy",
    "BattalionMove",
    "BattalionStatusType",
    "BattalionType",
    "CancelCondition",
    "ConsolidatedSummary",
    "DiplomaticOpinionChange",
    "DiplomaticRelation",
    "DiplomaticStatusChange",
    "DiplomaticStatusType",
    "EffectOpType",
    "EffectSpec",
    "Event",
    "EventCategoryType",
    "EventCauseType",
    "EventSeverityType",
    "GameState",
    "MapFeature",
    "MapFeatureType",
    "PlayerAction",
    "Polity",
    "PolityAttributes",
    "PolityDoctrineAdd",
    "PolityDoctrineRemove",
    "PolityLeaderChange",
    "PolityTensionAdd",
    "PolityTensionRemove",
    "Region",
    "RegionGeoType",
    "RegionOwnerChange",
    "ScheduledEvent",
    "StateDelta",
    "Trigger",
    "TriggerKind",
    "TurnBuffer",
]
