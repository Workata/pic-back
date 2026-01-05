import logging
import logging.config
import typing as t

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from pic_back.routers import auth_router, category_router, gdrive_router, image_router, map_router
from pic_back.services.backup import BackupMakerFactory
from pic_back.services.google_drive import GoogleDriveDiskMapperFactory
from pic_back.settings import LOGGING_CONFIG, EnvType, get_settings

"""
Define startup and shutdown logic if necessary
https://fastapi.tiangolo.com/advanced/events/

@asynccontextmanager
async def lifespan(app: FastAPI) -> t.Any:
    await backup_task()
    await map_disk_task()
    # startup logic
    yield
    # shutdown logic

app = FastAPI(lifespan=lifespan)
"""


logging.config.dictConfig(LOGGING_CONFIG)

settings = get_settings()
logger = logging.getLogger(name="main")
app = FastAPI()


@app.get("/")
def healthcheck() -> t.Dict[str, str]:
    return {"Status": "OK!"}


@app.get(f"{settings.global_api_prefix}/system/info")
def system_info() -> t.Dict[str, str]:
    return {"version": settings.version}


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
        logger.info(f"Backup omitted - not prod. Current env: `{settings.environment.value}`")
        return None
    BackupMakerFactory.create().make()


@repeat_every(seconds=60 * 60 * 24)
async def map_disk_task() -> None:
    if settings.environment != EnvType.PROD:
        logger.info(f"Mapping disk omitted - not prod. Current env: `{settings.environment.value}`")
        return None
    GoogleDriveDiskMapperFactory.create().run()
