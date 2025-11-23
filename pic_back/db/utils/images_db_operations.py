from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Image

from .db_operations import DbOperations

query = Query()


class DbImagesException(Exception):
    pass


class ImageExistsException(DbImagesException):
    pass


class ImagesDbOperations(DbOperations):
    @classmethod
    def create(cls, image: Image) -> Image:
        images_db = cls._get_db()
        if images_db.get(query.id == image.id):
            raise ImageExistsException
        images_db.insert(image.model_dump())
        return image

    @staticmethod
    def _get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.IMAGES)
