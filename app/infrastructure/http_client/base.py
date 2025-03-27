from abc import ABC, abstractmethod
from ssl import SSLContext
from types import SimpleNamespace
from typing import Any, Iterable, Mapping, Union

from aiohttp import BasicAuth, ClientResponse, ClientSession, ClientTimeout, Fingerprint
from aiohttp.client_exceptions import ClientError
from aiohttp.helpers import sentinel
from aiohttp.typedefs import LooseCookies, LooseHeaders, StrOrURL

from app.infrastructure.http_client.enums import ClientsEnum, RequestMethodType
from app.infrastructure.http_client.exceptions import ClientException


class BaseHTTPClient(ABC):
    def __init__(self, client_name: ClientsEnum, session: ClientSession):
        self._client_name = client_name
        self._session = session

    async def _request(
        self,
        method: RequestMethodType,
        str_or_url: StrOrURL,
        *,
        params: Mapping[str, str] | None = None,
        data: Any = None,
        json: Any | None = None,
        cookies: LooseCookies | None = None,
        headers: LooseHeaders | None = None,
        skip_auto_headers: Iterable[str] | None = None,
        auth: BasicAuth | None = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        compress: str | None = None,
        chunked: bool | None = None,
        expect100: bool = False,
        raise_for_status: bool | None = None,
        read_until_eof: bool = True,
        proxy: StrOrURL | None = None,
        proxy_auth: BasicAuth | None = None,
        timeout: Union[ClientTimeout, object] = sentinel,
        verify_ssl: bool | None = None,
        fingerprint: bytes | None = None,
        ssl_context: SSLContext | None = None,
        ssl: Union[SSLContext, bool, Fingerprint] | None = None,
        proxy_headers: LooseHeaders | None = None,
        trace_request_ctx: SimpleNamespace | None = None,
        read_bufsize: int | None = None,
    ) -> ClientResponse:
        try:
            response = await self._session.request(
                method,
                str_or_url,
                params=params,
                data=data,
                json=json,
                cookies=cookies,
                headers=headers,
                skip_auto_headers=skip_auto_headers,
                auth=auth,
                allow_redirects=allow_redirects,
                max_redirects=max_redirects,
                compress=compress,
                chunked=chunked,
                expect100=expect100,
                raise_for_status=raise_for_status,
                read_until_eof=read_until_eof,
                proxy=proxy,
                proxy_auth=proxy_auth,
                timeout=timeout,
                verify_ssl=verify_ssl,
                fingerprint=fingerprint,
                ssl_context=ssl_context,
                ssl=ssl,
                proxy_headers=proxy_headers,
                trace_request_ctx=trace_request_ctx,
                read_bufsize=read_bufsize,
            )
            return response
        except ClientError as exc:
            raise ClientException from exc

    @staticmethod
    @abstractmethod
    def get_session_config() -> dict[str, Any]:
        pass
