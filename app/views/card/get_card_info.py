from uuid import UUID

from sqlalchemy import select

from app.adapters.card_master.adapter import CardMasterAdapter
from app.api.card.schemas import GetCardInfoResponse
from app.api.errors.api_error import InvalidUserStatusApiError
from app.dto.card import CardState
from app.dto.user import UserStatus
from app.persistent.db_schemas.user import user_card_table, user_table
from app.repositories.uow import UnitOfWork


class GetCardInfoView:
    def __init__(self, uow: UnitOfWork, card_master_adapter: CardMasterAdapter):
        self._uow = uow
        self._card_master_adapter = card_master_adapter

    async def __call__(self, user_id: UUID) -> GetCardInfoResponse:
        async with self._uow.begin():
            user = await self._uow.user_repository.get(user_id)
            if user.status != UserStatus.ACTIVE:
                raise InvalidUserStatusApiError

            stmt = (
                select(
                    user_card_table.c.id,
                    user_card_table.c.qr,
                    user_card_table.c.state,
                )
                .join(user_table, user_table.c.id == user_card_table.c.user_id)
                .where(
                    user_table.c.id == user_id,
                    user_table.c.status == UserStatus.ACTIVE,
                    user_card_table.c.state == CardState.ACTIVE,
                )
            )

            card = (await self._uow.session.execute(stmt)).one_or_none()

            return GetCardInfoResponse(id=card.id, qr=card.qr, state=card.state)
