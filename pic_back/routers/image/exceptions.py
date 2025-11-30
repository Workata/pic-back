from fastapi import HTTPException, status


class ImageExistsHTTPException(HTTPException):
    def __init__(self, img_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image with id '{img_id}' already exists.",
            headers=None,
        )


class ImageNotFoundHTTPException(HTTPException):
    def __init__(self, img_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Image with id '{img_id}' not found.", headers=None
        )
