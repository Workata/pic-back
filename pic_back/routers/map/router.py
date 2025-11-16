from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from tinydb import Query

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import AuthenticatedUser, Marker
from pic_back.routers.auth.utils import get_current_user
from pic_back.routers.map.exceptions import MarkerExists
from pic_back.routers.shared.serializers.output import ResponseMessage
from pic_back.services import GoogleDriveImagesMapperFactory

router = APIRouter(prefix="/api/v1/map", tags=["map"])
query = Query()


@router.post("/marker", response_model=ResponseMessage)
async def create_marker(new_marker: Marker, user: AuthenticatedUser = Depends(get_current_user)) -> JSONResponse:
    markers_db = CollectionProvider.provide(CollectionName.MARKERS)
    if markers_db.get(
        (query.coords.latitude == new_marker.coords.latitude) & (query.coords.longitude == new_marker.coords.longitude)
    ):
        raise MarkerExists(lat=new_marker.coords.latitude, lon=new_marker.coords.longitude)
    markers_db.insert(new_marker.model_dump())
    return JSONResponse(
        content=ResponseMessage(
            detail=(
                f"Marker created for (lat: {new_marker.coords.latitude}, "
                f"lon: {new_marker.coords.longitude}) with url: '{new_marker.url}'."
            )
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.get("/marker", response_model=List[Marker], status_code=status.HTTP_200_OK)
async def get_all_markers() -> JSONResponse:
    markers_db = CollectionProvider.provide(CollectionName.MARKERS)
    return JSONResponse(content=markers_db.all())


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
