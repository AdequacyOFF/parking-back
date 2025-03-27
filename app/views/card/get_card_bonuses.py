from uuid import UUID

from sqlalchemy import and_, select

from app.adapters.card_master.adapter import CardMasterAdapter
from app.adapters.card_master.schemas import CAGetCardBonusesCommand
from app.api.card.schemas import GetCardBonusesResponse
from app.api.errors.api_error import CardNotFoundApiError
from app.dto.user import UserStatus
from app.persistent.db_schemas import user_card_table, user_table
from app.repositories.uow import UnitOfWork


class GetCardBonusesView:
    def __init__(self, uow: UnitOfWork, card_master_adapter: CardMasterAdapter):
        self._uow = uow
        self._card_master_adapter = card_master_adapter

    async def __call__(self, user_id: UUID) -> GetCardBonusesResponse:
        async with self._uow.begin():
            query = (
                select(user_card_table.c.qr.label("card_qr"))
                .where(and_(user_table.c.id == user_id, user_table.c.status == UserStatus.ACTIVE))
                .join(user_card_table, user_table.c.id == user_card_table.c.user_id)
            )
            user = (await self._uow.session.execute(query)).one_or_none()

            if not user:
                raise CardNotFoundApiError

            result = await self._card_master_adapter.get_card_boneses(cmd=CAGetCardBonusesCommand(card_id=user.card_qr))

            return GetCardBonusesResponse(bonuses=result.bonuses)
