from typing import List

from pydantic import TypeAdapter
from tinydb import Query, TinyDB

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import Marker

from .db_operations import DbOperations

query = Query()


class DbMarkersException(Exception):
    pass


class MarkerExistsException(DbMarkersException):
    pass


class MarkersDbOperations(DbOperations):
    """
    Unique: coords
    """

    @classmethod
    def create(cls, marker: Marker, overwrite: bool = False) -> Marker:
        db = cls._get_db()
        if db.get(
            (query.coords.latitude == marker.coords.latitude) & (query.coords.longitude == marker.coords.longitude)
        ):
            raise MarkerExistsException()
        db.insert(marker.model_dump())
        return marker

    @classmethod
    def get_all(cls) -> List[Marker]:
        adapter = TypeAdapter(list[Marker])
        db = cls._get_db()
        return adapter.validate_python(db.all())

    @staticmethod
    def _get_db() -> TinyDB:
        return CollectionProvider.provide(CollectionName.MARKERS)
