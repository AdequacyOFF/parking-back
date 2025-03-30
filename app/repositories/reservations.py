from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.reservation import Reservation
from app.repositories.exception import RepositoryNotFoundException


class IReservationRepository(Protocol):
    async def get(self, reservation_id: int) -> Reservation: ...

    async def get_by_place_id(self, place_id: int) -> Reservation: ...

    async def get_by_reserver_id(self, reserver_id: UUID) -> Reservation: ...

    def save(self, reservation: Reservation) -> None: ...


class ReservationRepository(IReservationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, reservation_id: int) -> Reservation:
        stmt = select(Reservation).filter_by(id=reservation_id)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    async def get_by_place_id(self, place_id: int) -> Reservation:
        stmt = select(Reservation).filter_by(place_id=place_id)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    async def get_by_reserver_id(self, reserver_id: UUID) -> Reservation:
        stmt = select(Reservation).filter_by(reserved_by=reserver_id)
        result = (await self._session.execute(stmt)).scalar()
        if not result:
            raise RepositoryNotFoundException
        return result

    def save(self, reservation: Reservation) -> None:
        self._session.add(reservation)
