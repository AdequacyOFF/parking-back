from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


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


class CreatePromotionResponse(ApiCamelModel):
    pass


class UpdatePromotionResponse(ApiCamelModel):
    pass


class DeletePromotionResponse(ApiCamelModel):
    pass


class ChangeMinFuelVolumeCommand(ApiCamelModel):
    volume: int = Field(description="Min Fuel Volume", ge=1, le=30001)


class ChangeMinFuelVolumeResponse(ApiCamelModel):
    pass
