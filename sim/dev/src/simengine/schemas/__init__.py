"""Schemas Pydantic do estado de jogo."""
from __future__ import annotations

from .action import PlayerAction
from .common import (
    BattalionStatusType,
    BattalionType,
    DiplomaticStatusType,
    EventCategoryType,
    EventCauseType,
    MapFeatureType,
    RegionGeoType,
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
from .polity import Battalion, Polity
from .region import MapFeature, Region
from .state import GameState
from .turn import TurnBuffer

__all__ = [
    "Battalion",
    "BattalionCreate",
    "BattalionDestroy",
    "BattalionMove",
    "BattalionStatusType",
    "BattalionType",
    "ConsolidatedSummary",
    "DiplomaticOpinionChange",
    "DiplomaticRelation",
    "DiplomaticStatusChange",
    "DiplomaticStatusType",
    "Event",
    "EventCategoryType",
    "EventCauseType",
    "GameState",
    "MapFeature",
    "MapFeatureType",
    "PlayerAction",
    "Polity",
    "PolityDoctrineAdd",
    "PolityDoctrineRemove",
    "PolityLeaderChange",
    "PolityTensionAdd",
    "PolityTensionRemove",
    "Region",
    "RegionGeoType",
    "RegionOwnerChange",
    "StateDelta",
    "TurnBuffer",
]
