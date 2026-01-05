from pic_back.services.google_drive.data_fetcher import GoogleDriveDataFetcher
from pic_back.services.google_drive.images_mapper import GoogleDriveImagesMapper


class GoogleDriveImagesMapperFactory:
    @staticmethod
    def create() -> GoogleDriveImagesMapper:
        return GoogleDriveImagesMapper(
            data_fetcher=GoogleDriveDataFetcher(),
        )
