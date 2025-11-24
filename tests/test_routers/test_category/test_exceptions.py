from fastapi import status

from pic_back.routers.category.exceptions import CategoryExistsHTTPException, CategoryNotFoundHTTPException


def test_category_exsists_exception():
    name = "cars"
    exc = CategoryExistsHTTPException(name=name)

    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.detail == f"Category with name '{name}' already exists. Please provide different name."


def test_category_not_found_exception():
    name = "cars"
    exc = CategoryNotFoundHTTPException(name=name)

    assert exc.status_code == status.HTTP_404_NOT_FOUND
    assert exc.detail == f"Category with name '{name}' not found."
