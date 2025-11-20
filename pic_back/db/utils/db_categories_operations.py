from typing import List

from pydantic import TypeAdapter
from tinydb import Query, TinyDB

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
    @classmethod
    def delete(cls, category_name: str) -> List[int]:
        categories_db = cls._get_categories_db()
        removed_categories_ids: List[int] = categories_db.remove(query.name == category_name)
        if not removed_categories_ids:
            raise CategoryNotFoundException
        return removed_categories_ids

    @classmethod
    def exists(cls, category_name: str) -> bool:
        categories_db = cls._get_categories_db()
        exists: bool = categories_db.contains(query.name == category_name)
        return exists

    @classmethod
    def get_all(cls) -> List[Category]:
        adapter = TypeAdapter(list[Category])
        categories_db = cls._get_categories_db()
        return adapter.validate_python(categories_db.all())

    @classmethod
    def get(cls, category_name: str) -> Category:
        categories_db = cls._get_categories_db()
        category = categories_db.get(query.name == category_name)
        if not category:
            raise CategoryNotFoundException
        return Category(**category)

    @classmethod
    def get_or_create(cls, category: Category) -> Category:
        categories_db = cls._get_categories_db()
        if categories_db.get(query.name == category.name):
            return category
        categories_db.insert(category.model_dump())
        return category

    @classmethod
    def create(cls, category: Category) -> Category:
        categories_db = cls._get_categories_db()
        if categories_db.get(query.name == category.name):
            raise CategoryExistsException
        categories_db.insert(category.model_dump())
        return category

    @staticmethod
    def _get_categories_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.CATEGORIES)
