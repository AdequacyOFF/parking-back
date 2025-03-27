from uuid import UUID

from pydantic import Field

from app.dto.card import CardState, CardType
from app.utils.model import ApiCamelModel


class GetCardInfoResponse(ApiCamelModel):
    id: UUID = Field(description="User Card ID")
    qr: str = Field(description="User Card QR-code")
    state: CardState = Field(description="User Card State")


class GetCardBonusesResponse(ApiCamelModel):
    bonuses: float = Field(description="User Card Bonuses")
