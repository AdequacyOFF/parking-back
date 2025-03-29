from dataclasses import dataclass
from enum import Enum
from uuid import UUID


# ENUMS
class UserStatus(str, Enum):
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


# User
@dataclass
class RefreshTokenCMD:
    user_id: UUID
    token: str
    session_id: UUID


@dataclass
class LogoutUserCMD:
    session_id: UUID
    refresh_token: str
    user_id: UUID


@dataclass
class GetUserSessionCMD:
    session_id: UUID
    token: str


@dataclass
class GetUserSessionForDeleteCMD:
    user_id: UUID


@dataclass
class CreateUserSessionCMD:
    id: UUID
    token: str


@dataclass
class RegisterUserDTO:
    phone_number: str
    password_hash: str
    first_name: str | None
    last_name: str | None
    patronymic: str | None



