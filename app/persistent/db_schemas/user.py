from sqlalchemy import (
    Column,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID

from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry


user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("phone_number", String(length=50), nullable=False),
    Column("status", String(length=50), nullable=False),
    Column("first_name", String(length=50), nullable=True),
    Column("last_name", String(length=50), nullable=True),
    Column("patronymic", String(length=50), nullable=True),
    Column("password_hash", String(255), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)
