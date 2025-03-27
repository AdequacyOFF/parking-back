from typing import Protocol

from app.adapters.notifications.exceptions import NotificationsError
from app.adapters.notifications.schemas import NASendOTPCommand
from app.infrastructure.http_client.notifications.client import NotificationsHTTPClient
from app.infrastructure.http_client.notifications.schemas import SMSCCSendSmsCommand


class INotificationsAdapter(Protocol):
    async def send_otp(self, cmd: NASendOTPCommand) -> None:
        pass


class NotificationsAdapter(INotificationsAdapter):
    def __init__(self, client: NotificationsHTTPClient):
        self._client = client

    async def send_otp(self, cmd: NASendOTPCommand) -> None:
        sms_text = f"Ваш код для входа в приложение Astra: {cmd.otp}."
        response = await self._client.send_sms(cmd=SMSCCSendSmsCommand(phones=cmd.phone_number, mes=sms_text))
        if response.status != 200:
            raise NotificationsError
