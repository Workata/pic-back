from services.google_drive.data_fetcher import GoogleDriveDataFetcher
from services.google_drive import GoogleDriveImagesMapperFactory

fetcher = GoogleDriveDataFetcher()

data = fetcher.query_content(
    query="mimeType = 'application/vnd.google-apps.folder' and not name contains 'test' and not name contains 'BACKUP'",
    fields=["id", "mimeType", "name"],
    page_size=100,
)
print(data)
folder_ids = [folder_data["id"] for folder_data in data["files"]]
print(folder_ids)


images_mapper = GoogleDriveImagesMapperFactory.create()


# images_mapper.map_folder("1jk1IKlnIJ1YsWki43eLV_qDYr6x8Z8S6")
for folder_id in folder_ids:
    print(f"Mapping folder - {folder_id}")
    images_mapper.map_folder(folder_id)
