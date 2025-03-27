from datetime import date
from uuid import UUID

from fastapi import UploadFile

from app.adapters.file_storage.adapter import IFileStorageAdapter
from app.adapters.file_storage.schemas import FSADeleteFilesCMD, FSAUploadFileCMD
from app.api.admin.schemas import UpdatePromotionResponse
from app.api.errors.api_error import FileInvalidFormatApiError, InvalidFileExtensionApiError, PromotionNotFoundApiError
from app.domain.exception import FileInvalidFormatDomainException, InvalidFileExtensionDomainException
from app.dto.promotions import UpdatePromotionCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class UpdatePromotionUseCase:
    def __init__(self, adapter: IFileStorageAdapter, uow: UnitOfWork):
        self._adapter = adapter
        self._uow = uow

    async def __call__(
        self,
        title: str,
        short_description: str,
        start_date: date,
        end_date: date,
        description: str,
        url: str | None,
        promotion_id: UUID,
        file: UploadFile | None,
    ) -> UpdatePromotionResponse:
        async with self._uow.begin():
            try:
                promotion = await self._uow.promotion_repository.get(promotion_id=promotion_id)
            except RepositoryNotFoundException:
                raise PromotionNotFoundApiError

            promotion.update(
                cmd=UpdatePromotionCMD(
                    title=title,
                    description=description,
                    url=url,
                    start_date=start_date,
                    end_date=end_date,
                    short_description=short_description,
                )
            )

            if file:
                await self._adapter.delete_files(cmd=FSADeleteFilesCMD(file_paths={promotion.photo_name}))

                try:
                    promotion.add_photo(file=file)
                except InvalidFileExtensionDomainException:
                    raise InvalidFileExtensionApiError
                except FileInvalidFormatDomainException:
                    raise FileInvalidFormatApiError

                await self._adapter.upload_file(
                    cmd=FSAUploadFileCMD(file_name=promotion.photo_name, file_content=file.file)
                )

        return UpdatePromotionResponse()
