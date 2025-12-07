import bcrypt

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import User


def create_user(username: str, password: str) -> User:
    hashed_password_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = User(username=username, hashed_password=hashed_password_bytes.decode("utf-8"))

    users_db = CollectionProvider.provide(CollectionName.USERS)
    users_db.insert(user.model_dump())
    return user
