from dataclasses import Field, dataclass
from enum import Enum
from uuid import UUID


class CardType(str, Enum):
    PLATINUM = "PLATINUM"
    GOLD = "GOLD"
    BRONZE = "BRONZE"


class CardState(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass
class CreateCardCMD:
    qr: str
    type: CardType
