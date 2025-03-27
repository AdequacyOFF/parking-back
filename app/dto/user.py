from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from uuid import UUID

from app.dto.session import DeviceType


# ENUMS
class UserSexType(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class UserStatus(str, Enum):
    INIT = "INIT"
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class FuelType(str, Enum):
    FUEL92 = "FUEL92"
    FUEL95 = "FUEL95"
    DIESEL = "DIESEL"
    GAS = "GAS"


# User
@dataclass
class InitUserCMD:
    phone_number: str
    use_telegram: bool


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
    sex: UserSexType | None


@dataclass
class RegisterUserAgreementsCMD:
    user_agreement: bool
    privacy_policy: bool
    company_rules: bool


@dataclass
class RegisterUserDTO:
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    sex: UserSexType | None = field(default=None)
    birth_date: date | None = field(default=None)


@dataclass
class AcceptAgreementsCMD:
    user_agreement: bool
    privacy_policy: bool
    company_rules: bool


@dataclass
class GetUserSessionCMD:
    session_id: UUID
    token: str


@dataclass
class GetUserSessionForDeleteCMD:
    user_id: UUID


@dataclass
class CreateOrderRequestCMD:
    fuel_type: FuelType
    volume: int
    comment: str


@dataclass
class SubmitFeedbackCMD:
    feedback_text: str
    feedback_score: int
