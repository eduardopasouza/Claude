from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Text, JSON,
    create_engine, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker
from geoalchemy2 import Geometry
from datetime import datetime, timezone

from app.config import settings

Base = declarative_base()


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_code = Column(String(100), unique=True, index=True)
    sigef_code = Column(String(100), index=True)
    area_total_ha = Column(Float)
    municipality = Column(String(200))
    state = Column(String(2))
    owner_name = Column(String(500))
    owner_cpf_cnpj = Column(String(20), index=True)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    car_status = Column(String(50))
    sigef_certified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    raw_data = Column(JSON)

    __table_args__ = (
        Index("idx_properties_municipality_state", "municipality", "state"),
    )


class EnvironmentalAlert(Base):
    __tablename__ = "environmental_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_car_code = Column(String(100), index=True)
    alert_type = Column(String(50))  # embargo, deforestation, overlap_uc, overlap_ti
    source = Column(String(50))  # ibama, inpe, icmbio, funai
    description = Column(Text)
    area_ha = Column(Float)
    date_detected = Column(DateTime)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class LegalRecord(Base):
    __tablename__ = "legal_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(20), index=True)
    record_type = Column(String(50))  # lawsuit, debt, protest, slave_labour
    source = Column(String(100))  # tribunal name, ibama, mte
    case_number = Column(String(100))
    description = Column(Text)
    amount = Column(Float)
    status = Column(String(50))
    date_filed = Column(DateTime)
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    commodity = Column(String(50), index=True)
    price = Column(Float)
    unit = Column(String(20))
    date = Column(DateTime, index=True)
    source = Column(String(50))
    variation_pct = Column(Float)
    location = Column(String(200))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_market_commodity_date", "commodity", "date"),
    )


class CachedQuery(Base):
    __tablename__ = "cached_queries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_type = Column(String(50), index=True)
    query_key = Column(String(500), index=True)
    response_data = Column(JSON)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_cache_type_key", "query_type", "query_key"),
    )


def get_engine():
    return create_engine(settings.database_url, echo=settings.debug)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)
