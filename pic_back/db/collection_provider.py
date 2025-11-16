from enum import Enum
from pathlib import Path
from typing import Callable, Dict

from tinydb import TinyDB

from pic_back.settings import get_settings


class CollectionName(str, Enum):
    CATEGORIES = "categories"
    IMAGES = "images"
    USERS = "users"
    MARKERS = "markers"


class CollectionProvider:
    COLLECTION_NAME_TO_COLLECTION_PATH_CREATOR: Dict[CollectionName, Callable[[], Path]] = {
        CollectionName.CATEGORIES: lambda: Path(get_settings().database_base_path, "categories.json"),
        CollectionName.IMAGES: lambda: Path(get_settings().database_base_path, "images.json"),
        CollectionName.USERS: lambda: Path(get_settings().database_base_path, "users.json"),
        CollectionName.MARKERS: lambda: Path(get_settings().database_base_path, "categories.json"),
    }

    @classmethod
    def provide(cls, collection_name: CollectionName) -> TinyDB:
        return TinyDB(cls.COLLECTION_NAME_TO_COLLECTION_PATH_CREATOR[collection_name]())
