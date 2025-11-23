import os

import pytest
from tinydb import where

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import User
from pic_back.routers.auth.utils import create_access_token
from pic_back.settings import get_settings
from pic_back.utils.create_user import create_user


@pytest.fixture(scope="session", autouse=True)
def set_env():
    """set test env vars"""
    os.environ["DATABASE_BASE_PATH"] = "./tests/data/"
    get_settings.cache_clear()


@pytest.fixture(scope="function", autouse=True)
def clear_db(set_env):
    """clear all test collections before executing a test function"""
    for collection_name in CollectionName:
        db = CollectionProvider.provide(collection_name)
        db.truncate()


@pytest.fixture
def test_user() -> User:
    """create test user (admin)"""
    test_user_username = "test_user"
    test_user_password = "12"
    users_db = CollectionProvider.provide(CollectionName.USERS)
    if user := users_db.get(where("username") == "test_user"):
        return User(**user)
    return create_user(username=test_user_username, password=test_user_password)


@pytest.fixture
def access_token(test_user):
    """create access token for previously created test user"""
    return create_access_token(data={"username": test_user.username})


@pytest.fixture
def categories_db():
    return CollectionProvider.provide(CollectionName.CATEGORIES)


@pytest.fixture
def images_db():
    return CollectionProvider.provide(CollectionName.IMAGES)


@pytest.fixture
def markers_db():
    return CollectionProvider.provide(CollectionName.MARKERS)


@pytest.fixture
def users_db():
    return CollectionProvider.provide(CollectionName.USERS)
