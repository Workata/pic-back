from fastapi import status
from fastapi.testclient import TestClient
from tinydb import Query

from pic_back.db.utils import DbCategoriesOperations
from pic_back.main import app
from pic_back.models import Category

client = TestClient(app)

query = Query()


categories_router_base_path = "/api/v1/categories"


def test_list_categories():
    existing_categories = [Category(name="cars"), Category(name="cats"), Category(name="birds")]
    for category in existing_categories:
        DbCategoriesOperations.create(category)
    expected_res_data = [category.model_dump() for category in existing_categories]

    res = client.get(categories_router_base_path)
    res_data = res.json()

    assert res_data == expected_res_data
    assert res.status_code == status.HTTP_200_OK
