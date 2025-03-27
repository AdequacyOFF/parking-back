from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class ProcessType(str, Enum):
    ENCODE = "ENCODE"
    DECODE = "DECODE"


class TokenType(str, Enum):
    ACCESS = "ACCESS_TOKEN"
    REFRESH = "REFRESH_TOKEN"


class UserData(BaseModel):
    id: UUID
    status: str | None = None


class AccessTokenData(BaseModel):
    jti: UUID
    user: UserData


class RefreshTokenData(BaseModel):
    token: str
    user_id: UUID
    jti: UUID


class CreateTokenData(BaseModel):
    type: TokenType
    token: str
    jti: UUID
