from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.card.schemas import GetCardBonusesResponse, GetCardInfoResponse
from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import AccessTokenData
from app.views.card.get_card_bonuses import GetCardBonusesView
from app.views.card.get_card_info import GetCardInfoView

router = APIRouter(prefix="/card", tags=["card"])


@router.get("/info", response_model=ApiResponse[GetCardInfoResponse], description="Returns user card information")
@inject
async def get_card(
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    view: GetCardInfoView = Depends(Provide[WebAppContainer.card_get_card_info_view]),
) -> ApiResponse[GetCardInfoResponse]:
    result = await view(token_data.user.id)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.get("/bonuses", response_model=ApiResponse[GetCardBonusesResponse], description="Returns user card bonuses")
@inject
async def get_card_bonuses(
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    view: GetCardBonusesView = Depends(Provide[WebAppContainer.card_get_card_bonuses_view]),
) -> ApiResponse[GetCardBonusesResponse]:
    result = await view(token_data.user.id)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
