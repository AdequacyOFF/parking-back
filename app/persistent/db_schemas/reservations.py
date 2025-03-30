from sqlalchemy import Column, ForeignKey, String, Table, Text, text, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.persistent.db_schemas.base import PARCKING_SCHEMA, mapper_registry

reservations_table = Table(
    "reservations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("place_id", Integer, ForeignKey("parcking.places.id", ondelete="CASCADE"), nullable=False),
    Column("reserved_from", TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("reserved_to", TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("reserved_by", UUID(), nullable=False),
    schema=PARCKING_SCHEMA,
)