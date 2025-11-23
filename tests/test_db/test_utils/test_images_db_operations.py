import pytest
from tinydb import Query

from pic_back.db.utils.images_db_operations import ImageExistsException, ImagesDbOperations
from pic_back.models import Image

query = Query()


def test_create_when_image_exists(images_db):
    image = Image(id="0123-123", name="image.jpg")
    images_db.insert(image.model_dump())
    assert len(images_db.all()) == 1

    with pytest.raises(ImageExistsException):
        ImagesDbOperations.create(image)


def test_create_when_image_doesnt_exist(images_db):
    image = Image(id="0123-123", name="image.jpg")
    assert len(images_db.all()) == 0

    res = ImagesDbOperations.create(image)

    assert res == image
    assert len(images_db.all()) == 1
