from typing import List

from pic_back.routers.gdrive.serializers.output.image_to_show import ImageToShowOutputSerializer
from pic_back.routers.shared.serializers.output import VerbosePaginatedResponseOutputSerializer


class ImagesFromCategoryOutputSerializer(VerbosePaginatedResponseOutputSerializer):
    images: List[ImageToShowOutputSerializer]
