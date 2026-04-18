"""Initial schema - all tables.

Revision ID: 001
Revises: None
Create Date: 2026-04-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(500), nullable=False),
        sa.Column("cpf_cnpj", sa.String(20), index=True),
        sa.Column("plan", sa.String(20), server_default="free"),
        sa.Column("reports_used_this_month", sa.Integer(), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # --- Properties ---
    op.create_table(
        "properties",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("car_code", sa.String(100), unique=True, index=True),
        sa.Column("matricula", sa.String(100), index=True),
        sa.Column("sncr_code", sa.String(100), index=True),
        sa.Column("nirf", sa.String(50), index=True),
        sa.Column("ccir", sa.String(50), index=True),
        sa.Column("sigef_code", sa.String(100), index=True),
        sa.Column("itr_number", sa.String(50), index=True),
        sa.Column("property_name", sa.String(500)),
        sa.Column("area_total_ha", sa.Float()),
        sa.Column("area_app_ha", sa.Float()),
        sa.Column("area_reserva_legal_ha", sa.Float()),
        sa.Column("area_uso_consolidado_ha", sa.Float()),
        sa.Column("area_remanescente_ha", sa.Float()),
        sa.Column("municipality", sa.String(200)),
        sa.Column("municipality_code", sa.String(10)),
        sa.Column("state", sa.String(2)),
        sa.Column("comarca", sa.String(200)),
        sa.Column("cartorio", sa.String(500)),
        sa.Column("classification", sa.String(100)),
        sa.Column("modules_fiscais", sa.Float()),
        sa.Column("owner_name", sa.String(500)),
        sa.Column("owner_cpf_cnpj", sa.String(20), index=True),
        sa.Column("car_status", sa.String(50)),
        sa.Column("sigef_certified", sa.Boolean(), server_default="false"),
        sa.Column("ccir_valid", sa.Boolean()),
        sa.Column("has_onus", sa.Boolean()),
        sa.Column("onus_description", sa.Text()),
        sa.Column("geometry", geoalchemy2.Geometry("MULTIPOLYGON", srid=4326), nullable=True),
        sa.Column("itr_vti", sa.Float()),
        sa.Column("itr_status", sa.String(50)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("raw_data", sa.JSON()),
    )
    op.create_index("idx_properties_municipality_state", "properties", ["municipality", "state"])

    # --- Persons ---
    op.create_table(
        "persons",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cpf_cnpj", sa.String(20), unique=True, index=True),
        sa.Column("person_type", sa.String(2)),
        sa.Column("name", sa.String(500), index=True),
        sa.Column("trade_name", sa.String(500)),
        sa.Column("registration_status", sa.String(50)),
        sa.Column("cnae_principal", sa.String(200)),
        sa.Column("address", sa.Text()),
        sa.Column("municipality", sa.String(200)),
        sa.Column("state", sa.String(2)),
        sa.Column("capital_social", sa.Float()),
        sa.Column("partners", sa.JSON()),
        sa.Column("monitored", sa.Boolean(), server_default="false"),
        sa.Column("last_checked_at", sa.DateTime()),
        sa.Column("alert_on_change", sa.Boolean(), server_default="false"),
        sa.Column("properties_count", sa.Integer(), server_default="0"),
        sa.Column("embargos_count", sa.Integer(), server_default="0"),
        sa.Column("lawsuits_count", sa.Integer(), server_default="0"),
        sa.Column("slave_labour_records", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("raw_data", sa.JSON()),
    )

    # --- Environmental Alerts ---
    op.create_table(
        "environmental_alerts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("property_car_code", sa.String(100), index=True),
        sa.Column("cpf_cnpj", sa.String(20), index=True),
        sa.Column("alert_type", sa.String(50)),
        sa.Column("source", sa.String(50)),
        sa.Column("description", sa.Text()),
        sa.Column("area_ha", sa.Float()),
        sa.Column("date_detected", sa.DateTime()),
        sa.Column("geometry", geoalchemy2.Geometry("MULTIPOLYGON", srid=4326), nullable=True),
        sa.Column("raw_data", sa.JSON()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # --- Legal Records ---
    op.create_table(
        "legal_records",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cpf_cnpj", sa.String(20), index=True),
        sa.Column("record_type", sa.String(50)),
        sa.Column("source", sa.String(100)),
        sa.Column("case_number", sa.String(100)),
        sa.Column("description", sa.Text()),
        sa.Column("amount", sa.Float()),
        sa.Column("status", sa.String(50)),
        sa.Column("date_filed", sa.DateTime()),
        sa.Column("municipality", sa.String(200)),
        sa.Column("state", sa.String(2)),
        sa.Column("raw_data", sa.JSON()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # --- Rural Credits ---
    op.create_table(
        "rural_credits",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cpf_cnpj", sa.String(20), index=True),
        sa.Column("contract_number", sa.String(100)),
        sa.Column("bank", sa.String(200)),
        sa.Column("credit_line", sa.String(100)),
        sa.Column("purpose", sa.String(100)),
        sa.Column("amount", sa.Float()),
        sa.Column("municipality", sa.String(200)),
        sa.Column("state", sa.String(2)),
        sa.Column("year", sa.Integer()),
        sa.Column("crop", sa.String(100)),
        sa.Column("raw_data", sa.JSON()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_rural_credits_cpf_year", "rural_credits", ["cpf_cnpj", "year"])

    # --- Land Prices ---
    op.create_table(
        "land_prices",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("municipality", sa.String(200)),
        sa.Column("municipality_code", sa.String(10)),
        sa.Column("state", sa.String(2)),
        sa.Column("land_type", sa.String(100)),
        sa.Column("price_per_ha", sa.Float()),
        sa.Column("source", sa.String(100)),
        sa.Column("reference_date", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_land_prices_location", "land_prices", ["municipality", "state"])

    # --- Market Data ---
    op.create_table(
        "market_data",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("commodity", sa.String(50), index=True),
        sa.Column("price", sa.Float()),
        sa.Column("unit", sa.String(20)),
        sa.Column("date", sa.DateTime(), index=True),
        sa.Column("source", sa.String(50)),
        sa.Column("variation_pct", sa.Float()),
        sa.Column("location", sa.String(200)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_market_commodity_date", "market_data", ["commodity", "date"])

    # --- Monitoring Alerts ---
    op.create_table(
        "monitoring_alerts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cpf_cnpj", sa.String(20), index=True),
        sa.Column("property_car_code", sa.String(100), index=True),
        sa.Column("alert_type", sa.String(100)),
        sa.Column("title", sa.String(500)),
        sa.Column("description", sa.Text()),
        sa.Column("severity", sa.String(20)),
        sa.Column("read", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # --- Cached Queries ---
    op.create_table(
        "cached_queries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("query_type", sa.String(50), index=True),
        sa.Column("query_key", sa.String(500), index=True),
        sa.Column("response_data", sa.JSON()),
        sa.Column("expires_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_cache_type_key", "cached_queries", ["query_type", "query_key"])


def downgrade() -> None:
    op.drop_table("cached_queries")
    op.drop_table("monitoring_alerts")
    op.drop_table("market_data")
    op.drop_table("land_prices")
    op.drop_table("rural_credits")
    op.drop_table("legal_records")
    op.drop_table("environmental_alerts")
    op.drop_table("persons")
    op.drop_table("properties")
    op.drop_table("users")
