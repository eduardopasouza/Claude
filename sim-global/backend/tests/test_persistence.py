"""Cobertura da camada de persistência (SQLAlchemy + repositórios)."""
from __future__ import annotations

from datetime import date

import pytest

from simengine.schemas import (
    Event,
    MapFeature,
    Region,
    RegionOwnerChange,
    TurnBuffer,
)
from simglobal.persistence import (
    CampaignAlreadyExistsError,
    apply_turn_buffer,
    delete_campaign,
    drop_db,
    events_since_summary,
    export_game_state,
    get_session,
    import_game_state,
    init_db,
    list_campaigns,
    make_engine,
    make_session_factory,
    record_scheduled_event_fired,
)
from simglobal.persistence.models import (
    Campaign,
    ConsolidatedSummary,
    DiplomaticRelation,
    Polity,
    Region as RegionORM,
)


# ---------- fixtures ----------


@pytest.fixture
def session_factory():
    """SQLite in-memory engine + factory; recriado a cada teste."""
    engine = make_engine("sqlite:///:memory:")
    init_db(engine)
    factory = make_session_factory(engine)
    yield factory
    drop_db(engine)
    engine.dispose()


# ---------- import / export ----------


def test_import_game_state_creates_campaign_and_entities(
    session_factory, base_state
):
    with get_session(session_factory) as s:
        campaign = import_game_state(s, "vargas-1930", base_state)
        assert campaign.id is not None
        assert campaign.name == "vargas-1930"
        assert campaign.player_polity_name == "Brasil"

    with get_session(session_factory) as s:
        loaded = s.query(Campaign).filter_by(name="vargas-1930").one()
        assert len(loaded.polities) == len(base_state.polities) == 2
        assert len(loaded.regions) == len(base_state.regions) == 3
        assert len(loaded.diplomatic_relations) == len(
            base_state.diplomatic_relations
        ) == 1
        # batallions atravessam polity → campaign
        battalions = [b for p in loaded.polities for b in p.battalions]
        assert len(battalions) == 1
        assert battalions[0].name == "1º BC"


def test_export_game_state_round_trip(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "vargas-1930", base_state)

    with get_session(session_factory) as s:
        exported = export_game_state(s, "vargas-1930")

    # Comparação a nível Pydantic dump (mode="json" para data como str).
    assert exported.current_date == base_state.current_date
    assert exported.player_polity == base_state.player_polity
    assert set(exported.polities.keys()) == set(base_state.polities.keys())
    assert set(exported.regions.keys()) == set(base_state.regions.keys())
    assert set(exported.diplomatic_relations.keys()) == set(
        base_state.diplomatic_relations.keys()
    )

    # Detalhe de polity preservado: doctrines, tensions, attributes default.
    brasil_in = base_state.polities["Brasil"]
    brasil_out = exported.polities["Brasil"]
    assert brasil_out.leader == brasil_in.leader
    assert brasil_out.capital_region == brasil_in.capital_region
    assert sorted(brasil_out.owned_regions) == sorted(brasil_in.owned_regions)
    assert brasil_out.attributes.stability == brasil_in.attributes.stability
    assert len(brasil_out.military_units) == 1
    assert brasil_out.military_units[0].polity == "Brasil"


def test_export_preserves_map_features(session_factory, base_state):
    base_state.regions["Rio-Vale do Paraíba"].features.append(
        MapFeature(name="Porto do Rio", type="porto", level=4, notes="entreposto")
    )
    with get_session(session_factory) as s:
        import_game_state(s, "feat-test", base_state)
    with get_session(session_factory) as s:
        exported = export_game_state(s, "feat-test")
    feats = exported.regions["Rio-Vale do Paraíba"].features
    assert len(feats) == 1
    assert feats[0].name == "Porto do Rio"
    assert feats[0].type == "porto"
    assert feats[0].level == 4
    assert feats[0].notes == "entreposto"


# ---------- listagem / deleção ----------


def test_list_campaigns(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "alpha", base_state)
        import_game_state(s, "beta", base_state)

    with get_session(session_factory) as s:
        names = [c.name for c in list_campaigns(s)]
    assert names == ["alpha", "beta"]


def test_delete_campaign_cascades(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "to-delete", base_state)

    with get_session(session_factory) as s:
        delete_campaign(s, "to-delete")

    with get_session(session_factory) as s:
        assert s.query(Campaign).count() == 0
        assert s.query(Polity).count() == 0
        assert s.query(RegionORM).count() == 0
        assert s.query(DiplomaticRelation).count() == 0


def test_import_duplicate_name_raises(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "dup", base_state)

    with pytest.raises(CampaignAlreadyExistsError):
        with get_session(session_factory) as s:
            import_game_state(s, "dup", base_state)

    # Garante que nenhuma alteração colateral foi persistida.
    with get_session(session_factory) as s:
        assert s.query(Campaign).count() == 1


# ---------- apply_turn_buffer ----------


def test_apply_turn_buffer_updates_state(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "turn-test", base_state)
        # Adiciona uma pending_action para confirmar que é limpa.
        from simglobal.persistence.models import PendingAction

        s.add(
            PendingAction(
                campaign_id=s.query(Campaign).one().id,
                description="apenas para limpar",
                submitted_on=date(1930, 11, 3),
            )
        )

    buffer = TurnBuffer(
        turn_start_date=date(1930, 11, 3),
        turn_end_date=date(1930, 12, 3),
        events=[
            Event(
                date=date(1930, 11, 15),
                category="diplomatic",
                description="Reconhecimento internacional do governo Vargas",
                affected_polities=["Brasil", "EUA"],
                caused_by="emergent",
                severity="moderate",
            ),
            Event(
                date=date(1930, 11, 28),
                category="internal",
                description="Decreto presidencial nº 19.398",
                affected_polities=["Brasil"],
                caused_by="player_action",
                severity="major",
            ),
        ],
        deltas=[
            RegionOwnerChange(
                region="São Paulo cafeeiro", new_owner="Argentina"
            )
        ],
        narrative="primeiro mês",
    )

    with get_session(session_factory) as s:
        new_state = apply_turn_buffer(s, "turn-test", buffer)

    assert new_state.current_date == date(1930, 12, 3)
    assert new_state.regions["São Paulo cafeeiro"].owner == "Argentina"
    assert "São Paulo cafeeiro" in new_state.polities["Argentina"].owned_regions

    with get_session(session_factory) as s:
        campaign = s.query(Campaign).one()
        assert campaign.current_date == date(1930, 12, 3)
        assert len(campaign.events) == 2
        assert len(campaign.pending_actions) == 0
        assert {e.description for e in campaign.events} == {
            "Reconhecimento internacional do governo Vargas",
            "Decreto presidencial nº 19.398",
        }


# ---------- scheduled events ----------


def test_record_scheduled_event_fired_idempotent(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "sched", base_state)

    with get_session(session_factory) as s:
        first = record_scheduled_event_fired(
            s, "sched", "constituicao_1934", date(1934, 7, 16)
        )
    with get_session(session_factory) as s:
        second = record_scheduled_event_fired(
            s, "sched", "constituicao_1934", date(1934, 7, 16)
        )

    assert first is True
    assert second is False

    from simglobal.persistence.models import ScheduledEventFire

    with get_session(session_factory) as s:
        rows = s.query(ScheduledEventFire).all()
    assert len(rows) == 1
    assert rows[0].event_id == "constituicao_1934"


# ---------- consolidação ----------


def test_events_since_summary_counts_after_last_summary(
    session_factory, base_state
):
    with get_session(session_factory) as s:
        import_game_state(s, "consol", base_state)
        campaign_id = s.query(Campaign).one().id

    # Cria 5 eventos antes do summary, 3 depois.
    from simglobal.persistence.models import (
        ConsolidatedSummary as ConsolORM,
    )
    from simglobal.persistence.models import Event as EventORM

    with get_session(session_factory) as s:
        for i in range(5):
            s.add(
                EventORM(
                    campaign_id=campaign_id,
                    date=date(1930, 11, 1 + i),
                    category="internal",
                    description=f"pre-summary {i}",
                    severity="minor",
                    caused_by="emergent",
                )
            )
        s.add(
            ConsolORM(
                campaign_id=campaign_id,
                period_start=date(1930, 11, 1),
                period_end=date(1930, 11, 10),
                state_changes_summary="resumo",
                generated_at=date(1930, 11, 11),
            )
        )
        for i in range(3):
            s.add(
                EventORM(
                    campaign_id=campaign_id,
                    date=date(1930, 11, 15 + i),
                    category="internal",
                    description=f"post-summary {i}",
                    severity="minor",
                    caused_by="emergent",
                )
            )

    with get_session(session_factory) as s:
        count = events_since_summary(s, "consol")
    assert count == 3


def test_events_since_summary_no_summary_counts_all(session_factory, base_state):
    with get_session(session_factory) as s:
        import_game_state(s, "no-sum", base_state)
        campaign_id = s.query(Campaign).one().id

        from simglobal.persistence.models import Event as EventORM

        for i in range(4):
            s.add(
                EventORM(
                    campaign_id=campaign_id,
                    date=date(1930, 11, 1 + i),
                    category="internal",
                    description=f"e{i}",
                    severity="minor",
                    caused_by="emergent",
                )
            )

    with get_session(session_factory) as s:
        assert events_since_summary(s, "no-sum") == 4
