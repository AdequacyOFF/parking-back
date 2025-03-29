from app.utils.exceptions import BaseAppException


class DomainException(BaseAppException):
    message: str

    def __init__(self, message: str | None = None):
        if message:
            self.message = message


class InvalidStatusException(DomainException):
    message = "User is already registered"


class SessionAlreadyExpiredException(DomainException):
    message = "Session is already expired"
