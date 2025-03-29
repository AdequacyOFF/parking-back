from uuid import UUID

from app.api.errors.api_error import InvalidUserStatusApiError, UserNotFoundApiError
from app.api.user.schemas import ChangeUser, ChangeUserCMD, ChangeUserResponse
from app.dto.user import UserStatus, RegisterUserDTO
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork

from app.utils.auth.hash import AuthHash


class ChangeUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: ChangeUserCMD, user_id: UUID) -> ChangeUserResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id=user_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            if user.status != UserStatus.ACTIVE:
                raise InvalidUserStatusApiError

            if cmd.password is None:
                password_hash = user.password_hash
            else:
                password_hash = AuthHash.hash_password(cmd.password)

            RegisterUserDTO(
                phone_number=getattr(cmd, 'phone_number', user.phone_number),
                password_hash=password_hash,
                first_name=getattr(cmd, 'first_name', user.first_name),
                last_name=getattr(cmd, 'last_name', user.last_name),
                patronymic=getattr(cmd, 'patronymic', user.patronymic),
            )
            user.update(**cmd.dict(exclude_unset=True))

            await self._uow.user_repository.save(user)
            return ChangeUserResponse(
                user=ChangeUser(
                    id=user.id,
                    phone_number=user.phone_number,
                    status=user.status,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    patronymic=user.patronymic,
                )
            )
