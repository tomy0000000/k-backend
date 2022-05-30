from zoneinfo import ZoneInfo

from sqlalchemy.types import TypeDecorator
from sqlmodel.sql.sqltypes import AutoString


class SATimezone(TypeDecorator):
    impl = AutoString
    cache_ok = True

    def process_bind_param(self, value, dialect):
        print("CONVERTED TO STRING")
        return str(value)

    def process_result_value(self, value, dialect):
        print("CONVERTED TO ZONEINFO")
        return ZoneInfo(value)


class PydanticTimezone(ZoneInfo):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(examples=["America/Los_Angeles", "Asia/Taipei"])

    @classmethod
    def validate(cls, v):
        if isinstance(v, ZoneInfo):
            return cls(str(v))
        if isinstance(v, str):
            return cls(v)
        raise TypeError("zoneinfo.ZoneInfo or str required")
