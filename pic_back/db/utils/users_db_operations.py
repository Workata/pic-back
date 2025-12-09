from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import User

query = Query()


class DbUsersException(Exception):
    pass


class UserExistsException(DbUsersException):
    pass


class UserNotFoundException(DbUsersException):
    pass


class UsersDbOperations:
    """
    Unique: username
    """

    @classmethod
    def create(cls, user: User) -> User:
        db = cls._get_db()
        if db.get(query.username == user.username):
            raise UserExistsException
        db.insert(user.model_dump())
        return user

    @classmethod
    def get(cls, username: str) -> User:
        db = cls._get_db()
        user = db.get(query.username == username)
        if user is None:
            raise UserNotFoundException
        return User(**user)

    @staticmethod
    def _get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.USERS)
