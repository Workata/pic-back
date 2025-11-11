from typing import List

from pydantic import BaseModel

from pic_back.routers.shared.serializers.output import VerbosePaginatedResponseOutputSerializer


class ImageToShow(BaseModel):
    id: str
    name: str
    comment: str
    thumbnail_url: str
    image_url: str


class ImagesFromCategoryOutputSerializer(VerbosePaginatedResponseOutputSerializer):
    images: List[ImageToShow]
