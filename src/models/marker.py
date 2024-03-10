from pydantic import BaseModel, validator

COORDS_PRECISION = 6


class Coords(BaseModel):
    latitude: float
    longitude: float

    @validator("latitude")
    def latitude_check(cls, v: float) -> float:
        return round(v, COORDS_PRECISION)

    @validator("longitude")
    def longitude_check(cls, v: float) -> float:
        return round(v, COORDS_PRECISION)


class Marker(BaseModel):
    coords: Coords
    url: str
