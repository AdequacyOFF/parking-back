from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def get_utc_now_tz() -> datetime:
    return datetime.now(tz=timezone.utc)


def get_now_as_tz(tz: str = "Europe/Moscow") -> datetime:
    return datetime.now().astimezone(ZoneInfo(tz))
