from uuid import UUID

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from pydantic import Field, field_validator

from app.dto.user import DeviceType
from app.settings import settings
from app.utils.model import ApiCamelModel


class InitCMD(ApiCamelModel):
    phone_number: str = Field(examples=["+79997778855"], description="User phone number", min_length=12, max_length=50)
    use_telegram: bool = Field(False, description="Использовать телеграм")

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number: str) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except NumberParseException as e:
            raise ValueError("Invalid phone number format") from e
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        return f"{parsed_number.country_code}{parsed_number.national_number}"


class InitResponse(ApiCamelModel):
    pass


class VerifyDevice(ApiCamelModel):
    device_id: str = Field(min_length=1, max_length=256, description="Device Identifier", examples=["1234567abc"])
    fcm_token: str | None = Field(
        None, min_length=1, max_length=256, description="FCM (Firebase Cloud Messaging) Token"
    )
    type: DeviceType = Field(description="Device Type", examples=["IOS"])
    os_version: str = Field(
        min_length=1,
        max_length=50,
        pattern=r"^\d+(\.\d+){0,2}$",
        description="Operating System Version",
        examples=["10.0.1"],
    )
    app_version: str = Field(
        min_length=1, max_length=50, pattern=r"^\d+(\.\d+){0,2}$", description="Application Version", examples=["1.0.0"]
    )
    locale: str = Field(
        min_length=1, max_length=50, pattern=r"^[a-z]{2}_[A-Z]{2}$", description="Locale", examples=["en_US"]
    )
    screen_resolution: str = Field(
        min_length=1, pattern=r"^\d+x\d+$", max_length=50, description="Screen Resolution", examples=["1920x1080"]
    )


class VerifyCMD(ApiCamelModel):
    phone_number: str = Field(examples=["+79997778855"], description="User phone number", max_length=50)
    otp: str = Field(
        description="OTP code sent to user",
        examples=["576279"],
        min_length=settings.auth.otp_length,
        max_length=settings.auth.otp_length,
    )
    device: VerifyDevice = Field(description="User device info")

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number: str) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except NumberParseException as e:
            raise ValueError("Invalid phone number format") from e
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        return f"{parsed_number.country_code}{parsed_number.national_number}"


class VerifyResponse(ApiCamelModel):
    access: str = Field(description="Access token")
    refresh: str = Field(description="Refresh token")


class LogoutCMD(ApiCamelModel):
    session_id: UUID = Field(description="Session ID")
    refresh_token: str = Field(description="Token")


class LogoutResponse(ApiCamelModel):
    pass
