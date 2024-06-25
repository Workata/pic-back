import typing as t
from pathlib import Path

from tinydb import Query

from db import CollectionProvider

from services.image_url_generator import GoogleDriveImageUrlGenerator


class GoogleDriveGeneralDataParser:
    def __init__(self) -> None:
        self._images_collection = CollectionProvider().provide("images")

    def parse(self, data: t.Dict[t.Any, t.Any]) -> t.Dict[str, t.Any]:
        content_objects = data["files"]
        images = []
        folders = []
        for obj in content_objects:
            if "folder" in obj.pop("mimeType"):
                folders.append(obj)
                continue
            img_id: str = obj["id"]
            obj["thumbnail_url"] = GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(img_id)
            obj["image_url"] = GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(img_id)
            obj["name"] = Path(obj["name"]).stem  # remove file extension
            obj["comment"] = self._get_comment(img_id)
            images.append(obj)
        next_page_token = data.get("nextPageToken", None)
        return {"images": images, "folders": folders, "nextPageToken": next_page_token}

    def _get_comment(self, img_id: str) -> str:
        img = self._images_collection.get(Query().id == img_id)
        return img["comment"] if img is not None else ""  # type: ignore
