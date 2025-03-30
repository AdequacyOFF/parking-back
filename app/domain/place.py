from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exception import SessionAlreadyExpiredException


@dataclass
class Place:
    id: int
    car_number: str | None = field(default=None)
    owner: UUID | None = field(default=None)
    is_busy: bool = field(default=False)
