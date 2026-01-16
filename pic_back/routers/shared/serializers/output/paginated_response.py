from typing import Optional

from pydantic import HttpUrl

from pic_back.settings import get_settings

from .base_output_serializer import BaseOutputSerializer

settings = get_settings()


class VerbosePaginatedResponseOutputSerializer(BaseOutputSerializer):
    """
    ! First page number should be 0
    """

    previous_page: Optional[int] = None
    previous_page_link: Optional[HttpUrl] = None

    current_page: int = 0

    next_page: Optional[int] = None
    next_page_link: Optional[HttpUrl] = None

    total_number_of_pages: int = 1
    total_number_of_records: int
    page_size: int = settings.default_page_size
