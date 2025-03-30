from typing import Protocol, Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.place import Place
from app.repositories.exception import RepositoryNotFoundException


class IPlaceRepository(Protocol):
    async def get(self, place_id: int) -> Place: ...

    async def get_by_owner(self, owner_id: UUID) -> Place: ...

    async def get_by_car_number(self, car_number: str) -> Place: ...

    async def get_all_places(self) -> Iterable[Place]: ...

    async def exists(self) -> bool: ...

    def save(self, place: Place) -> None: ...


class PlaceRepository(IPlaceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, place_id: int) -> Place:
        stmt = select(Place).filter_by(id=place_id)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    async def get_by_owner(self, owner_id: UUID) -> Place:
        stmt = select(Place).filter_by(owner=owner_id)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    async def get_by_car_number(self, car_number: str) -> Place:
        stmt = select(Place).filter_by(car_number=car_number)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    async def get_all_places(self) -> Iterable[Place]:
        stmt = (
            select(Place)
        )
        places = (await self._session.execute(stmt)).scalars().all()
        return places

    async def exists(self) -> bool:
        stmt = select(Place).limit(1)
        result = (await self._session.execute(stmt)).scalar()
        return result is not None

    def save(self, place: Place) -> None:
        self._session.add(place)
