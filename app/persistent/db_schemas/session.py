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
    Column("device_id", UUID(), ForeignKey("accounts.device.id"), nullable=False),
    Column("user_id", UUID(), ForeignKey("accounts.user.id"), nullable=True),
    Column("admin_id", UUID(), ForeignKey("accounts.admin.id"), nullable=True),
    Column("status", String(30), nullable=False),
    Column("token", Text, nullable=False),
    Column("expired_at", TIMESTAMP(timezone=True), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)

device_table = Table(
    "device",
    mapper_registry.metadata,
    mapper_registry.metadata,
    Column("id", UUID(), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    Column("user_id", UUID(), ForeignKey("accounts.user.id"), nullable=False),
    Column("device_id", String(length=256), nullable=False),
    Column("fcm_token", String(length=256), nullable=True),
    Column("type", String(length=50), nullable=False),
    Column("os_version", String(length=50), nullable=False),
    Column("app_version", String(length=50), nullable=False),
    Column("locale", String(length=50), nullable=False),
    Column("screen_resolution", String(length=50), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)
