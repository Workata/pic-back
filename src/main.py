import typing as t
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.tasks import repeat_every

from src.routers import (auth_router, category_router, gdrive_router,
                         image_router, map_router)
from src.settings import get_settings
from src.services.backups import BackupMakerFactory


@asynccontextmanager
async def lifespan(app: FastAPI) -> t.Any:
    """
    ? https://fastapi.tiangolo.com/advanced/events/
    """
    await backup_task()
    yield


settings = get_settings()

app = FastAPI(lifespan=lifespan)


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


backup_maker = BackupMakerFactory.create()

@repeat_every(seconds=60 * 60 * 24)
async def backup_task() -> None:
    print("Backup...")
    backup_maker.make()
