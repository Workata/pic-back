from tinydb import TinyDB, Query
from fastapi import APIRouter
from src.models import Marker

import typing as t


IMG_MAP_MARKER_DB_PATH = "./data/database/image_map.json"
img_map_marker_db = TinyDB(IMG_MAP_MARKER_DB_PATH)
query = Query()

router = APIRouter(prefix="/api/v1/map", tags=["map"])


@router.post("/marker")
async def create_marker(marker: Marker) -> t.Dict[str, str]:
    # TODO check duplicates by lon/lat
    # is_duplicated = bool(categories_db.search(query.category == category.name))
    # if is_duplicated:
    #     return {"info": "Category exists"}
    img_map_marker_db.insert({"latitude": marker.latitude, "longitude": marker.longitude, "url": marker.url})
    return {"info": f"Marker created for (lat: {marker.latitude}, lon: {marker.longitude}) with url: {marker.url}"}


@router.get("/marker")
async def get_markers() -> t.Any:  # t.List[Document]:
    return img_map_marker_db.all()
