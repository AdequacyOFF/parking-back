from app.utils.model import ApiCamelModel


class CCGetCardBonusesCommand(ApiCamelModel):
    card_id: str
