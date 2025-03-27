from enum import Enum


class EventType(str, Enum):
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    UPDATED = "UPDATED"
