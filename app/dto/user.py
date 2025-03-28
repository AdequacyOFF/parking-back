from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from app.dto.session import DeviceType


# ENUMS
class UserStatus(str, Enum):
    INIT = "INIT"
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


# User
@dataclass
class InitUserCMD:
    phone_number: str


@dataclass
class DeviceInfo:
    device_id: str
    type: DeviceType
    os_version: str
    app_version: str
    locale: str
    screen_resolution: str
    fcm_token: str | None


@dataclass
class VerifyOTPUserDTO:
    otp: str
    session_id: UUID
    token: str
    device: DeviceInfo


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
class RegisterUserCMD:
    first_name: str | None
    last_name: str | None


@dataclass
class RegisterUserDTO:
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)


@dataclass
class GetUserSessionCMD:
    session_id: UUID
    token: str


@dataclass
class GetUserSessionForDeleteCMD:
    user_id: UUID

