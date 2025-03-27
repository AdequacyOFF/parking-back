from typing import Any

from app.utils.model import ApiCamelModel


class KPProduceMessageCMD(ApiCamelModel):
    topic: str
    message: bytes
    headers: list[tuple[str, Any]]
