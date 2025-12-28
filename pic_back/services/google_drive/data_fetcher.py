from typing import Any, List, Optional

from pic_back.services.google_drive.google_drive_service_factory import GoogleDriveServiceFactory
from pic_back.settings import get_settings

settings = get_settings()


class GoogleDriveDataFetcher:
    SCOPES: List[str] = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    SPACES: str = "drive"

    def __init__(self) -> None:
        self._google_drive_service = GoogleDriveServiceFactory.create(scopes=self.SCOPES)

    def query_content(
        self,
        query: str,
        fields: List[str],
        page_token: Optional[str] = None,
        page_size: int = settings.default_page_size,
    ) -> Any:
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
