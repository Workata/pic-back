class GoogleDriveImageUrlGenerator:
    """
    base img: https://lh3.google.com/u/0/d/{img-ID}
    thumbnail img: https://lh3.googleusercontent.com/d/{img-ID}=s220?authuser=0

    ! Use 'https://lh3.google.com' as base URL - works better?
    (probably, at least its more direct and there are no second requests for thumbnails)

    """

    STANDARD_IMAGE_BASE_URL = "https://drive.google.com/uc"
    THUMBNAIL_IMG_BASE_URL = "https://drive.google.com/thumbnail"

    STANDARD_IMAGE_BASE_URL_V2 = "https://lh3.google.com/u/0/d"
    THUMBNAIL_IMG_BASE_URL_V2 = "https://lh3.googleusercontent.com/d"

    @classmethod
    def generate_standard_img_url_v1(cls, image_id: str) -> str:
        return f"{cls.STANDARD_IMAGE_BASE_URL}?id={image_id}"

    @classmethod
    def generate_standard_img_url(cls, image_id: str) -> str:
        return f"{cls.STANDARD_IMAGE_BASE_URL_V2}/{image_id}"

    @classmethod
    def generate_thumbnail_img_url(cls, image_id: str) -> str:
        # return f"{cls.THUMBNAIL_IMG_BASE_URL}?id={image_id}&authuser=0"
        return f"{cls.THUMBNAIL_IMG_BASE_URL_V2}/{image_id}=s220?authuser=0"
