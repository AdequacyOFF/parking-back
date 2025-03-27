from geoalchemy2 import Geography
from sqlalchemy import INTEGER, TIMESTAMP, UUID, Column, ForeignKey, String, Table, text

from app.persistent.db_schemas.base import ACCOUNTS_SCHEMA, mapper_registry

station_table = Table(
    "station",
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
    Column("name", String(60), nullable=False),
    Column("address", String(255), nullable=False),
    Column("coordinates", Geography(geometry_type="POINT"), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)


station_oils_table = Table(
    "oils",
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
    Column("title", String(90), nullable=False),
    Column("price", INTEGER, nullable=False),
    Column("station_id", UUID, ForeignKey("accounts.station.id"), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)


services_relation_table = Table(
    "services_relation_table",
    mapper_registry.metadata,
    Column("service_id", UUID, ForeignKey("accounts.services.id"), nullable=True),
    Column("station_id", UUID, ForeignKey("accounts.station.id"), nullable=True),
    schema=ACCOUNTS_SCHEMA,
)


station_services_table = Table(
    "services",
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
    Column("title", String(60), nullable=False),
    schema=ACCOUNTS_SCHEMA,
)
