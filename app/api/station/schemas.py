from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


class OilData(ApiCamelModel):
    id: UUID = Field(description="Oil ID")
    title: str = Field(description="Oil Title")
    price: int = Field(description="Oil Price")


class GetOilsResponse(ApiCamelModel):
    oils: list[OilData] = Field(description="Gas Station Oils")


class ServicesData(ApiCamelModel):
    id: UUID = Field(description="Oil ID")
    title: str = Field(description="Oil Title")


class GetServicesResponse(ApiCamelModel):
    services: list[ServicesData] = Field(description="Gas Station Service Provided")


class CoordinatesData(ApiCamelModel):
    latitude: float = Field(description="Latitude")
    longitude: float = Field(description="Longitude")


class StationData(ApiCamelModel):
    id: UUID = Field(description="Gas Station ID")
    name: str = Field(description="Gas Station Name")
    address: str = Field(description="Gas Station Address")
    coordinates: CoordinatesData = Field(description="Gas Station Coordinates")
    distance: int | None = Field(description="Gas Station Distance")
    services: list[ServicesData] = Field(description="Gas Station Service Provided")
    oils: list[OilData] = Field(description="Gas Station Oils")


class GetGasStationsResponse(ApiCamelModel):
    stations: list[StationData] = Field(description="Stations List Data")
