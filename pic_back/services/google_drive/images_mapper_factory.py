from pic_back.services.google_drive.data_fetcher import GoogleDriveDataFetcher
from pic_back.services.google_drive.images_mapper import GoogleDriveImagesMapper
from pic_back.services.google_drive.parsers.image_ids import GoogleDriveImageIdsDataParser
from pic_back.services.web_image_coordinates_getter import WebImageCoordinatesGetter


class GoogleDriveImagesMapperFactory:
    @classmethod
    def create(cls) -> GoogleDriveImagesMapper:
        return GoogleDriveImagesMapper(
            data_fetcher=GoogleDriveDataFetcher(),
            data_parser=GoogleDriveImageIdsDataParser(),
            coords_getter=WebImageCoordinatesGetter(),
        )
