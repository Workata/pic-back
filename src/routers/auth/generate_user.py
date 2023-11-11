""" 
    Script that will create a new user. This app should have only one user which is admin.
"""
from passlib.hash import bcrypt

from src.db import CollectionProvider
from src.models import User


collection_provider = CollectionProvider()

username = input("Username: ")
plain_password = input("Password: ")

hashed_password = bcrypt.hash(plain_password)
user = User(username, hashed_password)

users_coll = collection_provider.provide("users")
users_coll.insert(user.dict())
