from typing import List

from pic_back.models import ImageToShow
from pic_back.routers.shared.serializers.output import VerbosePaginatedResponseOutputSerializer


class ImagesFromCategoryOutputSerializer(VerbosePaginatedResponseOutputSerializer):
    images: List[ImageToShow]
