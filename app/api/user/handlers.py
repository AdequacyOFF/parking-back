from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.api.user.schemas import (
    ChangeUserCMD,
    ChangeUserResponse,
    DeleteUserResponse,
    GetFCMTokenResponse,
    GetUserResponse,
    RegisterAgreementsCMD,
    RegisterAgreementsResponse,
    RegisterCMD,
    RegisterResponse,
)
from app.dependencies.web_app import WebAppContainer
from app.use_cases.user.change_user import ChangeUserUseCase
from app.use_cases.user.delete_user import DeleteUserUseCase
from app.use_cases.user.register import RegisterUseCase
from app.use_cases.user.register_agreement import RegisterAgreementsUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import AccessTokenData
from app.views.user.get_fcm_token import GetFCMTokenView
from app.views.user.me import GetUserView

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/me", response_model=ApiResponse[GetUserResponse], description="Returns current user data")
@inject
async def get_user(
    token_data: AccessTokenData = Depends(AuthJWT.access_required),
    view: GetUserView = Depends(Provide[WebAppContainer.user_get_user_view]),
) -> ApiResponse[GetUserResponse]:
    result = await view(user_id=token_data.user.id)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.put("/change", response_model=ApiResponse[ChangeUserResponse], description="Changes User Data")
@inject
async def change_user(
    command: ChangeUserCMD,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: ChangeUserUseCase = Depends(Provide[WebAppContainer.user_change_user]),
) -> ApiResponse[ChangeUserResponse]:
    result = await use_case(user_id=token_data.user.id, cmd=command)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.post("/register", response_model=ApiResponse[RegisterResponse], description="Take data and register user")
@inject
async def register(
    command: RegisterCMD,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: RegisterUseCase = Depends(Provide[WebAppContainer.user_register_use_case]),
) -> ApiResponse[RegisterResponse]:
    result = await use_case(user_id=token_data.user.id, cmd=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/registerAgreements", response_model=ApiResponse[RegisterAgreementsResponse])
@inject
async def register_agreements(
    command: RegisterAgreementsCMD,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: RegisterAgreementsUseCase = Depends(Provide[WebAppContainer.user_register_agreements_use_case]),
) -> ApiResponse[RegisterAgreementsResponse]:
    result = await use_case(
        cmd=command,
        user_id=token_data.user.id,
    )
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/fcmToken", response_model=ApiResponse[GetFCMTokenResponse], description="Get user FCM token")
@inject
async def get_fcm_token(
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    view: GetFCMTokenView = Depends(Provide[WebAppContainer.user_get_fcm_token_view]),
) -> ApiResponse[GetFCMTokenResponse]:
    result = await view(user_id=token_data.user.id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.delete("/delete", description="Delete user")
@inject
async def delete_user(
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: DeleteUserUseCase = Depends(Provide[WebAppContainer.delete_user_use_case]),
) -> ApiResponse[DeleteUserResponse]:
    result = await use_case(user_id=token_data.user.id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")
