from typing import Any
from urllib.parse import urljoin

from aiohttp import AsyncResolver, ClientResponse, ClientTimeout, TCPConnector

from app.infrastructure.http_client.base import BaseHTTPClient
from app.infrastructure.http_client.enums import RequestMethodType
from app.infrastructure.http_client.telegram.schemas import TNCCheckAvailableCommand, TNCSendVerificationMessageCommand
from app.settings import settings


class TelegramNotificationsHTTPClient(BaseHTTPClient):
    async def send_otp(self, cmd: TNCSendVerificationMessageCommand) -> ClientResponse:
        response = await self._make_request(
            method=RequestMethodType.POST, uri="/sendVerificationMessage", params=cmd.dict()
        )
        return response

    async def check_available(self, cmd: TNCCheckAvailableCommand) -> ClientResponse:
        response = await self._make_request(method=RequestMethodType.POST, uri="/checkSendAbility", params=cmd.dict())
        return response

    async def _make_request(self, method: RequestMethodType, uri: str, params: dict[str, str]) -> ClientResponse:
        headers = {"Authorization": f"Bearer {settings.telegram_notifications.api_key}"}
        return await self._request(
            method=method,
            str_or_url=urljoin(settings.telegram_notifications.base_url, uri),
            params=params,
            ssl=settings.telegram_notifications.validate_cert,
            timeout=ClientTimeout(
                total=settings.telegram_notifications.total_timeout,
                connect=settings.telegram_notifications.connect_timeout,
            ),
            headers=headers,
        )

    @staticmethod
    def get_session_config() -> dict[str, Any]:
        return {
            "connector": TCPConnector(limit=settings.telegram_notifications.connection_limit, resolver=AsyncResolver()),
        }
