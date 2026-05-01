from __future__ import annotations

from pydantic import BaseModel, Field

from .common import BattalionStatusType, BattalionType


class Battalion(BaseModel):
    name: str
    polity: str
    location_region: str
    type: BattalionType
    strength: int = Field(ge=0, le=100)
    status: BattalionStatusType = "pronto"


class Polity(BaseModel):
    name: str
    government_type: str
    leader: str
    capital_region: str
    owned_regions: list[str] = Field(default_factory=list)
    military_units: list[Battalion] = Field(default_factory=list)
    doctrines: list[str] = Field(default_factory=list)
    internal_tensions: list[str] = Field(default_factory=list)
