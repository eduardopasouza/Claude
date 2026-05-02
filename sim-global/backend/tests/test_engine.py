"""Cobertura do engine: apply_delta, apply_turn_buffer, invariantes."""
from __future__ import annotations

from datetime import date

import pytest

from simengine.engine import (
    apply_delta,
    apply_turn_buffer,
    check_state_invariants,
    check_turn_invariants,
)
from simengine.schemas import (
    Battalion,
    BattalionCreate,
    BattalionDestroy,
    BattalionMove,
    DiplomaticOpinionChange,
    DiplomaticRelation,
    DiplomaticStatusChange,
    Event,
    PolityDoctrineAdd,
    PolityDoctrineRemove,
    PolityLeaderChange,
    PolityTensionAdd,
    PolityTensionRemove,
    RegionOwnerChange,
    TurnBuffer,
)


# ---------- apply_delta ----------

def test_region_owner_change_transfers_ownership(base_state):
    apply_delta(
        base_state,
        RegionOwnerChange(region="São Paulo cafeeiro", new_owner="Argentina"),
    )
    assert base_state.regions["São Paulo cafeeiro"].owner == "Argentina"
    assert "São Paulo cafeeiro" not in base_state.polities["Brasil"].owned_regions
    assert "São Paulo cafeeiro" in base_state.polities["Argentina"].owned_regions


def test_region_owner_change_to_none(base_state):
    apply_delta(
        base_state, RegionOwnerChange(region="São Paulo cafeeiro", new_owner=None)
    )
    assert base_state.regions["São Paulo cafeeiro"].owner is None
    assert "São Paulo cafeeiro" not in base_state.polities["Brasil"].owned_regions


def test_diplomatic_status_change_existing_relation(base_state):
    apply_delta(
        base_state,
        DiplomaticStatusChange(
            polity_a="Brasil", polity_b="Argentina", new_status="ruptura"
        ),
    )
    rel = base_state.diplomatic_relations["Argentina::Brasil"]
    assert rel.status == "ruptura"


def test_diplomatic_status_change_creates_new_relation(base_state):
    base_state.polities["Alemanha"] = base_state.polities["Argentina"].model_copy(
        update={"name": "Alemanha", "leader": "x", "owned_regions": [], "capital_region": "Berlim"}
    )
    apply_delta(
        base_state,
        DiplomaticStatusChange(
            polity_a="Brasil", polity_b="Alemanha", new_status="guerra"
        ),
    )
    key = DiplomaticRelation.make_key("Brasil", "Alemanha")
    assert base_state.diplomatic_relations[key].status == "guerra"
    assert base_state.diplomatic_relations[key].opinion_a_to_b == 0


def test_diplomatic_opinion_change_with_swap(base_state):
    apply_delta(
        base_state,
        DiplomaticOpinionChange(
            polity_a="Brasil",
            polity_b="Argentina",
            delta_a_to_b=20,
            delta_b_to_a=10,
        ),
    )
    rel = base_state.diplomatic_relations["Argentina::Brasil"]
    # rel está em ordem (Argentina, Brasil); o delta veio em (Brasil, Argentina).
    # Opinião Argentina->Brasil (rel.opinion_a_to_b) é incrementada por delta_b_to_a.
    assert rel.opinion_a_to_b == 10 + 10
    # Opinião Brasil->Argentina (rel.opinion_b_to_a) é incrementada por delta_a_to_b.
    assert rel.opinion_b_to_a == 5 + 20


def test_diplomatic_opinion_change_clamps_at_100(base_state):
    apply_delta(
        base_state,
        DiplomaticOpinionChange(
            polity_a="Argentina",
            polity_b="Brasil",
            delta_a_to_b=200,
            delta_b_to_a=-500,
        ),
    )
    rel = base_state.diplomatic_relations["Argentina::Brasil"]
    assert rel.opinion_a_to_b == 100
    assert rel.opinion_b_to_a == -100


def test_polity_leader_change(base_state):
    apply_delta(
        base_state,
        PolityLeaderChange(polity="Brasil", new_leader="Eurico Gaspar Dutra"),
    )
    assert base_state.polities["Brasil"].leader == "Eurico Gaspar Dutra"


def test_polity_doctrine_add_idempotent(base_state):
    apply_delta(base_state, PolityDoctrineAdd(polity="Brasil", doctrine="trabalhismo"))
    apply_delta(base_state, PolityDoctrineAdd(polity="Brasil", doctrine="trabalhismo"))
    assert base_state.polities["Brasil"].doctrines.count("trabalhismo") == 1


def test_polity_doctrine_remove_when_absent_is_noop(base_state):
    apply_delta(
        base_state, PolityDoctrineRemove(polity="Brasil", doctrine="inexistente")
    )
    assert "inexistente" not in base_state.polities["Brasil"].doctrines


def test_polity_tension_add_and_remove(base_state):
    apply_delta(
        base_state, PolityTensionAdd(polity="Brasil", tension="oposição paulista")
    )
    assert "oposição paulista" in base_state.polities["Brasil"].internal_tensions
    apply_delta(
        base_state, PolityTensionRemove(polity="Brasil", tension="oposição paulista")
    )
    assert "oposição paulista" not in base_state.polities["Brasil"].internal_tensions


def test_battalion_create(base_state):
    new_batt = Battalion(
        name="2º BC",
        polity="Brasil",
        location_region="São Paulo cafeeiro",
        type="cavalaria",
        strength=40,
    )
    apply_delta(base_state, BattalionCreate(battalion=new_batt))
    names = [u.name for u in base_state.polities["Brasil"].military_units]
    assert "2º BC" in names


def test_battalion_destroy(base_state):
    apply_delta(
        base_state, BattalionDestroy(battalion_name="1º BC", polity="Brasil")
    )
    assert base_state.polities["Brasil"].military_units == []


def test_battalion_move(base_state):
    apply_delta(
        base_state,
        BattalionMove(
            battalion_name="1º BC",
            polity="Brasil",
            new_region="São Paulo cafeeiro",
        ),
    )
    unit = base_state.polities["Brasil"].military_units[0]
    assert unit.location_region == "São Paulo cafeeiro"


# ---------- apply_turn_buffer ----------

def test_apply_turn_buffer_advances_current_date(base_state):
    buffer = TurnBuffer(
        turn_start_date=base_state.current_date,
        turn_end_date=date(1931, 5, 3),
        events=[],
        deltas=[PolityLeaderChange(polity="Brasil", new_leader="Outro")],
        narrative="...",
    )
    apply_turn_buffer(base_state, buffer)
    assert base_state.current_date == date(1931, 5, 3)
    assert base_state.polities["Brasil"].leader == "Outro"


# ---------- check_state_invariants ----------

def test_state_invariants_clean_state_has_no_violations(base_state):
    assert check_state_invariants(base_state) == []


def test_state_invariants_detects_player_polity_missing(base_state):
    base_state.player_polity = "Inexistente"
    violations = check_state_invariants(base_state)
    assert any("player_polity" in v for v in violations)


def test_state_invariants_detects_capital_not_owned(base_state):
    base_state.polities["Brasil"].owned_regions = ["São Paulo cafeeiro"]
    violations = check_state_invariants(base_state)
    assert any("capital" in v for v in violations)


def test_state_invariants_detects_battalion_in_unknown_region(base_state):
    base_state.polities["Brasil"].military_units[0].location_region = "Lua"
    violations = check_state_invariants(base_state)
    assert any("Lua" in v for v in violations)


def test_state_invariants_detects_diplomatic_key_mismatch(base_state):
    base_state.diplomatic_relations["WRONG_KEY"] = (
        base_state.diplomatic_relations.pop("Argentina::Brasil")
    )
    violations = check_state_invariants(base_state)
    assert any("WRONG_KEY" in v for v in violations)


# ---------- check_turn_invariants ----------

def _make_buffer(start, end, deltas=(), events=()):
    return TurnBuffer(
        turn_start_date=start,
        turn_end_date=end,
        deltas=list(deltas),
        events=list(events),
        narrative="x",
    )


def test_turn_invariants_clean_buffer_passes(base_state):
    buffer = _make_buffer(
        base_state.current_date, date(1931, 5, 3),
        deltas=[PolityLeaderChange(polity="Brasil", new_leader="X")],
        events=[
            Event(
                date=date(1931, 1, 1),
                category="internal",
                description="Algo",
                affected_polities=["Brasil"],
                affected_regions=["Rio-Vale do Paraíba"],
                caused_by="emergent",
            )
        ],
    )
    assert check_turn_invariants(base_state, buffer) == []


def test_turn_invariants_rejects_end_before_start(base_state):
    buffer = _make_buffer(date(1931, 5, 3), date(1930, 11, 3))
    violations = check_turn_invariants(base_state, buffer)
    assert any("anterior" in v for v in violations)


def test_turn_invariants_rejects_start_mismatch(base_state):
    buffer = _make_buffer(date(1932, 1, 1), date(1932, 6, 1))
    violations = check_turn_invariants(base_state, buffer)
    assert any("turn_start_date" in v for v in violations)


def test_turn_invariants_rejects_event_outside_window(base_state):
    buffer = _make_buffer(
        base_state.current_date,
        date(1931, 5, 3),
        events=[
            Event(
                date=date(1932, 1, 1),
                category="internal",
                description="fora da janela",
                affected_polities=["Brasil"],
                affected_regions=[],
                caused_by="emergent",
            )
        ],
    )
    violations = check_turn_invariants(base_state, buffer)
    assert any("fora da janela" in v for v in violations)


def test_turn_invariants_rejects_delta_with_unknown_polity(base_state):
    buffer = _make_buffer(
        base_state.current_date,
        date(1931, 5, 3),
        deltas=[PolityLeaderChange(polity="Atlântida", new_leader="X")],
    )
    violations = check_turn_invariants(base_state, buffer)
    assert any("Atlântida" in v for v in violations)


def test_turn_invariants_rejects_self_diplomatic_pair(base_state):
    buffer = _make_buffer(
        base_state.current_date,
        date(1931, 5, 3),
        deltas=[
            DiplomaticStatusChange(
                polity_a="Brasil", polity_b="Brasil", new_status="paz"
            )
        ],
    )
    violations = check_turn_invariants(base_state, buffer)
    assert any("iguais" in v for v in violations)
