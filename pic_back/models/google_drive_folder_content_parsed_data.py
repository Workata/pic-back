from typing import List, Optional

from pydantic import BaseModel

from .google_drive_folder import GoogleDriveFolder
from .image import ImageToShow


class GoogleDriveFolderContentParsedData(BaseModel):
    """
    DB Model: NO
    """

    images: List[ImageToShow]
    folders: List[GoogleDriveFolder]
    next_page_token: Optional[str] = None
