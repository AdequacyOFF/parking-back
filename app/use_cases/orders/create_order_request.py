from uuid import UUID

from app.adapters.mail.adapter import IMailAdapter
from app.adapters.mail.exceptions import MASendMailClientError
from app.adapters.mail.schemas import MASendMessageCommand
from app.api.errors.api_error import InvalidUserStatusApiError, OrderRequestEmailSendingApiError, UserNotFoundApiError
from app.api.orders.schemas import CreateOrderRequestCommand, CreateOrderRequestResponse
from app.domain.user import OrderRequest
from app.dto.user import CreateOrderRequestCMD, FuelType
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class CreateOrderRequestUseCase:
    def __init__(self, adapter: IMailAdapter, uow: UnitOfWork):
        self._adapter = adapter
        self._uow = uow
        self._fuel_mapper: dict[FuelType, str] = {
            FuelType.FUEL92: "АИ-92",
            FuelType.FUEL95: "АИ-95",
            FuelType.DIESEL: "Дизель",
            FuelType.GAS: "Газ",
        }

    async def __call__(self, command: CreateOrderRequestCommand, user_id: UUID) -> CreateOrderRequestResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id=user_id)
            except RepositoryNotFoundException:
                raise UserNotFoundApiError

            if not user.can_create_order_request:
                raise InvalidUserStatusApiError

            request = OrderRequest.create(
                cmd=CreateOrderRequestCMD(fuel_type=command.fuel_type, volume=command.volume, comment=command.comment)
            )

            try:
                await self._adapter.send_message(
                    cmd=MASendMessageCommand(
                        title=f"Заявка №{str(request.id)[:6]} от {request.created_at.strftime('%H:%M %d.%m.%Y')}",
                        body=(
                            f"ФИО: {user.first_name} {user.last_name}\n"
                            f"Номер телефона: {user.phone_number}\n"
                            f"Тип топлива: {self._fuel_mapper[command.fuel_type]}\n"
                            f"Комментарий к заказу: {command.comment}"
                        ),
                    )
                )
            except MASendMailClientError:
                raise OrderRequestEmailSendingApiError

            user.create_request(request=request)

        return CreateOrderRequestResponse(request_id=request.id)
