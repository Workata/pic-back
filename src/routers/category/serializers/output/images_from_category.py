from pydantic import BaseModel
from typing import List
from routers.shared.serializers.output import PaginatedResponseOutputSerializer


class ImageToShow(BaseModel):
    id: str
    name: str
    comment: str
    thumbnail_url: str
    image_url: str


class ImagesFromCategoryOutputSerializer(PaginatedResponseOutputSerializer):
    images: List[ImageToShow]
