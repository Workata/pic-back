from fastapi import status
from tinydb import Query

from pic_back.db.utils import CategoriesDbOperations, ImagesDbOperations
from pic_back.models import Category, Image
from pic_back.routers.category.serializers.input import UpdateCategoryInputSerializer

query = Query()
categories_router_base_path = "/api/v1/categories"


def test_list_categories(client):
    existing_categories = [Category(name="cars"), Category(name="cats"), Category(name="birds")]
    for category in existing_categories:
        CategoriesDbOperations.create(category)
    expected_res_data = [category.model_dump() for category in existing_categories]

    res = client.get(categories_router_base_path)
    res_data = res.json()

    assert res_data == expected_res_data
    assert res.status_code == status.HTTP_200_OK


def test_create_category_endpoint_with_authenticated_user_should_create_category(client, auth_headers):
    category_name = "cars"
    category_to_create = Category(name=category_name)
    assert CategoriesDbOperations.exists(category_name=category_name) is False

    res = client.post(categories_router_base_path, data=category_to_create.model_dump_json(), headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert res_data["detail"] == f"Category '{category_to_create.name}' has been created successfuly"
    assert CategoriesDbOperations.exists(category_name=category_name) is True


def test_create_category_endpoint_but_it_exists_with_authenticated_user_should_return_400(client, auth_headers):
    category_name = "cars"
    category_to_create = Category(name=category_name)
    CategoriesDbOperations.create(category_to_create)

    res = client.post(categories_router_base_path, data=category_to_create.model_dump_json(), headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res_data["detail"] == f"Category with name '{category_name}' already exists. Please provide different name."


def test_delete_category_endpoint_with_existing_category_and_authenticated_user_should_return_200(client, auth_headers):
    category_name = "cars"
    category = Category(name=category_name)
    image = Image(id="0123-0123", name="image.jpg", categories=[category])
    CategoriesDbOperations.create(category)
    ImagesDbOperations.create(image)

    res = client.delete(f"{categories_router_base_path}/{category_name}", headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_data["detail"] == f"Category '{category_name}' has been deleted successfuly"
    assert CategoriesDbOperations.exists(category_name) is False
    assert len(ImagesDbOperations.get(image.id).categories) == 0


def test_delete_category_endpoint_when_no_existing_category_and_authenticated_user_should_return_404(
    client, auth_headers
):
    category_name = "cars"

    res = client.delete(f"{categories_router_base_path}/{category_name}", headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res_data["detail"] == f"Category with name '{category_name}' not found."


def test_get_images_from_category_when_no_existing_category_should_return_404(client):
    category_name = "cars"

    res = client.get(f"{categories_router_base_path}/{category_name}")

    res_data = res.json()
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res_data["detail"] == f"Category with name '{category_name}' not found."


def test_get_images_from_category_should_return_200(client, settings):
    category_name = "cars"
    category = Category(name=category_name)
    image = Image(id="0123-0123", name="image.jpg", categories=[category])
    CategoriesDbOperations.create(category)
    ImagesDbOperations.create(image)

    res = client.get(f"{categories_router_base_path}/{category_name}")

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_data["images"][0]["id"] == image.id
    # test pagination
    assert res_data["previousPage"] is None
    assert res_data["previousPageLink"] is None
    assert res_data["currentPage"] == 0
    assert res_data["nextPage"] is None
    assert res_data["nextPageLink"] is None
    assert res_data["totalNumberOfPages"] == 1
    assert res_data["totalNumberOfRecords"] == 1
    assert res_data["pageSize"] == settings.default_page_size


def test_get_images_from_category_with_paginated_response(client, settings):
    category_name = "cars"
    category = Category(name=category_name)
    images = [Image(id=str(i), name=f"image_{i}.jpg", categories=[category]) for i in range(30)]
    images_count = len(images)
    CategoriesDbOperations.create(category)
    ImagesDbOperations.bulk_create(images)

    res = client.get(f"{categories_router_base_path}/{category_name}")

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    # test pagination
    assert res_data["previousPage"] is None
    assert res_data["previousPageLink"] is None
    assert res_data["currentPage"] == 0
    assert res_data["nextPage"] == 1
    assert res_data["nextPageLink"] == "http://testserver/api/v1/categories/cars?page=1"
    assert res_data["totalNumberOfPages"] == 2
    assert res_data["totalNumberOfRecords"] == images_count
    assert res_data["pageSize"] == settings.default_page_size


def test_update_category_endpoint_with_non_existing_category_and_authenticated_user_should_return_404(
    client, auth_headers
):
    old_category_name = "cars"
    new_category_name = "cats"
    category = Category(name=old_category_name)
    image = Image(id="0123-0123", name="image.jpg", categories=[category])
    ImagesDbOperations.create(image)
    update_category_input = UpdateCategoryInputSerializer(old_name=old_category_name, new_name=new_category_name)

    res = client.patch(categories_router_base_path, data=update_category_input.model_dump_json(), headers=auth_headers)

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_category_endpoint_with_existing_category_and_authenticated_user_should_return_204(client, auth_headers):
    old_category_name = "cars"
    new_category_name = "cats"
    category = Category(name=old_category_name)
    image = Image(id="0123-0123", name="image.jpg", categories=[category])
    CategoriesDbOperations.create(category)
    ImagesDbOperations.create(image)
    update_category_input = UpdateCategoryInputSerializer(old_name=old_category_name, new_name=new_category_name)

    res = client.patch(categories_router_base_path, data=update_category_input.model_dump_json(), headers=auth_headers)

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert CategoriesDbOperations.exists(old_category_name) is False
    assert CategoriesDbOperations.exists(new_category_name) is True
    assert ImagesDbOperations.get(image.id).categories[0].name == new_category_name
