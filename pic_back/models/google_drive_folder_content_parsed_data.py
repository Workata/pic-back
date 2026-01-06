from typing import List, Optional

from ..routers.shared.serializers import BaseOutputSerializer
from .google_drive_folder import GoogleDriveFolder
from .image import ImageToShow


class GoogleDriveFolderContentParsedData(BaseOutputSerializer):
    images: List[ImageToShow]
    folders: List[GoogleDriveFolder]
    next_page_token: Optional[str] = None
