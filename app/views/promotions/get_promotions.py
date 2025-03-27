from sqlalchemy import desc, func, select

from app.adapters.file_storage.adapter import IFileStorageAdapter
from app.adapters.file_storage.schemas import FSAGetFileUrlCMD
from app.api.promotions.schemas import GetPromotionsResponse, PromotionData
from app.dto.promotions import PromotionStatus
from app.persistent.db_schemas.promotions import promotions_table
from app.repositories.uow import UnitOfWork


class GetPromotionsView:
    def __init__(self, adapter: IFileStorageAdapter, uow: UnitOfWork):
        self._adapter = adapter
        self._uow = uow

    async def __call__(self, limit: int, offset: int) -> GetPromotionsResponse:
        async with self._uow.begin():
            query = (
                (
                    select(
                        promotions_table.c.id,
                        promotions_table.c.title,
                        promotions_table.c.short_description,
                        promotions_table.c.photo_name,
                        promotions_table.c.start_date,
                        promotions_table.c.end_date,
                    )
                    .limit(limit)
                    .offset(offset)
                )
                .where(promotions_table.c.status == PromotionStatus.ACTIVE)
                .order_by(desc(promotions_table.c.created_at))
            )

            result = (await self._uow.session.execute(query)).all()
            total = (
                await self._uow.session.execute(
                    select(func.count(promotions_table.c.id)).where(promotions_table.c.status == PromotionStatus.ACTIVE)
                )
            ).scalar()

            if not result:
                return GetPromotionsResponse()

            photo_urls = {
                p.id: (await self._adapter.generate_file_url(cmd=FSAGetFileUrlCMD(file_name=p.photo_name))).url
                for p in result
            }
            return GetPromotionsResponse(
                total=total,
                promotions=[
                    PromotionData(
                        id=p.id,
                        title=p.title,
                        photo=photo_urls.get(p.id),
                        short_description=p.short_description,
                        start_date=p.start_date,
                        end_date=p.end_date,
                    )
                    for p in result
                ],
            )
