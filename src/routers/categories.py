from tinydb import TinyDB, where, Query
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from src.models import Category
# from src.routers.auth import get_current_user


IMG_CATEGORIES_DB_PATH = "./data/database/image_categories.json"
img_categories_db = TinyDB(IMG_CATEGORIES_DB_PATH)
CATEGORIES_DB_PATH = "./data/database/categories.json"
categories_db = TinyDB(CATEGORIES_DB_PATH)
query = Query()

router = APIRouter(prefix="/api/categories", tags=["Categories"])

# TODO make it restful

@router.get("")
async def get_categories():
    categories = [row.get('category') for row in categories_db]
    return {"categories": categories}


@router.post("")
async def create_category(category: Category):
    is_duplicated = bool(categories_db.search(query.category == category.name))
    if is_duplicated:
        return {"info": "Category exists"}
    categories_db.insert({"category": category.name})
    return {"info": "Category created"}




@router.get("/{img_id}")
async def get_image_categories(img_id: str):
    categories = img_categories_db.search(query.id.search(img_id))
    print(categories)
    return {}


