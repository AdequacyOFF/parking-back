from typing import Generic, TypeVar

from app.api.errors.code import ErrorCode
from app.utils.model import ApiCamelModel

T = TypeVar("T")


class ApiResponse(ApiCamelModel, Generic[T]):
    error_code: ErrorCode
    message: str | None
    result: T | None = None
