import datetime as dt
from unittest import mock

import pytest
from freezegun import freeze_time

from pic_back.routers.auth.exceptions import AuthenticationFailedHTTPException
from pic_back.routers.auth.utils import create_access_token, get_current_user


@freeze_time("2026-01-14 03:21:34")
@mock.patch("jose.jwt.encode")
def test_create_access_token_flow(mock_encode, settings):
    given_data = {"username": "workata"}
    expected_data_to_be_encoded = {
        "username": "workata",
        "exp": dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15),
    }

    create_access_token(given_data)

    mock_encode.assert_called_once_with(
        claims=expected_data_to_be_encoded, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


@freeze_time("2026-01-14 03:21:34")
@mock.patch("jose.jwt.encode")
def test_create_access_token_flow_when_there_is_no_username_in_payload(mock_encode, settings):
    given_data = {"username": "workata"}
    expected_data_to_be_encoded = {
        "username": "workata",
        "exp": dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15),
    }

    create_access_token(given_data)

    mock_encode.assert_called_once_with(
        claims=expected_data_to_be_encoded, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


@pytest.mark.asyncio
async def test_get_current_user_with_correct_token(test_user_username, access_token):
    user = await get_current_user(access_token)

    assert user.username == test_user_username


@pytest.mark.asyncio
async def test_get_current_user_with_incorrect_token_format():
    with pytest.raises(AuthenticationFailedHTTPException) as err:
        await get_current_user("not-a-token")

    assert "JWT signature is invalid" in str(err)


@pytest.mark.asyncio
async def test_get_current_user_with_correct_token_format_but_unralated_user():
    access_token = create_access_token({"username": "non-existing-user"})

    with pytest.raises(AuthenticationFailedHTTPException) as err:
        await get_current_user(access_token)

    assert "Authentication failed! Check credentials" in str(err)


@pytest.mark.asyncio
async def test_get_current_user_with_bad_payload():
    access_token = create_access_token({"user__name": "non-existing-user"})

    with pytest.raises(AuthenticationFailedHTTPException) as err:
        await get_current_user(access_token)

    assert "Bad payload schema" in str(err)
