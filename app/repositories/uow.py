import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Protocol

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.infrastructure.db import Database, SessionContext
from app.repositories.admin import AdminRepository, IAdminRepository
from app.repositories.outbox import OutboxMessageRepository
from app.repositories.user import UserRepository


class IUnitOfWork(Protocol):
    accounts: UserRepository | None

    async def __aenter__(self) -> None: ...

    async def __aexit__(self, *args: Any) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, database: Database, session_context: SessionContext, otp_redis: Redis) -> None:
        self._database = database
        self._session_context = session_context
        self._otp_redis = otp_redis
        self.accounts: UserRepository | None = None

    @property
    def session(self) -> AsyncSession:
        assert self._session_context.session is not None  # nosec
        return self._session_context.session

    @asynccontextmanager
    async def begin(self) -> AsyncGenerator[AsyncSession, None]:
        scoped_session = None

        if not self._session_context.session:
            scoped_session = async_scoped_session(
                self._database.session_factory,
                asyncio.current_task,
            )
            self._session_context.session = scoped_session()

        if self.session.in_transaction():
            yield self.session
        else:
            try:
                async with self.session.begin():
                    yield self.session
            finally:
                if scoped_session:
                    await scoped_session.remove()
                self._session_context.close_session()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def user_repository(self) -> UserRepository:
        if self.accounts is None:
            self.accounts = UserRepository(session=self.session, otp_redis=self._otp_redis)
        return self.accounts

    @property
    def outbox_repository(self) -> OutboxMessageRepository:
        return OutboxMessageRepository(session=self.session)

    @property
    def admin_repository(self) -> IAdminRepository:
        return AdminRepository(session=self.session)

