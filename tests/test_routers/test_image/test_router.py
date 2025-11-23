import json

from fastapi import status
from fastapi.testclient import TestClient

from pic_back.db.utils import CategoriesDbOperations, ImagesDbOperations
from pic_back.main import app
from pic_back.models import Category, Image

client = TestClient(app)


def test_update_image_categories_endpoint_with_unathenticated_user_should_return_401():
    img_id = "0001-1213"

    res = client.patch(f"/api/v1/images/{img_id}/categories")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_single_category_to_image_with_authenticated_user_should_return_200(access_token):
    img_id = "0001-1213"
    category_name = "cars"
    ImagesDbOperations.create(Image(id=img_id, name="image.jpg"))
    CategoriesDbOperations.create(Category(name="cars"))

    res = client.patch(
        f"/api/v1/images/{img_id}/categories",
        data=json.dumps([category_name]),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == status.HTTP_200_OK
