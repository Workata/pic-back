import typing as t
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

from pic_back.settings import get_settings

settings = get_settings()


class GoogleDriveDataFetcher:
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    SPACES: str = "drive"

    def __init__(self, token_json_file_path: Path = Path("./data/token.json")) -> None:
        credentials = Credentials.from_authorized_user_file(filename=token_json_file_path, scopes=self.SCOPES)
        self._google_drive_service = discovery.build(serviceName="drive", version="v3", credentials=credentials)

    def query_content(
        self,
        query: str,
        fields: t.List[str],
        page_token: t.Optional[str] = None,
        page_size: int = settings.default_page_size,
    ) -> t.Any:
        fields_str = ", ".join(fields)
        if page_token:
            return (
                self._google_drive_service.files()
                .list(
                    q=query,
                    spaces=self.SPACES,
                    fields=f"nextPageToken, files({fields_str})",
                    pageToken=page_token,
                    pageSize=page_size,
                    orderBy="name",
                )
                .execute()
            )
        return (
            self._google_drive_service.files()
            .list(
                q=query,
                spaces=self.SPACES,
                fields=f"nextPageToken, files({fields_str})",
                pageSize=page_size,
                orderBy="name",
            )
            .execute()
        )
