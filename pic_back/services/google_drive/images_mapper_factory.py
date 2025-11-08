from db import CollectionProvider
from services.google_drive.data_fetcher import GoogleDriveDataFetcher
from services.google_drive.images_mapper import GoogleDriveImagesMapper
from services.google_drive.parsers.image_ids import GoogleDriveImageIdsDataParser
from services.web_image_coordinates_getter import WebImageCoordinatesGetter


class GoogleDriveImagesMapperFactory:
    @classmethod
    def create(cls) -> GoogleDriveImagesMapper:
        return GoogleDriveImagesMapper(
            data_fetcher=GoogleDriveDataFetcher(),
            data_parser=GoogleDriveImageIdsDataParser(),
            coords_getter=WebImageCoordinatesGetter(),
            collection_provider=CollectionProvider(),
        )
