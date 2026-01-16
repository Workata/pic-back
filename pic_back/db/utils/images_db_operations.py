from typing import List

from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Image

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
    def bulk_create(cls, images: List[Image]) -> None:
        """
        1. Check if it's possible to create all images
        2. Create all images
        """
        images_db = cls.get_db()
        for image in images:
            if images_db.get(query.id == image.id):
                raise ImageExistsDbException(f"Bulk create failed! Image with ID: {image.id} exists!")
        for image in images:
            images_db.insert(image.model_dump())

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
