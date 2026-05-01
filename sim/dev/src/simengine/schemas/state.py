from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from .action import PlayerAction
from .diplomatic import DiplomaticRelation
from .polity import Polity
from .region import Region


class GameState(BaseModel):
    """Estado canônico de uma campanha. Persistido em current_state.json."""

    current_date: date
    player_polity: str
    polities: dict[str, Polity]
    regions: dict[str, Region]
    diplomatic_relations: dict[str, DiplomaticRelation] = Field(default_factory=dict)
    pending_actions: list[PlayerAction] = Field(default_factory=list)
