"""Mutações discretas aplicáveis ao GameState.

Cada subtipo de delta tem um campo `type` literal que serve como
discriminador. Pydantic resolve a deserialização via
Annotated[Union, Field(discriminator="type")].
"""
from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from .common import DiplomaticStatusType
from .polity import Battalion


class RegionOwnerChange(BaseModel):
    type: Literal["region_owner_change"] = "region_owner_change"
    region: str
    new_owner: str | None = None


class DiplomaticStatusChange(BaseModel):
    type: Literal["diplomatic_status_change"] = "diplomatic_status_change"
    polity_a: str
    polity_b: str
    new_status: DiplomaticStatusType


class DiplomaticOpinionChange(BaseModel):
    type: Literal["diplomatic_opinion_change"] = "diplomatic_opinion_change"
    polity_a: str
    polity_b: str
    delta_a_to_b: int = 0
    delta_b_to_a: int = 0


class PolityLeaderChange(BaseModel):
    type: Literal["polity_leader_change"] = "polity_leader_change"
    polity: str
    new_leader: str


class PolityDoctrineAdd(BaseModel):
    type: Literal["polity_doctrine_add"] = "polity_doctrine_add"
    polity: str
    doctrine: str


class PolityDoctrineRemove(BaseModel):
    type: Literal["polity_doctrine_remove"] = "polity_doctrine_remove"
    polity: str
    doctrine: str


class PolityTensionAdd(BaseModel):
    type: Literal["polity_tension_add"] = "polity_tension_add"
    polity: str
    tension: str


class PolityTensionRemove(BaseModel):
    type: Literal["polity_tension_remove"] = "polity_tension_remove"
    polity: str
    tension: str


class BattalionCreate(BaseModel):
    type: Literal["battalion_create"] = "battalion_create"
    battalion: Battalion


class BattalionDestroy(BaseModel):
    type: Literal["battalion_destroy"] = "battalion_destroy"
    battalion_name: str
    polity: str


class BattalionMove(BaseModel):
    type: Literal["battalion_move"] = "battalion_move"
    battalion_name: str
    polity: str
    new_region: str


StateDelta = Annotated[
    Union[
        RegionOwnerChange,
        DiplomaticStatusChange,
        DiplomaticOpinionChange,
        PolityLeaderChange,
        PolityDoctrineAdd,
        PolityDoctrineRemove,
        PolityTensionAdd,
        PolityTensionRemove,
        BattalionCreate,
        BattalionDestroy,
        BattalionMove,
    ],
    Field(discriminator="type"),
]
