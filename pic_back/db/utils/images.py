from tinydb import Query

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Image

query = Query()


class DbImagesException(Exception):
    pass


class ImageExistsException(DbImagesException):
    pass


class DbImagesOperations:
    @staticmethod
    def create(image: Image) -> Image:
        images_db = CollectionProvider.provide(CollectionName.IMAGES)
        if images_db.get(query.id == image.id):
            raise ImageExistsException
        images_db.insert(image.model_dump())
        return image
