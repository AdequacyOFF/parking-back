from pydantic import BaseModel, Field


class TNCSendVerificationMessageCommand(BaseModel):
    phone_number: str = Field(description="Номер телефона")
    request_id: str = Field(description="Номер запроса")
    code: int = Field(description="OTP код")
    ttl: int = Field(description="Время жизни кода")


class TNCCheckAvailableCommand(BaseModel):
    phone_number: str = Field(description="Номер телефона")
