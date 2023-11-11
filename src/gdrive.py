from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pathlib import Path

import typing as t


# * needed only for testing, normally it should be on frontend only
ROOT_FOLDER = "1Q3AAZ7wW-I7vG0ONIW_o0vWnHEJv8Ckm"

# thumbnail (without admin):
# https://drive.google.com/thumbnail?id=1nHP3SRWm1gWTK5BG_009Bie4oJ-_MFYp

# full pic (without admin):
# <img src="https://drive.google.com/uc?id=FILEID" />

# high res:
# 1Q3AAZ7wW-I7vG0ONIW_o0vWnHEJv8Ckm

# USE ID FROM REQUEST (NOT FROM URL!!!)
# thumb
# https://drive.google.com/thumbnail?id=1F6WlnanzKcvP1cyAlHu5dBne61BuhWk_


class GDriveHandler:
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

    def __init__(self) -> None:
        creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    def query_content(self, query: str, fields: t.List[str], spaces: str = "drive", page_size: int = 10) -> t.Any:
        fields_str = ", ".join(fields)
        results = (
            self.service.files()
            .list(q=query, spaces=spaces, fields=f"nextPageToken, files({fields_str})", pageSize=page_size)
            .execute()
        )
        return results


class GDriveContentParser:
    THUMBNAIL_BASE_URL = "https://drive.google.com/thumbnail"
    IMAGE_BASE_URL = "https://drive.google.com/uc"

    def parse(self, gdrive_content: t.Dict[t.Any, t.Any]) -> t.Dict[str, t.Any]:
        content_objects = gdrive_content["files"]
        images = []
        folders = []
        for obj in content_objects:
            if "folder" in obj.pop("mimeType"):
                folders.append(obj)
            else:
                obj["thumbnail_url"] = f"{self.THUMBNAIL_BASE_URL}?id={obj['id']}"
                obj["image_url"] = f"{self.IMAGE_BASE_URL}?id={obj['id']}"
                obj["name"] = Path(obj["name"]).stem  # remove extension
                images.append(obj)
        return {"images": images, "folders": folders}
