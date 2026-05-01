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


class PolityAttributes(BaseModel):
    """Atributos quantitativos da Polity (inspirado em PaxHistoria)."""

    stability: int = Field(default=50, ge=0, le=100)
    war_support: int = Field(default=50, ge=0, le=100)
    treasury: int = 0
    manpower: int = Field(default=0, ge=0)
    political_power: int = 0


class Polity(BaseModel):
    name: str
    government_type: str
    leader: str
    capital_region: str
    owned_regions: list[str] = Field(default_factory=list)
    military_units: list[Battalion] = Field(default_factory=list)
    doctrines: list[str] = Field(default_factory=list)
    internal_tensions: list[str] = Field(default_factory=list)
    attributes: PolityAttributes = Field(default_factory=PolityAttributes)
