from pydantic import BaseModel


class UpdateCategorySerializer(BaseModel):
    old_name: str
    new_name: str
