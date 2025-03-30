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


class PlaceAssignResponse(ApiCamelModel):
    place_id: int = Field(description="Place number (ID)")
    owner_id: UUID | None = Field(description="User ID")
    first_name: str | None = Field(examples=["Иван"], description="First name")
    last_name: str | None = Field(examples=["Иванов"], description="Last name")
    patronymic: str | None = Field(examples=["Иванович"], description="Patronymic")
    pass


class GetParkingResponse(ApiCamelModel):
    all_places: list[PlaceAssignResponse] = Field(description="List of all places")


