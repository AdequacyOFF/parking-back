from sqlalchemy import select

from app.api.orders.schemas import GetMinFuelVolumeResponse
from app.persistent.db_schemas import admins_table
from app.repositories.uow import UnitOfWork


class GetMinFuelVolumeView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self) -> GetMinFuelVolumeResponse:
        async with self._uow.begin():
            query = select(admins_table.c.min_fuel_volume).limit(1)
            result = (await self._uow.session.execute(query)).one()

            return GetMinFuelVolumeResponse(min_fuel_volume=result.min_fuel_volume)
