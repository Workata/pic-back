from typing import Optional

from .base_output_serializer import BaseOutputSerializer


class VerbosePaginatedResponseOutputSerializer(BaseOutputSerializer):
    """
    First page number should be 0
    """

    previous_page_link: Optional[str] = None
    next_page_link: Optional[str] = None

    previous_page: Optional[int] = None
    current_page: int = 0
    next_page: Optional[int] = None

    total_number_of_pages: int
    total_number_of_records: int
    page_size: int
