from urllib.parse import urlparse

from pic_back.services.image_url_generator.google_drive import GoogleDriveImageUrlGenerator


def url_valid(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def test_google_drive_image_url_generator():
    img_id = "0123-0123"

    standard_url_v1 = GoogleDriveImageUrlGenerator.generate_standard_img_url_v1(img_id)
    standard_url_v2 = GoogleDriveImageUrlGenerator.generate_standard_img_url_v2(img_id)
    thumbnail_url_v1 = GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v1(img_id)
    thumbnail_url_v2 = GoogleDriveImageUrlGenerator.generate_thumbnail_img_url_v2(img_id)

    assert url_valid(standard_url_v1) is True
    assert url_valid(standard_url_v2) is True
    assert url_valid(thumbnail_url_v1) is True
    assert url_valid(thumbnail_url_v2) is True
