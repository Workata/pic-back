import json

from fastapi import status

from pic_back.db.utils import CategoriesDbOperations, ImagesDbOperations
from pic_back.models import Category, Image

images_router_base_path = "/api/v1/images"


def test_get_image_endpoint_with_existing_image_should_return_200(client):
    img_id = "0001-1213"
    name = "image.jpg"
    ImagesDbOperations.create(Image(id=img_id, name=name))

    res = client.get(f"{images_router_base_path}/{img_id}")

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_data["id"] == img_id
    assert res_data["name"] == name


def test_get_image_endpoint_with_non_exising_image_should_return_404(client):
    img_id = "0001-1213"

    res = client.get(f"{images_router_base_path}/{img_id}")

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_or_create_image_endpoint_with_exising_image_endpoint_should_return_200(client, auth_headers):
    img_id = "0001-1213"
    name = "image.jpg"
    image = ImagesDbOperations.create(Image(id=img_id, name=name))

    res = client.post(images_router_base_path, data=image.model_dump_json(), headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_data["id"] == img_id
    assert res_data["name"] == name


def test_update_image_categories_endpoint_with_unathenticated_user_should_return_401(client):
    img_id = "0001-1213"

    res = client.patch(f"{images_router_base_path}/{img_id}/categories")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_aupdate_image_categories_endpoint_with_authenticated_user_should_return_200(client, auth_headers):
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


def test_update_image_categories_endpoint_with_non_existing_image_should_return_404(client, auth_headers):
    img_id = "0001-1213"
    category_name = "cars"
    CategoriesDbOperations.create(Category(name="cars"))

    res = client.patch(
        f"{images_router_base_path}/{img_id}/categories",
        data=json.dumps([category_name]),
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_image_categories(client):
    img_id = "0001-1213"
    category_name = "cars"
    cars_category = CategoriesDbOperations.create(Category(name=category_name))
    ImagesDbOperations.create(Image(id=img_id, name="image.jpg", categories=[cars_category]))

    res = client.get(f"{images_router_base_path}/{img_id}/categories")

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_data == [cars_category.model_dump()]


def test_get_image_categories_with_non_existing_image(client):
    img_id = "0001-1213"

    res = client.get(f"{images_router_base_path}/{img_id}/categories")

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_image_comment_endpoint_with_non_existing_image_should_return_404(client, auth_headers):
    img_id = "0001-1213"

    res = client.patch(
        f"{images_router_base_path}/{img_id}/comment",
        data=json.dumps({"comment": "thats a bird"}),
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_image_comment_endpoint_with_existing_image_should_return_404(client, auth_headers):
    img_id = "0001-1213"
    new_comment = "thats a bird"
    ImagesDbOperations.create(Image(id=img_id, name="image.jpg"))

    res = client.patch(
        f"{images_router_base_path}/{img_id}/comment",
        data=json.dumps({"comment": new_comment}),
        headers=auth_headers,
    )
    updated_img = ImagesDbOperations.get(img_id=img_id)
    res_data = res.json()

    assert res_data["detail"] == f"Comment of img with ID '{img_id}' has been updated to '{new_comment}'"
    assert updated_img.comment == new_comment
    assert res.status_code == status.HTTP_200_OK
