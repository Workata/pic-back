from datetime import timedelta


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tinydb import where
from src.db import CollectionProvider
from .utils import create_access_token
from src.settings import get_settings
from fastapi.responses import JSONResponse


settings = get_settings()
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
collection_provider = CollectionProvider()


@router.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    users_coll = collection_provider.provide("users")
    user = users_coll.get(where('username') == form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not bcrypt.verify(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"username": user["username"]},
        expires_delta=timedelta(minutes=settings.access_token_lifetime_minutes)
    )
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=status.HTTP_200_OK) 
