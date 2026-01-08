from pic_back.routers.gdrive.serializers.output import ImageToShowOutputSerializer
from pic_back.services.image_url_generator.google_drive import GoogleDriveImageUrlGenerator


def test_fields_and_model_dump():
    img_id = "0123-0123-0123"

    image_to_show = ImageToShowOutputSerializer(id=img_id, name="Warsaw101", comment="maybe")

    assert image_to_show.image_url == GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(img_id)
    assert image_to_show.thumbnail_url == GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(img_id)

    dumped_image = image_to_show.model_dump()

    assert dumped_image["imageUrl"] == GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(img_id)
    assert dumped_image["thumbnailUrl"] == GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(img_id)
