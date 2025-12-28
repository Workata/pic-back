from pathlib import Path
from typing import List

from googleapiclient.http import MediaFileUpload

from pic_back.services.google_drive.google_drive_service_factory import GoogleDriveServiceFactory


class FileUploader:
    SCOPES: List[str] = ["https://www.googleapis.com/auth/drive.file"]

    def __init__(self) -> None:
        self._google_drive_service = GoogleDriveServiceFactory.create(scopes=self.SCOPES)

    def upload(self, file_path: Path, parent_folder_id: str, uploaded_file_name: str) -> None:
        file_metadata = {"name": uploaded_file_name, "parents": [parent_folder_id]}
        media = MediaFileUpload(filename=file_path)
        self._google_drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
