from pathlib import Path
from typing import Any, Dict, List

from pic_back.db.utils.images_db_operations import ImageNotFoundDbException, ImagesDbOperations

# from pic_back.routers.gdrive.serializers.output import (
#     GoogleDriveFolderContentOutputSerializer,
#     GoogleDriveFolderOutputSerializer,
#     ImageToShowOutputSerializer,
# )
from pic_back.routers.gdrive.serializers.output.folder import GoogleDriveFolderOutputSerializer
from pic_back.routers.gdrive.serializers.output.folder_content import GoogleDriveFolderContentOutputSerializer
from pic_back.routers.gdrive.serializers.output.image_to_show import ImageToShowOutputSerializer


class GoogleDriveFolderContentParser:
    def parse(self, data: Dict[Any, Any]) -> GoogleDriveFolderContentOutputSerializer:
        images: List[ImageToShowOutputSerializer] = []
        folders: List[GoogleDriveFolderOutputSerializer] = []
        for entity in data["files"]:
            id: str = entity["id"]
            name = Path(entity["name"]).stem
            if "folder" in entity.pop("mimeType"):
                folders.append(GoogleDriveFolderOutputSerializer(id=id, name=name))
                continue
            images.append(ImageToShowOutputSerializer(id=id, name=name, comment=self._get_comment(id)))
        return GoogleDriveFolderContentOutputSerializer(
            images=images, folders=folders, next_page_token=data.get("nextPageToken", None)
        )

    def _get_comment(self, img_id: str) -> str:
        try:
            img = ImagesDbOperations.get(img_id)
        except ImageNotFoundDbException:
            return ""
        return img.comment
