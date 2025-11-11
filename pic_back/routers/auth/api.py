from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tinydb import where

from pic_back.db import CollectionProvider
from pic_back.routers.auth.exceptions import WrongCredentials
from pic_back.routers.auth.utils import create_access_token
from pic_back.settings import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
collection_provider = CollectionProvider()


@router.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    users_coll = collection_provider.provide("users")
    user = users_coll.get(where("username") == form_data.username)

    if not user or not bcrypt.verify(form_data.password, user["hashed_password"]):
        raise WrongCredentials()

    access_token = create_access_token(
        data={"username": user["username"]}, expires_delta=timedelta(minutes=settings.access_token_lifetime_minutes)
    )
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=status.HTTP_200_OK)
