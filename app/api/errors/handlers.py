from functools import partial

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette import status

from app.api.errors.api_error import ApiError
from app.api.errors.code import ErrorCode
from app.api.models.base import ApiResponse


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, partial(api_exception_handler))
    app.add_exception_handler(Exception, partial(unhandled_exception_handler))
    app.add_exception_handler(RequestValidationError, partial(validation_exception_handler))


async def api_exception_handler(exc: ApiError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ApiResponse(error_code=exc.error_code, message=exc.message)),
    )


async def unhandled_exception_handler() -> ORJSONResponse:
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            ApiResponse(error_code=ErrorCode.INTERNAL_SERVER_ERROR, message="Interval Server Error")
        ),
    )


async def validation_exception_handler(exc: RequestValidationError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(ApiResponse(error_code=ErrorCode.VALIDATION_ERROR, message=f"{exc.errors()}")),
    )
