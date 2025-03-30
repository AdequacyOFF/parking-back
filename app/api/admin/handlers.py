from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.admin.schemas import (
    AdminAuthCommand,
    AdminAuthResponse,
    AdminRefreshTokenCommand,
    AdminRefreshTokenResponse,
    UserRegisterCMD,
    UserRegisterResponse,
    UserDeleteCMD,
    UserDeleteResponse,
)
from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.use_cases.admin.auth import AdminAuthUseCase
from app.use_cases.admin.refresh import AdminTokenRefreshUseCase
from app.use_cases.admin.delete_user import UserDeleteUseCase
from app.use_cases.admin.register_user import UserRegisterUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import RefreshTokenData, AccessTokenData

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


@router.post("/userRegister", response_model=ApiResponse[UserRegisterResponse], description="Take data and register user")
@inject
async def register(
    command: UserRegisterCMD,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: UserRegisterUseCase = Depends(Provide[WebAppContainer.user_register_use_case]),
) -> ApiResponse[UserRegisterResponse]:
    result = await use_case(admin_id=token_data.user.id, cmd=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.delete("/userDelete", description="Delete user")
@inject
async def delete_user(
    command: UserDeleteCMD,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: UserDeleteUseCase = Depends(Provide[WebAppContainer.user_delete_use_case]),
) -> ApiResponse[UserDeleteResponse]:
    result = await use_case(admin_id=token_data.user.id, cmd=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")