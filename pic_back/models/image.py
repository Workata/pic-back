from typing import List

from pydantic import BaseModel, Field

from pic_back.models.category import Category


class Image(BaseModel):
    """
    DB model
    """

    id: str
    name: str
    categories: List[Category] = Field(default=[])
    comment: str = Field(default="")
