class GDriveImageUrlGenerator:
    STANDARD_IMAGE_BASE_URL = "https://drive.google.com/uc"
    THUMBNAIL_IMG_BASE_URL = "https://drive.google.com/thumbnail"

    @classmethod
    def generate_standard_img_url(cls, image_id: str) -> str:
        return f"{cls.STANDARD_IMAGE_BASE_URL}?id={image_id}"

    @classmethod
    def generate_thumbnail_img_url(cls, image_id: str) -> str:
        return f"{cls.THUMBNAIL_IMG_BASE_URL}?id={image_id}&authuser=0"
