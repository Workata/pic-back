from pydantic import BaseModel


class GoogleDriveFolder(BaseModel):
    id: str
    name: str
