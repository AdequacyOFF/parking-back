from app.api.auth.schemas import LogoutResponse
from app.api.errors.api_error import SessionAlreadyExpiredApiError, UserNotFoundApiError
from app.domain.exception import SessionAlreadyExpiredException
from app.dto.user import GetUserSessionCMD, LogoutUserCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class LogoutUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: LogoutUserCMD) -> LogoutResponse:
        async with self._uow.begin():
            await self._uow.user_repository.get_w_exp_sessions(batch_size=10)

            try:
                user = await self._uow.user_repository.get(user_id=cmd.user_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            try:
                session = user.get_session(cmd=GetUserSessionCMD(session_id=cmd.session_id, token=cmd.refresh_token))
            except SessionAlreadyExpiredException as e:
                raise SessionAlreadyExpiredApiError from e

            session.expire()

            await self._uow.user_repository.save(user)
            return LogoutResponse()
