from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.types import TypeDecorator
from sqlmodel.sql.sqltypes import AutoString

EXTENDED_JSON_ENCODERS = {ZoneInfo: lambda v: str(v)}


class SATimezone(TypeDecorator):
    impl = AutoString
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return PydanticTimezone(value)


class PydanticTimezone(ZoneInfo):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(examples=["America/Los_Angeles", "Asia/Taipei"])

    @classmethod
    def validate(cls, v):
        if isinstance(v, ZoneInfo):
            return v
        if isinstance(v, str):
            try:
                return cls(v)
            except ZoneInfoNotFoundError:
                raise ValueError(f"{v} is not a valid timezone")
        raise TypeError("zoneinfo.ZoneInfo or str required")


def create_timestamp_validator(values):
    try:
        timestamp = values["timestamp"]
        timezone = values["timezone"]
        if timestamp.tzinfo is None:
            values["timestamp"] = timestamp.replace(tzinfo=timezone)
            return values
        stamp_offset = timestamp.tzinfo.utcoffset(timestamp)
        zone_offset = timezone.utcoffset(timestamp)
        if stamp_offset != zone_offset:
            raise ValueError(
                f"Inconsistent timestamp offset ({stamp_offset}) and timezone offset ({zone_offset})"
            )
    except KeyError:
        raise ValueError("Missing timestamp or timezone")
    return values


def tz_timestamp_reader(values):
    timezone = values.get("timezone")
    if timezone is not None:
        values["timestamp"] = values["timestamp"].astimezone(timezone)
    return values
