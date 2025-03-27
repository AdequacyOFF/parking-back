from sqlalchemy import JSON, TIMESTAMP, UUID, VARCHAR, Column, Table, text

from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry

outbox_table = Table(
    "outbox_message",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("header", JSON(), nullable=False),
    Column("body", JSON(), nullable=False),
    Column("topic", VARCHAR(240), nullable=False),
    Column("status", VARCHAR(240), nullable=False),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=ACCOUNTS_SCHEMA,
)
