from uuid import UUID

from pydantic import BaseModel, Field

from app.utils.model import ApiCamelModel


class SMSCCSendSmsCommand(BaseModel):
    phone_number: str = Field(alias="phones")
    text: str = Field(alias="mes")
