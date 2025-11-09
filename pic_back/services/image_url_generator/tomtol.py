import typing as t

from pic_back.settings import get_settings


class TomtolImageUrlGenerator:
    """
    {base_url}/#/album/{folder_id}/{img_id}
    """

    @classmethod
    def generate(cls, folder_id: str, img_id: str, page_token: t.Optional[str] = None) -> str:
        settings = get_settings()
        if page_token:
            return f"{settings.frontend_base_url}/#/album/{folder_id}/{img_id}?page={page_token}"
        return f"{settings.frontend_base_url}/#/album/{folder_id}/{img_id}"
