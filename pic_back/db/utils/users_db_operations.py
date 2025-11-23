from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import User

query = Query()


class DbCategoriesException(Exception):
    pass


class CategoryExistsException(DbCategoriesException):
    pass


class CategoryNotFoundException(DbCategoriesException):
    pass


class UsersDbOperations:
    @classmethod
    def create(cls, user: User) -> User:
        db = cls._get_db()
        if db.get(query.username == user.username):
            raise CategoryExistsException
        db.insert(user.model_dump())
        return user

    @staticmethod
    def _get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.USERS)
