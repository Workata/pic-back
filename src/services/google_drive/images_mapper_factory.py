from .images_mapper import GoogleDriveImagesMapper
from ..web_image_coordinates_getter import WebImageCoordinatesGetter
from .data_fetcher import GoogleDriveDataFetcher
from .parsers.image_ids import GoogleDriveImageIdsDataParser
from db import CollectionProvider


class GoogleDriveImagesMapperFactory:
    @classmethod
    def create(cls) -> GoogleDriveImagesMapper:
        return GoogleDriveImagesMapper(
            data_fetcher=GoogleDriveDataFetcher(),
            data_parser=GoogleDriveImageIdsDataParser(),
            coords_getter=WebImageCoordinatesGetter(),
            collection_provider=CollectionProvider(),
        )
