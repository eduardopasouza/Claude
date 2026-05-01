"""Repositórios: fronteira entre o domínio Pydantic (simengine.schemas) e
o ORM SQLAlchemy.

Responsáveis por (de)serialização entre as duas representações e por
operações de alto nível (importar/exportar GameState completo, aplicar
TurnBuffer, registrar eventos, log diplomático etc.).
"""
from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from simengine.engine import apply_turn_buffer as _apply_turn_buffer_engine
from simengine.schemas import (
    Battalion as BattalionSchema,
)
from simengine.schemas import (
    DiplomaticRelation as DiplomaticRelationSchema,
)
from simengine.schemas import (
    Event as EventSchema,
)
from simengine.schemas import (
    GameState,
    MapFeature,
    PlayerAction,
    PolityAttributes,
    TurnBuffer,
)
from simengine.schemas import (
    Polity as PolitySchema,
)
from simengine.schemas import (
    Region as RegionSchema,
)

from . import models as m


# ---------- erros ----------


class CampaignAlreadyExistsError(ValueError):
    """Levantado em import_game_state quando o nome já existe."""


class CampaignNotFoundError(LookupError):
    """Levantado quando uma operação requer Campaign existente."""


# ---------- helpers internos ----------


def _get_campaign(session: Session, campaign_name: str) -> m.Campaign:
    stmt = select(m.Campaign).where(m.Campaign.name == campaign_name)
    campaign = session.execute(stmt).scalar_one_or_none()
    if campaign is None:
        raise CampaignNotFoundError(f"campanha não encontrada: {campaign_name!r}")
    return campaign


def _get_campaign_loaded(session: Session, campaign_name: str) -> m.Campaign:
    """Get campaign with all relations eager-loaded for export."""
    stmt = (
        select(m.Campaign)
        .where(m.Campaign.name == campaign_name)
        .options(
            selectinload(m.Campaign.polities).selectinload(m.Polity.battalions),
            selectinload(m.Campaign.polities).selectinload(m.Polity.doctrines),
            selectinload(m.Campaign.polities).selectinload(m.Polity.internal_tensions),
            selectinload(m.Campaign.regions),
            selectinload(m.Campaign.diplomatic_relations),
            selectinload(m.Campaign.pending_actions),
        )
    )
    campaign = session.execute(stmt).scalar_one_or_none()
    if campaign is None:
        raise CampaignNotFoundError(f"campanha não encontrada: {campaign_name!r}")
    return campaign


# ---------- import / export ----------


def import_game_state(
    session: Session,
    campaign_name: str,
    state: GameState,
    lore_md: str | None = None,
) -> m.Campaign:
    """Cria Campaign + entidades a partir de um GameState Pydantic.

    Idempotência: se o nome já existe, levanta CampaignAlreadyExistsError
    sem alterar nada (transação revertida).
    """
    existing = session.execute(
        select(m.Campaign.id).where(m.Campaign.name == campaign_name)
    ).first()
    if existing is not None:
        raise CampaignAlreadyExistsError(
            f"campanha {campaign_name!r} já existe"
        )

    campaign = m.Campaign(
        name=campaign_name,
        current_date=state.current_date,
        player_polity_name=state.player_polity,
        lore_md=lore_md,
    )

    for pname, polity in state.polities.items():
        attrs = polity.attributes
        orm_polity = m.Polity(
            name=polity.name,
            government_type=polity.government_type,
            leader=polity.leader,
            capital_region_name=polity.capital_region,
            stability=attrs.stability,
            war_support=attrs.war_support,
            treasury=attrs.treasury,
            manpower=attrs.manpower,
            political_power=attrs.political_power,
        )
        for idx, doctrine in enumerate(polity.doctrines):
            orm_polity.doctrines.append(
                m.Doctrine(label=doctrine, ordering=idx)
            )
        for idx, tension in enumerate(polity.internal_tensions):
            orm_polity.internal_tensions.append(
                m.InternalTension(label=tension, ordering=idx)
            )
        for batt in polity.military_units:
            orm_polity.battalions.append(
                m.Battalion(
                    name=batt.name,
                    location_region_name=batt.location_region,
                    type=batt.type,
                    strength=batt.strength,
                    status=batt.status,
                )
            )
        campaign.polities.append(orm_polity)

    for rname, region in state.regions.items():
        campaign.regions.append(
            m.Region(
                name=region.name,
                type=region.type,
                owner_polity_name=region.owner,
                population_estimate_thousands=region.population_estimate_thousands,
                economic_profile=region.economic_profile,
                features=[f.model_dump(mode="json") for f in region.features],
            )
        )

    for _key, rel in state.diplomatic_relations.items():
        campaign.diplomatic_relations.append(
            m.DiplomaticRelation(
                polity_a=rel.polity_a,
                polity_b=rel.polity_b,
                status=rel.status,
                opinion_a_to_b=rel.opinion_a_to_b,
                opinion_b_to_a=rel.opinion_b_to_a,
                treaties=list(rel.treaties),
                notes=rel.notes,
            )
        )

    for action in state.pending_actions:
        campaign.pending_actions.append(
            m.PendingAction(
                description=action.description,
                submitted_on=action.submitted_on,
                target_polities=list(action.target_polities),
                target_regions=list(action.target_regions),
                category=action.category,
            )
        )

    session.add(campaign)
    try:
        session.flush()
    except IntegrityError as exc:  # corrida com outra sessão
        session.rollback()
        raise CampaignAlreadyExistsError(
            f"campanha {campaign_name!r} já existe"
        ) from exc

    return campaign


def export_game_state(session: Session, campaign_name: str) -> GameState:
    """Lê do DB e materializa um GameState Pydantic equivalente."""
    campaign = _get_campaign_loaded(session, campaign_name)

    polities: dict[str, PolitySchema] = {}
    for orm_polity in campaign.polities:
        owned = sorted(
            r.name
            for r in campaign.regions
            if r.owner_polity_name == orm_polity.name
        )
        polities[orm_polity.name] = PolitySchema(
            name=orm_polity.name,
            government_type=orm_polity.government_type,
            leader=orm_polity.leader,
            capital_region=orm_polity.capital_region_name,
            owned_regions=owned,
            military_units=[
                BattalionSchema(
                    name=b.name,
                    polity=orm_polity.name,
                    location_region=b.location_region_name,
                    type=b.type,
                    strength=b.strength,
                    status=b.status,
                )
                for b in orm_polity.battalions
            ],
            doctrines=[d.label for d in orm_polity.doctrines],
            internal_tensions=[t.label for t in orm_polity.internal_tensions],
            attributes=PolityAttributes(
                stability=orm_polity.stability,
                war_support=orm_polity.war_support,
                treasury=orm_polity.treasury,
                manpower=orm_polity.manpower,
                political_power=orm_polity.political_power,
            ),
        )

    regions: dict[str, RegionSchema] = {}
    for orm_region in campaign.regions:
        regions[orm_region.name] = RegionSchema(
            name=orm_region.name,
            type=orm_region.type,
            owner=orm_region.owner_polity_name,
            population_estimate_thousands=orm_region.population_estimate_thousands,
            economic_profile=orm_region.economic_profile,
            features=[MapFeature.model_validate(f) for f in (orm_region.features or [])],
        )

    diplomatic_relations: dict[str, DiplomaticRelationSchema] = {}
    for orm_rel in campaign.diplomatic_relations:
        rel = DiplomaticRelationSchema(
            polity_a=orm_rel.polity_a,
            polity_b=orm_rel.polity_b,
            status=orm_rel.status,
            opinion_a_to_b=orm_rel.opinion_a_to_b,
            opinion_b_to_a=orm_rel.opinion_b_to_a,
            treaties=list(orm_rel.treaties or []),
            notes=orm_rel.notes,
        )
        diplomatic_relations[
            DiplomaticRelationSchema.make_key(rel.polity_a, rel.polity_b)
        ] = rel

    pending_actions = [
        PlayerAction(
            description=a.description,
            submitted_on=a.submitted_on,
            target_polities=list(a.target_polities or []),
            target_regions=list(a.target_regions or []),
            category=a.category,
        )
        for a in campaign.pending_actions
    ]

    return GameState(
        current_date=campaign.current_date,
        player_polity=campaign.player_polity_name,
        polities=polities,
        regions=regions,
        diplomatic_relations=diplomatic_relations,
        pending_actions=pending_actions,
    )


# ---------- listagem / deleção ----------


def list_campaigns(session: Session) -> list[m.Campaign]:
    stmt = select(m.Campaign).order_by(m.Campaign.created_at.asc())
    return list(session.execute(stmt).scalars().all())


def delete_campaign(session: Session, campaign_name: str) -> None:
    """Apaga campanha + todas as entidades dependentes (cascade ORM)."""
    campaign = _get_campaign(session, campaign_name)
    session.delete(campaign)
    session.flush()


# ---------- aplicação de turno ----------


def apply_turn_buffer(
    session: Session, campaign_name: str, buffer: TurnBuffer
) -> GameState:
    """Aplica deltas do buffer, persiste estado novo, append em events,
    limpa pending_actions. Retorna o GameState pós-turno.
    """
    state = export_game_state(session, campaign_name)
    _apply_turn_buffer_engine(state, buffer)

    # Reescreve estado no DB. Estratégia: apaga as entidades do campaign
    # e recria a partir do GameState. Simples e robusto; volume é
    # baixo (poucas dezenas de polities/regions).
    campaign = _get_campaign_loaded(session, campaign_name)

    # apaga filhas que reescrevemos
    for orm_polity in list(campaign.polities):
        session.delete(orm_polity)
    for orm_region in list(campaign.regions):
        session.delete(orm_region)
    for orm_rel in list(campaign.diplomatic_relations):
        session.delete(orm_rel)
    for orm_action in list(campaign.pending_actions):
        session.delete(orm_action)
    session.flush()

    campaign.current_date = state.current_date
    campaign.player_polity_name = state.player_polity

    for polity in state.polities.values():
        attrs = polity.attributes
        orm_polity = m.Polity(
            name=polity.name,
            government_type=polity.government_type,
            leader=polity.leader,
            capital_region_name=polity.capital_region,
            stability=attrs.stability,
            war_support=attrs.war_support,
            treasury=attrs.treasury,
            manpower=attrs.manpower,
            political_power=attrs.political_power,
        )
        for idx, doctrine in enumerate(polity.doctrines):
            orm_polity.doctrines.append(m.Doctrine(label=doctrine, ordering=idx))
        for idx, tension in enumerate(polity.internal_tensions):
            orm_polity.internal_tensions.append(
                m.InternalTension(label=tension, ordering=idx)
            )
        for batt in polity.military_units:
            orm_polity.battalions.append(
                m.Battalion(
                    name=batt.name,
                    location_region_name=batt.location_region,
                    type=batt.type,
                    strength=batt.strength,
                    status=batt.status,
                )
            )
        campaign.polities.append(orm_polity)

    for region in state.regions.values():
        campaign.regions.append(
            m.Region(
                name=region.name,
                type=region.type,
                owner_polity_name=region.owner,
                population_estimate_thousands=region.population_estimate_thousands,
                economic_profile=region.economic_profile,
                features=[f.model_dump(mode="json") for f in region.features],
            )
        )

    for rel in state.diplomatic_relations.values():
        campaign.diplomatic_relations.append(
            m.DiplomaticRelation(
                polity_a=rel.polity_a,
                polity_b=rel.polity_b,
                status=rel.status,
                opinion_a_to_b=rel.opinion_a_to_b,
                opinion_b_to_a=rel.opinion_b_to_a,
                treaties=list(rel.treaties),
                notes=rel.notes,
            )
        )

    # pending_actions: limpa (já apagamos acima); buffer não traz novas

    # append eventos
    for event in buffer.events:
        campaign.events.append(
            m.Event(
                date=event.date,
                category=event.category,
                description=event.description,
                severity=event.severity,
                caused_by=event.caused_by,
                affected_polities=list(event.affected_polities),
                affected_regions=list(event.affected_regions),
            )
        )

    session.flush()
    return state


# ---------- log de eventos / diplomático ----------


def append_event_log_entries(
    session: Session,
    campaign_name: str,
    events: list[EventSchema],
) -> None:
    campaign = _get_campaign(session, campaign_name)
    for event in events:
        session.add(
            m.Event(
                campaign_id=campaign.id,
                date=event.date,
                category=event.category,
                description=event.description,
                severity=event.severity,
                caused_by=event.caused_by,
                affected_polities=list(event.affected_polities),
                affected_regions=list(event.affected_regions),
            )
        )
    session.flush()


def append_diplomatic_log(
    session: Session,
    campaign_name: str,
    polity: str,
    entry: dict[str, Any],
) -> m.DiplomaticLogEntry:
    """Adiciona entry diplomática.

    `entry` dict deve conter: date, from_polity, to_polity, message_in,
    message_out, proposed_deltas (lista). `polity` é a contraparte.
    """
    campaign = _get_campaign(session, campaign_name)
    orm_entry = m.DiplomaticLogEntry(
        campaign_id=campaign.id,
        counterparty_polity=polity,
        date=entry["date"],
        from_polity=entry["from_polity"],
        to_polity=entry["to_polity"],
        message_in=entry.get("message_in"),
        message_out=entry.get("message_out"),
        proposed_deltas=list(entry.get("proposed_deltas") or []),
    )
    session.add(orm_entry)
    session.flush()
    return orm_entry


# ---------- scheduled events ----------


def record_scheduled_event_fired(
    session: Session,
    campaign_name: str,
    event_id: str,
    fired_at: date,
) -> bool:
    """Registra que um scheduled event disparou. Idempotente: se já
    existe, retorna False sem erro; se cria novo, retorna True.
    """
    campaign = _get_campaign(session, campaign_name)
    existing = session.execute(
        select(m.ScheduledEventFire).where(
            m.ScheduledEventFire.campaign_id == campaign.id,
            m.ScheduledEventFire.event_id == event_id,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return False
    session.add(
        m.ScheduledEventFire(
            campaign_id=campaign.id,
            event_id=event_id,
            fired_at_date=fired_at,
        )
    )
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        return False
    return True


# ---------- consolidação ----------


def events_since_summary(session: Session, campaign_name: str) -> int:
    """Conta Events com date posterior ao último ConsolidatedSummary
    (ou todos, se não há summary).
    """
    campaign = _get_campaign(session, campaign_name)
    last_period_end = session.execute(
        select(func.max(m.ConsolidatedSummary.period_end)).where(
            m.ConsolidatedSummary.campaign_id == campaign.id
        )
    ).scalar()

    stmt = select(func.count(m.Event.id)).where(m.Event.campaign_id == campaign.id)
    if last_period_end is not None:
        stmt = stmt.where(m.Event.date > last_period_end)

    return int(session.execute(stmt).scalar_one())
