from pydantic import BaseModel


class UpdateCategoryInputSerializer(BaseModel):
    old_name: str
    new_name: str
