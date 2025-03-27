from typing import Any

import orjson
from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    s = "".join(word.capitalize() for word in string.split("_"))
    return s[0].lower() + s[1:]


def _orjson_dumps(val: Any, *, default: Any) -> Any:
    return orjson.dumps(val, default=default).decode()


class AppBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ApiCamelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)
