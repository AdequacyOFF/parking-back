from sqlalchemy import and_
from sqlalchemy.orm import relationship

from app.domain.admin import Admin
from app.domain.outbox import OutboxMessage
from app.domain.promotions import Promotion
from app.domain.stations import Oil, Service, Station
from app.domain.user import Card, Device, OrderRequest, Session, User
from app.dto.session import SessionStatus
from app.persistent.db_schemas.admin import admins_table
from app.persistent.db_schemas.base import mapper_registry
from app.persistent.db_schemas.outbox import outbox_table
from app.persistent.db_schemas.promotions import promotions_table
from app.persistent.db_schemas.session import device_table, session_table
from app.persistent.db_schemas.station import (
    services_relation_table,
    station_oils_table,
    station_services_table,
    station_table,
)
from app.persistent.db_schemas.user import order_requests_table, user_card_table, user_table


def init_mappers() -> None:
    mapper_registry.map_imperatively(
        OutboxMessage,
        outbox_table,
    )

    mapper_registry.map_imperatively(
        Promotion,
        promotions_table,
    )

    mapper_registry.map_imperatively(Oil, station_oils_table)

    mapper_registry.map_imperatively(
        Service,
        station_services_table,
        properties={
            "station": relationship(
                Station,
                secondary=services_relation_table,
                lazy="selectin",
                back_populates="services",
            )
        },
    )

    mapper_registry.map_imperatively(
        Station,
        station_table,
        properties={
            "oils": relationship(Oil, foreign_keys=[station_oils_table.c.station_id]),
            "services": relationship(
                Service,
                lazy="selectin",
                secondary=services_relation_table,
                back_populates="station",
            ),
        },
    )

    device_mapper = mapper_registry.map_imperatively(Device, device_table)
    session_mapper = mapper_registry.map_imperatively(Session, session_table)
    card_mapper = mapper_registry.map_imperatively(Card, user_card_table)
    orders_mapper = mapper_registry.map_imperatively(OrderRequest, order_requests_table)

    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "sessions": relationship(
                session_mapper,
                backref="user",
                foreign_keys=session_mapper.c.user_id,
                lazy="selectin",
                collection_class=list,
                primaryjoin=and_(
                    session_table.c.user_id == user_table.c.id,
                    session_table.c.status == SessionStatus.ACTIVE.value,
                ),
            ),
            "devices": relationship(
                device_mapper,
                backref="user",
                foreign_keys=device_mapper.c.user_id,
                lazy="selectin",
                collection_class=set,
            ),
            "card": relationship(card_mapper, foreign_keys=card_mapper.c.user_id, lazy="selectin", uselist=False),
            "order_requests": relationship(
                orders_mapper, foreign_keys=orders_mapper.c.user_id, lazy="selectin", collection_class=list
            ),
        },
    )

    mapper_registry.map_imperatively(
        Admin,
        admins_table,
        properties={
            "sessions": relationship(
                session_mapper,
                backref="admin",
                foreign_keys=session_mapper.c.admin_id,
                lazy="selectin",
                collection_class=list,
                primaryjoin=and_(
                    session_table.c.admin_id == admins_table.c.id,
                    session_table.c.status == SessionStatus.ACTIVE.value,
                ),
            )
        },
    )
