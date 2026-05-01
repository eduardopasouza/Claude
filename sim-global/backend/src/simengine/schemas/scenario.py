"""Scripting híbrido de eventos pré-programados.

Combina predicados estruturados (triggers, cancel_conditions, effects)
com fallback para prosa em linguagem natural. O game_master interpreta
os campos em prosa quando os estruturados estão vazios. Inspirado nos
patterns observados em PaxHistoria, com formalização adicional para
eventos historicamente determinísticos.
"""
from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from .common import (
    EffectOpType,
    EventCategoryType,
    EventSeverityType,
    TriggerKind,
)


class Trigger(BaseModel):
    """Predicado que dispara o evento. Avaliado pelo game_master."""

    kind: TriggerKind
    expr: str  # expressão estruturada ou linguagem natural


class CancelCondition(BaseModel):
    """Predicado que cancela o evento se verdadeiro no estado atual."""

    kind: str  # "state", "doctrine_present", "tension_absent", etc.
    expr: str


class EffectSpec(BaseModel):
    """Efeito estruturado do evento.

    Padrão: target identifica entidade ("polity:Brasil", "region:Sul gaúcho",
    "relation:Argentina::Brasil"). path navega para o campo dentro da
    entidade ("attributes.stability", "doctrines"). value é o operando.
    op define a operação.
    """

    op: EffectOpType
    target: str
    path: str
    value: Any
    notes: str | None = None


class ScheduledEvent(BaseModel):
    """Evento pré-programado com scripting híbrido.

    Campos estruturados (triggers, cancel_conditions, effects) têm
    prioridade. Quando vazios, o game_master cai no fallback de prosa
    (natural_cancel, natural_effects), legado do formato YAML inicial
    do cenário Brasil-Vargas.
    """

    id: str
    date: date
    trigger_window_days: int = Field(default=30, ge=1)
    category: EventCategoryType
    severity: EventSeverityType = "moderate"
    description: str
    source: str | None = None
    affected_polities: list[str] = Field(default_factory=list)
    affected_regions: list[str] = Field(default_factory=list)

    triggers: list[Trigger] = Field(default_factory=list)
    cancel_conditions: list[CancelCondition] = Field(default_factory=list)
    effects: list[EffectSpec] = Field(default_factory=list)

    natural_cancel: str | None = None
    natural_effects: str | None = None
