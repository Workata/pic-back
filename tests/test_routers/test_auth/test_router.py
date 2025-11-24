from fastapi import status

auth_router_base_path = "/api/v1/auth"


def test_login_endpoint_with_correct_credentials(client, test_user_username, test_user_password, test_user):
    res = client.post(
        f"{auth_router_base_path}/login",
        data={"username": test_user_username, "password": test_user_password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert res.status_code == status.HTTP_200_OK


def test_login_endpoint_with_incorrect_credentials(client):
    res = client.post(
        f"{auth_router_base_path}/login",
        data={"username": "dummy", "password": "value"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
