from fastapi import APIRouter
import typing as t
from src.services.gdrive import GDriveHandler, GDriveContentParser


router = APIRouter(prefix="/api/v1/gdrive", tags=["gdrive"])


@router.get("/folder/{folder_url_id}")
def read_root(folder_url_id: str) -> t.Any:
    handler = GDriveHandler()
    res = handler.query_content(query=f"'{folder_url_id}' in parents", fields=["id", "name", "mimeType"])
    parser = GDriveContentParser()
    parsed_res = parser.parse(res)
    return parsed_res
