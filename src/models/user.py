from pydantic import BaseModel


class User(BaseModel):
    """All the data that we want to store about user"""

    username: str
    hashed_password: str


class AuthenticatedUser(BaseModel):
    """
    General data about user that is potentialy neccesary for processing authenticated requests.
    Should be a subset of user data
    """

    username: str
