from uuid import UUID

from app.api.errors.api_error import UserAlreadyRegisteredApiError, AccessDeniedApiError
from app.api.admin.schemas import UserRegisterCMD, UserRegisterResponse
from app.dto.user import RegisterUserDTO
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.hash import AuthHash
from app.domain.user import User

import secrets
import string


class UserRegisterUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, admin_id: UUID, cmd: UserRegisterCMD) -> UserRegisterResponse:
        async with self._uow.begin():
            try:
                await self._uow.admin_repository.get(admin_id=admin_id)
            except RepositoryNotFoundException as e:
                raise AccessDeniedApiError from e

            numbers = await self._uow.user_repository.get_all_phone_numbers()
            if cmd.phone_number in numbers:
                raise UserAlreadyRegisteredApiError

            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(alphabet) for _ in range(8))
            password_hash = AuthHash.hash_password(password)

            user = User.register(
                cmd=RegisterUserDTO(
                    phone_number=cmd.phone_number,
                    password_hash=password_hash,
                    first_name=cmd.first_name,
                    last_name=cmd.last_name,
                    patronymic=cmd.patronymic,
                )
            )

            await self._uow.user_repository.save(user)

            return UserRegisterResponse(
                id=user.id,
                phone_number=user.phone_number,
                status=user.status,
                first_name=user.first_name,
                last_name=user.last_name,
                patronymic=user.patronymic,
                password=password
            )
