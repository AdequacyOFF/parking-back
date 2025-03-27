from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import Field

from app.dto.user import FuelType
from app.utils.model import ApiCamelModel


class CoordinatesData(ApiCamelModel):
    latitude: float = Field(description="Latitude")
    longitude: float = Field(description="Longitude")


class StationData(ApiCamelModel):
    id: UUID = Field(description="Gas Station ID")
    name: str = Field(description="Gas Station Name")
    address: str = Field(description="Gas Station Address")
    coordinates: CoordinatesData = Field(description="Gas Station Coordinates")


class OrderData(ApiCamelModel):
    id: UUID = Field(description="Order ID")
    created_at: datetime = Field(description="Order Creation Date")
    station: StationData = Field(description="Order Address Service")
    bonuses: int = Field(description="Order Bonuses")


class GetOrdersResponse(ApiCamelModel):
    orders: list[OrderData] = Field(description="User Orders List Data")


class CreateOrderRequestCommand(ApiCamelModel):
    fuel_type: FuelType = Field(description="OrderRequest Fuel Type")
    volume: int = Field(description="Order Request Fuel Volume Liters", ge=1, le=30001)
    comment: str | None = Field(description="OrderRequest User Command", max_length=250)


class CreateOrderRequestResponse(ApiCamelModel):
    request_id: UUID = Field(description="Request order ID")


class OrderSubmitFeedbackCommand(ApiCamelModel):
    request_id: UUID = Field(description="Request order ID")
    feedback_score: int = Field(description="Feedback Score")
    feedback_text: str | None = Field(description="Feedback Comment")


class OrderSubmitFeedbackResponse(ApiCamelModel):
    pass


class GetMinFuelVolumeResponse(ApiCamelModel):
    min_fuel_volume: int = Field(description="Min Fuel Volume")
