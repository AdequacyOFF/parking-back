from typing import Iterable, Optional, Protocol
from uuid import UUID

from aioredis import Redis
from orjson import dumps, loads
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user import OTP, Session, User
from app.dto.session import SessionStatus
from app.dto.user import UserStatus
from app.repositories.exception import RepositoryNotFoundException
from app.utils.dt_utils import get_utc_now_tz


class IUserRepository(Protocol):
    async def get(self, user_id: UUID, with_lock: bool = True) -> User:
        pass

    async def get_by_phone_number(self, phone_number: str, with_lock: bool = True) -> User:
        pass

    async def save(self, user: User) -> None:
        pass

    async def get_w_exp_sessions(self, batch_size: int) -> Iterable[User]:
        pass

    async def _get_otp(self, user: User) -> OTP | None:
        pass

    async def _save_otp(self, user: User) -> None:
        pass


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession, otp_redis: Redis) -> None:
        self.session = session
        self.redis = otp_redis
        self.seen = set()  # type: set[User]

    async def get(self, user_id: UUID, with_lock: bool = True) -> User:
        stmt = select(User).filter(User.id == user_id, User.status != UserStatus.DELETED)  # type: ignore
        if with_lock:
            stmt = stmt.with_for_update()
        user: Optional[User] = (await self.session.execute(stmt)).scalar()
        if not user:
            raise RepositoryNotFoundException
        user.otp_code = await self._get_otp(user)
        self.seen.add(user)
        return user

    async def get_by_phone_number(self, phone_number: str, with_lock: bool = True) -> User:
        stmt = select(User).filter(User.phone_number == phone_number, User.status != UserStatus.DELETED)  # type: ignore
        if with_lock:
            stmt = stmt.with_for_update()
        user: Optional[User] = (await self.session.execute(stmt)).scalar()
        if not user:
            raise RepositoryNotFoundException
        user.otp_code = await self._get_otp(user)
        self.seen.add(user)
        return user

    async def save(self, user: User) -> None:
        await self._save_otp(user)
        self.session.add(user)
        self.seen.add(user)

    async def get_w_exp_sessions(self, batch_size: int) -> Iterable[User]:
        stmt = (
            select(User)
            .join(User.sessions)  # type: ignore
            .filter(Session.status == SessionStatus.ACTIVE, Session.expired_at < get_utc_now_tz())  # type: ignore
            .order_by(Session.expired_at)  # type: ignore
            .with_for_update(skip_locked=True)
            .limit(batch_size)
        )
        sessions = (await self.session.execute(stmt)).scalars().all()
        return sessions

    async def _get_otp(self, user: User) -> OTP | None:
        otp = await self.redis.get(str(user.id))
        if otp is None:
            return otp
        return OTP(**loads(otp))

    async def _save_otp(self, user: User) -> None:
        if user.otp_code is None:
            await self.redis.delete(str(user.id))
        else:
            await self.redis.set(str(user.id), dumps(user.otp_code))
