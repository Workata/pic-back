from typing import List, Any, Optional

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse, Response
from tinydb import Query
from tinydb.table import Document

from models import Category, AuthenticatedUser
from db import CollectionProvider
from services import GoogleDriveImageUrlGenerator
from routers.auth.utils import get_current_user
from .exceptions import CategoryNotFound, CategoryExists
from .serializers import UpdateCategorySerializer


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
    categories_coll = collection_provider.provide("categories")

    if not categories_coll.get(query.name == category_name):
        raise CategoryNotFound(name=category_name)

    images = images_coll.search(query.categories.any(query.name == category_name))
    formatted_images = [
        {
            "id": img["id"],
            "name": img["name"],
            "comment": img["comment"],
            "thumbnail_url": GoogleDriveImageUrlGenerator.generate_thumbnail_img_url(img["id"]),
            "image_url": GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(img["id"]),
        }
        for img in images
    ]
    return JSONResponse(content=formatted_images, status_code=status.HTTP_200_OK)


@router.post("")
async def create_category(new_category: Category, user: AuthenticatedUser = Depends(get_current_user)) -> JSONResponse:
    categories = collection_provider.provide("categories")
    if categories.get(query.name == new_category.name):
        raise CategoryExists(name=new_category.name)
    categories.insert(new_category.dict())
    return JSONResponse(
        content={"detail": f"Category '{new_category.name}' has been created successfuly."},
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{category_name}")
async def delete_category(category_name: str, user: AuthenticatedUser = Depends(get_current_user)) -> Response:
    """
    Delete category from 'categories' collection
    and then delete it from every image that contains this category ('images' collection)
    """
    categories_coll = collection_provider.provide("categories")
    removed_categories: Optional[Document] = categories_coll.remove(query.name == category_name)
    if not removed_categories:
        raise CategoryNotFound(name=category_name)
    images_coll = collection_provider.provide("images")
    images = images_coll.search(query.categories.any(query.name == category_name))
    for image in images:
        updated_categories = list(filter(lambda item: item["name"] != category_name, image["categories"]))
        images_coll.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("")
async def update_category(
    category_to_update: UpdateCategorySerializer, user: AuthenticatedUser = Depends(get_current_user)
) -> Response:
    """
    Update category in 'categories' collection
    and then update it in every image that contains this category ('images' collection)
    """
    categories_coll = collection_provider.provide("categories")
    category: Optional[Document] = categories_coll.get(query.name == category_to_update.old_name)
    if not category:
        raise CategoryNotFound(name=category_to_update.old_name)
    new_category = Category(name=category_to_update.new_name).dict()
    categories_coll.update(new_category, doc_ids=[category.doc_id])

    images_coll = collection_provider.provide("images")
    images = images_coll.search(query.categories.any(query.name == category_to_update.old_name))
    for image in images:
        # TODO this can be probably done with one operation
        updated_categories = list(
            filter(lambda item: item["name"] != category_to_update.old_name, image["categories"])
        )  # delete old category
        updated_categories.append(new_category)  # append updated one
        images_coll.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
