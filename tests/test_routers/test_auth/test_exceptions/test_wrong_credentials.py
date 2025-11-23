from fastapi import status

from pic_back.routers.auth.exceptions import WrongCredentials


def test_exception_msg():
    wrong_credentials_exception = WrongCredentials()

    assert wrong_credentials_exception.status_code == status.HTTP_401_UNAUTHORIZED
    assert wrong_credentials_exception.detail == "Incorrect username or password!"
    assert wrong_credentials_exception.headers == {"WWW-Authenticate": "Bearer"}
