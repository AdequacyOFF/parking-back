from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class AdminStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass
class CreateAdminSessionCMD:
    id: UUID
    token: str


@dataclass
class GetAdminSessionCMD:
    session_id: UUID
    token: str

