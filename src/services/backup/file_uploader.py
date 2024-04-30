import typing as t

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class FileUploader:
    SCOPES: t.List[str] = ["https://www.googleapis.com/auth/drive.file"]

    def __init__(self) -> None:
        creds = Credentials.from_authorized_user_file("../data/token.json", self.SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    def upload(self, file_path: str, parent_folder_id: str, uploaded_file_name: str) -> None:
        file_metadata = {"name": uploaded_file_name, "parents": [parent_folder_id]}
        media = MediaFileUpload(file_path)
        self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
