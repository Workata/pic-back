from fastapi import status

from pic_back.routers.image.exceptions import ImageExistsHTTPException, ImageNotFoundHTTPException


def test_image_exsists_exception():
    img_id = "0123-0123"
    exc = ImageExistsHTTPException(img_id)

    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.detail == f"Image with id '{img_id}' already exists."


def test_image_not_found_exception():
    img_id = "0123-0123"
    exc = ImageNotFoundHTTPException(img_id)

    assert exc.status_code == status.HTTP_404_NOT_FOUND
    assert exc.detail == f"Image with id '{img_id}' not found."
