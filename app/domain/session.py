from dataclasses import dataclass, field
from datetime import datetime, timedelta
from secrets import randbelow
from typing import Any
from uuid import UUID, uuid4

from pydantic.dataclasses import dataclass as pd_dataclass

from app.dto.session import (
    CreateDeviceCMD,
    DeviceType,
    InitSessionCMD,
    OTPStatus,
    RefreshSessionCMD,
    SessionStatus,
    UpdateDeviceCMD,
)
from app.settings import settings
from app.utils.dt_utils import get_utc_now_tz


@pd_dataclass
class OTP:
    id: UUID
    code: str
    expired_at: datetime
    attempts: int = field(default=0)
    is_used: bool = field(default=False)

    @property
    def status(self) -> OTPStatus:
        if get_utc_now_tz() > self.expired_at or self.attempts >= settings.auth.otp_max_attempts or self.is_used:
            return OTPStatus.EXPIRED
        return OTPStatus.ACTIVE

    @classmethod
    def create(cls) -> "OTP":
        return cls(
            id=uuid4(),
            code=cls._generate_otp(),
            expired_at=get_utc_now_tz() + timedelta(minutes=settings.auth.otp_valid_time_minutes),
        )

    def verify(self, code: str) -> bool:
        self.attempts += 1
        if self.code == code:
            self.is_used = True
            return True
        return False

    @staticmethod
    def _generate_otp() -> str:
        return "".join(str(randbelow(10)) for _ in range(settings.auth.otp_length))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Session:
    id: UUID
    status: SessionStatus
    token: str
    expired_at: datetime
    device_id: UUID | None = None
    user_id: UUID | None = None
    admin_id: UUID | None = None

    @classmethod
    def init(cls, cmd: InitSessionCMD) -> "Session":
        return cls(
            id=cmd.id,
            status=SessionStatus.ACTIVE,
            token=cmd.token,
            device_id=cmd.device_id,
            expired_at=cls._get_exp_dt(),
        )

    def refresh(self, cmd: RefreshSessionCMD) -> None:
        self.token = cmd.token
        self.expired_at = self._get_exp_dt()

    @property
    def is_expired(self) -> bool:
        return self.expired_at < get_utc_now_tz()

    def expire(self) -> None:
        self.status = SessionStatus.EXPIRED

    @staticmethod
    def _get_exp_dt() -> datetime:
        return get_utc_now_tz() + timedelta(seconds=settings.auth_jwt.refresh_expired_at)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Device:
    id: UUID
    device_id: str
    type: DeviceType
    os_version: str
    app_version: str
    locale: str
    screen_resolution: str
    fcm_token: str | None = field(default=None)

    @classmethod
    def create(cls, cmd: CreateDeviceCMD) -> "Device":
        return cls(
            id=uuid4(),
            device_id=cmd.device_id,
            fcm_token=cmd.fcm_token,
            type=cmd.type,
            os_version=cmd.os_version,
            app_version=cmd.app_version,
            locale=cmd.locale,
            screen_resolution=cmd.screen_resolution,
        )

    def update(self, cmd: UpdateDeviceCMD) -> None:
        self.fcm_token = cmd.fcm_token
        self.type = cmd.type
        self.os_version = cmd.os_version
        self.app_version = cmd.app_version
        self.locale = cmd.locale
        self.screen_resolution = cmd.screen_resolution

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)
