import datetime as dt

from pydantic import BaseModel, field_serializer


class Timestamp(BaseModel):
    """DB model"""

    name: str
    time: dt.datetime

    @field_serializer("time", mode="plain")
    def convert_to_iso_str(self, value: dt.datetime) -> str:
        return value.isoformat()
