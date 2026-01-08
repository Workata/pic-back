from typing import List, Optional

from pic_back.routers.shared.serializers.output import BaseOutputSerializer

from .folder import GoogleDriveFolderOutputSerializer
from .image_to_show import ImageToShowOutputSerializer


class GoogleDriveFolderContentOutputSerializer(BaseOutputSerializer):
    images: List[ImageToShowOutputSerializer]
    folders: List[GoogleDriveFolderOutputSerializer]
    next_page_token: Optional[str] = None
