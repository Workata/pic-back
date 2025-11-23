import logging
import logging.config
import typing as t
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from pic_back.routers import auth_router, category_router, gdrive_router, image_router, map_router
from pic_back.services.backup import BackupMakerFactory
from pic_back.settings import LOGGING_CONFIG, EnvType, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> t.Any:
    """
    ? https://fastapi.tiangolo.com/advanced/events/
    """
    await backup_task()
    yield


settings = get_settings()
logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(lifespan=lifespan)

logger = logging.getLogger(name="main")


@app.get("/")
def healthcheck() -> t.Dict[str, str]:
    return {"Status": "OK!"}


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


@repeat_every(seconds=60 * 60 * 24)
async def backup_task() -> None:
    if settings.environment != EnvType.PROD:
        logger.info(f"Backup omitted - not prod. Current env: {settings.environment}")
        return None
    BackupMakerFactory.create().make()
