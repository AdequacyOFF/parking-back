from app.api.errors.api_error import UserNotFoundApiError, ParkingDontExistApiError
from app.api.place.schemas import PlaceAssignCMD, PlaceAssignResponse
from app.repositories.uow import UnitOfWork
from app.repositories.exception import RepositoryNotFoundException
from app.domain.place import Place


class PlaceAssignUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: PlaceAssignCMD) -> PlaceAssignResponse:
        async with self._uow.begin():
            if not await self._uow.place_repository.exists():
                raise ParkingDontExistApiError

            try:
                user = await self._uow.user_repository.get_by_full_name(
                    last_name=cmd.last_name,
                    first_name=cmd.first_name,
                    patronymic=cmd.patronymic,  # Опционально
                )
            except RepositoryNotFoundException:
                raise UserNotFoundApiError

            place: Place = await self._uow.place_repository.get(cmd.place_id)
            place.assign(user.id)

            return PlaceAssignResponse(
                place_id=place.id,
                owner_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                patronymic=user.patronymic,
            )
