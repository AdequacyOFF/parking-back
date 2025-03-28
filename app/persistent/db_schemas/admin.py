from sqlalchemy import UUID, Column, Integer, String, Table

from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry

admins_table = Table(
    "admin",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("status", String(50), nullable=False),
    Column("name", String(255), nullable=False),
    Column("username", String(50), nullable=False),
    Column("password_hash", String(255), nullable=False),
    Column("min_fuel_volume", Integer, nullable=False),
    schema=ACCOUNTS_SCHEMA,
)
