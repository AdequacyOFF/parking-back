from app.api.errors.api_error import SessionAlreadyExpiredApiError, UserNotFoundApiError
from app.api.token.schemas import RefreshResponse
from app.domain.exception import SessionAlreadyExpiredException
from app.dto.session import RefreshSessionCMD
from app.dto.user import GetUserSessionCMD, RefreshTokenCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import UserData


class RefreshUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: RefreshTokenCMD) -> RefreshResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id=cmd.user_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            try:
                session = user.get_session(cmd=GetUserSessionCMD(session_id=cmd.session_id, token=cmd.token))
            except SessionAlreadyExpiredException as e:
                raise SessionAlreadyExpiredApiError from e

            new_refresh_token = AuthJWT.create_refresh_token(user_data=UserData(id=user.id), jti=cmd.session_id)
            access_token = AuthJWT.create_access_token(
                user_data=UserData(id=user.id, status=user.status), jti=new_refresh_token.jti
            )

            session.refresh(cmd=RefreshSessionCMD(token=new_refresh_token.token))

            await self._uow.user_repository.save(user)
            return RefreshResponse(access=access_token.token, refresh=new_refresh_token.token)
