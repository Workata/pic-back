from tinydb import TinyDB
from typing import Dict


class CollectionProvider:

    COLLECTION_NAME_TO_LOCATION: Dict[str, str] = {
        "categories": "./data/database/categories.json",
        "images": "./data/database/images.json",
        "users": "./data/database/users.json"
    }

    def provide(self, collection_name: str) -> TinyDB:
        return TinyDB(self.COLLECTION_NAME_TO_LOCATION[collection_name])
