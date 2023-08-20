from pydantic import BaseModel


class Marker(BaseModel):
    latitude: float
    longitude: float
    url: str
