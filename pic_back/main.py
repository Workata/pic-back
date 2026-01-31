import asyncio
import logging
import logging.config
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pic_back.routers import auth_router, category_router, gdrive_router, image_router, map_router
from pic_back.settings import LOGGING_CONFIG, get_settings
from pic_back.tasks import tasks


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan-events
    """
    asyncio.gather(*[task() for task in tasks])
    yield


logging.config.dictConfig(LOGGING_CONFIG)

settings = get_settings()
logger = logging.getLogger(name="main")
app = FastAPI(lifespan=lifespan)


@app.get("/")
def healthcheck() -> Dict[str, str]:
    return {"Status": "OK!"}


@app.get(f"{settings.global_api_prefix}/system/info")
def system_info() -> Dict[str, str]:
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
