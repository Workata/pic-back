import json

from fastapi import status
from fastapi.testclient import TestClient
from tinydb import Query, TinyDB

from pic_back.main import app
from pic_back.models import Category, Image
from pic_back.db import CollectionProvider, CollectionName

client = TestClient(app)

query = Query()


categories_router_base_path = "/api/v1/categories"


def insert_category_to_db(category: Category) -> Category:
    categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
    if categories_db.get(query.name == category.name):
        return category
    categories_db.insert(category.model_dump())
    return category


def test_list_categories():
    res = client.get(categories_router_base_path)

    print(res.json())

    assert res.status_code == status.HTTP_200_OK
