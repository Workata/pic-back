from typing import List

from pydantic import TypeAdapter
from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Category

from .db_operations import DbOperations

query = Query()


class DbCategoriesException(Exception):
    pass


class CategoryExistsException(DbCategoriesException):
    pass


class CategoryNotFoundException(DbCategoriesException):
    pass


class CategoriesDbOperations(DbOperations):
    """
    Unique: name
    """

    @classmethod
    def delete(cls, category_name: str) -> List[int]:
        db = cls.get_db()
        removed_categories_ids: List[int] = db.remove(query.name == category_name)
        if not removed_categories_ids:
            raise CategoryNotFoundException
        return removed_categories_ids

    @classmethod
    def exists(cls, category_name: str) -> bool:
        db = cls.get_db()
        exists: bool = db.contains(query.name == category_name)
        return exists

    @classmethod
    def update(cls, old_name: str, new_name: str) -> None:
        db = cls.get_db()
        db.update({"name": new_name}, query.name == old_name)

    @classmethod
    def get(cls, category_name: str) -> Category:
        db = cls.get_db()
        category = db.get(query.name == category_name)
        if not category:
            raise CategoryNotFoundException
        return Category(**category)

    @classmethod
    def get_or_create(cls, category: Category) -> Category:
        db = cls.get_db()
        if db.get(query.name == category.name):
            return category
        db.insert(category.model_dump())
        return category

    @classmethod
    def get_all(cls) -> List[Category]:
        adapter = TypeAdapter(list[Category])
        db = cls.get_db()
        return adapter.validate_python(db.all())

    @classmethod
    def count_all(cls) -> int:
        return len(cls.get_all())

    @classmethod
    def create(cls, category: Category) -> Category:
        db = cls.get_db()
        if db.get(query.name == category.name):
            raise CategoryExistsException
        db.insert(category.model_dump())
        return category

    @staticmethod
    def get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.CATEGORIES)
