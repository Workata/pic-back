from typing import List

from pydantic import TypeAdapter
from tinydb import Query

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Category

query = Query()


class DbCategoriesException(Exception):
    pass


class CategoryExistsException(DbCategoriesException):
    pass


class CategoryNotFoundException(DbCategoriesException):
    pass


class DbCategoriesOperations:
    @staticmethod
    def delete(category_name: str) -> List[int]:
        categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
        removed_categories_ids: List[int] = categories_db.remove(query.name == category_name)
        if not removed_categories_ids:
            raise CategoryNotFoundException
        return removed_categories_ids

    @staticmethod
    def get_all() -> List[Category]:
        adapter = TypeAdapter(list[Category])
        categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
        return adapter.validate_python(categories_db.all())

    @staticmethod
    def get(category_name: str) -> Category:
        categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
        category = categories_db.get(query.name == category_name)
        if not category:
            raise CategoryNotFoundException
        return Category(**category)

    @staticmethod
    def get_or_create(category: Category) -> Category:
        categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
        if categories_db.get(query.name == category.name):
            return category
        categories_db.insert(category.model_dump())
        return category

    @staticmethod
    def create(category: Category) -> Category:
        categories_db = CollectionProvider.provide(CollectionName.CATEGORIES)
        if categories_db.get(query.name == category.name):
            raise CategoryExistsException
        categories_db.insert(category.model_dump())
        return category
