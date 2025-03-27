from datetime import datetime, timedelta
from typing import Any, Callable
from uuid import UUID, uuid4

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.errors.api_error import AccessTokenRequiredApiError, RefreshTokenRequiredApiError
from app.settings import settings
from app.utils.auth.schemas import AccessTokenData, CreateTokenData, ProcessType, RefreshTokenData, TokenType, UserData


class AuthJWT:
    ACCESS_SCHEMA = HTTPBearer(bearerFormat="JWT", description="Access Token")

    __PRIVATE_KEY = settings.auth_jwt.private_key
    __PUBLIC_KEY = settings.auth_jwt.public_key
    __ALGORITHM = settings.auth_jwt.algorithm
    __ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth_jwt.access_expired_at
    __ACCESS_REFRESH_TOKEN_EXPIRE_MINUTES = settings.auth_jwt.refresh_expired_at

    @classmethod
    def access_required(cls, access_token: HTTPAuthorizationCredentials = Depends(ACCESS_SCHEMA)) -> AccessTokenData:
        payload = cls._validate_token(token=access_token, token_type=TokenType.ACCESS)
        return AccessTokenData(
            jti=UUID(payload["jti"]),
            user=UserData(id=UUID(payload["user"])),
        )

    @classmethod
    def access_status_required(cls) -> Callable[[HTTPAuthorizationCredentials], AccessTokenData]:
        def _access_status_required(
            access_token: HTTPAuthorizationCredentials = Depends(cls.ACCESS_SCHEMA),
        ) -> AccessTokenData:
            payload = cls._validate_token(access_token, TokenType.ACCESS)
            return AccessTokenData(jti=UUID(payload["jti"]), user=UserData(id=UUID(payload["user"])))

        return _access_status_required

    @classmethod
    def refresh_required(cls, refresh_token: HTTPAuthorizationCredentials = Depends(ACCESS_SCHEMA)) -> RefreshTokenData:
        payload = cls._validate_token(refresh_token, TokenType.REFRESH)
        return RefreshTokenData(
            token=refresh_token.credentials, jti=UUID(payload["jti"]), user_id=UUID(payload["user"])
        )

    @classmethod
    def create_access_token(cls, user_data: UserData, jti: UUID | None = None) -> CreateTokenData:
        if jti is None:
            jti = uuid4()
        return cls._create_token(token_type=TokenType.ACCESS, user_data=user_data, jti=jti)

    @classmethod
    def create_refresh_token(cls, user_data: UserData, jti: UUID | None = None) -> CreateTokenData:
        if jti is None:
            jti = uuid4()
        return cls._create_token(token_type=TokenType.REFRESH, user_data=user_data, jti=jti)

    @classmethod
    def _validate_token(cls, token: HTTPAuthorizationCredentials, token_type: TokenType) -> dict[str, Any]:
        if token_type not in (TokenType.ACCESS, TokenType.REFRESH):
            raise ValueError("Invalid token")

        payload = cls._decode_jwt_token(token=token)

        if token_type.value != payload["type"]:
            if token_type == TokenType.ACCESS:
                raise AccessTokenRequiredApiError
            if token_type == TokenType.REFRESH:
                raise RefreshTokenRequiredApiError
        return payload

    @classmethod
    def _create_token(
        cls,
        token_type: TokenType,
        user_data: UserData,
        jti: UUID,
        process_type: ProcessType | None = ProcessType.ENCODE,
    ) -> CreateTokenData:
        token = jwt.encode(
            payload=cls._create_payload(user_data, token_type, jti),
            key=cls._get_secret_key(process=process_type),
            algorithm=cls.__ALGORITHM,
        )
        return CreateTokenData(type=token_type, token=token, jti=jti)

    @classmethod
    def _decode_jwt_token(cls, token: HTTPAuthorizationCredentials) -> dict[str, Any]:
        try:
            decoded = jwt.decode(
                token.credentials,
                key=cls._get_secret_key(process=ProcessType.DECODE),
                algorithms=[cls.__ALGORITHM],
            )
            return decoded
        except jwt.ExpiredSignatureError as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError(e)

    @classmethod
    def _create_payload(cls, user_data: UserData, token_type: TokenType, jti: UUID | None) -> dict[str, Any]:
        return {
            "id": str(user_data.id),
            "type": token_type.value,
            "user": str(user_data.id),
            "jti": str(jti),
            "exp": int((datetime.utcnow().timestamp() + cls._get_exp_time(token_type).timestamp())),
        }

    @classmethod
    def _get_secret_key(cls, process: ProcessType | None) -> Any:
        if not jwt.algorithms.has_crypto:
            raise RuntimeError("Missing dependencies for run 'poetry add cryptography'")
        if process not in (ProcessType.ENCODE, ProcessType.DECODE):
            raise ValueError("Process must be 'encode' or 'decode'")
        if not cls.__PRIVATE_KEY:
            raise RuntimeError("Private key must be set when encoding JWT")

        return cls.__PRIVATE_KEY if ProcessType.ENCODE == process else cls.__PUBLIC_KEY

    @classmethod
    def _get_exp_time(cls, token_type: TokenType) -> datetime:
        return (
            datetime.utcnow() + timedelta(minutes=cls.__ACCESS_TOKEN_EXPIRE_MINUTES)
            if token_type == TokenType.ACCESS
            else datetime.utcnow() + timedelta(minutes=cls.__ACCESS_REFRESH_TOKEN_EXPIRE_MINUTES)
        )
