from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.api.orders.schemas import (
    CreateOrderRequestCommand,
    CreateOrderRequestResponse,
    GetMinFuelVolumeResponse,
    GetOrdersResponse,
    OrderSubmitFeedbackCommand,
    OrderSubmitFeedbackResponse,
)
from app.dependencies.web_app import WebAppContainer
from app.use_cases.orders.create_order_request import CreateOrderRequestUseCase
from app.use_cases.orders.submit_feedback import SubmitFeedbackUseCase
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import AccessTokenData
from app.views.orders.get_min_volume import GetMinFuelVolumeView
from app.views.orders.get_orders import GetOrdersView

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/getOrders", response_model=ApiResponse[GetOrdersResponse], description="Returns user orders list")
@inject
async def get_orders(
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    limit: int = Query(20, description="Limit", ge=1, le=50),
    offset: int = Query(0, description="Offset", ge=0, le=2147483647),
    view: GetOrdersView = Depends(Provide[WebAppContainer.orders_get_orders_view]),
) -> ApiResponse[GetOrdersResponse]:
    result = await view(token_data.user.id, limit=limit, offset=offset)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.post("/request/create", description="Create order request")
@inject
async def create_order_request(
    command: CreateOrderRequestCommand,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: CreateOrderRequestUseCase = Depends(Provide[WebAppContainer.orders_create_order_request_use_case]),
) -> ApiResponse[CreateOrderRequestResponse]:
    result = await use_case(user_id=token_data.user.id, command=command)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.post("/request/feedback", description="User submit feedback")
@inject
async def submit_feedback(
    command: OrderSubmitFeedbackCommand,
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    use_case: SubmitFeedbackUseCase = Depends(Provide[WebAppContainer.orders_submit_feedback_use_case]),
) -> ApiResponse[OrderSubmitFeedbackResponse]:
    result = await use_case(user_id=token_data.user.id, command=command)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.get("/fuel/volume", description="Get min fuel volume")
@inject
async def get_min_fuel_volume(
    view: GetMinFuelVolumeView = Depends(Provide[WebAppContainer.orders_get_min_fuel_volume_use_case]),
) -> ApiResponse[GetMinFuelVolumeResponse]:
    result = await view()
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
