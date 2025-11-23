from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from tinydb import Query

from pic_back.db.utils import MarkerExistsException, MarkersDbOperations
from pic_back.models import AuthenticatedUser, Marker
from pic_back.routers.auth.utils import get_current_user
from pic_back.routers.map.exceptions import MarkerExistsHTTPException
from pic_back.routers.shared.serializers.output import ResponseMessage
from pic_back.services import GoogleDriveImagesMapperFactory
from pic_back.settings import get_settings

settings = get_settings()
router = APIRouter(prefix=f"{settings.global_api_prefix}/map", tags=["map"])
query = Query()


@router.get("/marker", response_model=List[Marker], status_code=status.HTTP_200_OK)
async def list_markers() -> List[Marker]:
    return MarkersDbOperations.get_all()


@router.post("/marker", response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
async def create_marker(marker: Marker, user: AuthenticatedUser = Depends(get_current_user)) -> ResponseMessage:
    try:
        MarkersDbOperations.create(marker)
    except MarkerExistsException:
        raise MarkerExistsHTTPException(lat=marker.coords.latitude, lon=marker.coords.longitude)
    return ResponseMessage(
        detail=(
            f"Marker created for (lat: {marker.coords.latitude}, lon: {marker.coords.longitude}) with url: '{marker.url}'."
        )
    )


def map_folder_task(folder_id: str) -> None:
    mapper = GoogleDriveImagesMapperFactory.create()
    mapper.map_folder(folder_id)


@router.post("/folder/{folder_id}")
async def map_folder(
    folder_id: str, background_tasks: BackgroundTasks, user: AuthenticatedUser = Depends(get_current_user)
) -> JSONResponse:
    background_tasks.add_task(map_folder_task, folder_id)
    return JSONResponse(
        content={"info": "Folder will be mapped in the background!"}, status_code=status.HTTP_201_CREATED
    )
