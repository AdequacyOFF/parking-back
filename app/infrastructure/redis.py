from enum import IntEnum
from typing import AsyncIterator

from aioredis import Redis, from_url

from app.settings import RedisSettings


class RedisDatabaseType(IntEnum):
    OTP = 1


async def init_redis_pool(settings: RedisSettings, db: RedisDatabaseType) -> AsyncIterator[Redis]:
    session = from_url(
        f"redis://{settings.host}", password=settings.password, encoding="utf-8", decode_responses=True, db=db.value
    )
    yield session
    await session.close()
