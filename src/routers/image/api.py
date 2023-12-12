from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from tinydb import Query
from tinydb.table import Document

from src.db import CollectionProvider
from src.models import Image, ResponseMessage, Category
from src.serializers import CommentInputSerializer

collection_provider = CollectionProvider()
query = Query()
router = APIRouter(prefix="/api/v1/images", tags=["images"])


@router.post("", response_model=Image)
async def create_image(new_img: Image) -> JSONResponse:
    """Create new image"""
    images_coll = collection_provider.provide("images")

    image: Optional[Document] = images_coll.get(query.id == new_img.id)
    if image:
        raise HTTPException(
            detail=f"Image with ID '{new_img.id}' already exists!",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    new_img_dict = new_img.dict()
    images_coll.insert(new_img_dict)
    return JSONResponse(content=new_img_dict, status_code=status.HTTP_201_CREATED)


@router.get("/{img_id}", response_model=Image)
async def get_image(img_id: str) -> JSONResponse:
    images_coll = collection_provider.provide("images")
    image: Optional[Document] = images_coll.get(query.id == img_id)
    if not image:
        raise HTTPException(
            detail=f"Image with id {img_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(content=image, status_code=status.HTTP_200_OK)


@router.get("/category/{category_name}", response_model=Any)
async def get_images_from_category(category_name: str) -> JSONResponse:
    """
    Select category and get images belonging to this category
    Res: [{id, name, image_url, thumbnail_url}]
    """
    THUMBNAIL_BASE_URL = "https://drive.google.com/thumbnail"
    IMAGE_BASE_URL = "https://drive.google.com/uc"

    images_coll = collection_provider.provide("images")
    images = images_coll.search(query.categories.any(query.name == category_name))
    # TODO refactor URL creator service (image/thumbnail), remove code duplication (gservice)
    formatted_images = [
        {
            "id": img["id"],
            "name": img["name"],
            "thumbnail_url": f"{THUMBNAIL_BASE_URL}?id={img['id']}&authuser=0",
            "image_url": f"{IMAGE_BASE_URL}?id={img['id']}",
        }
        for img in images
    ]
    return JSONResponse(content=formatted_images, status_code=status.HTTP_200_OK)


@router.get("/{img_id}/categories", response_model=List[Category])
async def get_categories_of_image(img_id: str) -> JSONResponse:
    images_coll = collection_provider.provide("images")

    image: Optional[Document] = images_coll.get(query.id == img_id)
    if not image:
        raise HTTPException(
            detail=f"Image with id {img_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(content=image.get("categories", []), status_code=status.HTTP_200_OK)


@router.patch("/{img_id}/categories", response_model=ResponseMessage)
async def update_image_categories(img_id: str, categories: List[str]) -> JSONResponse:
    images_coll = collection_provider.provide("images")
    categories_coll = collection_provider.provide("categories")
    found_categories = categories_coll.search(query.name.one_of(categories))

    image: Optional[Document] = images_coll.get(query.id == img_id)
    if not image:
        raise HTTPException(
            detail=f"Image with id {img_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    images_coll.update({"categories": found_categories}, doc_ids=[image.doc_id])
    return JSONResponse(
        content=ResponseMessage(detail=f"Categories of img with ID '{img_id}' has been updated").dict(),
        status_code=status.HTTP_200_OK,
    )


@router.patch("/{img_id}/comment", response_model=ResponseMessage)
async def update_image_comment(img_id: str, comment: CommentInputSerializer) -> JSONResponse:
    comment_value: str = comment.comment  # TODO refactor this
    images_coll = collection_provider.provide("images")

    image: Optional[Document] = images_coll.get(query.id == img_id)
    if not image:
        raise HTTPException(
            detail=f"Image with id {img_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    images_coll.update({"comment": comment_value}, doc_ids=[image.doc_id])
    return JSONResponse(
        content=ResponseMessage(
            detail=f"Comment of img with ID '{img_id}' has been updated to '{comment_value}'"
        ).dict(),
        status_code=status.HTTP_200_OK,
    )
