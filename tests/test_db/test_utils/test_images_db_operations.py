import pytest
from tinydb import Query

from pic_back.db.utils.images_db_operations import ImageExistsDbException, ImageNotFoundDbException, ImagesDbOperations
from pic_back.models import Image

query = Query()


def test_create_when_image_exists(images_db):
    image = Image(id="0123-123", name="image.jpg")
    images_db.insert(image.model_dump())
    assert len(images_db.all()) == 1

    with pytest.raises(ImageExistsDbException):
        ImagesDbOperations.create(image)


def test_create_when_image_doesnt_exist(images_db):
    image = Image(id="0123-123", name="image.jpg")
    assert len(images_db.all()) == 0

    res = ImagesDbOperations.create(image)

    assert res == image
    assert len(images_db.all()) == 1


def test_get_when_image_exists(images_db):
    img_id = "0123-123"
    image = Image(id=img_id, name="image.jpg")
    images_db.insert(image.model_dump())

    res = ImagesDbOperations.get(img_id)

    assert res == image


def test_get_when_image_doesnt_exist(images_db):
    img_id = "0123-123"
    assert len(images_db.all()) == 0

    with pytest.raises(ImageNotFoundDbException):
        ImagesDbOperations.get(img_id)


def test_get_or_create_when_image_not_in_db(images_db):
    img_id = "0123-123"
    image = Image(id=img_id, name="image.jpg")
    assert len(images_db.all()) == 0

    res = ImagesDbOperations.get_or_create(image)

    assert res == image
    assert len(images_db.all()) == 1


def test_get_or_create_when_image_in_db(images_db):
    img_id = "0123-123"
    image = Image(id=img_id, name="image.jpg")
    images_db.insert(image.model_dump())
    assert len(images_db.all()) == 1

    res = ImagesDbOperations.get_or_create(image)

    assert res == image
    assert len(images_db.all()) == 1


def test_bulk_create_with_no_duplicates_and_clean_db(images_db):
    images_to_create = [Image(id="123-123", name="image1.jpg"), Image(id="091-091", name="image2.jpg")]
    assert len(images_db.all()) == 0

    ImagesDbOperations.bulk_create(images_to_create)

    assert len(images_db.all()) == 2


def test_bulk_create_where_image_already_exists_in_db(images_db):
    images_to_create = [Image(id="123-123", name="image1.jpg"), Image(id="091-091", name="image2.jpg")]
    images_db.insert(images_to_create[0].model_dump())
    assert len(images_db.all()) == 1

    with pytest.raises(ImageExistsDbException):
        ImagesDbOperations.bulk_create(images_to_create)

    assert len(images_db.all()) == 1
