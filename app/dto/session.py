from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class DeviceType(str, Enum):
    IOS = "IOS"
    ANDROID = "ANDROID"


class SessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class OTPStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


@dataclass
class InitSessionCMD:
    id: UUID
    token: str
    device_id: UUID | None = None


@dataclass
class RefreshSessionCMD:
    token: str


# Device
@dataclass
class CreateDeviceCMD:
    device_id: str
    type: DeviceType
    os_version: str
    app_version: str
    locale: str
    screen_resolution: str
    fcm_token: str | None


@dataclass
class UpdateDeviceCMD:
    fcm_token: str
    type: DeviceType
    os_version: str
    app_version: str
    locale: str
    screen_resolution: str
