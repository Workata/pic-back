from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware

from src.routers import category_router, map_router, gdrive_router, image_router, auth_router
from src.settings import get_settings
import sys
import os


settings = get_settings()

app = FastAPI()

# * https://pyngrok.readthedocs.io/en/latest/integrations.html#fastapi
if settings.use_ngrok and os.environ.get("NGROK_AUTHTOKEN"):
    print("Using ngrok tunneling...")
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(public_url, port))
    print(public_url)
    print(port)

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.base_url = public_url
    # init_webhooks(public_url)


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
