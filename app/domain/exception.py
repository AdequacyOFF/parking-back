from app.utils.exceptions import BaseAppException


class DomainException(BaseAppException):
    message: str

    def __init__(self, message: str | None = None):
        if message:
            self.message = message


class OTPSendTimeoutException(DomainException):
    message: str = "Can't send OTP too often. Please try again later"


class InvalidOTPException(DomainException):
    message = "Invalid OTP"


class OTPExpiredException(DomainException):
    message = "OTP code is expired"


class InvalidStatusException(DomainException):
    message = "User is already registered"


class SessionAlreadyExpiredException(DomainException):
    message = "Session is already expired"


class AgreementsNotAcceptedException(DomainException):
    message = "All agreements must be accepted"


class InvalidFileExtensionDomainException(DomainException):
    pass


class FileInvalidFormatDomainException(DomainException):
    pass
