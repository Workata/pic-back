from typing import List, Optional

from pydantic import BaseModel

from pic_back.services.google_drive.google_drive_service_factory import GoogleDriveServiceFactory
from pic_back.settings import get_settings

settings = get_settings()


class ChainedGoogleDriveFolder(BaseModel):
    id: str
    name: str
    level: int


class GoogleDriveFolderPathGetter:
    SCOPES: List[str] = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

    def __init__(self) -> None:
        self._gdrive_service = GoogleDriveServiceFactory.create(scopes=self.SCOPES)

    def get(
        self, folder_id: str, search_up_to_folder_id: Optional[str] = settings.google_drive_upload_images_folder_id
    ) -> List[ChainedGoogleDriveFolder]:
        """
        search_up_to_folder_id - not included in a result
        """
        folders = []
        level = 0
        target_folder = self._gdrive_service.files().get(fileId=folder_id, fields="id, name, parents").execute()

        folders.append(
            ChainedGoogleDriveFolder(id=target_folder.get("id"), name=target_folder.get("name"), level=level)
        )

        parent = target_folder.get("parents")
        if not parent:
            return folders

        while True:
            level += 1
            folder = self._gdrive_service.files().get(fileId=parent[0], fields="id, name, parents").execute()
            parent = folder.get("parents")
            folder_name = folder.get("name")
            folder_id = folder.get("id")
            if parent is None or (search_up_to_folder_id is not None and search_up_to_folder_id == folder_id):
                break
            folders.append(ChainedGoogleDriveFolder(id=folder_id, name=folder_name, level=level))
        return folders
