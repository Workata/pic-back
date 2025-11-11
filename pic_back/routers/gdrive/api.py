import typing as t

from fastapi import APIRouter

from pic_back.services import GoogleDriveDataFetcher, GoogleDriveGeneralDataParser
from pic_back.settings import get_settings

router = APIRouter(prefix="/api/v1/gdrive", tags=["gdrive"])
settings = get_settings()


@router.get("/folder/{folder_id}")
def get_folder_content(folder_id: str, page_token: t.Optional[str] = None) -> t.Any:
    """
    TODO ANALAYZE
    if page size is more than 25 there seems to be a problem
    with loading pics in viewer on frontend site
    e.g.: click on 29th pic
    """
    fetcher = GoogleDriveDataFetcher()
    res = fetcher.query_content(
        query=f"'{folder_id}' in parents", fields=["id", "name", "mimeType"], page_token=page_token
    )
    parser = GoogleDriveGeneralDataParser()
    parsed_res = parser.parse(res)
    return parsed_res
