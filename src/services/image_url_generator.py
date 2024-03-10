from settings import get_settings


class ImageUrlGenerator:
    """
    {base_url}/album/{folder_id}/{img_id}
    """

    @classmethod
    def generate(cls, folder_id: str, img_id: str) -> str:
        settings = get_settings()
        return f"{settings.base_url}/album/{folder_id}/{img_id}"
