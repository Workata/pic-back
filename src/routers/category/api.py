from typing import List, Any

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from tinydb import Query

from src.models import Category, AuthenticatedUser
from src.db import CollectionProvider
from src.services import GDriveImageUrlGenerator
from src.routers.auth.utils import get_current_user


collection_provider = CollectionProvider()
query = Query()
router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("", response_model=List[Category])
async def get_all_categories() -> JSONResponse:
    categories_coll = collection_provider.provide("categories")
    return JSONResponse(content=categories_coll.all(), status_code=status.HTTP_200_OK)


@router.get("/{category_name}", response_model=Any)
async def get_images_from_category(category_name: str) -> JSONResponse:
    """
    Select category and get images belonging to this category
    Res: [{id, name, comment, image_url, thumbnail_url}]
    """
    images_coll = collection_provider.provide("images")
    images = images_coll.search(query.categories.any(query.name == category_name))
    formatted_images = [
        {
            "id": img["id"],
            "name": img["name"],
            "comment": img["comment"],
            "thumbnail_url": GDriveImageUrlGenerator.generate_thumbnail_img_url(img["id"]),
            "image_url": GDriveImageUrlGenerator.generate_standard_img_url(img["id"]),
        }
        for img in images
    ]
    return JSONResponse(content=formatted_images, status_code=status.HTTP_200_OK)


@router.post("")
async def create_new_category(
    new_category: Category, user: AuthenticatedUser = Depends(get_current_user)
) -> JSONResponse:
    categories = collection_provider.provide("categories")
    if bool(categories.search(query.name == new_category.name)):
        return JSONResponse(
            content={"info": "Category already exists. Please provide different name."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    categories.insert(new_category.dict())
    return JSONResponse(
        content={"info": f"Category '{new_category.name}' has been created successfuly."},
        status_code=status.HTTP_201_CREATED,
    )
