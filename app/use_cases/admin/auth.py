from app.api.admin.schemas import AdminAuthCommand, AdminAuthResponse
from app.api.errors.api_error import InvalidLoginOrPasswordApiError
from app.dto.admin import AdminStatus, CreateAdminSessionCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.hash import AuthHash
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import UserData


class AdminAuthUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, command: AdminAuthCommand) -> AdminAuthResponse:
        async with self._uow.begin():
            try:
                admin = await self._uow.admin_repository.get_by_username(username=command.username)
            except RepositoryNotFoundException:
                raise InvalidLoginOrPasswordApiError

            if not admin:
                raise InvalidLoginOrPasswordApiError

            if not AuthHash.verify_password(command.password, admin.password_hash):
                raise InvalidLoginOrPasswordApiError

            refresh_data = AuthJWT.create_refresh_token(user_data=UserData(id=admin.id))
            access_data = AuthJWT.create_access_token(
                user_data=UserData(id=admin.id, status=AdminStatus.ACTIVE), jti=refresh_data.jti
            )

            admin.add_session(cmd=CreateAdminSessionCMD(id=refresh_data.jti, token=refresh_data.token))
            self._uow.admin_repository.save(admin)

        return AdminAuthResponse(token=access_data.token, refresh_token=refresh_data.token)
