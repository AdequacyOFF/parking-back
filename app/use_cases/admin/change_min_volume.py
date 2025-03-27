from app.api.admin.schemas import ChangeMinFuelVolumeCommand, ChangeMinFuelVolumeResponse
from app.domain.admin import Admin
from app.dto.admin import ChangeMinFuelVolume
from app.repositories.uow import UnitOfWork


class ChangeMinFuelVolumeUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, command: ChangeMinFuelVolumeCommand, admin: Admin) -> ChangeMinFuelVolumeResponse:
        async with self._uow.begin():
            admin.change_min_fuel_volume(cmd=ChangeMinFuelVolume(volume=command.volume))
            self._uow.admin_repository.save(admin)

        return ChangeMinFuelVolumeResponse()
