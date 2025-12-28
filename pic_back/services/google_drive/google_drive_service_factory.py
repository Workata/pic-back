from typing import Any, List

from google.oauth2.credentials import Credentials
from googleapiclient import discovery

from pic_back.settings import get_settings

# class GoogleDriveServiceInterface(Protocol):
#     def

settings = get_settings()


class GoogleDriveServiceFactory:
    @staticmethod
    def create(scopes: List[str], service_name: str = "drive", version: str = "v3") -> Any:
        credentials = Credentials.from_authorized_user_file(
            filename=str(settings.google_drive_token_json_file_path), scopes=scopes
        )
        return discovery.build(serviceName=service_name, version=version, credentials=credentials)
