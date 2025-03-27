import asyncio
from asyncio import Event
from typing import AsyncGenerator

from loguru import logger

from app.repositories.uow import UnitOfWork
from app.settings import AuthSettings


class CollectorExpiredSessionsHandler:
    def __init__(self, uow: UnitOfWork, settings: AuthSettings):
        self._uow = uow
        self._settings = settings
        self._shutdown_event = Event()
        self._is_shutdown = Event()

    async def startup(self) -> None:
        if self._settings.collector_expired_sessions_enable_cron:
            asyncio.create_task(self._startup())

    async def shutdown(self) -> None:
        if self._settings.collector_expired_sessions_enable_cron:
            self._shutdown_event.set()
            await self._is_shutdown.wait()

    async def _startup(self) -> None:
        logger.info("CollectorExpiredSessionsHandler started")
        while True:
            try:
                await self._handle_sessions()
                if self._shutdown_event.is_set():
                    self._is_shutdown.set()
                    break
            except Exception as e:
                logger.exception(f"CollectorExpiredSessionsHandler crushed. Exception: {str(e)}")
                await asyncio.sleep(5)

    async def _handle_sessions(self) -> None:
        async with self._uow.begin():
            logger.info("CollectorExpiredSessionsHandler finding expired sessions")
            users = await self._uow.user_repository.get_w_exp_sessions(
                batch_size=self._settings.collector_expired_sessions_batch_size,
            )
            if users:
                tasks = []
                logger.info("CollectorExpiredSessionsHandler founded expired sessions")
                for user in users:
                    for session in user.sessions:
                        if session.is_expired:
                            session.expire()
                    tasks.append(self._uow.user_repository.save(user))
                await asyncio.gather(*tasks, return_exceptions=True)
                logger.info("CollectorExpiredSessionsHandler handled sessions")
            else:
                logger.info("CollectorExpiredSessionsHandler does not founded expired sessions")
        await asyncio.sleep(5)


async def init_collector_expired_sessions_handler(
    uow: UnitOfWork, settings: AuthSettings
) -> AsyncGenerator[CollectorExpiredSessionsHandler, None]:
    cron = CollectorExpiredSessionsHandler(uow=uow, settings=settings)
    await cron.startup()
    yield cron
    await cron.shutdown()
