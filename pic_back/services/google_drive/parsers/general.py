from pathlib import Path
from typing import Any, Dict, List

from pic_back.db.utils.images_db_operations import ImageNotFoundDbException, ImagesDbOperations
from pic_back.models import GoogleDriveFolder, GoogleDriveFolderContentParsedData, ImageToShow
from pic_back.services.image_url_generator import GoogleDriveImageUrlGenerator


class GoogleDriveFolderContentDataParser:
    def parse(self, data: Dict[Any, Any]) -> GoogleDriveFolderContentParsedData:
        images: List[ImageToShow] = []
        folders: List[GoogleDriveFolder] = []
        for entity in data["files"]:
            id: str = entity["id"]
            name = Path(entity["name"]).stem
            if "folder" in entity.pop("mimeType"):
                folders.append(GoogleDriveFolder(id=id, name=name))
                continue
            images.append(
                ImageToShow(
                    id=id,
                    name=name,
                    comment=self._get_comment(id),
                    thumbnail_url=GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(id),
                    image_url=GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(id),
                )
            )
        return GoogleDriveFolderContentParsedData(
            images=images, folders=folders, next_page_token=data.get("nextPageToken", None)
        )

    def _get_comment(self, img_id: str) -> str:
        try:
            img = ImagesDbOperations.get(img_id)
        except ImageNotFoundDbException:
            return ""
        return img.comment
