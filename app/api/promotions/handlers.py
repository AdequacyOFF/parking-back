from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.api.promotions.schemas import GetPromotionResponse, GetPromotionsResponse
from app.dependencies.web_app import WebAppContainer
from app.views.promotions.get_promotion import GetPromotionView
from app.views.promotions.get_promotions import GetPromotionsView

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/", response_model=ApiResponse[GetPromotionsResponse], description="Returns promotions list")
@inject
async def get_promotions(
    limit: int = Query(5, description="Limit", ge=1, le=50),
    offset: int = Query(0, description="Offset", ge=0, le=2147483647),
    view: GetPromotionsView = Depends(Provide[WebAppContainer.promotions_get_promotions_view]),
) -> ApiResponse[GetPromotionsResponse]:
    result = await view(limit=limit, offset=offset)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.get("/{promotionId}", response_model=ApiResponse[GetPromotionResponse], description="Return promotion data")
@inject
async def get_promotion(
    promotion_id: UUID = Path(description="Promotion ID", alias="promotionId"),
    view: GetPromotionView = Depends(Provide[WebAppContainer.promotions_get_promotion_view]),
) -> ApiResponse[GetPromotionResponse]:
    result = await view(promotion_id=promotion_id)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
