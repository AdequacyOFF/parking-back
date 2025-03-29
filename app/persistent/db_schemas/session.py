from sqlalchemy import Column, ForeignKey, String, Table, Text, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry

session_table = Table(
    "session",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    Column("user_id", UUID(), ForeignKey("accounts.user.id"), nullable=True),
    Column("admin_id", UUID(), ForeignKey("accounts.admin.id"), nullable=True),
    Column("status", String(30), nullable=False),
    Column("token", Text, nullable=False),
    Column("expired_at", TIMESTAMP(timezone=True), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)
