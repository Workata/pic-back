from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models.timestamp import Timestamp

query = Query()


class DbTimestampException(Exception):
    pass


class TimestampExistsException(DbTimestampException):
    pass


class TimestampNotFoundException(DbTimestampException):
    pass


class TimestampDbOperations:
    """
    Unique: name
    """

    @classmethod
    def create(cls, timestamp: Timestamp) -> Timestamp:
        db = cls.get_db()
        if db.get(query.name == timestamp.name):
            raise TimestampExistsException
        db.insert(timestamp.model_dump())
        return timestamp

    @classmethod
    def get(cls, name: str) -> Timestamp:
        db = cls.get_db()
        timestamp = db.get(query.name == name)
        if timestamp is None:
            raise TimestampNotFoundException
        return Timestamp(**timestamp)

    @staticmethod
    def get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.TIMESTAMPS)
