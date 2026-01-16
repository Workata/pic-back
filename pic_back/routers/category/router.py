import math
from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import Response
from pydantic import HttpUrl
from tinydb import Query

from pic_back.db import CollectionName, CollectionProvider
from pic_back.db.utils import CategoriesDbOperations, CategoryExistsException, CategoryNotFoundException
from pic_back.models import AuthenticatedUser, Category
from pic_back.routers.auth.utils import get_current_user
from pic_back.routers.category.exceptions import CategoryExistsHTTPException, CategoryNotFoundHTTPException
from pic_back.routers.category.serializers.input import UpdateCategoryInputSerializer
from pic_back.routers.category.serializers.output import ImagesFromCategoryOutputSerializer
from pic_back.routers.gdrive.serializers.output import ImageToShowOutputSerializer
from pic_back.routers.shared.serializers.output import ResponseMessage
from pic_back.settings import get_settings

query = Query()
settings = get_settings()
router_prefix = f"{settings.global_api_prefix}/categories"
router = APIRouter(prefix=router_prefix, tags=["categories"])


@router.get("", response_model=List[Category], status_code=status.HTTP_200_OK)
async def list_categories() -> List[Category]:
    return CategoriesDbOperations.get_all()


@router.post("", response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
async def create_category(
    new_category: Category, user: AuthenticatedUser = Depends(get_current_user)
) -> ResponseMessage:
    try:
        CategoriesDbOperations.create(new_category)
    except CategoryExistsException:
        raise CategoryExistsHTTPException(name=new_category.name)
    return ResponseMessage(detail=f"Category '{new_category.name}' has been created successfuly")


@router.delete("/{category_name}", response_model=ResponseMessage, status_code=status.HTTP_200_OK)
async def delete_category(category_name: str, user: AuthenticatedUser = Depends(get_current_user)) -> ResponseMessage:
    """
    Delete category from 'categories' collection
    and then delete it from every image that contains this category ('images' collection)
    """
    try:
        CategoriesDbOperations.delete(category_name)
    except CategoryNotFoundException:
        raise CategoryNotFoundHTTPException(name=category_name)

    images_db = CollectionProvider.provide(CollectionName.IMAGES)
    images = images_db.search(query.categories.any(query.name == category_name))
    for image in images:
        updated_categories = list(filter(lambda item: item["name"] != category_name, image["categories"]))
        images_db.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return ResponseMessage(detail=f"Category '{category_name}' has been deleted successfuly")


@router.get("/{category_name}", response_model=ImagesFromCategoryOutputSerializer, status_code=status.HTTP_200_OK)
async def get_images_from_category(
    category_name: str, request: Request, page: int = 0, page_size: int = settings.default_page_size
) -> ImagesFromCategoryOutputSerializer:
    """
    Get images belonging to given category (paginated)

    TODO move to images router
    """
    if not CategoriesDbOperations.exists(category_name):
        raise CategoryNotFoundHTTPException(name=category_name)

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
    images = [ImageToShowOutputSerializer(id=img["id"], name=img["name"], comment=img["comment"]) for img in images]

    base_url = str(request.base_url).strip("/")
    _router_prefix = router_prefix.strip("/")
    endpoint_url = f"{base_url}/{_router_prefix}/{category_name}"
    previous_page = page - 1 if page != 0 else None
    previous_page_link = HttpUrl(f"{endpoint_url}?page={previous_page}") if previous_page is not None else None
    next_page = page + 1 if page < total_number_of_pages - 1 else None
    next_page_link = HttpUrl(f"{endpoint_url}?page={next_page}") if next_page is not None else None
    return ImagesFromCategoryOutputSerializer(
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


@router.patch("", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(
    update_category_input: UpdateCategoryInputSerializer, user: AuthenticatedUser = Depends(get_current_user)
) -> Response:
    """
    Update category in 'categories' collection
    and then update it in every image that contains this category ('images' collection)
    """
    if CategoriesDbOperations.exists(category_name=update_category_input.old_name) is False:
        raise CategoryNotFoundHTTPException(name=update_category_input.old_name)

    new_category = Category(name=update_category_input.new_name).model_dump()
    CategoriesDbOperations.update(old_name=update_category_input.old_name, new_name=update_category_input.new_name)

    images_db = CollectionProvider.provide(CollectionName.IMAGES)
    images = images_db.search(query.categories.any(query.name == update_category_input.old_name))
    for image in images:
        # TODO this can be probably done with one operation
        updated_categories = list(
            filter(lambda item: item["name"] != update_category_input.old_name, image["categories"])
        )  # delete old category
        updated_categories.append(new_category)  # append updated one
        images_db.update({"categories": updated_categories}, doc_ids=[image.doc_id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
