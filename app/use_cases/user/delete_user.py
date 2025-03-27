from uuid import UUID

from app.api.errors.api_error import SessionAlreadyExpiredApiError, UserNotFoundApiError
from app.api.user.schemas import DeleteUserResponse
from app.domain.exception import SessionAlreadyExpiredException
from app.dto.user import GetUserSessionForDeleteCMD
from app.infrastructure.metrics import MetricClient, MetricsType
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class DeleteUserUseCase:
    def __init__(self, uow: UnitOfWork, metric_manager: MetricClient):
        self._uow = uow
        self._metric_manager = metric_manager

    async def __call__(self, user_id: UUID) -> DeleteUserResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id=user_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            try:
                session = user.get_session_for_delete(cmd=GetUserSessionForDeleteCMD(user_id=user_id))
            except SessionAlreadyExpiredException as e:
                raise SessionAlreadyExpiredApiError from e

            session.expire()
            user.delete()

            await self._uow.user_repository.save(user)
            self._metric_manager.register_metric(MetricsType.DELETED_USER)
            return DeleteUserResponse()
