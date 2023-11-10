from typing import Any, Dict, List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from tinydb import Query

from src.db import CollectionProvider
from src.models import Image

collection_provider = CollectionProvider()
query = Query()
router = APIRouter(prefix="/api/v1/images", tags=["images"])


@router.post("")
async def create_image(new_img: Image) -> JSONResponse:
    """Create new image"""
    images = collection_provider.provide("images")
    if bool(images.search(query.id == new_img.id)):
        return JSONResponse(
            content={"info": "Image with this ID already exists!"}, status_code=status.HTTP_400_BAD_REQUEST
        )
    new_img_dict = new_img.dict()
    images.insert(new_img_dict)
    return JSONResponse(content=new_img_dict, status_code=status.HTTP_201_CREATED)


@router.get("/{img_id}")
async def get_image(img_id: str) -> JSONResponse:
    images_coll = collection_provider.provide("images")
    image: Dict[str, Any] = images_coll.get(query.id == img_id)
    if not image:
        return JSONResponse(
            content={"info": f"Image with id {img_id} not found!"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(content=image, status_code=status.HTTP_200_OK)


@router.get("/category/{category_name}")
async def get_images_from_category(category_name: str) -> JSONResponse:
    images_coll = collection_provider.provide("images")
    images = images_coll.search(query.categories.any(query.name == category_name))
    return JSONResponse(content=images, status_code=status.HTTP_200_OK)


@router.get("/{img_id}/categories")
async def get_categories_of_image(img_id: str) -> JSONResponse:
    images_coll = collection_provider.provide("images")
    image: Dict[str, Any] = images_coll.get(query.id == img_id)
    if not image:
        return JSONResponse(
            content={"info": f"Image with id {img_id} not found!"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(content=image.get("categories", []), status_code=status.HTTP_200_OK)


@router.patch("/{img_id}/categories")
async def update_image_categories(img_id: str, categories: List[str]) -> JSONResponse:
    images_coll = collection_provider.provide("images")
    categories_coll = collection_provider.provide("categories")
    found_categories = categories_coll.search(query.name.one_of(categories))

    image: Image = images_coll.search(query.id.search(img_id))
    if not image:
        return JSONResponse(
            content={"info": f"Image with id {img_id} not found!"}, status_code=status.HTTP_404_NOT_FOUND
        )

    images_coll.update({"categories": found_categories}, query.id.search(img_id))
    return JSONResponse(
        content={"info": f"Categories of img {img_id} has been updated!"}, status_code=status.HTTP_200_OK
    )
