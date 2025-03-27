from typing import Protocol

from loguru import logger

from app.adapters.telegram.exceptions import TelegramNotificationsError
from app.adapters.telegram.schemas import (
    CheckAvailableResult,
    TNACheckAvailableCommand,
    TNASendVerificationMessageCommand,
)
from app.infrastructure.http_client.telegram.client import TelegramNotificationsHTTPClient
from app.infrastructure.http_client.telegram.schemas import TNCCheckAvailableCommand, TNCSendVerificationMessageCommand


class ITelegramNotificationsAdapter(Protocol):
    async def send_otp(self, cmd: TNASendVerificationMessageCommand) -> None:
        pass

    async def check_available(self, cmd: TNACheckAvailableCommand) -> CheckAvailableResult:
        pass


class TelegramNotificationsAdapter(ITelegramNotificationsAdapter):
    def __init__(self, client: TelegramNotificationsHTTPClient):
        self._client = client

    async def send_otp(self, cmd: TNASendVerificationMessageCommand) -> None:
        response = await self._client.send_otp(
            cmd=TNCSendVerificationMessageCommand(
                phone_number=f"+{cmd.phone_number}", code=int(cmd.code), request_id=cmd.request_id, ttl=60 * 5
            )
        )
        result = await response.json()
        logger.debug(result)
        if response.status != 200:
            raise TelegramNotificationsError

    async def check_available(self, cmd: TNACheckAvailableCommand) -> CheckAvailableResult:
        response = await self._client.check_available(cmd=TNCCheckAvailableCommand(phone_number=f"+{cmd.phone_number}"))
        if response.status == 200:
            result = await response.json()
            return CheckAvailableResult(request_id=result["result"]["request_id"], status=True)
        else:
            return CheckAvailableResult(request_id=None, status=False)
