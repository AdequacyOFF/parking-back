from dataclasses import dataclass
from enum import Enum


class OutboxMessageStatus(str, Enum):
    PENDING = "PENDING"
    SEND = "SEND"


@dataclass
class CreateOutboxMessageCMD:
    header: str
    body: str
    topic: str
