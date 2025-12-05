from typing import List, Optional

from fastapi import APIRouter, Depends, status
from tinydb import Query
from tinydb.table import Document

from pic_back.db import CollectionName, CollectionProvider
from pic_back.db.utils import ImageNotFoundDbException, ImagesDbOperations
from pic_back.models import AuthenticatedUser, Category, Image
from pic_back.routers.auth.utils import get_current_user
from pic_back.routers.image.exceptions import ImageNotFoundHTTPException
from pic_back.routers.image.serializers.input import CommentInputSerializer
from pic_back.routers.shared.serializers.output import ResponseMessage
from pic_back.settings import get_settings

settings = get_settings()
query = Query()
router = APIRouter(prefix=f"{settings.global_api_prefix}/images", tags=["images"])


@router.get("/{img_id}", response_model=Image, status_code=status.HTTP_200_OK)
async def get_image(img_id: str) -> Image:
    try:
        return ImagesDbOperations.get(img_id)
    except ImageNotFoundDbException:
        raise ImageNotFoundHTTPException(img_id)


@router.post("", response_model=Image, status_code=status.HTTP_200_OK)
async def get_or_create_image(image: Image, user: AuthenticatedUser = Depends(get_current_user)) -> Image:
    """
    TODO conditional status code (200/201) and `get_or_create` -> Tuple[Image, bool]
    """
    return ImagesDbOperations.get_or_create(image)


@router.get("/{img_id}/categories", response_model=List[Category], status_code=status.HTTP_200_OK)
async def get_image_categories(img_id: str) -> List[Category]:
    try:
        image = ImagesDbOperations.get(img_id)
    except ImageNotFoundDbException:
        raise ImageNotFoundHTTPException(img_id)

    return image.categories


@router.patch("/{img_id}/categories", response_model=ResponseMessage, status_code=status.HTTP_200_OK)
async def update_image_categories(
    img_id: str, categories: List[str], user: AuthenticatedUser = Depends(get_current_user)
) -> ResponseMessage:
    images_db = CollectionProvider.provide(CollectionName.IMAGES)
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)

    found_categories = categories_db.search(query.name.one_of(categories))
    image: Optional[Document] = images_db.get(query.id == img_id)
    if not image:
        raise ImageNotFoundHTTPException(img_id)

    images_db.update({"categories": found_categories}, doc_ids=[image.doc_id])
    return ResponseMessage(detail=f"Categories of img with ID '{img_id}' has been updated")


@router.patch("/{img_id}/comment", response_model=ResponseMessage, status_code=status.HTTP_200_OK)
async def update_image_comment(
    img_id: str, input: CommentInputSerializer, user: AuthenticatedUser = Depends(get_current_user)
) -> ResponseMessage:
    comment: str = input.comment
    images_db = CollectionProvider.provide(CollectionName.IMAGES)

    image: Optional[Document] = images_db.get(query.id == img_id)
    if not image:
        raise ImageNotFoundHTTPException(img_id)

    images_db.update({"comment": comment}, doc_ids=[image.doc_id])
    return ResponseMessage(detail=f"Comment of img with ID '{img_id}' has been updated to '{comment}'")
