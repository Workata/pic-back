from datetime import timedelta

import bcrypt
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from tinydb import where

from pic_back.db import CollectionName, CollectionProvider
from pic_back.routers.auth.exceptions import WrongCredentials
from pic_back.routers.auth.utils import create_access_token
from pic_back.settings import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    users_db = CollectionProvider.provide(CollectionName.USERS)
    user = users_db.get(where("username") == form_data.username)

    if not user or not bcrypt.checkpw(form_data.password.encode("utf-8"), user["hashed_password"].encode("utf-8")):
        raise WrongCredentials()

    access_token = create_access_token(
        data={"username": user["username"]}, expires_delta=timedelta(minutes=settings.access_token_lifetime_minutes)
    )
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=status.HTTP_200_OK)
