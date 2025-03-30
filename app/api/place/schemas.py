from uuid import UUID

from pydantic import Field, field_validator

from app.utils.model import ApiCamelModel


class ParkingCreateCMD(ApiCamelModel):
    count: int = Field(examples=[100], description="Count of places on parking")


class ParkingCreateResponse(ApiCamelModel):
    pass


class PlaceAssignCMD(ApiCamelModel):
    first_name: str = Field(examples=["Иван"], description="First name")
    last_name: str = Field(examples=["Иванов"], description="Last name")
    patronymic: str = Field(examples=["Иванович"], description="Patronymic")
    place_id: int = Field(description="Place number (ID)")


class PlaceAssignResponse(ApiCamelModel):
    place_id: int = Field(description="Place number (ID)")
    owner_id: UUID = Field(description="User ID")
    first_name: str = Field(examples=["Иван"], description="First name")
    last_name: str = Field(examples=["Иванов"], description="Last name")
    patronymic: str = Field(examples=["Иванович"], description="Patronymic")
    pass


