from datetime import date
from uuid import UUID

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from pydantic import Field, field_validator

from app.api.errors.api_error import AgreementsNotAcceptedApiError
from app.dto.user import UserSexType, UserStatus
from app.utils.model import ApiCamelModel


class GetUserResponse(ApiCamelModel):
    id: UUID = Field(description="User ID")
    phone_number: str = Field(description="User phone number")
    status: UserStatus = Field(description="User status")
    first_name: str | None = Field(description="User first name")
    last_name: str | None = Field(description="User last name")
    sex: UserSexType | None = Field(description="User sex")
    birth_date: date | None = Field(description="User birth date")


class ChangeUserCMD(ApiCamelModel):
    first_name: str | None = Field(None, examples=["Иван"], min_length=1, max_length=50, description="User first name")
    last_name: str | None = Field(None, examples=["Иванов"], min_length=1, max_length=50, description="User last name")
    phone_number: str = Field(examples=["+79997778855"], min_length=1, max_length=50, description="User phone number")
    sex: UserSexType | None = Field(None, description="User sex")
    birth_date: date | None = Field(description="User birth date")

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


class ChangeUser(ApiCamelModel):
    id: UUID = Field(description="User id")
    phone_number: str = Field(description="User phone number")
    status: UserStatus = Field(description="User status")
    first_name: str | None = Field(description="User first name")
    last_name: str | None = Field(description="User last name")
    sex: UserSexType | None = Field(description="User sex")
    birth_date: date | None = Field(description="User birth date")


class ChangeUserResponse(ApiCamelModel):
    user: ChangeUser = Field(description="User Data")


class RegisterCMD(ApiCamelModel):
    first_name: str | None = Field(None, examples=["Иван"], min_length=1, max_length=50, description="User first name")
    last_name: str | None = Field(None, examples=["Иванов"], min_length=1, max_length=50, description="User last name")
    sex: UserSexType | None = Field(None, description="User sex")
    birth_date: date | None = Field(None, description="User birth date")

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


class RegisterResponse(ApiCamelModel):
    id: UUID = Field(description="User id")
    phone_number: str = Field(description="User phone number")
    status: UserStatus = Field(description="User status")
    first_name: str | None = Field(None, description="User first name")
    last_name: str | None = Field(None, description="User last name")
    sex: UserSexType | None = Field(None, description="User sex")
    birth_date: date | None = Field(description="User birth date")


class RegisterAgreementsCMD(ApiCamelModel):
    user_agreement: bool = Field(description="Accepted User Agreement")
    privacy_policy: bool = Field(description="Privacy Policy")
    company_rules: bool = Field(description="Privacy Policy")

    @field_validator("user_agreement")
    def validate_user_agreement(cls, v: bool) -> bool:
        if not v:
            raise AgreementsNotAcceptedApiError
        return v

    @field_validator("privacy_policy")
    def validate_privacy_policy(cls, v: bool) -> bool:
        if not v:
            raise AgreementsNotAcceptedApiError
        return v

    @field_validator("company_rules")
    def validate_company_rules(cls, v: bool) -> bool:
        if not v:
            raise AgreementsNotAcceptedApiError
        return v


class RegisterAgreementsResponse(ApiCamelModel):
    pass


class GetFCMTokenResponse(ApiCamelModel):
    fcm_token: str | None = Field(description="FCM token")


class DeleteUserResponse(ApiCamelModel):
    pass
