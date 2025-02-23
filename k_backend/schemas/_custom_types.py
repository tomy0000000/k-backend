from typing import Any

from pydantic_extra_types.timezone_name import TimeZoneName
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator
from sqlmodel.sql.sqltypes import AutoString


class SATimezone(TypeDecorator[str | TimeZoneName]):
    impl = AutoString
    cache_ok = True

    def process_bind_param(
        self, value: str | TimeZoneName | None, dialect: Dialect
    ) -> Any:
        return str(value)

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> TimeZoneName | None:
        return TimeZoneName(value)
