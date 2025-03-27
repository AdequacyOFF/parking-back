import random
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from orjson import loads
from sqlalchemy import select

from app.api.errors.api_error import UserNotFoundApiError
from app.api.orders.schemas import CoordinatesData, GetOrdersResponse, OrderData, StationData
from app.dto.user import UserStatus
from app.persistent.db_schemas.station import station_table
from app.persistent.db_schemas.user import user_table
from app.repositories.uow import UnitOfWork


class GetOrdersView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, user_id: UUID, limit: int, offset: int) -> GetOrdersResponse:
        async with self._uow.begin():
            users_stmt = select(user_table.c.id).where(
                user_table.c.id == user_id, user_table.c.status == UserStatus.ACTIVE
            )

            user = (await self._uow.session.execute(users_stmt)).one_or_none()

            if user is None:
                raise UserNotFoundApiError

            stations_stmt = select(
                station_table.c.id,
                station_table.c.name,
                station_table.c.address,
                station_table.c.coordinates.ST_AsGeoJSON().label("coordinates"),
            )
            stations = (await self._uow.session.execute(stations_stmt)).all()

            station = [
                StationData(
                    id=s.id,
                    name=s.name,
                    address=s.address,
                    coordinates=CoordinatesData(
                        latitude=loads(s.coordinates)["coordinates"][1],
                        longitude=loads(s.coordinates)["coordinates"][0],
                    ),
                )
                for s in stations
            ]

            return GetOrdersResponse(
                orders=[
                    OrderData(
                        id=uuid4(),
                        created_at=datetime.now() - timedelta(days=i),
                        station=random.choice(station),
                        bonuses=random.randint(100, 2000),
                    )
                    for i in range(10)  # Mock data
                ][offset : offset + limit]
            )
