from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.auth.schemas import LogoutResponse
from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.dto.user import LogoutUserCMD
# from app.use_cases.auth.init import InitUseCase
from app.use_cases.auth.logout import LogoutUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import RefreshTokenData

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/{userId}/logout", response_model=ApiResponse[LogoutResponse], description="Logouts the user")
@inject
async def logout(
    token_data: RefreshTokenData = Depends(AuthJWT.refresh_required),
    use_case: LogoutUseCase = Depends(Provide[WebAppContainer.auth_logout_use_case]),
) -> ApiResponse[LogoutResponse]:
    result = await use_case(
        cmd=LogoutUserCMD(session_id=token_data.jti, refresh_token=token_data.token, user_id=token_data.user_id)
    )
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
