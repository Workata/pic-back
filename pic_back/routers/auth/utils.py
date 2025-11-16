import datetime as dt
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from tinydb import where

from pic_back.db import CollectionName, CollectionProvider
from pic_back.models import AuthenticatedUser
from pic_back.routers.auth.exceptions import WrongCredentials
from pic_back.settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthenticatedUser:
    users_db = CollectionProvider.provide(CollectionName.USERS)
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username = payload.get("username")
        if username is None:
            raise WrongCredentials()
    except JWTError as jwt_error:
        raise WrongCredentials() from jwt_error
    user = users_db.get(where("username") == username)
    if not user:
        raise WrongCredentials()
    return AuthenticatedUser(username=user["username"])


def create_access_token(data: dict, expires_delta: Optional[dt.timedelta] = None) -> str:
    """shouldnt be async"""
    to_encode = data.copy()
    expire = (
        dt.datetime.now(dt.timezone.utc) + expires_delta
        if expires_delta
        else dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(  # type: ignore [no-any-return]
        claims=to_encode, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
