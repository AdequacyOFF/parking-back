from sqlalchemy import select

from app.api.station.schemas import GetOilsResponse, OilData
from app.persistent.db_schemas.station import station_oils_table
from app.repositories.uow import UnitOfWork


class GetOilsView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self) -> GetOilsResponse:
        async with self._uow.begin():
            stmt = select(station_oils_table.c.id, station_oils_table.c.title, station_oils_table.c.price)
            oils = (await self._uow.session.execute(stmt)).all()

            return GetOilsResponse(oils=[OilData(id=o.id, title=o.title, price=o.price) for o in oils])
