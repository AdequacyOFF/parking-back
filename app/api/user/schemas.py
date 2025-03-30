from uuid import UUID

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from pydantic import Field, field_validator

from app.dto.user import UserStatus
from app.utils.model import ApiCamelModel


class UserAuthCMD(ApiCamelModel):
    phone_number: str = Field(description="Authorization Username", min_length=1, max_length=50)
    password: str = Field(description="Authorization Password", min_length=8, max_length=20)

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number: str) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except NumberParseException as e:
            raise ValueError("Invalid phone number format") from e
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        return f"{parsed_number.country_code}{parsed_number.national_number}"


class UserAuthResponse(ApiCamelModel):
    token: str = Field(description="Authorization User Token")
    refresh_token: str = Field(description="Authorization User Refresh Token")


class GetUserResponse(ApiCamelModel):
    id: UUID = Field(description="User ID")
    phone_number: str = Field(description="User phone number")
    status: UserStatus = Field(description="User status")
    first_name: str | None = Field(description="User first name")
    last_name: str | None = Field(description="User last name")
    patronymic: str | None = Field(description="User patronymic")
    places_id: list[str] = Field(description="User places id")


class ChangeUserCMD(ApiCamelModel):
    first_name: str | None = Field(None, examples=["Иван"], min_length=1, max_length=50, description="User first name")
    last_name: str | None = Field(None, examples=["Иванов"], min_length=1, max_length=50, description="User last name")
    patronymic: str | None = Field(None, examples=["Иванович"], min_length=1, max_length=50,
                                   description="User patronymic")
    phone_number: str | None = Field(None, examples=["+79997778855"], min_length=1
                                     , max_length=50, description="User phone number")
    password: str | None = Field(None, examples=["********"], min_length=8, max_length=16, description="User password")

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number: str | None) -> str | None:
        if phone_number:
            try:
                parsed_number = phonenumbers.parse(f"+{phone_number}")
            except NumberParseException as e:
                raise ValueError("Invalid phone number format") from e
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number")
            return f"{parsed_number.country_code}{parsed_number.national_number}"
        return None

    @field_validator("first_name")
    def validate_first_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if all(i.isalpha() or i in (" ", "-") for i in v):
            return v.strip()
        raise ValueError("first_name must contain only letters")

    @field_validator("last_name")
    def validate_last_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if all(i.isalpha() or i in (" ", "-") for i in v):
            return v.strip()
        raise ValueError("last_name must contain only letters")

    @field_validator("patronymic")
    def validate_last_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if all(i.isalpha() or i in (" ", "-") for i in v):
            return v.strip()
        raise ValueError("patronymic must contain only letters")


class ChangeUser(ApiCamelModel):
    id: UUID = Field(description="User id")
    phone_number: str = Field(description="User phone number")
    status: UserStatus = Field(description="User status")
    first_name: str | None = Field(description="User first name")
    last_name: str | None = Field(description="User last name")
    patronymic: str | None = Field(None, description="User patronymic")

    @field_validator("first_name")
    def validate_first_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if all(i.isalpha() or i in (" ", "-") for i in v):
            return v.strip()
        raise ValueError("first_name must contain only letters")

    @field_validator("last_name")
    def validate_last_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if all(i.isalpha() or i in (" ", "-") for i in v):
            return v.strip()
        raise ValueError("last_name must contain only letters")

    @field_validator("patronymic")
    def validate_last_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if all(i.isalpha() or i in (" ", "-") for i in v):
            return v.strip()
        raise ValueError("patronymic must contain only letters")


class ChangeUserResponse(ApiCamelModel):
    user: ChangeUser = Field(description="User Data")




