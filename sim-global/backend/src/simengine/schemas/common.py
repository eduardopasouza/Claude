"""Tipos primitivos compartilhados entre schemas."""
from __future__ import annotations

from typing import Literal

DiplomaticStatusType = Literal[
    "guerra",
    "paz",
    "aliança",
    "neutralidade armada",
    "embargo",
    "ruptura",
]

EventCategoryType = Literal[
    "diplomatic",
    "military",
    "internal",
    "economic",
    "natural",
    "cultural",
    "social",
    "religious",
    "technological",
    "scientific",
    "demographic",
    "environmental",
]

EventCauseType = Literal["player_action", "scheduled", "emergent"]

RegionGeoType = Literal["land", "coastal", "ocean", "strait"]

BattalionType = Literal[
    "infantaria",
    "cavalaria",
    "artilharia",
    "naval",
    "aviação",
]

BattalionStatusType = Literal[
    "pronto",
    "em movimento",
    "engajado",
    "exausto",
]

MapFeatureType = Literal[
    "cidade",
    "porto",
    "ferrovia",
    "fortaleza",
    "indústria",
    "fronteira",
]

EventSeverityType = Literal["minor", "moderate", "major", "critical"]

TriggerKind = Literal["date", "state", "event_chain"]

EffectOpType = Literal["delta", "set", "add", "remove"]
