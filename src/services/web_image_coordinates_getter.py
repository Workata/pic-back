import typing as t
from io import BytesIO

import requests
from exif import Image

from models import Coords


class WebImageCoordinatesGetter:
    """
    Doesnt work with thumbnail images
    """

    def get_coords(self, img_url: str) -> t.Optional[Coords]:
        img = self._get_img(img_url)
        return self._get_image_coordinates(img)

    def _get_img(self, img_url: str) -> Image:
        res = requests.get(img_url)
        return Image(BytesIO(res.content))

    def _get_image_coordinates(self, img: Image) -> t.Optional[Coords]:
        if img.has_exif:
            try:
                coords = (
                    self._get_decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                    self._get_decimal_coords(img.gps_longitude, img.gps_longitude_ref),
                )
            except AttributeError:
                return None  # image has no coordinates
        else:
            return None  # image has no EXIF information
        return Coords(latitude=coords[0], longitude=coords[1])

    def _get_decimal_coords(self, coords: t.Tuple[float, float, float], ref: str) -> float:
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees
        return decimal_degrees
