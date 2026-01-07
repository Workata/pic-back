import datetime as dt
import logging
from typing import Any, List, Optional, Protocol

from tinydb import Query

from pic_back.db.utils.timestamps_db_operations import TimestampDbOperations, TimestampNotFoundException
from pic_back.models.marker import Coords
from pic_back.models.timestamp import Timestamp


class GoogleDriveDataFetcherInterface(Protocol):  # pragma: no cover
    def query_content(
        self, query: str, fields: List[str], page_token: Optional[str] = None, page_size: int = 25
    ) -> Any:
        pass


class ImagesMapperInterface(Protocol):  # pragma: no cover
    def map_folder(self, folder_id: str, page_token: Optional[str] = None) -> None:
        pass

    def map_image(self, folder_id: str, img_id: str, coords: Coords, page_token: Optional[str] = None) -> None:
        pass


logger = logging.getLogger("disk_mapper")


class GoogleDriveDiskMapper:
    TIMESTAMP_NAME: str = "disk_mapper_last_run"

    def __init__(self, data_fetcher: GoogleDriveDataFetcherInterface, images_mapper: ImagesMapperInterface):
        self._data_fetcher = data_fetcher
        self._images_mapper = images_mapper

    def run(self) -> None:
        last_run_dt = self._get_last_run_datetime()
        data = self._data_fetcher.query_content(
            query="mimeType = 'application/vnd.google-apps.folder' and not name contains 'test' and not name contains 'BACKUP' and trashed=false",
            fields=["id", "modifiedTime"],
            page_size=100,  # TODO check
        )
        for folder in data["files"]:
            folder_id = folder["id"]
            last_modified_dt = dt.datetime.fromisoformat(folder["modifiedTime"])
            if last_run_dt is None or last_modified_dt > last_run_dt:
                logger.info(f"Mapping folder `{folder_id}`")
                self._images_mapper.map_folder(folder_id)
            else:
                logger.info(f"Folder `{folder_id}` skipped - already mapped")
        self._update_last_run_datetime()

    def _get_last_run_datetime(self) -> Optional[dt.datetime]:
        try:
            return TimestampDbOperations.get(self.TIMESTAMP_NAME).time
        except TimestampNotFoundException:
            return None

    def _update_last_run_datetime(self) -> None:
        new_last_run_dt = dt.datetime.now(dt.timezone.utc)
        query = Query()
        timestamp = Timestamp(name=self.TIMESTAMP_NAME, time=new_last_run_dt)
        timestamp_db = TimestampDbOperations.get_db()
        timestamp_db.upsert(timestamp.model_dump(), query.name == self.TIMESTAMP_NAME)
