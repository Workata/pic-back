from pydantic import BaseModel


class GoogleDriveFolder(BaseModel):
    """
    DB Model: NO
    """

    id: str
    name: str
