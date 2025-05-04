from pydantic import BaseModel
from typing import Optional


class PaginatedResponseOutputSerializer(BaseModel):
    """
        First page number should be 0
    """
    previous_page_link: Optional[str] = None
    next_page_link: Optional[str] = None

    current_page: int = 0
    total_number_of_pages: int
    total_number_of_records: int
    page_size: int
