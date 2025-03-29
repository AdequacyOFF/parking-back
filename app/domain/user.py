from dataclasses import dataclass, field
from uuid import UUID
from app.domain.exception import (
    SessionAlreadyExpiredException,
)
from app.domain.session import Session
from app.dto.session import SessionStatus, InitSessionCMD
from app.dto.user import (
    RegisterUserDTO,
    CreateUserSessionCMD,
    GetUserSessionCMD,
    GetUserSessionForDeleteCMD,
    UserStatus,
)


@dataclass
class User:
    id: UUID
    phone_number: str
    status: UserStatus
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    sessions: list[Session] = field(default_factory=list)

    def __init__(
            self,
            id: UUID,
            phone_number: str,
            status: UserStatus,
            password_hash: str,
            first_name: str | None = None,
            last_name: str | None = None,
            patronymic: str | None = None,
    ) -> None:
        super().__init__()
        self.id = id
        self.phone_number = phone_number
        self.status = status
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.sessions = []

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_deleted(self) -> bool:
        return self.status == UserStatus.DELETED

    def update(self, **kwargs) -> None:  # type: ignore
        for filed in kwargs:
            self.__setattr__(filed, kwargs[filed])

    def delete(self) -> None:
        self.status = UserStatus.DELETED

    def add_session(self, cmd: CreateUserSessionCMD) -> None:
        self.sessions.append(Session.init(cmd=InitSessionCMD(id=cmd.id, token=cmd.token)))

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

    @classmethod
    def register(cls, cmd: RegisterUserDTO) -> "User":
        return cls(
            id=UUID(),
            phone_number=cmd.phone_number,
            status=UserStatus.REGISTERED,
            first_name=cmd.first_name,
            last_name=cmd.last_name,
            patronymic=cmd.patronymic,
            password_hash=cmd.password_hash
        )
