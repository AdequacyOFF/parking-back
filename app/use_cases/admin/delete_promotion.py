from uuid import UUID

from app.adapters.file_storage.adapter import IFileStorageAdapter
from app.adapters.file_storage.schemas import FSADeleteFilesCMD
from app.api.admin.schemas import DeletePromotionResponse
from app.api.errors.api_error import PromotionNotFoundApiError
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class DeletePromotionUseCase:
    def __init__(self, adapter: IFileStorageAdapter, uow: UnitOfWork):
        self._adapter = adapter
        self._uow = uow

    async def __call__(self, promotion_id: UUID) -> DeletePromotionResponse:
        async with self._uow.begin():
            try:
                promotion = await self._uow.promotion_repository.get(promotion_id=promotion_id)
            except RepositoryNotFoundException:
                raise PromotionNotFoundApiError

            promotion.delete()
            await self._adapter.delete_files(cmd=FSADeleteFilesCMD(file_paths={promotion.photo_name}))

        return DeletePromotionResponse()
