from datetime import date
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Form, Path, Query, UploadFile

from app.api.admin.schemas import (
    AdminAuthCommand,
    AdminAuthResponse,
    AdminRefreshTokenCommand,
    AdminRefreshTokenResponse,
    ChangeMinFuelVolumeCommand,
    ChangeMinFuelVolumeResponse,
    CreatePromotionResponse,
    DeletePromotionResponse,
    UpdatePromotionResponse,
)
from app.api.deps import auth_admin
from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.domain.admin import Admin
from app.use_cases.admin.auth import AdminAuthUseCase
from app.use_cases.admin.change_min_volume import ChangeMinFuelVolumeUseCase
from app.use_cases.admin.create_promotion import CreatePromotionUseCase
from app.use_cases.admin.delete_promotion import DeletePromotionUseCase
from app.use_cases.admin.refresh import AdminTokenRefreshUseCase
from app.use_cases.admin.update_promotion import UpdatePromotionUseCase
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


@router.post("/promotions", description="Create promotion")
@inject
async def create_promotion(
    _: Admin = Depends(auth_admin),
    title: str = Form(description="Promotion title"),
    short_description: str = Form(
        description="Promotion short description", alias="shortDescription", validation_alias="shortDescription"
    ),
    start_date: date = Form(description="Promotion start date", alias="startDate", validation_alias="startDate"),
    end_date: date = Form(description="Promotion end date", alias="endDate", validation_alias="endDate"),
    description: str = Form(description="Promotion description"),
    url: str | None = Form(None, description="Promotion url"),
    file: UploadFile = File(description="File content"),
    use_case: CreatePromotionUseCase = Depends(Provide[WebAppContainer.admin_create_promotion_use_case]),
) -> ApiResponse[CreatePromotionResponse]:
    result = await use_case(
        title=title,
        short_description=short_description,
        start_date=start_date,
        end_date=end_date,
        description=description,
        url=url,
        file=file,
    )
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.put("/promotions/{promotionId}", description="Update promotion")
@inject
async def update_promotion(
    _: Admin = Depends(auth_admin),
    promotion_id: UUID = Path(description="Promotion ID", alias="promotionId", validation_alias="promotionId"),
    title: str = Form(description="Promotion title"),
    short_description: str = Form(
        description="Promotion short description", alias="shortDescription", validation_alias="shortDescription"
    ),
    start_date: date = Form(description="Promotion start date", alias="startDate", validation_alias="startDate"),
    end_date: date = Form(description="Promotion end date", alias="endDate", validation_alias="endDate"),
    description: str = Form(description="Promotion description"),
    url: str | None = Form(None, description="Promotion url"),
    file: UploadFile | None = File(None, description="File content"),
    use_case: UpdatePromotionUseCase = Depends(Provide[WebAppContainer.admin_update_promotion_use_case]),
) -> ApiResponse[UpdatePromotionResponse]:
    result = await use_case(
        title=title,
        short_description=short_description,
        start_date=start_date,
        end_date=end_date,
        description=description,
        url=url,
        promotion_id=promotion_id,
        file=file,
    )
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.delete("/promotions/{promotionId}", description="Delete promotion")
@inject
async def delete_promotion(
    _: Admin = Depends(auth_admin),
    promotion_id: UUID = Path(description="Promotion ID", alias="promotionId"),
    use_case: DeletePromotionUseCase = Depends(Provide[WebAppContainer.admin_delete_promotion_use_case]),
) -> ApiResponse[DeletePromotionResponse]:
    result = await use_case(promotion_id=promotion_id)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.put("/fuel/volume", description="Change min oil volume")
@inject
async def change_min_fuel_volume(
    command: ChangeMinFuelVolumeCommand,
    admin: Admin = Depends(auth_admin),
    use_case: ChangeMinFuelVolumeUseCase = Depends(Provide[WebAppContainer.admin_change_min_fuel_volume_use_case]),
) -> ApiResponse[ChangeMinFuelVolumeResponse]:
    result = await use_case(admin=admin, command=command)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
