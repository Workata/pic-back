import typing as t

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from settings import get_settings


settings = get_settings()


class GoogleDriveDataFetcher:
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    SPACES: str = "drive"

    def __init__(self) -> None:
        creds = Credentials.from_authorized_user_file("../data/token.json", self.SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    def query_content(
        self,
        query: str,
        fields: t.List[str],
        page_token: t.Optional[str] = None,
        page_size: int = settings.images_page_size,
    ) -> t.Any:
        fields_str = ", ".join(fields)
        if page_token:
            return (
                self.service.files()
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
            self.service.files()
            .list(
                q=query,
                spaces=self.SPACES,
                fields=f"nextPageToken, files({fields_str})",
                pageSize=page_size,
                orderBy="name",
            )
            .execute()
        )
