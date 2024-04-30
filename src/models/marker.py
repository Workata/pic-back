from pydantic import BaseModel, field_validator

COORDS_PRECISION = 6


class Coords(BaseModel):
    latitude: float
    longitude: float

    @field_validator("latitude")
    def latitude_check(cls, v: float) -> float:
        return round(v, COORDS_PRECISION)

    @field_validator("longitude")
    def longitude_check(cls, v: float) -> float:
        return round(v, COORDS_PRECISION)

    def __str__(self) -> str:
        return f"lat: {self.latitude}, lon: {self.longitude}"


class Marker(BaseModel):
    coords: Coords
    url: str
