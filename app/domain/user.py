from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.exception import (
    InvalidOTPException,
    InvalidStatusException,
    OTPExpiredException,
    OTPSendTimeoutException,
    SessionAlreadyExpiredException,
)
from app.domain.session import OTP, Device, Session
from app.dto.session import CreateDeviceCMD, InitSessionCMD, OTPStatus, SessionStatus, UpdateDeviceCMD
from app.dto.user import (
    DeviceInfo,
    GetUserSessionCMD,
    GetUserSessionForDeleteCMD,
    InitUserCMD,
    RegisterUserDTO,
    UserStatus,
    VerifyOTPUserDTO,
)
from app.utils.dt_utils import get_now_as_tz, get_utc_now_tz


@dataclass
class OrderRequest:
    id: UUID
    fuel_type: str
    volume: int
    comment: str
    created_at: datetime = field(default=get_now_as_tz())
    feedback_score: int | None = field(default=None)
    feedback_text: str | None = field(default=None)


@dataclass
class User:
    id: UUID
    phone_number: str
    status: UserStatus
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    otp_code: OTP | None = field(default=None)
    sessions: list[Session] = field(default_factory=list)
    devices: set[Device] = field(default_factory=set)

    def __init__(
        self,
        id: UUID,
        phone_number: str,
        status: UserStatus,
        first_name: str | None = None,
        last_name: str | None = None,
        otp_code: OTP | None = None,
    ) -> None:
        super().__init__()
        self.id = id
        self.phone_number = phone_number
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.otp_code = otp_code
        self.sessions = []
        self.devices = set()

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def can_add_otp(self) -> bool:
        if self.otp_code is None or self.otp_code.expired_at < get_utc_now_tz():
            return True
        return False

    @property
    def can_register(self) -> bool:
        return self.status in (UserStatus.INIT, UserStatus.DELETED)

    @property
    def is_deleted(self) -> bool:
        return self.status == UserStatus.DELETED

    @classmethod
    def init(cls, cmd: InitUserCMD) -> "User":
        user = cls(id=uuid4(), phone_number=cmd.phone_number, status=UserStatus.INIT)
        return user

    def update(self, **kwargs) -> None:  # type: ignore
        for filed in kwargs:
            self.__setattr__(filed, kwargs[filed])

    def delete(self) -> None:
        self.status = UserStatus.DELETED

    def add_otp(self, otp: OTP) -> None:
        if not self.can_add_otp:
            raise OTPSendTimeoutException
        self.otp_code = otp

    def verify_otp(self, cmd: VerifyOTPUserDTO) -> None:
        if self.otp_code is None or self.otp_code.status != OTPStatus.ACTIVE:
            raise OTPExpiredException
        if not self.otp_code.verify(code=cmd.otp):
            raise InvalidOTPException

        device_id = self._add_or_update_device(
            device_info=DeviceInfo(
                device_id=cmd.device.device_id,
                fcm_token=cmd.device.fcm_token,
                type=cmd.device.type,
                os_version=cmd.device.os_version,
                app_version=cmd.device.app_version,
                locale=cmd.device.locale,
                screen_resolution=cmd.device.screen_resolution,
            )
        )
        self.sessions.append(Session.init(cmd=InitSessionCMD(id=cmd.session_id, token=cmd.token, device_id=device_id)))

    def register(self, cmd: RegisterUserDTO) -> None:
        if not self.can_register:
            raise InvalidStatusException
        self.status = UserStatus.REGISTERED
        self.first_name = cmd.first_name
        self.last_name = cmd.last_name

    def get_session(self, cmd: GetUserSessionCMD) -> Session:
        for session in self.sessions:
            if session.id == cmd.session_id and session.token == cmd.token:
                if session.is_expired or session.status == SessionStatus.EXPIRED:
                    break
                return session
        raise SessionAlreadyExpiredException

    def get_session_for_delete(self, cmd: GetUserSessionForDeleteCMD) -> Session:
        for session in self.sessions:
            if session.user_id == cmd.user_id:
                if session.is_expired or session.status == SessionStatus.EXPIRED:
                    break
                return session
        raise SessionAlreadyExpiredException

    def _add_or_update_device(self, device_info: DeviceInfo) -> UUID:
        try:
            device = next(d for d in self.devices if d.device_id == device_info.device_id)
            device.update(
                cmd=UpdateDeviceCMD(
                    fcm_token=device_info.fcm_token,
                    type=device_info.type,
                    os_version=device_info.os_version,
                    app_version=device_info.app_version,
                    locale=device_info.locale,
                    screen_resolution=device_info.screen_resolution,
                )
            )
        except StopIteration:
            device = Device.create(
                cmd=CreateDeviceCMD(
                    device_id=device_info.device_id,
                    fcm_token=device_info.fcm_token,
                    type=device_info.type,
                    os_version=device_info.os_version,
                    app_version=device_info.app_version,
                    locale=device_info.locale,
                    screen_resolution=device_info.screen_resolution,
                )
            )
            self.devices.add(device)
        return device.id
