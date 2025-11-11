from typing import Dict

from tinydb import TinyDB


class CollectionProvider:
    COLLECTIONS_BASE_PATH: str = "../data/database"

    COLLECTION_NAME_TO_LOCATION: Dict[str, str] = {
        "categories": f"{COLLECTIONS_BASE_PATH}/categories.json",
        "images": f"{COLLECTIONS_BASE_PATH}/images.json",
        "users": f"{COLLECTIONS_BASE_PATH}/users.json",
        "markers": f"{COLLECTIONS_BASE_PATH}/markers.json",
    }

    def provide(self, collection_name: str) -> TinyDB:
        return TinyDB(self.COLLECTION_NAME_TO_LOCATION[collection_name])
