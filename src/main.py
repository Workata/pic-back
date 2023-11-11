from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import category_router, map_router, gdrive_router, image_router, auth_router


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


# * https://github.com/Itz-fork/Fastapi-Swagger-UI-Dark
# TODO make it work
# from fastapi.openapi.docs import get_swagger_ui_html
# from starlette.responses import HTMLResponse
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html_cdn() -> HTMLResponse:
#     return get_swagger_ui_html(
#     openapi_url=app.openapi_url,
#     title=f"{app.title} - Swagger UI",
#     # swagger_ui_dark.css CDN link
#     swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
# )
