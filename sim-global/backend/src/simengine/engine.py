"""Aplicação determinística de deltas e checagem de invariantes globais.

Estas funções são chamadas pelos scripts CLI (`simengine.scripts.*`) e
pelos testes pytest. Todo trabalho é mutação in-place do GameState ou
inspeção pura — nenhuma I/O.
"""
from __future__ import annotations

from .schemas import (
    BattalionCreate,
    BattalionDestroy,
    BattalionMove,
    DiplomaticOpinionChange,
    DiplomaticRelation,
    DiplomaticStatusChange,
    GameState,
    PolityDoctrineAdd,
    PolityDoctrineRemove,
    PolityLeaderChange,
    PolityTensionAdd,
    PolityTensionRemove,
    RegionOwnerChange,
    StateDelta,
    TurnBuffer,
)


# ---------- aplicação de deltas ----------

def apply_delta(state: GameState, delta: StateDelta) -> None:
    """Aplica um único delta ao GameState in-place."""
    if isinstance(delta, RegionOwnerChange):
        _apply_region_owner_change(state, delta)
    elif isinstance(delta, DiplomaticStatusChange):
        _apply_diplomatic_status_change(state, delta)
    elif isinstance(delta, DiplomaticOpinionChange):
        _apply_diplomatic_opinion_change(state, delta)
    elif isinstance(delta, PolityLeaderChange):
        state.polities[delta.polity].leader = delta.new_leader
    elif isinstance(delta, PolityDoctrineAdd):
        doctrines = state.polities[delta.polity].doctrines
        if delta.doctrine not in doctrines:
            doctrines.append(delta.doctrine)
    elif isinstance(delta, PolityDoctrineRemove):
        doctrines = state.polities[delta.polity].doctrines
        if delta.doctrine in doctrines:
            doctrines.remove(delta.doctrine)
    elif isinstance(delta, PolityTensionAdd):
        tensions = state.polities[delta.polity].internal_tensions
        if delta.tension not in tensions:
            tensions.append(delta.tension)
    elif isinstance(delta, PolityTensionRemove):
        tensions = state.polities[delta.polity].internal_tensions
        if delta.tension in tensions:
            tensions.remove(delta.tension)
    elif isinstance(delta, BattalionCreate):
        state.polities[delta.battalion.polity].military_units.append(delta.battalion)
    elif isinstance(delta, BattalionDestroy):
        polity = state.polities[delta.polity]
        polity.military_units = [
            u for u in polity.military_units if u.name != delta.battalion_name
        ]
    elif isinstance(delta, BattalionMove):
        polity = state.polities[delta.polity]
        for unit in polity.military_units:
            if unit.name == delta.battalion_name:
                unit.location_region = delta.new_region
                break
    else:
        raise ValueError(f"tipo de delta desconhecido: {type(delta).__name__}")


def _apply_region_owner_change(state: GameState, delta: RegionOwnerChange) -> None:
    region = state.regions[delta.region]
    old_owner = region.owner
    region.owner = delta.new_owner
    if old_owner and old_owner in state.polities:
        owned = state.polities[old_owner].owned_regions
        if delta.region in owned:
            owned.remove(delta.region)
    if delta.new_owner and delta.new_owner in state.polities:
        owned = state.polities[delta.new_owner].owned_regions
        if delta.region not in owned:
            owned.append(delta.region)


def _apply_diplomatic_status_change(
    state: GameState, delta: DiplomaticStatusChange
) -> None:
    key = DiplomaticRelation.make_key(delta.polity_a, delta.polity_b)
    if key in state.diplomatic_relations:
        state.diplomatic_relations[key].status = delta.new_status
        return
    a, b = sorted([delta.polity_a, delta.polity_b])
    state.diplomatic_relations[key] = DiplomaticRelation(
        polity_a=a,
        polity_b=b,
        status=delta.new_status,
        opinion_a_to_b=0,
        opinion_b_to_a=0,
    )


def _apply_diplomatic_opinion_change(
    state: GameState, delta: DiplomaticOpinionChange
) -> None:
    sorted_a, sorted_b = sorted([delta.polity_a, delta.polity_b])
    swap = delta.polity_a != sorted_a
    key = f"{sorted_a}::{sorted_b}"
    if key not in state.diplomatic_relations:
        state.diplomatic_relations[key] = DiplomaticRelation(
            polity_a=sorted_a,
            polity_b=sorted_b,
            status="paz",
            opinion_a_to_b=0,
            opinion_b_to_a=0,
        )
    rel = state.diplomatic_relations[key]
    inc_ab = delta.delta_b_to_a if swap else delta.delta_a_to_b
    inc_ba = delta.delta_a_to_b if swap else delta.delta_b_to_a
    rel.opinion_a_to_b = _clamp(rel.opinion_a_to_b + inc_ab)
    rel.opinion_b_to_a = _clamp(rel.opinion_b_to_a + inc_ba)


def _clamp(value: int, lo: int = -100, hi: int = 100) -> int:
    return max(lo, min(hi, value))


def apply_turn_buffer(state: GameState, buffer: TurnBuffer) -> None:
    """Aplica todos os deltas do buffer e avança current_date."""
    for delta in buffer.deltas:
        apply_delta(state, delta)
    state.current_date = buffer.turn_end_date


# ---------- invariantes globais ----------

def check_state_invariants(state: GameState) -> list[str]:
    """Retorna lista de violações. Vazia se o estado é íntegro."""
    violations: list[str] = []

    if state.player_polity not in state.polities:
        violations.append(
            f"player_polity {state.player_polity!r} não existe em polities"
        )

    for pname, polity in state.polities.items():
        if polity.capital_region not in state.regions:
            violations.append(
                f"capital de {pname!r} ({polity.capital_region!r}) não existe em regions"
            )
        elif polity.capital_region not in polity.owned_regions:
            violations.append(
                f"capital de {pname!r} ({polity.capital_region!r}) não está em owned_regions"
            )
        for rname in polity.owned_regions:
            if rname not in state.regions:
                violations.append(
                    f"{pname!r} reivindica região inexistente {rname!r}"
                )
            elif state.regions[rname].owner != pname:
                violations.append(
                    f"{pname!r} reivindica {rname!r} mas Region.owner é "
                    f"{state.regions[rname].owner!r}"
                )
        for batt in polity.military_units:
            if batt.polity != pname:
                violations.append(
                    f"battalion {batt.name!r} dentro de {pname!r} declara "
                    f"polity={batt.polity!r}"
                )
            if batt.location_region not in state.regions:
                violations.append(
                    f"battalion {batt.name!r} de {pname!r} aponta para região "
                    f"inexistente {batt.location_region!r}"
                )

    for rname, region in state.regions.items():
        if region.owner is not None and region.owner not in state.polities:
            violations.append(
                f"owner de {rname!r} ({region.owner!r}) não existe em polities"
            )

    for key, rel in state.diplomatic_relations.items():
        expected = f"{rel.polity_a}::{rel.polity_b}"
        if key != expected:
            violations.append(
                f"diplomatic key {key!r} não bate com {expected!r}"
            )
        if rel.polity_a not in state.polities:
            violations.append(
                f"polity_a {rel.polity_a!r} de diplomatic_relations não existe"
            )
        if rel.polity_b not in state.polities:
            violations.append(
                f"polity_b {rel.polity_b!r} de diplomatic_relations não existe"
            )

    return violations


def check_turn_invariants(state: GameState, buffer: TurnBuffer) -> list[str]:
    """Checa coerência do TurnBuffer contra o GameState anterior à aplicação."""
    violations: list[str] = []

    if buffer.turn_end_date < buffer.turn_start_date:
        violations.append(
            f"turn_end_date ({buffer.turn_end_date}) anterior a "
            f"turn_start_date ({buffer.turn_start_date})"
        )

    if buffer.turn_start_date != state.current_date:
        violations.append(
            f"turn_start_date ({buffer.turn_start_date}) não bate com "
            f"state.current_date ({state.current_date})"
        )

    for event in buffer.events:
        if not (buffer.turn_start_date <= event.date <= buffer.turn_end_date):
            violations.append(
                f"evento em {event.date} fora da janela "
                f"[{buffer.turn_start_date}, {buffer.turn_end_date}]: "
                f"{event.description!r}"
            )
        for pname in event.affected_polities:
            if pname not in state.polities:
                violations.append(
                    f"evento {event.description!r} afeta polity inexistente {pname!r}"
                )
        for rname in event.affected_regions:
            if rname not in state.regions:
                violations.append(
                    f"evento {event.description!r} afeta região inexistente {rname!r}"
                )

    for delta in buffer.deltas:
        violations.extend(_check_delta_targets(state, delta))

    return violations


def _check_delta_targets(state: GameState, delta: StateDelta) -> list[str]:
    """Valida que o delta referencia entidades existentes no state."""
    violations: list[str] = []
    name = type(delta).__name__

    if isinstance(delta, RegionOwnerChange):
        if delta.region not in state.regions:
            violations.append(f"{name}: região {delta.region!r} inexistente")
        if delta.new_owner is not None and delta.new_owner not in state.polities:
            violations.append(f"{name}: new_owner {delta.new_owner!r} inexistente")
    elif isinstance(delta, (DiplomaticStatusChange, DiplomaticOpinionChange)):
        if delta.polity_a not in state.polities:
            violations.append(f"{name}: polity_a {delta.polity_a!r} inexistente")
        if delta.polity_b not in state.polities:
            violations.append(f"{name}: polity_b {delta.polity_b!r} inexistente")
        if delta.polity_a == delta.polity_b:
            violations.append(f"{name}: polity_a e polity_b iguais ({delta.polity_a!r})")
    elif isinstance(
        delta,
        (
            PolityLeaderChange,
            PolityDoctrineAdd,
            PolityDoctrineRemove,
            PolityTensionAdd,
            PolityTensionRemove,
        ),
    ):
        if delta.polity not in state.polities:
            violations.append(f"{name}: polity {delta.polity!r} inexistente")
    elif isinstance(delta, BattalionCreate):
        if delta.battalion.polity not in state.polities:
            violations.append(
                f"{name}: polity {delta.battalion.polity!r} inexistente"
            )
        if delta.battalion.location_region not in state.regions:
            violations.append(
                f"{name}: region {delta.battalion.location_region!r} inexistente"
            )
    elif isinstance(delta, BattalionDestroy):
        if delta.polity not in state.polities:
            violations.append(f"{name}: polity {delta.polity!r} inexistente")
    elif isinstance(delta, BattalionMove):
        if delta.polity not in state.polities:
            violations.append(f"{name}: polity {delta.polity!r} inexistente")
        if delta.new_region not in state.regions:
            violations.append(f"{name}: new_region {delta.new_region!r} inexistente")

    return violations
