from fastapi import FastAPI

from .gdrive import GDriveHandler, GDriveContentParser
from fastapi.middleware.cors import CORSMiddleware

from src.routers import categories

app = FastAPI()
app.include_router(categories.router)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/folder/{folder_url_id}")
def read_root(folder_url_id: str):
    handler = GDriveHandler()
    res = handler.query_content(
        query=f"'{folder_url_id}' in parents",    
        fields=['id', 'name', 'mimeType']
    )
    parser = GDriveContentParser()
    parsed_res = parser.parse(res)
    return parsed_res
