from uuid import UUID

from app.api.errors.api_error import UserNotFoundApiError, AccessDeniedApiError
from app.api.admin.schemas import UserDeleteResponse, UserDeleteCMD
from app.domain.exception import SessionAlreadyExpiredException
from app.dto.user import GetUserSessionForDeleteCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class UserDeleteUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, admin_id: UUID, cmd: UserDeleteCMD) -> UserDeleteResponse:
        async with self._uow.begin():

            try:
                await self._uow.admin_repository.get(admin_id=admin_id)
            except RepositoryNotFoundException as e:
                raise AccessDeniedApiError from e

            try:
                user = await self._uow.user_repository.get(user_id=cmd.delete_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            try:
                session = user.get_session_for_delete(cmd=GetUserSessionForDeleteCMD(user_id=cmd.delete_id))
            except SessionAlreadyExpiredException:
                pass

            session.expire()
            user.delete()

            await self._uow.user_repository.save(user)
            return UserDeleteResponse()
