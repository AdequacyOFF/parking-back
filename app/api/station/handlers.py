from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse
from app.api.station.schemas import GetGasStationsResponse, GetOilsResponse, GetServicesResponse
from app.dependencies.web_app import WebAppContainer
from app.views.stations.get_oils import GetOilsView
from app.views.stations.get_services import GetServicesView
from app.views.stations.get_stations import GetGasStationsView

router = APIRouter(prefix="/stations", tags=["gas stations"])


@router.get("/", response_model=ApiResponse[GetGasStationsResponse], description="Returns gas station list")
@inject
async def get_gas_stations(
    oils: list[str] = Query([], description="Gas Station Oils Available"),
    services: list[str] = Query([], description="Gas Station Services Available"),
    lon: float | None = Query(None),
    lat: float | None = Query(None),
    view: GetGasStationsView = Depends(Provide[WebAppContainer.stations_get_stations_view]),
) -> ApiResponse[GetGasStationsResponse]:
    result = await view(oils=oils, services=services, lat=lat, lon=lon)
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.get("/oils", response_model=ApiResponse[GetOilsResponse], description="Returns gas station oils list")
@inject
async def get_oils(
    view: GetOilsView = Depends(Provide[WebAppContainer.stations_get_oils_view]),
) -> ApiResponse[GetOilsResponse]:
    result = await view()
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)


@router.get(
    "/services", response_model=ApiResponse[GetServicesResponse], description="Returns gas stations services list"
)
@inject
async def get_services(
    view: GetServicesView = Depends(Provide[WebAppContainer.stations_get_services_view]),
) -> ApiResponse[GetServicesResponse]:
    result = await view()
    return ApiResponse(error_code=ErrorCode.SUCCESS, message="Success", result=result)
