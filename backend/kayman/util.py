from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import simplejson
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def handle_special_types(obj: Any) -> Any:
    print(f"handled type: {type(obj)}, {obj=}")
    if isinstance(obj, BaseModel):
        return obj.dict()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, ZoneInfo):
        return str(obj)
    return str(obj)  # Not sure if this is a good idea, but we'll see


class KustomJSONResponse(JSONResponse):
    """
    This is the default custom response class for K,
    which made improvement on following data types:

    - decimal.Decimal: unlimited precision
    - datetime.datetime: format with dt.isoformat()
    - zoneinfo.ZoneInfo: format with str(zoneinfo.ZoneInfo)
    """

    def render(self, content: Any) -> bytes:
        return simplejson.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=handle_special_types,
            use_decimal=True,
        ).encode("utf-8")
