from uuid import UUID

from app.adapters.mail.adapter import IMailAdapter
from app.adapters.mail.exceptions import MASendMailClientError
from app.adapters.mail.schemas import MASendMessageCommand
from app.api.errors.api_error import (
    InvalidUserStatusApiError,
    OrderRequestEmailSendingApiError,
    OrderRequestNotFoundApiError,
    UserNotFoundApiError,
)
from app.api.orders.schemas import OrderSubmitFeedbackCommand, OrderSubmitFeedbackResponse
from app.dto.user import SubmitFeedbackCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class SubmitFeedbackUseCase:
    def __init__(self, adapter: IMailAdapter, uow: UnitOfWork):
        self._adapter = adapter
        self._uow = uow

    async def __call__(self, command: OrderSubmitFeedbackCommand, user_id: UUID) -> OrderSubmitFeedbackResponse:

        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id=user_id)
            except RepositoryNotFoundException:
                raise UserNotFoundApiError

            if not user.can_submit_feedback:
                raise InvalidUserStatusApiError

            request = user.get_order_request(request_id=command.request_id)
            if request is None:
                raise OrderRequestNotFoundApiError

            if command.feedback_text:
                try:
                    await self._adapter.send_message(
                        cmd=MASendMessageCommand(
                            title=f"Обратная связь по заявке №{str(command.request_id)[:6]} от {request.created_at.strftime('%H:%M %d.%m.%Y')}",
                            body=(
                                f"ФИО: {user.first_name} {user.last_name}\n"
                                f"Номер телефона: {user.phone_number}\n"
                                f"Оценка: {command.feedback_score}\n"
                                f"Комментарий пользователя: {command.feedback_text}"
                            ),
                        )
                    )
                except MASendMailClientError:
                    raise OrderRequestEmailSendingApiError

            request.submit_feedback(
                cmd=SubmitFeedbackCMD(feedback_score=command.feedback_score, feedback_text=command.feedback_text)
            )

        return OrderSubmitFeedbackResponse()
