from typing import List

from db import CollectionProvider
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from models import AuthenticatedUser, Marker, ResponseMessage
from routers.auth.utils import get_current_user
from routers.map.exceptions import MarkerExists
from services import GoogleDriveImagesMapperFactory
from tinydb import Query

router = APIRouter(prefix="/api/v1/map", tags=["map"])
collection_provider = CollectionProvider()
query = Query()


@router.post("/marker", response_model=ResponseMessage)
async def create_marker(new_marker: Marker, user: AuthenticatedUser = Depends(get_current_user)) -> JSONResponse:
    markers_coll = collection_provider.provide("markers")
    if markers_coll.get(
        (query.coords.latitude == new_marker.coords.latitude) & (query.coords.longitude == new_marker.coords.longitude)
    ):
        raise MarkerExists(lat=new_marker.coords.latitude, lon=new_marker.coords.longitude)
    markers_coll.insert(new_marker.model_dump())
    return JSONResponse(
        content=ResponseMessage(
            detail=(
                f"Marker created for (lat: {new_marker.coords.latitude}, "
                f"lon: {new_marker.coords.longitude}) with url: '{new_marker.url}'."
            )
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.get("/marker", response_model=List[Marker])
async def get_all_markers() -> JSONResponse:
    markers_coll = collection_provider.provide("markers")
    return JSONResponse(content=markers_coll.all(), status_code=status.HTTP_200_OK)


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
