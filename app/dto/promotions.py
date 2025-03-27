from dataclasses import dataclass
from datetime import date
from enum import Enum


class PromotionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass
class CreatePromotionCMD:
    title: str
    description: str
    url: str | None
    short_description: str
    start_date: date
    end_date: date


@dataclass
class UpdatePromotionCMD:
    title: str
    description: str
    url: str | None
    short_description: str
    start_date: date
    end_date: date
