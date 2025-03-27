from uuid import UUID

from sqlalchemy import select

from app.api.user.schemas import GetFCMTokenResponse
from app.dto.session import SessionStatus
from app.persistent.db_schemas.session import device_table, session_table
from app.repositories.uow import UnitOfWork


class GetFCMTokenView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, user_id: UUID) -> GetFCMTokenResponse:
        async with self._uow.begin():
            stmt = (
                select(device_table.c.fcm_token)
                .select_from(session_table.outerjoin(device_table))
                .where(session_table.c.user_id == user_id, session_table.c.status == SessionStatus.ACTIVE.value)
                .order_by(session_table.c.updated_at.desc())
                .limit(1)
            )

            fcm_token = (await self._uow.session.execute(stmt)).scalar_one_or_none()
            return GetFCMTokenResponse(fcm_token=fcm_token)
