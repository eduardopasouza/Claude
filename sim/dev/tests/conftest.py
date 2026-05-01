"""Fixtures compartilhadas pelos testes."""
from __future__ import annotations

from datetime import date

import pytest

from simengine.schemas import (
    Battalion,
    DiplomaticRelation,
    GameState,
    Polity,
    Region,
)


@pytest.fixture
def base_state() -> GameState:
    """GameState mínimo coerente: Brasil + Argentina, 3 regiões."""
    return GameState(
        current_date=date(1930, 11, 3),
        player_polity="Brasil",
        polities={
            "Brasil": Polity(
                name="Brasil",
                government_type="Governo Provisório",
                leader="Getúlio Vargas",
                capital_region="Rio-Vale do Paraíba",
                owned_regions=["Rio-Vale do Paraíba", "São Paulo cafeeiro"],
                military_units=[
                    Battalion(
                        name="1º BC",
                        polity="Brasil",
                        location_region="Rio-Vale do Paraíba",
                        type="infantaria",
                        strength=60,
                    )
                ],
            ),
            "Argentina": Polity(
                name="Argentina",
                government_type="República presidencialista",
                leader="José Félix Uriburu",
                capital_region="Buenos Aires",
                owned_regions=["Buenos Aires"],
            ),
        },
        regions={
            "Rio-Vale do Paraíba": Region(
                name="Rio-Vale do Paraíba",
                type="coastal",
                owner="Brasil",
                population_estimate_thousands=2500,
                economic_profile="industrial-administrativo",
            ),
            "São Paulo cafeeiro": Region(
                name="São Paulo cafeeiro",
                type="coastal",
                owner="Brasil",
                population_estimate_thousands=8000,
                economic_profile="café exportador",
            ),
            "Buenos Aires": Region(
                name="Buenos Aires",
                type="coastal",
                owner="Argentina",
                population_estimate_thousands=2300,
                economic_profile="agroexportador",
            ),
        },
        diplomatic_relations={
            "Argentina::Brasil": DiplomaticRelation(
                polity_a="Argentina",
                polity_b="Brasil",
                status="paz",
                opinion_a_to_b=10,
                opinion_b_to_a=5,
            )
        },
    )
