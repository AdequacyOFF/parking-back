from app.adapters.notifications.adapter import NotificationsAdapter
from app.adapters.notifications.schemas import NASendOTPCommand
from app.adapters.telegram.adapter import TelegramNotificationsAdapter
from app.adapters.telegram.schemas import TNACheckAvailableCommand, TNASendVerificationMessageCommand
from app.api.auth.schemas import InitResponse
from app.api.errors.api_error import OTPSendTimeoutApiError
from app.domain.exception import OTPSendTimeoutException
from app.domain.user import OTP, User
from app.dto.user import InitUserCMD
from app.infrastructure.metrics import MetricClient, MetricsType
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.settings import Settings


class InitUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        settings: Settings,
        metric_manager: MetricClient,
        notifications_adapter: NotificationsAdapter,
        telegram_notification_adapter: TelegramNotificationsAdapter,
    ):
        self._uow = uow
        self._settings = settings
        self._metric_manager = metric_manager
        self._notifications_adapter = notifications_adapter
        self._telegram_notification_adapter = telegram_notification_adapter

    async def __call__(self, cmd: InitUserCMD) -> InitResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get_by_phone_number(cmd.phone_number)
            except RepositoryNotFoundException:
                user = User.init(cmd=InitUserCMD(phone_number=cmd.phone_number, use_telegram=False))

                self._metric_manager.register_metric(MetricsType.CREATED_USER)

            try:
                otp = OTP.create()
                user.add_otp(otp)
            except OTPSendTimeoutException as e:
                raise OTPSendTimeoutApiError from e

            if not self._settings.notifications.is_enabled or cmd.phone_number == "79999999999":
                otp.code = "2" * self._settings.auth.otp_length
            else:
                if not user.otp_code:
                    raise RuntimeError
            if cmd.use_telegram and self._settings.telegram_notifications.is_enabled:
                result = await self._telegram_notification_adapter.check_available(
                    cmd=TNACheckAvailableCommand(phone_number=user.phone_number)
                )
                if result.status and result.request_id:
                    await self._telegram_notification_adapter.send_otp(
                        cmd=TNASendVerificationMessageCommand(
                            request_id=result.request_id, code=user.otp_code.code, phone_number=user.phone_number
                        )
                    )
                elif self._settings.notifications.is_enabled:
                    await self._notifications_adapter.send_otp(
                        cmd=NASendOTPCommand(
                            user_id=user.id,
                            phone_number=f"+{user.phone_number}",
                            otp=str(user.otp_code.code),
                        )
                    )
            elif self._settings.notifications.is_enabled:
                await self._notifications_adapter.send_otp(
                    cmd=NASendOTPCommand(
                        user_id=user.id,
                        phone_number=f"+{user.phone_number}",
                        otp=str(user.otp_code.code),
                    )
                )
            await self._uow.user_repository.save(user=user)
            return InitResponse()
