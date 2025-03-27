from sqlalchemy import (
    INTEGER,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.dto.user import UserSexType
from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry

user_card_table = Table(
    "card",
    mapper_registry.metadata,
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
    Column("qr", String(length=255), primary_key=True),
    Column("bonuses", INTEGER, nullable=False),
    Column("type", String(length=50), nullable=False),
    Column("state", String(length=50), nullable=False),
    Column("user_id", UUID, ForeignKey("accounts.user.id"), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    Column("phone_number", String(length=50), nullable=False),
    Column("status", String(length=50), nullable=False),
    Column("first_name", String(length=50), nullable=True),
    Column("last_name", String(length=50), nullable=True),
    Column("sex", Enum(UserSexType, name="sex_type"), nullable=True),
    Column("user_agreement", Boolean, nullable=False, default=False),
    Column("privacy_policy", Boolean, nullable=False, default=False),
    Column("company_rules", Boolean, nullable=False, default=False),
    Column("birth_date", Date, nullable=False),
    schema=ACCOUNTS_SCHEMA,
)

order_requests_table = Table(
    "order_requests",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    Column("fuel_type", String(50), nullable=False),
    Column("volume", BigInteger, nullable=False),
    Column("user_id", UUID, ForeignKey(f"{ACCOUNTS_SCHEMA}.user.id"), nullable=False),
    Column("comment", Text, nullable=True),
    Column("feedback_score", Integer, nullable=True),
    Column("feedback_text", Text, nullable=True),
    schema=ACCOUNTS_SCHEMA,
)
