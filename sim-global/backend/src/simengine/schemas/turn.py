from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from .delta import StateDelta
from .event import Event


class TurnBuffer(BaseModel):
    """Saída transitória do Skill simulator. Validada antes de aplicar."""

    turn_start_date: date
    turn_end_date: date
    events: list[Event] = Field(default_factory=list)
    deltas: list[StateDelta] = Field(default_factory=list)
    narrative: str
