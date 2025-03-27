from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.admin import Admin
from app.dto.admin import AdminStatus
from app.repositories.exception import RepositoryNotFoundException


class IAdminRepository(Protocol):
    async def get(self, admin_id: UUID) -> Admin: ...

    async def get_by_username(self, username: str) -> Admin: ...

    def save(self, admin: Admin) -> None: ...


class AdminRepository(IAdminRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, admin_id: UUID) -> Admin:
        stmt = select(Admin).filter_by(id=admin_id, status=AdminStatus.ACTIVE)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    async def get_by_username(self, username: str) -> Admin:
        stmt = select(Admin).filter_by(username=username, status=AdminStatus.ACTIVE)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    def save(self, admin: Admin) -> None:
        self._session.add(admin)
