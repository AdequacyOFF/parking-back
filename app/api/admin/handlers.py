from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.admin.schemas import (
    AdminAuthCommand,
    AdminAuthResponse,
    AdminRefreshTokenCommand,
    AdminRefreshTokenResponse,
)
from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.use_cases.admin.auth import AdminAuthUseCase
from app.use_cases.admin.refresh import AdminTokenRefreshUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import RefreshTokenData

router = APIRouter(tags=["admin"], prefix="/admin")


@router.post("/login", description="Login")
@inject
async def login(
    command: AdminAuthCommand,
    use_case: AdminAuthUseCase = Depends(Provide[WebAppContainer.admin_auth_use_case]),
) -> ApiResponse[AdminAuthResponse]:
    result = await use_case(command=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/refreshToken", description="Refresh token")
@inject
async def refresh_token(
    token_data: RefreshTokenData = Depends(AuthJWT.refresh_required),
    use_case: AdminTokenRefreshUseCase = Depends(Provide[WebAppContainer.admin_token_refresh_use_case]),
) -> ApiResponse[AdminRefreshTokenResponse]:
    result = await use_case(
        cmd=AdminRefreshTokenCommand(admin_id=token_data.user_id, token=token_data.token, session_id=token_data.jti)
    )
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
