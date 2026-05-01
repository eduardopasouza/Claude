from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from .common import EventCategoryType, EventCauseType


class Event(BaseModel):
    date: date
    category: EventCategoryType
    description: str
    affected_polities: list[str] = Field(default_factory=list)
    affected_regions: list[str] = Field(default_factory=list)
    caused_by: EventCauseType


class ConsolidatedSummary(BaseModel):
    period_start: date
    period_end: date
    key_events: list[str] = Field(default_factory=list)
    state_changes_summary: str
    emerging_tensions: list[str] = Field(default_factory=list)
    generated_at: date
