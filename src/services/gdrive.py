import typing as t
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from tinydb import Query

from src.db import CollectionProvider

from . import GDriveImageUrlGenerator


class GDriveHandler:
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

    def __init__(self) -> None:
        creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    def query_content(self, query: str, fields: t.List[str], spaces: str = "drive", page_size: int = 10) -> t.Any:
        fields_str = ", ".join(fields)
        results = (
            self.service.files()
            .list(
                q=query, spaces=spaces, fields=f"nextPageToken, files({fields_str})", pageSize=page_size, orderBy="name"
            )
            .execute()
        )
        return results


class GDriveContentParser:
    def __init__(self) -> None:
        self._images_collection = CollectionProvider().provide("images")

    def parse(self, gdrive_content: t.Dict[t.Any, t.Any]) -> t.Dict[str, t.Any]:
        content_objects = gdrive_content["files"]
        images = []
        folders = []
        for obj in content_objects:
            if "folder" in obj.pop("mimeType"):
                folders.append(obj)
            else:
                img_id: str = obj["id"]
                obj["thumbnail_url"] = GDriveImageUrlGenerator.generate_thumbnail_img_url(img_id)
                obj["image_url"] = GDriveImageUrlGenerator.generate_standard_img_url(img_id)
                obj["name"] = Path(obj["name"]).stem  # remove file extension
                obj["comment"] = self._get_comment(img_id)
                images.append(obj)
        return {"images": images, "folders": folders}

    def _get_comment(self, img_id: str) -> str:
        img = self._images_collection.get(Query().id == img_id)
        return img["comment"] if img is not None else ""  # type: ignore
