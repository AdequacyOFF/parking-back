from datetime import date

from fastapi import UploadFile

from app.adapters.file_storage.adapter import IFileStorageAdapter
from app.adapters.file_storage.schemas import FSAUploadFileCMD
from app.api.admin.schemas import CreatePromotionResponse
from app.api.errors.api_error import FileInvalidFormatApiError, InvalidFileExtensionApiError
from app.domain.exception import FileInvalidFormatDomainException, InvalidFileExtensionDomainException
from app.domain.promotions import Promotion
from app.dto.promotions import CreatePromotionCMD
from app.repositories.uow import UnitOfWork


class CreatePromotionUseCase:
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
        file: UploadFile,
    ) -> CreatePromotionResponse:
        async with self._uow.begin():
            promotion = Promotion.create(
                cmd=CreatePromotionCMD(
                    title=title,
                    description=description,
                    url=url,
                    start_date=start_date,
                    end_date=end_date,
                    short_description=short_description,
                )
            )

            try:
                promotion.add_photo(file=file)
            except InvalidFileExtensionDomainException:
                raise InvalidFileExtensionApiError
            except FileInvalidFormatDomainException:
                raise FileInvalidFormatApiError

            await self._adapter.upload_file(
                cmd=FSAUploadFileCMD(file_name=promotion.photo_name, file_content=file.file)
            )

            self._uow.promotion_repository.save(promotion=promotion)
        return CreatePromotionResponse()
