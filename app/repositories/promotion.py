from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.promotions import Promotion
from app.repositories.exception import RepositoryNotFoundException


class IPromotionRepository(Protocol):
    async def get(self, promotion_id: UUID) -> Promotion:
        pass

    def save(self, promotion: Promotion) -> None:
        pass


class PromotionRepository(IPromotionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, promotion_id: UUID) -> Promotion:
        stmt = select(Promotion).filter_by(id=promotion_id)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    def save(self, promotion: Promotion) -> None:
        self._session.add(promotion)
