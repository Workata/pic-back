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


class ImageToShow(BaseModel):
    """
    image from the Google drive API with added comment (from db)
    """

    id: str
    name: str
    comment: str
    thumbnail_url: str
    image_url: str
