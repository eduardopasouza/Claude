from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from .common import DiplomaticStatusType


class DiplomaticRelation(BaseModel):
    """Relação bilateral entre duas polities. polity_a < polity_b alfabeticamente."""

    polity_a: str
    polity_b: str
    status: DiplomaticStatusType
    opinion_a_to_b: int = Field(ge=-100, le=100)
    opinion_b_to_a: int = Field(ge=-100, le=100)
    treaties: list[str] = Field(default_factory=list)
    notes: str | None = None

    @model_validator(mode="after")
    def _check_polity_order(self) -> DiplomaticRelation:
        if self.polity_a >= self.polity_b:
            raise ValueError(
                "polity_a deve ser alfabeticamente menor que polity_b "
                f"(recebido: {self.polity_a!r} >= {self.polity_b!r})"
            )
        return self

    @staticmethod
    def make_key(polity_a: str, polity_b: str) -> str:
        a, b = sorted([polity_a, polity_b])
        return f"{a}::{b}"
