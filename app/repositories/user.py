from typing import Iterable, Optional, Protocol
from uuid import UUID

from aioredis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user import Session, User
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

    async def get_by_full_name(self, last_name: str, first_name: str, patronymic: str, with_lock: bool = False) -> User:
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
        self.seen.add(user)
        return user

    async def get_by_phone_number(self, phone_number: str, with_lock: bool = True) -> User:
        stmt = select(User).filter(User.phone_number == phone_number, User.status != UserStatus.DELETED)  # type: ignore
        if with_lock:
            stmt = stmt.with_for_update()
        user: Optional[User] = (await self.session.execute(stmt)).scalar()
        if not user:
            raise RepositoryNotFoundException
        self.seen.add(user)
        return user

    async def get_by_full_name(
            self,
            last_name: str,
            first_name: str,
            patronymic: str,
            with_lock: bool = False,
    ) -> User:
        stmt = select(User).filter(User.last_name == last_name, User.first_name == first_name, User.status != UserStatus.DELETED)

        user: Optional[User] = (await self.session.execute(stmt)).scalar()
        if not user:
            raise RepositoryNotFoundException

        self.seen.add(user)
        return user

    async def save(self, user: User) -> None:
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

    async def get_all_phone_numbers(self) -> Iterable[str]:
        stmt = (
            select(User.phone_number)
        )
        phone_numbers = (await self.session.execute(stmt)).scalars().all()
        return phone_numbers
