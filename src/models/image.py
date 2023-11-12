from pydantic import BaseModel, Field
from .category import Category
from typing import List


class Image(BaseModel):
    id: str
    categories: List[Category]
    comment: str = Field(default="")
