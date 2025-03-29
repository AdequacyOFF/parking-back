from app.api.user.schemas import UserAuthCMD, UserAuthResponse
from app.api.errors.api_error import InvalidLoginOrPasswordApiError
from app.dto.user import UserStatus, CreateUserSessionCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.hash import AuthHash
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import UserData


class UserAuthUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, command: UserAuthCMD) -> UserAuthResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get_by_phone_number(phone_number=command.phone_number)
            except RepositoryNotFoundException:
                raise InvalidLoginOrPasswordApiError

            if not user:
                raise InvalidLoginOrPasswordApiError

            if not AuthHash.verify_password(command.password, user.password_hash):
                raise InvalidLoginOrPasswordApiError

            refresh_data = AuthJWT.create_refresh_token(user_data=UserData(id=user.id))
            access_data = AuthJWT.create_access_token(
                user_data=UserData(id=user.id, status=UserStatus.ACTIVE), jti=refresh_data.jti
            )

            user.add_session(cmd=CreateUserSessionCMD(id=refresh_data.jti, token=refresh_data.token))
            await self._uow.user_repository.save(user)

        return UserAuthResponse(token=access_data.token, refresh_token=refresh_data.token)
