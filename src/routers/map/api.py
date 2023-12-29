from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from tinydb import Query

from src.db import CollectionProvider
from src.models import AuthenticatedUser, Marker, ResponseMessage
from src.routers.auth.utils import get_current_user
from src.routers.map.exceptions import MarkerExists

router = APIRouter(prefix="/api/v1/map", tags=["map"])
collection_provider = CollectionProvider()
query = Query()


@router.post("/marker", response_model=ResponseMessage)
async def create_marker(new_marker: Marker, user: AuthenticatedUser = Depends(get_current_user)) -> JSONResponse:
    markers_coll = collection_provider.provide("markers")
    if markers_coll.get((query.latitude == new_marker.latitude) & (query.longitude == new_marker.longitude)):
        raise MarkerExists(lat=new_marker.latitude, lon=new_marker.longitude)
    markers_coll.insert(new_marker.dict())
    return JSONResponse(
        content=ResponseMessage(
            detail=(
                f"Marker created for (lat: {new_marker.latitude}, "
                f"lon: {new_marker.longitude}) with url: '{new_marker.url}'."
            )
        ).dict(),
        status_code=status.HTTP_200_OK,
    )


@router.get("/marker", response_model=List[Marker])
async def get_all_markers() -> JSONResponse:
    markers_coll = collection_provider.provide("markers")
    return JSONResponse(content=markers_coll.all(), status_code=status.HTTP_200_OK)
