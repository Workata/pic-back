from fastapi import HTTPException, status


class CategoryNotFound(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with name '{name}' not found.", headers=None
        )
