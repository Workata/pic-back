from pydantic import computed_field

from pic_back.routers.shared.serializers.output import BaseOutputSerializer
from pic_back.services.image_url_generator.google_drive import GoogleDriveImageUrlGenerator


class ImageToShowOutputSerializer(BaseOutputSerializer):
    """
    image from the Google drive API with added comment (from db)
    """

    id: str
    name: str
    comment: str

    @computed_field
    @property
    def thumbnail_url(self) -> str:
        return GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(self.id)

    @computed_field
    @property
    def image_url(self) -> str:
        return GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(self.id)
