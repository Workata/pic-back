from fastapi import status

from pic_back.routers.auth.exceptions import AuthenticationFailedHTTPException


def test_exception_msg():
    expected_msg = "dummy"

    wrong_credentials_exception = AuthenticationFailedHTTPException(detail=expected_msg)

    assert wrong_credentials_exception.status_code == status.HTTP_401_UNAUTHORIZED
    assert wrong_credentials_exception.detail == expected_msg
    assert wrong_credentials_exception.headers == {"WWW-Authenticate": "Bearer"}
