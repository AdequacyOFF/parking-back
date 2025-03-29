from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.api.user.schemas import (
    UserAuthCMD,
    UserAuthResponse,
    ChangeUserCMD,
    ChangeUserResponse,
    GetUserResponse,

)
from app.dependencies.web_app import WebAppContainer
from app.use_cases.user.change_user import ChangeUserUseCase
from app.use_cases.user.auth import UserAuthUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import AccessTokenData
from app.views.user.me import GetUserView

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/login", description="Login")
@inject
async def login(
    command: UserAuthCMD,
    use_case: UserAuthUseCase = Depends(Provide[WebAppContainer.user_auth_use_case]),
) -> ApiResponse[UserAuthResponse]:
    result = await use_case(command=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


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

