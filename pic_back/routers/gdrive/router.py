from typing import List, Optional

from fastapi import APIRouter, status

from pic_back.models import GoogleDriveFolderContentParsedData
from pic_back.services import GoogleDriveDataFetcher, GoogleDriveFolderContentDataParser
from pic_back.services.google_drive.folder_path_getter import ChainedGoogleDriveFolder, GoogleDriveFolderPathGetter
from pic_back.settings import get_settings

settings = get_settings()
router = APIRouter(prefix=f"{settings.global_api_prefix}/gdrive", tags=["gdrive"])


@router.get("/folder/{folder_id}", response_model=GoogleDriveFolderContentParsedData, status_code=status.HTTP_200_OK)
async def get_folder_content(folder_id: str, page_token: Optional[str] = None) -> GoogleDriveFolderContentParsedData:
    """
    TODO ANALAYZE
    if page size is more than 25 there seems to be a problem
    with loading pics in viewer on frontend site
    e.g.: click on 29th pic
    """
    fetcher = GoogleDriveDataFetcher()
    parser = GoogleDriveFolderContentDataParser()

    google_drive_data = fetcher.query_content(
        query=f"'{folder_id}' in parents", fields=["id", "name", "mimeType"], page_token=page_token
    )
    return parser.parse(google_drive_data)


@router.get("/folder/path/{folder_id}", response_model=List[ChainedGoogleDriveFolder], status_code=status.HTTP_200_OK)
async def get_folder_path(folder_id: str) -> List[ChainedGoogleDriveFolder]:
    folder_path_getter = GoogleDriveFolderPathGetter()
    return folder_path_getter.get(folder_id)
