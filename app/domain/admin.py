from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exception import SessionAlreadyExpiredException
from app.domain.user import Session
from app.dto.admin import AdminStatus, ChangeMinFuelVolume, CreateAdminSessionCMD, GetAdminSessionCMD
from app.dto.session import InitSessionCMD, SessionStatus


@dataclass
class Admin:
    id: UUID
    name: str
    status: AdminStatus
    username: str
    password_hash: str
    min_fuel_volume: int
    sessions: list[Session] = field(default_factory=list)

    def add_session(self, cmd: CreateAdminSessionCMD) -> None:
        self.sessions.append(Session.init(cmd=InitSessionCMD(id=cmd.id, token=cmd.token)))

    def get_session(self, cmd: GetAdminSessionCMD) -> Session:
        for session in self.sessions:
            if session.id == cmd.session_id and session.token == cmd.token:
                if session.is_expired or session.status == SessionStatus.EXPIRED:
                    break
                return session
        raise SessionAlreadyExpiredException

    def change_min_fuel_volume(self, cmd: ChangeMinFuelVolume) -> None:
        self.min_fuel_volume = cmd.volume
