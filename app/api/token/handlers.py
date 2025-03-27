from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.api.token.schemas import RefreshResponse
from app.dependencies.web_app import WebAppContainer
from app.dto.user import RefreshTokenCMD
from app.use_cases.token.refresh import RefreshUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import RefreshTokenData

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/refresh", response_model=ApiResponse[RefreshResponse])
@inject
async def refresh(
    token_data: RefreshTokenData = Depends(AuthJWT.refresh_required),
    use_case: RefreshUseCase = Depends(Provide[WebAppContainer.token_refresh_use_case]),
) -> ApiResponse[RefreshResponse]:
    result = await use_case(
        cmd=RefreshTokenCMD(user_id=token_data.user_id, token=token_data.token, session_id=token_data.jti)
    )
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
