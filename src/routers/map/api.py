from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from tinydb import Query, TinyDB

from src.models import AuthenticatedUser, Marker
from src.routers.auth.utils import get_current_user

IMG_MAP_MARKER_DB_PATH = "./data/database/image_map.json"
img_map_marker_db = TinyDB(IMG_MAP_MARKER_DB_PATH)
query = Query()

router = APIRouter(prefix="/api/v1/map", tags=["map"])


@router.post("/marker")  # TODO define response model
async def create_marker(marker: Marker, user: AuthenticatedUser = Depends(get_current_user)) -> JSONResponse:
    # TODO check duplicates by lon/lat
    # is_duplicated = bool(categories_db.search(query.category == category.name))
    # if is_duplicated:
    #     return {"detail": "Category exists"}
    img_map_marker_db.insert({"latitude": marker.latitude, "longitude": marker.longitude, "url": marker.url})
    return JSONResponse(
        content={
            "detail": f"Marker created for (lat: {marker.latitude}, lon: {marker.longitude}) with url: {marker.url}"
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/marker", response_model=List[Marker])
async def get_all_markers() -> JSONResponse:
    return JSONResponse(content=img_map_marker_db.all(), status_code=status.HTTP_200_OK)
