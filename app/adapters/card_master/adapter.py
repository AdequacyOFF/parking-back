from typing import Protocol

from app.adapters.card_master.exception import CardExceedAdapterError
from app.adapters.card_master.schemas import CAGetCardBonusesCommand, CAGetCardBonusesResult, FetchCardResult
from app.infrastructure.http_client.card_master.client import CardMasterHTTPClient
from app.infrastructure.http_client.card_master.schemas import CCGetCardBonusesCommand


class ICardMasterAdapter(Protocol):
    async def fetch_card(self) -> FetchCardResult:
        pass


class CardMasterAdapter(ICardMasterAdapter):
    def __init__(self, client: CardMasterHTTPClient) -> None:
        self._client = client

    async def fetch_card(self) -> FetchCardResult:
        result = await self._client.fetch_card()
        if "result" not in result:
            raise CardExceedAdapterError
        return FetchCardResult(card_id=result["result"]["cardId"])

    async def get_card_boneses(self, cmd: CAGetCardBonusesCommand) -> CAGetCardBonusesResult:
        result = await self._client.get_card_bonuses(cmd=CCGetCardBonusesCommand(card_id=cmd.card_id))
        return CAGetCardBonusesResult(bonuses=result["result"]["bonuses"])
