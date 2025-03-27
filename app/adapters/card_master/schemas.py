from app.utils.model import ApiCamelModel


class FetchCardResult(ApiCamelModel):
    card_id: str


class CAGetCardBonusesCommand(ApiCamelModel):
    card_id: str


class CAGetCardBonusesResult(ApiCamelModel):
    bonuses: float
