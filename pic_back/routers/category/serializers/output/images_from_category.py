from typing import List

from pic_back.routers.gdrive.serializers.output import ImageToShowOutputSerializer
from pic_back.routers.shared.serializers.output import VerbosePaginatedResponseOutputSerializer


class ImagesFromCategoryOutputSerializer(VerbosePaginatedResponseOutputSerializer):
    images: List[ImageToShowOutputSerializer]
