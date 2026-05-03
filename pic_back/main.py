import logging
import logging.config
from contextlib import asynccontextmanager
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from pic_back.models import HealthcheckStatus, SystemInfo
from pic_back.routers import auth_router, category_router, gdrive_router, image_router, map_router
from pic_back.settings import LOGGING_CONFIG, get_settings
from pic_back.tasks import tasks

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan-events
    """
    for task in tasks:
        scheduler.add_job(task.func, trigger="interval", seconds=task.interval_sec)
    scheduler.start()
    yield


logging.config.dictConfig(LOGGING_CONFIG)

settings = get_settings()
logger = logging.getLogger(name="main")
app = FastAPI(lifespan=lifespan)


@app.get(path="/", status_code=status.HTTP_200_OK)
def healthcheck() -> HealthcheckStatus:
    return HealthcheckStatus(status="OK!")


@app.get(path=f"{settings.global_api_prefix}/system/info", status_code=status.HTTP_200_OK)
def system_info() -> SystemInfo:
    return SystemInfo(version=settings.version)


app.include_router(category_router)
app.include_router(map_router)
app.include_router(gdrive_router)
app.include_router(image_router)
app.include_router(auth_router)

origins = ["*"]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
