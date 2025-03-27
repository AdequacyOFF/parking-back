from sqlalchemy import select

from app.api.station.schemas import GetServicesResponse, ServicesData
from app.persistent.db_schemas.station import station_services_table
from app.repositories.uow import UnitOfWork


class GetServicesView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self) -> GetServicesResponse:
        async with self._uow.begin():
            stmt = select(station_services_table.c.id, station_services_table.c.title)
            services = (await self._uow.session.execute(stmt)).all()

            return GetServicesResponse(services=[ServicesData(id=s.id, title=s.title) for s in services])
