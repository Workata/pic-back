import typing as t
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.tasks import repeat_every

from routers import category_router, map_router, gdrive_router, image_router, auth_router
from settings import get_settings
from services.backup import BackupMakerFactory

import logging
import logging.config


@asynccontextmanager
async def lifespan(app: FastAPI) -> t.Any:
    """
    ? https://fastapi.tiangolo.com/advanced/events/
    """
    await backup_task()
    yield


settings = get_settings()
logging.config.dictConfig(settings.logging)

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
    if settings.environment == "dev":
        print("Backup omitted - dev env")
        return
    backup_maker.make()
