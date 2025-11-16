from tinydb import Query

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Category

query = Query()


class DbCategoriesException(Exception):
    pass


class CategoryExistsException(DbCategoriesException):
    pass


class DbCategoriesOperations:
    @staticmethod
    def insert(category: Category) -> Category:
        categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
        if categories_db.get(query.name == category.name):
            raise CategoryExistsException
        categories_db.insert(category.model_dump())
        return category
