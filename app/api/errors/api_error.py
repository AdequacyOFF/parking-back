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


class OTPSendTimeoutApiError(BusinessApiError):
    status_code = 400
    message: str = "Слишком частые запросы на код подтверждения. Пожалуйста, попробуйте позже"
    error_code = ErrorCode.CANT_SEND_OTP_TOO_OFTEN


class UserNotFoundApiError(BusinessApiError):
    status_code = 404
    message = "Пользователь не найден"
    error_code = ErrorCode.USER_NOT_FOUND


class InvalidOTPApiError(BusinessApiError):
    status_code = 400
    message = "Неверный код подтверждения"
    error_code = ErrorCode.INVALID_OTP_CODE


class OTPExpiredApiError(BusinessApiError):
    status_code = 400
    message = "Срок действия OTP-кода истек"
    error_code = ErrorCode.OTP_CODE_IS_EXPIRED


class UserAlreadyRegisteredApiError(BusinessApiError):
    status_code = 400
    message = "Пользователь уже зарегистрирован"
    error_code = ErrorCode.USER_IS_ALREADY_REGISTERED


class AgreementsNotAcceptedApiError(BusinessApiError):
    status_code = 400
    message = "Все соглашения должны быть приняты"
    error_code = ErrorCode.ALL_AGREEMENTS_MUST_BE_ACCEPTED


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


class CardNotFoundApiError(BusinessApiError):
    status_code = 404
    message = "Карта не найдена"
    error_code = ErrorCode.CARD_NOT_FOUND


class PromotionNotFoundApiError(BusinessApiError):
    status_code = 404
    message = "Акция не найдена"
    error_code = ErrorCode.PROMOTION_NOT_FOUND


class NoAvailableCardApiError(BusinessApiError):
    status_code = 400
    message = "Нет активных карт"
    error_code = ErrorCode.NO_AVAILABLE_CARDS


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


class InvalidFileExtensionApiError(BusinessApiError):
    status_code = 400
    message = "Некорректное расширение файла"
    error_code = ErrorCode.INVALID_FILE_EXTENSION


class FileInvalidFormatApiError(BusinessApiError):
    status_code = 400
    message = "Некорректный формат файла"
    error_code = ErrorCode.FILE_IS_INVALID_FORMAT


class OrderRequestEmailSendingApiError(BusinessApiError):
    status_code = 500
    message = "Ошибка отправки запроса"
    error_code = ErrorCode.ORDER_SENDING_REQUEST_ERROR


class OrderRequestNotFoundApiError(BusinessApiError):
    status_code = 404
    message = "Заявка не найдена"
    error_code = ErrorCode.ORDER_REQUEST_NOT_FOUND
