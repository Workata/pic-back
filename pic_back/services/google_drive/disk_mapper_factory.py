from pic_back.services.google_drive.data_fetcher import GoogleDriveDataFetcher
from pic_back.services.google_drive.disk_mapper import GoogleDriveDiskMapper
from pic_back.services.google_drive.images_mapper_factory import GoogleDriveImagesMapperFactory


class GoogleDriveDiskMapperFactory:
    @staticmethod
    def create() -> GoogleDriveDiskMapper:
        return GoogleDriveDiskMapper(
            data_fetcher=GoogleDriveDataFetcher(), images_mapper=GoogleDriveImagesMapperFactory.create()
        )
