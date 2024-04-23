import typing as t

from tinydb import Query, TinyDB

from db import CollectionProvider
from models import Coords, Marker
from settings import get_settings

from services.image_url_generator import TomtolImageUrlGenerator, GoogleDriveImageUrlGenerator


class WebImageCoordinatesGetterInterface(t.Protocol):
    def get_coords(self, img_url: str) -> t.Optional[Coords]:
        pass


class GoogleDriveDataFetcherInterface(t.Protocol):
    def query_content(
        self, query: str, fields: t.List[str], page_token: t.Optional[str], page_size: int, spaces: str = "drive"
    ) -> t.Any:
        pass


class GoogleDriveImageIdsDataParserInterface(t.Protocol):
    def parse(self, data: t.Dict[t.Any, t.Any]) -> t.List[str]:  # Returns list of images IDs
        pass


class CollectionProviderInterface(t.Protocol):
    def provide(self, collection_name: str) -> TinyDB:
        pass


collection_provider = CollectionProvider()


class GoogleDriveImagesMapper:
    def __init__(
        self,
        data_fetcher: GoogleDriveDataFetcherInterface,
        data_parser: GoogleDriveImageIdsDataParserInterface,
        coords_getter: WebImageCoordinatesGetterInterface,
        collection_provider: CollectionProviderInterface,
    ) -> None:
        self._data_fetcher = data_fetcher
        self._data_parser = data_parser
        self._coords_getter = coords_getter
        self._markers_collection = collection_provider.provide("markers")
        self._settings = get_settings()

    def map_folder(self, folder_id: str, page_token: t.Optional[str] = None) -> None:
        data = self._data_fetcher.query_content(
            query=f"'{folder_id}' in parents",
            fields=["id", "name", "mimeType"],
            page_size=self._settings.images_page_size,
            page_token=page_token,
        )

        img_ids = self._data_parser.parse(data)
        for img_id in img_ids:
            self.map_image(folder_id=folder_id, img_id=img_id, page_token=page_token)

        if next_page_token := data.get("nextPageToken", None):
            self.map_folder(folder_id=folder_id, page_token=next_page_token)

    def map_image(self, folder_id: str, img_id: str, page_token: t.Optional[str] = None) -> None:
        img_url = GoogleDriveImageUrlGenerator.generate_standard_img_url_v1(img_id)
        coords = self._coords_getter.get_coords(img_url)
        if not coords:
            return None
        url = TomtolImageUrlGenerator.generate(folder_id=folder_id, img_id=img_id, page_token=page_token)
        new_marker = Marker(coords=coords, url=url)
        query = Query()
        self._markers_collection.upsert(
            new_marker.model_dump(),
            (query.coords.latitude == coords.latitude) & (query.coords.longitude == coords.longitude),
        )
