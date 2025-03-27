from app.domain.user import OTP
from app.utils.model import ApiCamelModel


class TNASendVerificationMessageCommand(ApiCamelModel):
    phone_number: str
    code: str
    request_id: str


class TNACheckAvailableCommand(ApiCamelModel):
    phone_number: str


class CheckAvailableResult(ApiCamelModel):
    request_id: str | None = None
    status: bool
