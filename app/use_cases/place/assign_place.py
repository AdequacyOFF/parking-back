from app.api.errors.api_error import UserNotFoundApiError, ParkingDontExistApiError
from app.api.place.schemas import PlaceAssignCMD, PlaceAssignResponse
from app.repositories.uow import UnitOfWork
from app.repositories.exception import RepositoryNotFoundException
from app.domain.place import Place


class PlaceAssignUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, command: PlaceAssignCMD) -> PlaceAssignResponse:
        async with self._uow.begin():
            if not await self._uow.place_repository.exists():
                raise ParkingDontExistApiError

            try:
                user = await self._uow.user_repository.get_by_full_name(
                    last_name=command.last_name,
                    first_name=command.first_name,
                    patronymic=command.patronymic,  # Опционально
                )
            except RepositoryNotFoundException:
                raise UserNotFoundApiError
            all_places = await self._uow.place_repository.get_all_places()
            for place in all_places:
                if place.owner is None:
                    place.assign(user.id)
                    break

            return PlaceAssignResponse(
                place_id=place.id,
                owner_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                patronymic=user.patronymic,
            )
