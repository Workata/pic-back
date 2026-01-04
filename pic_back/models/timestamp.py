import datetime as dt

from pydantic import BaseModel


class Timestamp(BaseModel):
    """DB model"""

    name: str
    time: dt.datetime
