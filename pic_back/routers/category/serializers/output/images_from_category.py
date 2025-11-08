from pydantic import BaseModel
from typing import List
from routers.shared.serializers.output import VerbosePaginatedResponseOutputSerializer


class ImageToShow(BaseModel):
    id: str
    name: str
    comment: str
    thumbnail_url: str
    image_url: str


class ImagesFromCategoryOutputSerializer(VerbosePaginatedResponseOutputSerializer):
    images: List[ImageToShow]
