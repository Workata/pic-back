from fastapi import HTTPException, status


class ImageNotFound(HTTPException):
    def __init__(self, img_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Image with id '{img_id}' not found.", headers=None
        )
