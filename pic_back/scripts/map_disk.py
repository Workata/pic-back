import logging

from pic_back.services.google_drive import GoogleDriveImagesMapperFactory
from pic_back.services.google_drive.data_fetcher import GoogleDriveDataFetcher


def map_disk() -> None:
    logger = logging.getLogger(name="map_disk")
    fetcher = GoogleDriveDataFetcher()

    data = fetcher.query_content(
        query="mimeType = 'application/vnd.google-apps.folder' and not name contains 'test' and not name contains 'BACKUP'",
        fields=["id", "mimeType", "name"],
        page_size=100,
    )
    folder_ids = [folder_data["id"] for folder_data in data["files"]]
    logger.info(f"Folder IDs: {folder_ids}")

    images_mapper = GoogleDriveImagesMapperFactory.create()

    for folder_id in folder_ids:
        logger.info(f"Mapping folder - {folder_id}")
        images_mapper.map_folder(folder_id)


if __name__ == "__main__":
    map_disk()
