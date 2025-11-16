import json

from fastapi import status
from fastapi.testclient import TestClient
from tinydb import Query, TinyDB

from pic_back.main import app
from pic_back.models import Category, Image

client = TestClient(app)

query = Query()


def insert_category_to_db(category: Category) -> Category:
    categories = TinyDB("./tests/test_data/categories.json")
    if categories.get(query.name == category.name):
        return category
    categories.insert(category.model_dump())
    return category


def insert_image_to_db(image: Image) -> Image:
    images = TinyDB("./tests/test_data/images.json")
    if images.get(query.id == image.id):
        return image
    images.insert(image.model_dump())
    return image


def test_update_image_categories_endpoint_with_unathenticated_user_should_return_401():
    img_id = "0001-1213"

    res = client.patch(f"/api/v1/images/{img_id}/categories")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_image_single_category_with_authenticated_user(access_token):
    print("Access token")
    print(access_token)
    img_id = "0001-1213"
    category_name = "cars"
    insert_image_to_db(Image(id=img_id, name="image.jpg"))
    insert_category_to_db(Category(name="cars"))

    res = client.patch(
        f"/api/v1/images/{img_id}/categories",
        data=json.dumps([category_name]),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print(res.content)
    # image with ID not found add DB mounting

    assert res.status_code == status.HTTP_200_OK
