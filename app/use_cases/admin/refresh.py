from app.api.admin.schemas import AdminRefreshTokenCommand, AdminRefreshTokenResponse
from app.api.errors.api_error import AdminNotFoundApiError
from app.dto.admin import GetAdminSessionCMD
from app.dto.session import RefreshSessionCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import UserData


class AdminTokenRefreshUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: AdminRefreshTokenCommand) -> AdminRefreshTokenResponse:
        async with self._uow.begin():
            try:
                admin = await self._uow.admin_repository.get(admin_id=cmd.admin_id)
            except RepositoryNotFoundException as e:
                raise AdminNotFoundApiError from e

            session = admin.get_session(cmd=GetAdminSessionCMD(session_id=cmd.session_id, token=cmd.token))

            new_refresh_token = AuthJWT.create_refresh_token(user_data=UserData(id=admin.id), jti=cmd.session_id)
            access_token = AuthJWT.create_access_token(
                user_data=UserData(id=admin.id, status=admin.status), jti=new_refresh_token.jti
            )

            session.refresh(cmd=RefreshSessionCMD(token=new_refresh_token.token))

            self._uow.admin_repository.save(admin)
            return AdminRefreshTokenResponse(token=access_token.token, refresh_token=new_refresh_token.token)
