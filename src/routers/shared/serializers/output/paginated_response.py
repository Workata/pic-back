from pydantic import BaseModel
from typing import Optional


class PaginatedResponseOutputSerializer(BaseModel):
    previous_page_link: Optional[str] = None
    next_page_link: Optional[str] = None

    # total_number_of_records
    # current_page
    # number_of_pages
    # page_size
