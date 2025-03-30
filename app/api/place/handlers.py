from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.place.schemas import (
    ParkingCreateCMD,
    ParkingCreateResponse,
    PlaceAssignCMD,
    PlaceAssignResponse,
    GetParkingResponse,
)
from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.use_cases.place.create_parking import ParkingCreateUseCase
from app.use_cases.place.assign_place import PlaceAssignUseCase
from app.views.place.get_parking import GetParkingView

router = APIRouter(tags=["place"], prefix="/place")


@router.post("/createParking", response_model=ApiResponse[ParkingCreateResponse], description="Create new parking")
@inject
async def create_parking(
    command: ParkingCreateCMD,
    use_case: ParkingCreateUseCase = Depends(Provide[WebAppContainer.parking_create_use_case]),
) -> ApiResponse[ParkingCreateResponse]:
    result = await use_case(cmd=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/getParking", response_model=ApiResponse[GetParkingResponse], description="Assign place to user")
@inject
async def place_assign(
    view: GetParkingView = Depends(Provide[WebAppContainer.get_parking_view]),
) -> ApiResponse[GetParkingResponse]:
    result = await view()
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/assign", response_model=ApiResponse[PlaceAssignResponse], description="Assign place to user")
@inject
async def place_assign(
    command: PlaceAssignCMD,
    use_case: PlaceAssignUseCase = Depends(Provide[WebAppContainer.place_assign_use_case]),
) -> ApiResponse[PlaceAssignResponse]:
    result = await use_case(command=command)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")
