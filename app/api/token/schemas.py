from uuid import UUID

from pydantic import Field

from app.utils.model import ApiCamelModel


class RefreshCMD(ApiCamelModel):
    session_id: UUID = Field(description="Session ID")
    refresh_token: str = Field(description="Token")


class RefreshResponse(ApiCamelModel):
    access: str = Field(description="Access token")
    refresh: str = Field(description="Refresh token")
