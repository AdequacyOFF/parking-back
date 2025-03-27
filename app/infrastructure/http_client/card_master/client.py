from typing import Any
from urllib.parse import urljoin

from aiohttp import AsyncResolver, ClientResponse, ClientTimeout, TCPConnector

from app.infrastructure.http_client.base import BaseHTTPClient
from app.infrastructure.http_client.card_master.schemas import CCGetCardBonusesCommand
from app.infrastructure.http_client.enums import RequestMethodType
from app.settings import settings


class CardMasterHTTPClient(BaseHTTPClient):
    async def fetch_card(self) -> dict[str, Any]:
        response = await self._make_request(
            method=RequestMethodType.POST,
            uri=f"/card",
        )
        return await response.json()

    async def get_card_bonuses(self, cmd: CCGetCardBonusesCommand) -> dict[str, Any]:
        response = await self._make_request(
            method=RequestMethodType.GET,
            uri=f"/card/{cmd.card_id}/bonuses",
        )
        return await response.json()

    async def _make_request(self, method: RequestMethodType, uri: str) -> ClientResponse:
        headers = {"X-Api-Key": settings.card_master.api_key}
        return await self._request(
            method=method,
            str_or_url=urljoin(settings.card_master.base_url, uri),
            ssl=settings.card_master.validate_cert,
            headers=headers,
            timeout=ClientTimeout(
                total=settings.card_master.total_timeout, connect=settings.card_master.connect_timeout
            ),
        )

    @staticmethod
    def get_session_config() -> dict[str, Any]:
        return {
            "connector": TCPConnector(limit=settings.card_master.connection_limit, resolver=AsyncResolver()),
        }
