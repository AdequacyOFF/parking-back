from uuid import UUID

from sqlalchemy import select

from app.api.errors.api_error import ParkingDontExistApiError
from app.api.place.schemas import GetParkingResponse, PlaceAssignResponse
from app.repositories.uow import UnitOfWork


class GetParkingView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self) -> GetParkingResponse:
        async with self._uow.begin():
            if not await self._uow.place_repository.exists():
                raise ParkingDontExistApiError

            all_places = await self._uow.place_repository.get_all_places()
            response: list[PlaceAssignResponse] = []
            for place in all_places:
                if place.owner is None:
                    response.append(PlaceAssignResponse(
                        place_id=place.id,
                        owner_id=None,
                        first_name=None,
                        last_name=None,
                        patronymic=None,
                    ))
                else:
                    user = await self._uow.user_repository.get(place.owner)
                    response.append(PlaceAssignResponse(
                        place_id=place.id,
                        owner_id=place.owner,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        patronymic=user.patronymic,
                    ))

            return GetParkingResponse(
                all_places=response,
            )