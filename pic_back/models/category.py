from pydantic import BaseModel


class Category(BaseModel):
    """DB model"""

    name: str
