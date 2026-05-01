from __future__ import annotations

from pydantic import BaseModel, Field

from .common import MapFeatureType, RegionGeoType


class MapFeature(BaseModel):
    name: str
    type: MapFeatureType
    level: int = Field(ge=1, le=5)
    notes: str | None = None


class Region(BaseModel):
    name: str
    type: RegionGeoType
    owner: str | None = None
    population_estimate_thousands: int = Field(ge=0)
    economic_profile: str
    features: list[MapFeature] = Field(default_factory=list)
