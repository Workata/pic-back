from pathlib import Path
from typing import Dict

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from tinydb import TinyDB, where

from pic_back.db import CollectionName, CollectionProvider
from pic_back.main import app
from pic_back.models import User
from pic_back.routers.auth.utils import create_access_token
from pic_back.settings import Settings, get_settings
from pic_back.utils.auth import create_user


@pytest.fixture(scope="session", autouse=True)
def set_env():
    load_dotenv(Path("./tests/.env.test"))
    get_settings.cache_clear()


@pytest.fixture
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="function", autouse=True)
def clear_db(set_env):
    """clear all test collections before executing a test function"""
    for collection_name in CollectionName:
        db = CollectionProvider.provide(collection_name)
        db.truncate()


@pytest.fixture
def test_user_username() -> str:
    return "workata"


@pytest.fixture
def test_user_password() -> str:
    return "123456"


@pytest.fixture
def test_user(test_user_username, test_user_password) -> User:
    """create test user (admin)"""
    users_db = CollectionProvider.provide(CollectionName.USERS)
    if user := users_db.get(where("username") == "test_user"):
        return User(**user)
    return create_user(username=test_user_username, password=test_user_password)


@pytest.fixture
def access_token(test_user) -> str:
    """create access token for previously created test user"""
    return create_access_token(data={"username": test_user.username})


@pytest.fixture
def auth_headers(access_token) -> Dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def categories_db() -> TinyDB:
    return CollectionProvider.provide(CollectionName.CATEGORIES)


@pytest.fixture
def images_db() -> TinyDB:
    return CollectionProvider.provide(CollectionName.IMAGES)


@pytest.fixture
def markers_db() -> TinyDB:
    return CollectionProvider.provide(CollectionName.MARKERS)


@pytest.fixture
def users_db() -> TinyDB:
    return CollectionProvider.provide(CollectionName.USERS)


@pytest.fixture
def timestamps_db() -> TinyDB:
    return CollectionProvider.provide(CollectionName.TIMESTAMPS)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
