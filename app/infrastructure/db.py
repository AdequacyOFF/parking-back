from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.settings import DatabaseSettings
from app.utils.common import Singleton


class Database:
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings
        self._engine = self._create_engine()

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def connection_factory(self) -> AsyncConnection:
        return self._engine.connect()

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[AsyncConnection]:
        async with self.connection_factory() as conn:
            yield conn

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(self._settings.url, poolclass=NullPool, echo=self._settings.echo)

    async def shutdown(self) -> None:
        await self._engine.dispose()


class SessionContext(metaclass=Singleton):
    _session: ContextVar[AsyncSession | None] = ContextVar("session", default=None)

    @property
    def session(self) -> AsyncSession:
        current_session = self._session.get()
        return current_session  # type: ignore

    @session.setter
    def session(self, session: AsyncSession) -> None:
        current_session = self._session.get()
        assert current_session is None, "Cannot set session twice"  # nosec
        self._session.set(session)

    def close_session(self) -> None:
        current_session = self._session.get()
        assert current_session is not None, "Cannot close None"  # nosec
        self._session.set(None)
