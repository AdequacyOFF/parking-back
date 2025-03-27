from sqlalchemy import DATE, TIMESTAMP, UUID, VARCHAR, Column, Table, text

from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry

promotions_table = Table(
    "promotions",
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
    Column("title", VARCHAR(60), nullable=False),
    Column("short_description", VARCHAR(255), nullable=False),
    Column("description", VARCHAR(255), nullable=False),
    Column("photo_name", VARCHAR(255), nullable=False),
    Column("url", VARCHAR(255), nullable=True),
    Column("start_date", DATE, nullable=False),
    Column("end_date", DATE, nullable=False),
    Column("status", VARCHAR(50), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)
