from uuid import UUID

from sqlalchemy import and_, select

from app.adapters.file_storage.adapter import IFileStorageAdapter
from app.adapters.file_storage.schemas import FSAGetFileUrlCMD
from app.api.errors.api_error import PromotionNotFoundApiError
from app.api.promotions.schemas import GetPromotionResponse
from app.dto.promotions import PromotionStatus
from app.persistent.db_schemas.promotions import promotions_table
from app.repositories.uow import UnitOfWork


class GetPromotionView:
    def __init__(self, adapter: IFileStorageAdapter, uow: UnitOfWork):
        self._adapter = adapter
        self._uow = uow

    async def __call__(self, promotion_id: UUID) -> GetPromotionResponse:
        async with self._uow.begin():
            query = select(
                promotions_table.c.id,
                promotions_table.c.title,
                promotions_table.c.photo_name,
                promotions_table.c.description,
                promotions_table.c.url,
                promotions_table.c.start_date,
                promotions_table.c.end_date,
                promotions_table.c.short_description,
            ).where(and_(promotions_table.c.id == promotion_id, promotions_table.c.status == PromotionStatus.ACTIVE))

            promotion = (await self._uow.session.execute(query)).one_or_none()
            if promotion is None:
                raise PromotionNotFoundApiError

            photo = await self._adapter.generate_file_url(cmd=FSAGetFileUrlCMD(file_name=promotion.photo_name))
            return GetPromotionResponse(
                id=promotion.id,
                title=promotion.title,
                photo=photo.url,
                description=promotion.description,
                url=promotion.url,
                start_date=promotion.start_date,
                end_date=promotion.end_date,
                short_description=promotion.short_description,
            )
