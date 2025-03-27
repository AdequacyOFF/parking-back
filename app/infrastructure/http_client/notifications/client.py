from typing import Any
from urllib.parse import urljoin

from aiohttp import AsyncResolver, ClientResponse, ClientTimeout, TCPConnector

from app.infrastructure.http_client.base import BaseHTTPClient
from app.infrastructure.http_client.enums import RequestMethodType
from app.infrastructure.http_client.notifications.schemas import SMSCCSendSmsCommand
from app.settings import settings


class NotificationsHTTPClient(BaseHTTPClient):
    async def send_sms(self, cmd: SMSCCSendSmsCommand) -> ClientResponse:
        response = await self._make_request(
            method=RequestMethodType.POST, uri="/sys/send.php", params=cmd.dict(by_alias=True)
        )
        return response

    async def _make_request(self, method: RequestMethodType, uri: str, params: dict[str, str]) -> ClientResponse:
        params["login"] = settings.notifications.user
        params["psw"] = settings.notifications.password

        return await self._request(
            method=method,
            str_or_url=urljoin(settings.notifications.base_url, uri),
            params=params,
            ssl=settings.notifications.validate_cert,
            timeout=ClientTimeout(
                total=settings.notifications.total_timeout, connect=settings.notifications.connect_timeout
            ),
        )

    @staticmethod
    def get_session_config() -> dict[str, Any]:
        return {
            "connector": TCPConnector(limit=settings.notifications.connection_limit, resolver=AsyncResolver()),
        }
