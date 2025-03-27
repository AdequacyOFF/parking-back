from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.outbox import OutboxMessage
from app.dto.outbox import OutboxMessageStatus
from app.persistent.db_schemas.outbox import outbox_table
from app.repositories.exception import RepositoryNotFoundException


class IOutboxMessageRepository(Protocol):
    async def get(self, outbox_message_id: UUID) -> OutboxMessage:
        pass

    async def get_pending(self) -> Sequence[OutboxMessage]:
        pass

    async def save(self, outbox_message: OutboxMessage) -> None:
        pass


class OutboxMessageRepository(IOutboxMessageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, outbox_id: UUID) -> OutboxMessage:
        stmt = select(OutboxMessage).filter_by(id=outbox_id)
        outbox_message = (await self.session.execute(stmt)).scalar_one_or_none()
        if not outbox_message:
            raise RepositoryNotFoundException
        return outbox_message

    async def get_pending(self) -> Sequence[OutboxMessage]:
        stmt = (
            select(OutboxMessage)
            .filter_by(status=OutboxMessageStatus.PENDING)
            .order_by(outbox_table.c.created_at.asc())
        )
        outbox_messages = (await self.session.execute(stmt)).scalars().all()
        return outbox_messages

    async def save(self, outbox_message: OutboxMessage) -> None:
        self.session.add(outbox_message)
