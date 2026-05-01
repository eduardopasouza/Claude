from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class PlayerAction(BaseModel):
    description: str
    submitted_on: date
    target_polities: list[str] = Field(default_factory=list)
    target_regions: list[str] = Field(default_factory=list)
    category: str | None = None
