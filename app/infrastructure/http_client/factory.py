import asyncio
from typing import Any, Type
from uuid import UUID

import aiohttp
import orjson
from aiohttp import ClientSession

from app.infrastructure.http_client.base import BaseHTTPClient
from app.infrastructure.http_client.card_master.client import CardMasterHTTPClient
from app.infrastructure.http_client.enums import ClientsEnum
from app.infrastructure.http_client.notifications.client import NotificationsHTTPClient
from app.infrastructure.http_client.telegram.client import TelegramNotificationsHTTPClient


class HttpClientsFactory:
    _clients_mapping: dict[ClientsEnum, Type[BaseHTTPClient]] = {
        ClientsEnum.NOTIFICATIONS: NotificationsHTTPClient,
        ClientsEnum.CARD_MASTER: CardMasterHTTPClient,
        ClientsEnum.TELEGRAM_NOTIFICATION: TelegramNotificationsHTTPClient,
    }
    _sessions: dict[ClientsEnum, ClientSession] = {}

    def __call__(self, client_name: ClientsEnum) -> BaseHTTPClient:
        if client_name not in self._sessions:
            raise RuntimeError(f"Init session for {client_name} first.")
        session = self._sessions[client_name]
        client_class: Type[BaseHTTPClient] = self._clients_mapping[client_name]
        return client_class(client_name, session)

    @classmethod
    async def init_all(cls) -> None:
        for client in ClientsEnum:
            await cls.init(client)

    @classmethod
    async def init(cls, client_name: ClientsEnum) -> None:
        client_class = cls._clients_mapping[client_name]

        params = client_class.get_session_config()
        session = aiohttp.ClientSession(**params, json_serialize=cls._serialize_json)
        cls._sessions[client_name] = session

    @staticmethod
    def _serialize_json(val: Any) -> str:
        def default(obj: Any) -> Any:
            if isinstance(obj, UUID):
                return str(obj)
            raise TypeError

        return orjson.dumps(val, default=default).decode()

    @classmethod
    async def close_all(cls) -> None:
        await asyncio.sleep(0.250)

        for _, session in cls._sessions.items():
            await session.close()
