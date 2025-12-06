import typing as t
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload


class FileUploader:
    SCOPES: t.List[str] = ["https://www.googleapis.com/auth/drive.file"]

    def __init__(self, token_json_file_path: Path = Path("./data/token.json")) -> None:
        credentials = Credentials.from_authorized_user_file(filename=str(token_json_file_path), scopes=self.SCOPES)
        self._google_drive_service = discovery.build(serviceName="drive", version="v3", credentials=credentials)

    def upload(self, file_path: Path, parent_folder_id: str, uploaded_file_name: str) -> None:
        file_metadata = {"name": uploaded_file_name, "parents": [parent_folder_id]}
        media = MediaFileUpload(filename=file_path)
        self._google_drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
