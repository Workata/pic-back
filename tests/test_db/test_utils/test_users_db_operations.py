import pytest
from tinydb import Query

from pic_back.db.utils.users_db_operations import UserExistsException, UsersDbOperations
from pic_back.models import User

query = Query()


def test_create_when_user_exists(users_db):
    user = User(username="workata", hashed_password="12312!@#1231241241!@")
    users_db.insert(user.model_dump())
    assert len(users_db.all()) == 1

    with pytest.raises(UserExistsException):
        UsersDbOperations.create(user)


def test_create_when_user_doesnt_exist(users_db):
    user = User(username="workata", hashed_password="12312!@#1231241241!@")
    assert len(users_db.all()) == 0

    res = UsersDbOperations.create(user)

    assert res == user
    assert len(users_db.all()) == 1
