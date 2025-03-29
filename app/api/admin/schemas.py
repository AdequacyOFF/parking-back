from uuid import UUID

from pydantic import Field, field_validator

from app.utils.model import ApiCamelModel
from app.dto.user import UserStatus

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


class AdminAuthCommand(ApiCamelModel):
    username: str = Field(description="Authorization Username", min_length=1, max_length=50)
    password: str = Field(description="Authorization Password", min_length=1, max_length=50)


class AdminAuthResponse(ApiCamelModel):
    token: str = Field(description="Authorization Admin Token")
    refresh_token: str = Field(description="Authorization Admin Refresh Token")


class AdminRefreshTokenCommand(ApiCamelModel):
    admin_id: UUID = Field(description="Admin ID")
    session_id: UUID = Field(description="Session ID")
    token: str = Field(description="Token")


class AdminRefreshTokenResponse(ApiCamelModel):
    token: str = Field(description="Authorization Admin Token")
    refresh_token: str = Field(description="Authorization Admin Refresh Token")


class UserRegisterCMD(ApiCamelModel):
    phone_number: str = Field(description="User phone number")
    first_name: str | None = Field(None, examples=["Иван"], min_length=1, max_length=50, description="User first name")
    last_name: str | None = Field(None, examples=["Иванов"], min_length=1, max_length=50, description="User last name")
    patronymic: str | None = Field(None, examples=["Иванович"], min_length=1, max_length=50,
                                   description="User patronymic")

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number: str) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except NumberParseException as e:
            raise ValueError("Invalid phone number format") from e
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        return f"{parsed_number.country_code}{parsed_number.national_number}"


class UserRegisterResponse(ApiCamelModel):
    id: UUID = Field(description="User id")
    phone_number: str = Field(description="User phone number")
    status: UserStatus = Field(description="User status")
    password: str = Field(description="User password")
    first_name: str | None = Field(None, description="User first name")
    last_name: str | None = Field(None, description="User last name")
    patronymic: str | None = Field(None, description="User patronymic")


class UserDeleteCMD(ApiCamelModel):
    delete_id: UUID = Field(description="User delete ID")


class UserDeleteResponse(ApiCamelModel):
    pass
