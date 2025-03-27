from typing import Protocol

from app.adapters.mail.exceptions import MASendMailClientError
from app.adapters.mail.schemas import MASendMessageCommand
from app.infrastructure.smtp import ISmtpClient, SmtpClient


class IMailAdapter(Protocol):
    async def send_message(self, cmd: MASendMessageCommand) -> None:
        pass


class MailAdapter(IMailAdapter):
    def __init__(self, client: ISmtpClient):
        self._client = client

    async def send_message(self, cmd: MASendMessageCommand) -> None:
        try:
            await self._client.send_message(message_text=cmd.body, header=cmd.title)
        except Exception as e:
            raise MASendMailClientError from e
