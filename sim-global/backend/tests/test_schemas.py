"""Cobertura dos schemas: round-trip JSON, validações de campo, discriminated union."""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import TypeAdapter, ValidationError

from simengine.schemas import (
    Battalion,
    BattalionCreate,
    BattalionMove,
    ConsolidatedSummary,
    DiplomaticOpinionChange,
    DiplomaticRelation,
    DiplomaticStatusChange,
    Event,
    GameState,
    MapFeature,
    PlayerAction,
    Polity,
    PolityDoctrineAdd,
    Region,
    RegionOwnerChange,
    StateDelta,
    TurnBuffer,
)


# ---- region / map feature ----

def test_region_round_trip():
    region = Region(
        name="São Paulo cafeeiro",
        type="land",
        owner="Brasil",
        population_estimate_thousands=8000,
        economic_profile="café exportador",
        features=[MapFeature(name="São Paulo", type="cidade", level=5)],
    )
    assert Region.model_validate_json(region.model_dump_json()) == region


@pytest.mark.parametrize("level", [0, 6, -1, 100])
def test_map_feature_level_out_of_range(level: int):
    with pytest.raises(ValidationError):
        MapFeature(name="x", type="cidade", level=level)


def test_region_negative_population_rejected():
    with pytest.raises(ValidationError):
        Region(
            name="x",
            type="land",
            population_estimate_thousands=-1,
            economic_profile="?",
        )


# ---- polity / battalion ----

def test_battalion_strength_bounds():
    Battalion(
        name="1º BC",
        polity="Brasil",
        location_region="Rio-Vale do Paraíba",
        type="infantaria",
        strength=0,
    )
    Battalion(
        name="1º BC",
        polity="Brasil",
        location_region="Rio-Vale do Paraíba",
        type="infantaria",
        strength=100,
    )
    with pytest.raises(ValidationError):
        Battalion(
            name="1º BC",
            polity="Brasil",
            location_region="Rio-Vale do Paraíba",
            type="infantaria",
            strength=101,
        )


def test_polity_default_status_pronto():
    b = Battalion(
        name="1º BC",
        polity="Brasil",
        location_region="Rio-Vale do Paraíba",
        type="infantaria",
        strength=50,
    )
    assert b.status == "pronto"


# ---- diplomatic ----

def test_diplomatic_relation_requires_alpha_order():
    DiplomaticRelation(
        polity_a="Argentina",
        polity_b="Brasil",
        status="paz",
        opinion_a_to_b=10,
        opinion_b_to_a=5,
    )
    with pytest.raises(ValidationError):
        DiplomaticRelation(
            polity_a="Brasil",
            polity_b="Argentina",
            status="paz",
            opinion_a_to_b=10,
            opinion_b_to_a=5,
        )


def test_diplomatic_relation_rejects_self_pair():
    with pytest.raises(ValidationError):
        DiplomaticRelation(
            polity_a="Brasil",
            polity_b="Brasil",
            status="paz",
            opinion_a_to_b=0,
            opinion_b_to_a=0,
        )


def test_diplomatic_relation_make_key_is_sorted():
    assert DiplomaticRelation.make_key("Brasil", "Argentina") == "Argentina::Brasil"
    assert DiplomaticRelation.make_key("Argentina", "Brasil") == "Argentina::Brasil"


@pytest.mark.parametrize("opinion", [-101, 101, -200, 200])
def test_diplomatic_opinion_out_of_range(opinion: int):
    with pytest.raises(ValidationError):
        DiplomaticRelation(
            polity_a="Argentina",
            polity_b="Brasil",
            status="paz",
            opinion_a_to_b=opinion,
            opinion_b_to_a=0,
        )


# ---- event / consolidated summary ----

def test_event_round_trip():
    event = Event(
        date=date(1932, 7, 9),
        category="internal",
        description="Eclode a Revolução Constitucionalista em São Paulo.",
        affected_polities=["Brasil"],
        affected_regions=["São Paulo cafeeiro"],
        caused_by="scheduled",
    )
    assert Event.model_validate_json(event.model_dump_json()) == event


def test_consolidated_summary_round_trip():
    summary = ConsolidatedSummary(
        period_start=date(1930, 11, 3),
        period_end=date(1932, 6, 30),
        key_events=["Posse de Vargas", "Reforma educacional"],
        state_changes_summary="Centralização administrativa avança.",
        emerging_tensions=["Oposição paulista crescente"],
        generated_at=date(1932, 7, 1),
    )
    assert ConsolidatedSummary.model_validate_json(summary.model_dump_json()) == summary


# ---- player action ----

def test_player_action_minimal():
    action = PlayerAction(
        description="Nacionalizar produção de petróleo",
        submitted_on=date(1933, 1, 15),
    )
    assert action.target_polities == []
    assert action.category is None


# ---- state delta discriminated union ----

def test_state_delta_region_owner_change_round_trip():
    adapter: TypeAdapter[StateDelta] = TypeAdapter(StateDelta)
    raw = (
        '{"type": "region_owner_change", "region": "Acre", "new_owner": "Brasil"}'
    )
    delta = adapter.validate_json(raw)
    assert isinstance(delta, RegionOwnerChange)
    assert delta.region == "Acre"
    assert delta.new_owner == "Brasil"


def test_state_delta_diplomatic_status_change_round_trip():
    adapter: TypeAdapter[StateDelta] = TypeAdapter(StateDelta)
    raw = (
        '{"type": "diplomatic_status_change", "polity_a": "Brasil",'
        ' "polity_b": "Alemanha", "new_status": "guerra"}'
    )
    delta = adapter.validate_json(raw)
    assert isinstance(delta, DiplomaticStatusChange)
    assert delta.new_status == "guerra"


def test_state_delta_battalion_create_nested_validation():
    adapter: TypeAdapter[StateDelta] = TypeAdapter(StateDelta)
    raw = (
        '{"type": "battalion_create", "battalion": {'
        '"name": "FEB-1", "polity": "Brasil",'
        ' "location_region": "Rio-Vale do Paraíba",'
        ' "type": "infantaria", "strength": 80}}'
    )
    delta = adapter.validate_json(raw)
    assert isinstance(delta, BattalionCreate)
    assert delta.battalion.name == "FEB-1"


def test_state_delta_unknown_type_rejected():
    adapter: TypeAdapter[StateDelta] = TypeAdapter(StateDelta)
    raw = '{"type": "magic_change", "foo": "bar"}'
    with pytest.raises(ValidationError):
        adapter.validate_json(raw)


# ---- turn buffer ----

def test_turn_buffer_round_trip_with_mixed_deltas():
    buffer = TurnBuffer(
        turn_start_date=date(1930, 11, 3),
        turn_end_date=date(1931, 5, 3),
        events=[
            Event(
                date=date(1931, 1, 10),
                category="internal",
                description="Vargas centraliza interventorias.",
                affected_polities=["Brasil"],
                affected_regions=[],
                caused_by="scheduled",
            )
        ],
        deltas=[
            PolityDoctrineAdd(polity="Brasil", doctrine="centralismo administrativo"),
            DiplomaticOpinionChange(
                polity_a="Argentina",
                polity_b="Brasil",
                delta_a_to_b=-3,
                delta_b_to_a=-1,
            ),
            BattalionMove(
                battalion_name="1º BC",
                polity="Brasil",
                new_region="São Paulo cafeeiro",
            ),
        ],
        narrative="Os primeiros meses do governo provisório consolidam poder no Catete.",
    )
    j = buffer.model_dump_json()
    buffer2 = TurnBuffer.model_validate_json(j)
    assert buffer == buffer2


# ---- game state ----

def test_game_state_minimal_round_trip():
    state = GameState(
        current_date=date(1930, 11, 3),
        player_polity="Brasil",
        polities={
            "Brasil": Polity(
                name="Brasil",
                government_type="Governo Provisório",
                leader="Getúlio Vargas",
                capital_region="Rio-Vale do Paraíba",
                owned_regions=["Rio-Vale do Paraíba", "São Paulo cafeeiro"],
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
    assert GameState.model_validate_json(state.model_dump_json()) == state
