from pydantic import BaseModel


class CommentInputSerializer(BaseModel):
    comment: str
