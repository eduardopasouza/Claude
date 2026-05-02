from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator

from .common import EventCategoryType, EventCauseType, EventSeverityType


_CATEGORY_VALID = {
    "diplomatic", "military", "internal", "economic", "natural",
    "cultural", "social", "religious", "technological",
    "scientific", "demographic", "environmental",
}
_SEVERITY_VALID = {"minor", "moderate", "major", "critical"}
_CAUSE_VALID = {"player_action", "scheduled", "emergent"}


class Event(BaseModel):
    """Aceita str em category/severity/caused_by; normaliza desconhecidos.

    Mantém os tipos como str (não Literal) para resiliência: se o
    LLM gerar uma categoria não prevista (ex.: 'cultural' antes de
    constar no enum), o evento ainda entra com fallback em vez de
    derrubar o turno inteiro.
    """

    date: date
    category: str
    description: str
    affected_polities: list[str] = Field(default_factory=list)
    affected_regions: list[str] = Field(default_factory=list)
    caused_by: str
    severity: str = "moderate"

    @field_validator("category", mode="before")
    @classmethod
    def _norm_category(cls, v):
        if not isinstance(v, str):
            return "internal"
        v_low = v.lower().strip()
        return v_low if v_low in _CATEGORY_VALID else "internal"

    @field_validator("severity", mode="before")
    @classmethod
    def _norm_severity(cls, v):
        if not isinstance(v, str):
            return "moderate"
        v_low = v.lower().strip()
        return v_low if v_low in _SEVERITY_VALID else "moderate"

    @field_validator("caused_by", mode="before")
    @classmethod
    def _norm_cause(cls, v):
        if not isinstance(v, str):
            return "emergent"
        v_low = v.lower().strip()
        return v_low if v_low in _CAUSE_VALID else "emergent"


class ConsolidatedSummary(BaseModel):
    period_start: date
    period_end: date
    key_events: list[str] = Field(default_factory=list)
    state_changes_summary: str
    emerging_tensions: list[str] = Field(default_factory=list)
    generated_at: date
