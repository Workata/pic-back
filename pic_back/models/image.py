from typing import List

from pydantic import BaseModel, Field

from pic_back.models.category import Category


class Image(BaseModel):
    id: str
    name: str
    categories: List[Category] = Field(default=[])
    comment: str = Field(default="")
