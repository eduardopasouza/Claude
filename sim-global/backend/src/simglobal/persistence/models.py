"""SQLAlchemy 2.x ORM models para persistência do sim-global.

Cada Campaign agrega Polities, Regions, Battalions, DiplomaticRelations,
Doctrines, InternalTensions, Events, ConsolidatedSummaries,
PendingActions, DiplomaticLogEntries e ScheduledEventFires. Cascade
delete via relationships ORM (passive_deletes desligado de propósito
para funcionar tanto em SQLite quanto em backends que respeitam FK
ON DELETE CASCADE). Todos os JSONs ficam em colunas SQLAlchemy.JSON
(serialização nativa em SQLite via TEXT).
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Declarative base com metadata global."""


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    current_date: Mapped[date] = mapped_column(Date, nullable=False)
    player_polity_name: Mapped[str] = mapped_column(String(200), nullable=False)
    lore_md: Mapped[str | None] = mapped_column(Text, nullable=True)

    polities: Mapped[list["Polity"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    regions: Mapped[list["Region"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    diplomatic_relations: Mapped[list["DiplomaticRelation"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    consolidated_summaries: Mapped[list["ConsolidatedSummary"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    pending_actions: Mapped[list["PendingAction"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    diplomatic_log_entries: Mapped[list["DiplomaticLogEntry"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
    scheduled_event_fires: Mapped[list["ScheduledEventFire"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )


class Polity(Base):
    __tablename__ = "polities"
    __table_args__ = (
        UniqueConstraint("campaign_id", "name", name="uq_polities_campaign_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    government_type: Mapped[str] = mapped_column(String(400), nullable=False)
    leader: Mapped[str] = mapped_column(String(200), nullable=False)
    capital_region_name: Mapped[str] = mapped_column(String(200), nullable=False)
    iso3: Mapped[str | None] = mapped_column(String(3), nullable=True)

    stability: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    war_support: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    treasury: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    manpower: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    political_power: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    campaign: Mapped[Campaign] = relationship(back_populates="polities")
    battalions: Mapped[list["Battalion"]] = relationship(
        back_populates="polity",
        cascade="all, delete-orphan",
    )
    doctrines: Mapped[list["Doctrine"]] = relationship(
        back_populates="polity",
        cascade="all, delete-orphan",
        order_by="Doctrine.ordering",
    )
    internal_tensions: Mapped[list["InternalTension"]] = relationship(
        back_populates="polity",
        cascade="all, delete-orphan",
        order_by="InternalTension.ordering",
    )


class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (
        UniqueConstraint("campaign_id", "name", name="uq_regions_campaign_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    owner_polity_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    population_estimate_thousands: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    economic_profile: Mapped[str] = mapped_column(Text, nullable=False, default="")
    features: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False, default=list
    )

    campaign: Mapped[Campaign] = relationship(back_populates="regions")


class Battalion(Base):
    __tablename__ = "battalions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    polity_id: Mapped[int] = mapped_column(
        ForeignKey("polities.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location_region_name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="pronto")

    polity: Mapped[Polity] = relationship(back_populates="battalions")


class DiplomaticRelation(Base):
    __tablename__ = "diplomatic_relations"
    __table_args__ = (
        UniqueConstraint(
            "campaign_id",
            "polity_a",
            "polity_b",
            name="uq_diplomatic_relations_campaign_pair",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    polity_a: Mapped[str] = mapped_column(String(200), nullable=False)
    polity_b: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    opinion_a_to_b: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    opinion_b_to_a: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    treaties: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    campaign: Mapped[Campaign] = relationship(back_populates="diplomatic_relations")


class Doctrine(Base):
    __tablename__ = "doctrines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    polity_id: Mapped[int] = mapped_column(
        ForeignKey("polities.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(400), nullable=False)
    ordering: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    polity: Mapped[Polity] = relationship(back_populates="doctrines")


class InternalTension(Base):
    __tablename__ = "internal_tensions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    polity_id: Mapped[int] = mapped_column(
        ForeignKey("polities.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(400), nullable=False)
    ordering: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    polity: Mapped[Polity] = relationship(back_populates="internal_tensions")


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        Index("ix_events_campaign_date", "campaign_id", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(40), nullable=False, default="moderate")
    caused_by: Mapped[str] = mapped_column(String(40), nullable=False)
    affected_polities: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    affected_regions: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )

    campaign: Mapped[Campaign] = relationship(back_populates="events")


class ConsolidatedSummary(Base):
    __tablename__ = "consolidated_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    key_events: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    state_changes_summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    emerging_tensions: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    generated_at: Mapped[date] = mapped_column(Date, nullable=False)

    campaign: Mapped[Campaign] = relationship(back_populates="consolidated_summaries")


class PendingAction(Base):
    __tablename__ = "pending_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_on: Mapped[date] = mapped_column(Date, nullable=False)
    target_polities: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    target_regions: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)

    campaign: Mapped[Campaign] = relationship(back_populates="pending_actions")


class DiplomaticLogEntry(Base):
    __tablename__ = "diplomatic_log_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    counterparty_polity: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    from_polity: Mapped[str] = mapped_column(String(200), nullable=False)
    to_polity: Mapped[str] = mapped_column(String(200), nullable=False)
    message_in: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_out: Mapped[str | None] = mapped_column(Text, nullable=True)
    proposed_deltas: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False, default=list
    )

    campaign: Mapped[Campaign] = relationship(back_populates="diplomatic_log_entries")


class ScheduledEventFire(Base):
    __tablename__ = "scheduled_event_fires"
    __table_args__ = (
        UniqueConstraint(
            "campaign_id",
            "event_id",
            name="uq_scheduled_event_fires_campaign_event",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    event_id: Mapped[str] = mapped_column(String(200), nullable=False)
    fired_at_date: Mapped[date] = mapped_column(Date, nullable=False)

    campaign: Mapped[Campaign] = relationship(back_populates="scheduled_event_fires")
