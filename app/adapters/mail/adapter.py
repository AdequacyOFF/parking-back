from typing import Protocol

from app.adapters.mail.schemas import MASendMessageCommand


class IMailAdapter(Protocol):
    async def send_message(self, cmd: MASendMessageCommand) -> None:
        pass
