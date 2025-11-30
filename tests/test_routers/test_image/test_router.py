import json

from fastapi import status

from pic_back.db.utils import CategoriesDbOperations, ImagesDbOperations
from pic_back.models import Category, Image

images_router_base_path = "/api/v1/images"


def test_update_image_categories_endpoint_with_unathenticated_user_should_return_401(client):
    img_id = "0001-1213"

    res = client.patch(f"{images_router_base_path}/{img_id}/categories")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_single_category_to_image_with_authenticated_user_should_return_200(client, auth_headers):
    img_id = "0001-1213"
    category_name = "cars"
    ImagesDbOperations.create(Image(id=img_id, name="image.jpg"))
    CategoriesDbOperations.create(Category(name="cars"))

    res = client.patch(
        f"{images_router_base_path}/{img_id}/categories",
        data=json.dumps([category_name]),
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_200_OK
