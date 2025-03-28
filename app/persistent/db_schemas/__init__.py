from sqlalchemy import and_
from sqlalchemy.orm import relationship

from app.domain.admin import Admin
from app.domain.outbox import OutboxMessage
from app.domain.user import Device, Session, User
from app.dto.session import SessionStatus
from app.persistent.db_schemas.admin import admins_table
from app.persistent.db_schemas.base import mapper_registry
from app.persistent.db_schemas.outbox import outbox_table
from app.persistent.db_schemas.session import device_table, session_table
from app.persistent.db_schemas.user import user_table


def init_mappers() -> None:
    mapper_registry.map_imperatively(
        OutboxMessage,
        outbox_table,
    )

    device_mapper = mapper_registry.map_imperatively(Device, device_table)
    session_mapper = mapper_registry.map_imperatively(Session, session_table)

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
