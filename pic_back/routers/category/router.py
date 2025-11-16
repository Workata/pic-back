import math
from typing import List, Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, Response
from tinydb import Query
from tinydb.table import Document

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import AuthenticatedUser, Category
from pic_back.routers.auth.utils import get_current_user
from pic_back.routers.category.exceptions import CategoryExists, CategoryNotFound
from pic_back.routers.category.serializers.input import UpdateCategoryInputSerializer
from pic_back.routers.category.serializers.output import ImagesFromCategoryOutputSerializer, ImageToShow
from pic_back.services import GoogleDriveImageUrlGenerator
from pic_back.settings import get_settings

query = Query()
router_path = "api/v1/categories"
router = APIRouter(prefix=f"/{router_path}", tags=["categories"])
config = get_settings()


@router.get("", response_model=List[Category], status_code=status.HTTP_200_OK)
async def list_categories() -> JSONResponse:
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
    return JSONResponse(content=categories_db.all())


@router.get("/{category_name}", response_model=ImagesFromCategoryOutputSerializer)
async def get_images_from_category(
    category_name: str, request: Request, page: int = 0, page_size: int = config.default_page_size
) -> JSONResponse:
    """
    Get images belonging to given category
    Paginated
    TODO page, page_size validation
    """
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
    if not categories_db.get(query.name == category_name):
        raise CategoryNotFound(name=category_name)

    images_db = CollectionProvider.provide(CollectionName.IMAGES)
    images_from_category = images_db.search(query.categories.any(query.name == category_name))
    number_of_images_from_category = len(images_from_category)
    total_number_of_pages = math.ceil(number_of_images_from_category / page_size)
    offset = page * page_size
    images = images_db.search(
        query.categories.any(query.name == category_name)
    )[
        offset : offset
        + page_size  # noqa: E203
    ]
    images = [
        ImageToShow(
            id=img["id"],
            name=img["name"],
            comment=img["comment"],
            thumbnail_url=GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(img["id"]),
            image_url=GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(img["id"]),
        ).model_dump()
        for img in images
    ]

    endpoint_url = f"{request.base_url}{router_path}/{category_name}"
    previous_page = page - 1 if page != 0 else None
    previous_page_link = f"{endpoint_url}?page={previous_page}" if previous_page is not None else None
    next_page = page + 1 if page < total_number_of_pages - 1 else None
    next_page_link = f"{endpoint_url}?page={next_page}" if next_page is not None else None
    serialized_response = ImagesFromCategoryOutputSerializer(
        images=images,
        previous_page_link=previous_page_link,
        next_page_link=next_page_link,
        total_number_of_records=number_of_images_from_category,
        total_number_of_pages=total_number_of_pages,
        previous_page=previous_page,
        current_page=page,
        next_page=next_page,
        page_size=page_size,
    )
    return JSONResponse(content=serialized_response.model_dump(), status_code=status.HTTP_200_OK)


@router.post("")
async def create_category(new_category: Category, user: AuthenticatedUser = Depends(get_current_user)) -> JSONResponse:
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
    if categories_db.get(query.name == new_category.name):
        raise CategoryExists(name=new_category.name)
    categories_db.insert(new_category.model_dump())
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
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
    removed_categories: Optional[Document] = categories_db.remove(query.name == category_name)
    if not removed_categories:
        raise CategoryNotFound(name=category_name)
    images_db = CollectionProvider.provide(CollectionName.IMAGES)
    images = images_db.search(query.categories.any(query.name == category_name))
    for image in images:
        updated_categories = list(filter(lambda item: item["name"] != category_name, image["categories"]))
        images_db.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("")
async def update_category(
    category_to_update: UpdateCategoryInputSerializer, user: AuthenticatedUser = Depends(get_current_user)
) -> Response:
    """
    Update category in 'categories' collection
    and then update it in every image that contains this category ('images' collection)
    """
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
    category: Optional[Document] = categories_db.get(query.name == category_to_update.old_name)
    if not category:
        raise CategoryNotFound(name=category_to_update.old_name)
    new_category = Category(name=category_to_update.new_name).dict()
    categories_db.update(new_category, doc_ids=[category.doc_id])

    images_db = CollectionProvider.provide(CollectionName.IMAGES)
    images = images_db.search(query.categories.any(query.name == category_to_update.old_name))
    for image in images:
        # TODO this can be probably done with one operation
        updated_categories = list(
            filter(lambda item: item["name"] != category_to_update.old_name, image["categories"])
        )  # delete old category
        updated_categories.append(new_category)  # append updated one
        images_db.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
