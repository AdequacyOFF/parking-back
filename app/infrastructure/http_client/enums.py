from enum import Enum


class RequestMethodType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ClientsEnum(str, Enum):
    """Это перечисление возможных клиентов для HttpClientsFactory"""

    NOTIFICATIONS = "NOTIFICATIONS"
    CARD_MASTER = "CARD_MASTER"
    TELEGRAM_NOTIFICATION = "TELEGRAM_NOTIFICATION"
