from uuid import UUID

from app.api.errors.api_error import UserAlreadyRegisteredApiError, UserNotFoundApiError
from app.api.user.schemas import RegisterCMD, RegisterResponse
from app.domain.exception import InvalidStatusException
from app.dto.user import RegisterUserDTO
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class RegisterUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow


    async def __call__(self, user_id: UUID, cmd: RegisterCMD) -> RegisterResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            try:
                user.register(
                    cmd=RegisterUserDTO(
                        first_name=cmd.first_name, last_name=cmd.last_name
                    )
                )
            except InvalidStatusException as e:
                raise UserAlreadyRegisteredApiError from e
            await self._uow.user_repository.save(user)

            return RegisterResponse(
                id=user.id,
                phone_number=user.phone_number,
                status=user.status,
                first_name=user.first_name,
                last_name=user.last_name,
            )
