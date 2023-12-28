from typing import List, Any, Optional

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse, Response
from tinydb import Query
from tinydb.table import Document

from src.models import Category, AuthenticatedUser
from src.db import CollectionProvider
from src.services import GDriveImageUrlGenerator
from src.routers.auth.utils import get_current_user
from .exceptions import CategoryNotFound, CategoryExists


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
    Get images belonging to given category
    Res: [{id, name, comment, image_url, thumbnail_url}]
    TODO create response model
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
        raise CategoryExists(name=new_category.name)
    categories.insert(new_category.dict())
    return JSONResponse(
        content={"detail": f"Category '{new_category.name}' has been created successfuly."},
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("")
async def delete_category(
    category_to_delete: Category, user: AuthenticatedUser = Depends(get_current_user)
) -> Response:
    """
    Delete category from 'categories' collection
    and then delete it from every image that contains this category ('images' collection)
    """
    categories_coll = collection_provider.provide("categories")
    removed_categories: Optional[Document] = categories_coll.remove(query.name == category_to_delete.name)
    if not removed_categories:
        raise CategoryNotFound(name=category_to_delete.name)
    images_coll = collection_provider.provide("images")
    images = images_coll.search(query.categories.any(query.name == category_to_delete.name))
    for image in images:
        updated_categories = list(filter(lambda item: item["name"] != category_to_delete.name, image["categories"]))
        images_coll.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
