from app.utils.exceptions import BaseAppException


class RepositoryException(BaseAppException):
    ...


class RepositoryNotFoundException(RepositoryException):
    ...
