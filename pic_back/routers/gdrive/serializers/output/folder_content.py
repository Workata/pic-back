from typing import List, Optional

from pic_back.routers.gdrive.serializers.output.folder import GoogleDriveFolderOutputSerializer

# from .folder import GoogleDriveFolderOutputSerializer
# from .image_to_show import ImageToShowOutputSerializer
from pic_back.routers.gdrive.serializers.output.image_to_show import ImageToShowOutputSerializer
from pic_back.routers.shared.serializers.output.base_output_serializer import BaseOutputSerializer


class GoogleDriveFolderContentOutputSerializer(BaseOutputSerializer):
    images: List[ImageToShowOutputSerializer]
    folders: List[GoogleDriveFolderOutputSerializer]
    next_page_token: Optional[str] = None
