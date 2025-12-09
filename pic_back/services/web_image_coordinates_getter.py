import io
import logging
import typing as t

import httpx
from exif import Image

from pic_back.models import Coords

logger = logging.getLogger("web_img_coords_getter")


class WebImageCoordinatesGetter:
    """
    Doesnt work with thumbnail images
    """

    def get_coords(self, img_url: str) -> t.Optional[Coords]:
        logger.info(f"Processing image {img_url}")
        img = self._get_img(img_url)
        coords = self._get_image_coordinates(img)
        if coords is None or (coords.latitude == 0.0 and coords.longitude == 0.0):
            # ! when latitude and longitude is (0.0, 0.0) then most likely something wrong during coords extraction
            return None
        return coords

    def _get_img(self, img_url: str) -> Image:
        res = httpx.get(img_url)
        return Image(io.BytesIO(res.content))

    def _get_image_coordinates(self, img: Image) -> t.Optional[Coords]:
        if img.has_exif:
            try:
                coords = (
                    self._get_decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                    self._get_decimal_coords(img.gps_longitude, img.gps_longitude_ref),
                )
            except AttributeError:
                logger.info("Given image has exif data but no coordinates")
                return None
        else:
            logger.info("Given image has no exif data")
            return None
        return Coords(latitude=coords[0], longitude=coords[1])

    def _get_decimal_coords(self, coords: t.Tuple[float, float, float], ref: str) -> float:
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":  # pragma: no cover
            decimal_degrees = -decimal_degrees
        return decimal_degrees
