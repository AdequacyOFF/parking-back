from app.api.errors.api_error import ParkingAlreadyExistsApiError
from app.api.admin.schemas import ParkingCreateCMD, ParkingCreateResponse
from app.repositories.uow import UnitOfWork
from app.domain.place import Place


class ParkingCreateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: ParkingCreateCMD) -> ParkingCreateResponse:
        async with self._uow.begin():
            count = cmd.count
            if await self._uow.place_repository.exists():
                raise ParkingAlreadyExistsApiError

            for i in range(count):
                place = Place(i+1)
                self._uow.place_repository.save(place)

            return ParkingCreateResponse()
