from uuid import UUID

from sqlalchemy import select

from app.api.errors.api_error import UserNotFoundApiError, OnlyForUserApiError
from app.api.user.schemas import GetUserResponse
from app.dto.user import UserStatus
from app.persistent.db_schemas.user import user_table
from app.persistent.db_schemas.admin import admins_table
from app.repositories.uow import UnitOfWork


class GetUserView:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, user_id: UUID) -> GetUserResponse:
        async with self._uow.begin():
            if (await self._uow.session.execute(
                    select(
                        admins_table.c.id
                    ).where(admins_table.c.id == user_id)
            )).one_or_none():
                raise OnlyForUserApiError
            user = (
                await self._uow.session.execute(
                    select(
                        user_table.c.id,
                        user_table.c.phone_number,
                        user_table.c.status,
                        user_table.c.first_name,
                        user_table.c.last_name,
                        user_table.c.patronymic,
                    ).where(user_table.c.id == user_id)
                )
            ).one_or_none()

            if not user or user.status == UserStatus.DELETED:
                raise UserNotFoundApiError

            return GetUserResponse(
                id=user.id,
                phone_number=user.phone_number,
                status=user.status,
                first_name=user.first_name,
                last_name=user.last_name,
                patronymic=user.patronymic,
            )
