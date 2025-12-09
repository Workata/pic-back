from fastapi import HTTPException, status


class CategoryExistsHTTPException(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{name}' already exists. Please provide different name.",
        )


class CategoryNotFoundHTTPException(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with name '{name}' not found.", headers=None
        )
