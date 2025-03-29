from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from app.dto.session import (
    InitSessionCMD,
    RefreshSessionCMD,
    SessionStatus,
)
from app.settings import settings
from app.utils.dt_utils import get_utc_now_tz


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
