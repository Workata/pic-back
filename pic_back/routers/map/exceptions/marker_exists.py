from fastapi import HTTPException, status


class MarkerExists(HTTPException):
    def __init__(self, lat: float, lon: float) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Marker with lat '{lat}' and lon '{lon}' coords already exists. Please provide different coordinates."
            ),
            headers=None,
        )
