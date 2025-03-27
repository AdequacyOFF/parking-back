import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Protocol

import aiosmtplib

from app.settings import MailSettings


class ISmtpClient(Protocol):
    async def send_message(self, message_text: str, header: str) -> None:
        pass


class SmtpClient(ISmtpClient):
    def __init__(self, settings: MailSettings) -> None:
        self._settings = settings
        self._context = ssl.create_default_context()
        self._context.check_hostname = False
        self._context.verify_mode = ssl.CERT_NONE
        self._client = aiosmtplib.SMTP(
            hostname=self._settings.smtp_host, port=self._settings.smtp_port, use_tls=True, tls_context=self._context
        )

    async def send_message(self, message_text: str, header: str) -> None:
        await self._client.connect()
        await self._client.login(self._settings.smtp_username, self._settings.smtp_password)
        message = self._create_message(addr=self._settings.addr, message_text=message_text, header=header)
        await self._client.send_message(message)
        await self._client.quit()

    def _create_message(self, addr: str, message_text: str, header: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self._settings.smtp_username
        message["To"] = addr
        message["Subject"] = header
        message.attach(MIMEText(message_text, "plain"))
        return message
