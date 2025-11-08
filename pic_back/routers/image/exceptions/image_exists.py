from fastapi import HTTPException, status


class ImageExists(HTTPException):
    def __init__(self, img_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image with id '{img_id}' already exists.",
            headers=None,
        )
