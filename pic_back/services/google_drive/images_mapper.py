import logging
from typing import Any, List, Optional, Protocol

from tinydb import Query

from pic_back.db.utils.markers_db_operations import MarkersDbOperations
from pic_back.models import Coords, Marker
from pic_back.services.image_url_generator import TomtolImageUrlGenerator
from pic_back.settings import get_settings


class GoogleDriveDataFetcherInterface(Protocol):  # pragma: no cover
    def query_content(
        self, query: str, fields: List[str], page_token: Optional[str] = None, page_size: int = 25
    ) -> Any:
        pass


logger = logging.getLogger("images_mapper")


class GoogleDriveImagesMapper:
    def __init__(
        self,
        data_fetcher: GoogleDriveDataFetcherInterface,
    ) -> None:
        self._data_fetcher = data_fetcher
        self._markers_db = MarkersDbOperations.get_db()
        self._settings = get_settings()

    def map_folder(self, folder_id: str, page_token: Optional[str] = None) -> None:
        """
        map images that belong to the single folder (without recursion) - respects page token
        ! query here should be (~) the same as in 'get_folder_content' endpoint - pagination problem
        """
        data = self._data_fetcher.query_content(
            query=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
            fields=["id", "imageMediaMetadata/location/latitude", "imageMediaMetadata/location/longitude"],
            page_token=page_token,
        )

        # TODO refactor
        for img_data in data["files"]:
            img_id = img_data.get("id")
            if metadata := img_data.get("imageMediaMetadata", None):
                if location := metadata.get("location", None):
                    latitude = location.get("latitude", None)
                    longitude = location.get("longitude", None)
                    if latitude is None or longitude is None:
                        logger.info(f"Image `{img_id}` skipped - either lat or lon is missing")
                        continue
                else:
                    logger.info(f"Image `{img_id}` skipped - no `location` attr")
                    continue
            else:
                logger.info(f"Image `{img_id}` skipped - no `imageMediaMetadata` attr")
                continue
            self.map_image(
                folder_id=folder_id,
                img_id=img_id,
                coords=Coords(latitude=latitude, longitude=longitude),
                page_token=page_token,
            )

        if next_page_token := data.get("nextPageToken", None):
            self.map_folder(folder_id=folder_id, page_token=next_page_token)

    def map_image(self, folder_id: str, img_id: str, coords: Coords, page_token: Optional[str] = None) -> None:
        url = TomtolImageUrlGenerator.generate(folder_id=folder_id, img_id=img_id, page_token=page_token)
        new_marker = Marker(coords=coords, url=url)
        query = Query()
        self._markers_db.upsert(
            new_marker.model_dump(),
            (query.coords.latitude == coords.latitude) & (query.coords.longitude == coords.longitude),
        )
        logger.info(f"Succesfully mapped image `{img_id}` to {coords}")
