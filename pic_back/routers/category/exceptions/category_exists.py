from fastapi import HTTPException, status


class CategoryExists(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{name}' already exists. Please provide different name.",
            headers=None,
        )
