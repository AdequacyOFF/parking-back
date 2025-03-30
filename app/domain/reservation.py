from dataclasses import dataclass, field
from uuid import UUID

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.utils.dt_utils import get_now_as_tz

from app.domain.exception import SessionAlreadyExpiredException



@dataclass
class Reservation:
    id: int
    place_id: str
    reserved_by: UUID
    reserved_from: datetime = field(default=get_now_as_tz)
    reserved_to: datetime = field(default=get_now_as_tz)

