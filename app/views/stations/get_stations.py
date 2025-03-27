from geoalchemy2.functions import ST_Distance, ST_DistanceSphere, ST_MakePoint, ST_SetSRID
from orjson import loads
from sqlalchemy import select

from app.api.station.schemas import CoordinatesData, GetGasStationsResponse, OilData, ServicesData, StationData
from app.persistent.db_schemas.station import (
    services_relation_table,
    station_oils_table,
    station_services_table,
    station_table,
)
from app.repositories.uow import UnitOfWork


class GetGasStationsView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(
        self, oils: list[str], services: list[str], lat: float | None, lon: float | None
    ) -> GetGasStationsResponse:
        async with self._uow.begin():
            stations_stmt = select(
                station_table.c.id,
                station_table.c.name,
                station_table.c.address,
                station_table.c.coordinates.ST_AsGeoJSON().label("coordinates"),
            )

            is_calc_distance = lon and lat
            if is_calc_distance:
                stations_stmt = stations_stmt.add_columns(
                    ST_Distance(
                        station_table.c.coordinates,
                        ST_SetSRID(ST_MakePoint(lon, lat), 4326),
                    ).label("distance")
                )
                stations_stmt = stations_stmt.order_by("distance")
            else:
                stations_stmt = stations_stmt.order_by("name")

            stations = (await self._uow.session.execute(stations_stmt)).all()

            services_stmt = (
                select(station_services_table.c.id, station_services_table.c.title)
                .outerjoin(services_relation_table, station_services_table.c.id == services_relation_table.c.service_id)
                .outerjoin(station_table, services_relation_table.c.station_id == station_table.c.id)
            )
            if services:
                services_stmt = services_stmt.where(station_services_table.c.title.in_(services))

            services_result = (await self._uow.session.execute(services_stmt)).all()

            oils_stmt = select(
                station_oils_table.c.id,
                station_oils_table.c.title,
                station_oils_table.c.price,
                station_oils_table.c.station_id,
            )
            if oils:
                oils_stmt = oils_stmt.where(station_oils_table.c.title.in_(oils))

            oils_result = (await self._uow.session.execute(oils_stmt)).all()

            return GetGasStationsResponse(
                stations=[
                    StationData(
                        id=s.id,
                        name=s.name,
                        address=s.address,
                        coordinates=CoordinatesData(
                            latitude=loads(s.coordinates)["coordinates"][1],
                            longitude=loads(s.coordinates)["coordinates"][0],
                        ),
                        distance=int(s.distance) if is_calc_distance else None,
                        services=[ServicesData(id=s.id, title=s.title) for s in services_result],
                        oils=[
                            OilData(id=o.id, title=o.title, price=o.price) for o in oils_result if o.station_id == s.id
                        ],
                    )
                    for s in stations
                ]
            )
