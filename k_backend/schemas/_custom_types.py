from pydantic_extra_types.timezone_name import TimeZoneName
from sqlalchemy.types import TypeDecorator
from sqlmodel.sql.sqltypes import AutoString


class SATimezone(TypeDecorator):
    impl = AutoString
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return TimeZoneName(value)
