from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import category_router, map_router, gdrive_router, image_router, auth_router
from settings import get_settings


settings = get_settings()

app = FastAPI()


app.include_router(category_router)
app.include_router(map_router)
app.include_router(gdrive_router)
app.include_router(image_router)
app.include_router(auth_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
