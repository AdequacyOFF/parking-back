from app.api.errors.code import ErrorCode
from app.utils.exceptions import BaseAppException


class ApiError(BaseAppException):
    status_code: int
    message: str | None
    error_code: ErrorCode

    def __init__(self, message: str | None = None):
        if message:
            self.message = message


class BusinessApiError(ApiError):
    pass


class UserNotFoundApiError(BusinessApiError):
    status_code = 404
    message = "Пользователь не найден"
    error_code = ErrorCode.USER_NOT_FOUND


class UserAlreadyRegisteredApiError(BusinessApiError):
    status_code = 400
    message = "Пользователь уже зарегистрирован"
    error_code = ErrorCode.USER_IS_ALREADY_REGISTERED


class SessionAlreadyExpiredApiError(BusinessApiError):
    status_code = 400
    message = "Срок действия сессии истек"
    error_code = ErrorCode.SESSION_IS_ALREADY_EXPIRED


class InvalidUserStatusApiError(BusinessApiError):
    status_code = 400
    message = "Некорректный статус пользователя"
    error_code = ErrorCode.INVALID_USER_STATUS


class AccessTokenRequiredApiError(ApiError):
    status_code = 422
    message = "Требуется токен доступа"
    error_code = ErrorCode.ACCESS_TOKEN_REQUIRED


class RefreshTokenRequiredApiError(ApiError):
    status_code = 422
    message = "Требуется обновить токен"
    error_code = ErrorCode.REFRESH_TOKEN_REQUIRED


class InvalidLoginOrPasswordApiError(BusinessApiError):
    status_code = 403
    message = "Некорректный логин или пароль"
    error_code = ErrorCode.ADMIN_INVALID_LOGIN_OR_PASSWORD


class AdminNotFoundApiError(BusinessApiError):
    status_code = 404
    message = "Учетная запись администратора не найдена"
    error_code = ErrorCode.ADMIN_NOT_FOUND


class AccessDeniedApiError(BusinessApiError):
    status_code = 403
    message = "Доступ запрещен"
    error_code = ErrorCode.ADMIN_ACCESS_DENIED
