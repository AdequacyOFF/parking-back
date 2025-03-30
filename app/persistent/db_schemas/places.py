from sqlalchemy import Column, ForeignKey, String, Table, Text, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.persistent.db_schemas.base import PARKING_SCHEMA, mapper_registry

places_table = Table(
    "places",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("car_number", String(9), nullable=True),
    Column("owner", UUID(), ForeignKey("accounts.user.id", ondelete="SET NULL"), nullable=True),
    Column("is_busy", Boolean, nullable=False),
    schema=PARKING_SCHEMA,
)
