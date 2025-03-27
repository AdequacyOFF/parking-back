from uuid import UUID

from app.utils.model import AppBaseModel


class NASendOTPCommand(AppBaseModel):
    user_id: UUID
    phone_number: str
    otp: str
