from sqlalchemy import and_
from sqlalchemy.orm import relationship

from app.domain.admin import Admin
from app.domain.user import Session, User
from app.domain.place import Place
from app.domain.reservation import Reservation
from app.dto.session import SessionStatus
from app.persistent.db_schemas.admin import admins_table
from app.persistent.db_schemas.base import mapper_registry
from app.persistent.db_schemas.session import session_table
from app.persistent.db_schemas.user import user_table
from app.persistent.db_schemas.places import places_table
from app.persistent.db_schemas.reservations import reservations_table


def init_mappers() -> None:

    session_mapper = mapper_registry.map_imperatively(Session, session_table)
    reservation_mapper = mapper_registry.map_imperatively(Reservation, reservations_table)

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
            "reservations": relationship(
                reservation_mapper,
                backref="user",
                foreign_keys=reservation_mapper.c.reserved_by,
                lazy="selectin",
                collection_class=list,
                primaryjoin=and_(user_table.c.id == reservations_table.c.reserved_by),
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

    mapper_registry.map_imperatively(
        Place,
        places_table,
        properties={
            "reservations": relationship(
                reservation_mapper,
                backref="place",
                foreign_keys=reservation_mapper.c.place_id,
                lazy="selectin",
                collection_class=list,
                primaryjoin=and_(places_table.c.id == reservations_table.c.place_id),
            ),
        },
    )
