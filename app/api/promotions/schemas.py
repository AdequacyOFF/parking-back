from datetime import date
from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


class PromotionData(ApiCamelModel):
    id: UUID = Field(description="Promotion ID")
    title: str = Field(description="Promotion title")
    photo: str = Field(description="Promotion photo url")
    short_description: str = Field(description="Promotion short description")
    start_date: date = Field(description="Promotion start date")
    end_date: date = Field(description="Promotion end date")


class GetPromotionsResponse(ApiCamelModel):
    total: int = Field(0, description="Promotions total quantity")
    promotions: list[PromotionData | None] = Field([], description="Promotions list data")


class GetPromotionResponse(ApiCamelModel):
    id: UUID = Field(description="Promotion ID")
    title: str = Field(description="Promotion title")
    photo: str = Field(description="Promotion photo url")
    description: str = Field(description="Promotion description")
    url: str | None = Field(None, description="Promotion url")
    short_description: str = Field(description="Promotion short description")
    start_date: date = Field(description="Promotion start date")
    end_date: date = Field(description="Promotion end date")
