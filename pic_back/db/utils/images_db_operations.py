from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models.image import Image

from .db_operations import DbOperations

query = Query()


class DbImagesException(Exception):
    pass


class ImageExistsDbException(DbImagesException):
    pass


class ImageNotFoundDbException(DbImagesException):
    pass


class ImagesDbOperations(DbOperations):
    @classmethod
    def create(cls, image: Image) -> Image:
        images_db = cls.get_db()
        if images_db.get(query.id == image.id):
            raise ImageExistsDbException
        images_db.insert(image.model_dump())
        return image

    @classmethod
    def get(cls, img_id: str) -> Image:
        db = cls.get_db()
        image = db.get(query.id == img_id)
        if not image:
            raise ImageNotFoundDbException
        return Image(**image)

    @classmethod
    def get_or_create(cls, image: Image) -> Image:
        db = cls.get_db()
        image_from_db = db.get(query.id == image.id)
        if image_from_db is not None:
            return Image(**image_from_db)
        db.insert(image.model_dump())
        return image

    @staticmethod
    def get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.IMAGES)
