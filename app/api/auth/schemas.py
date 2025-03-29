from uuid import UUID


from pydantic import Field


from app.utils.model import ApiCamelModel


class LogoutCMD(ApiCamelModel):
    session_id: UUID = Field(description="Session ID")
    refresh_token: str = Field(description="Token")


class LogoutResponse(ApiCamelModel):
    pass
