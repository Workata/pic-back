from pydantic import BaseModel, validator

COORDS_PRECISION = 6


class Marker(BaseModel):
    latitude: float
    longitude: float
    url: str

    @validator("latitude")
    def latitude_check(cls, v: float) -> float:
        return round(v, COORDS_PRECISION)

    @validator("longitude")
    def longitude_check(cls, v: float) -> float:
        return round(v, COORDS_PRECISION)
