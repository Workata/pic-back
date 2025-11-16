import pytest
import os



from tinydb import where

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import User
from pic_back.routers.auth.utils import create_access_token
from pic_back.services.create_user import create_user

from pic_back.settings import get_settings


@pytest.fixture(scope="session", autouse=True)
def set_env():
    print("autouse set env")
    os.environ["DATABASE_BASE_PATH"] = "./tests/data/"
    get_settings.cache_clear()
    print(get_settings().database_base_path)

@pytest.fixture
def test_user() -> User:
    test_user_username = "test_user"
    test_user_password = "12"
    users_db = CollectionProvider.provide(CollectionName.USERS)
    if user := users_db.get(where("username") == "test_user"):
        return User(**user)
    return create_user(username=test_user_username, password=test_user_password)


@pytest.fixture
def access_token(test_user):
    return create_access_token(data={"username": test_user.username})
