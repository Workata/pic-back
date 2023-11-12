from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from tinydb import Query

from src.models import Category
from src.db import CollectionProvider


collection_provider = CollectionProvider()
query = Query()
router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("", response_model=List[Category])
async def get_all_categories() -> JSONResponse:
    categories_coll = collection_provider.provide("categories")
    return JSONResponse(content=categories_coll.all(), status_code=status.HTTP_200_OK)


@router.post("")
async def create_new_category(new_category: Category) -> JSONResponse:
    categories = collection_provider.provide("categories")
    if bool(categories.search(query.name == new_category.name)):
        return JSONResponse(
            content={"info": "Category already exists. Please provide different name."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    categories.insert(new_category.dict())
    return JSONResponse(
        content={"info": f"Category {new_category.name} has been created successfuly."},
        status_code=status.HTTP_201_CREATED,
    )
