from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from dependencies import get_settings
from models import InfoResponse

settings = get_settings()

app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=settings.docs_swagger_url,
    redoc_url=settings.docs_redoc_url,
)

# Register middlewares
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.get("/")
async def root(request: Request):
    return {
        "url": request.url._url,
        "query_params": request.query_params,
        "path_params": request.path_params,
        "scheme": request.url.scheme,
        "method": request.method,
        "headers": request.headers,
        "cookies": request.cookies,
    }


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]) -> InfoResponse:
    return InfoResponse(
        app_name=settings.app_name,
        app_description=settings.app_description,
        app_author=settings.app_author,
        app_version=settings.app_version,
    )


if __name__ == "__main__":
    import uvicorn

    # run the http server at 0.0.0.0:8888 with reload and debug mode enabled
    uvicorn.run("main:app", host=settings.uvicorn_host, port=settings.uvicorn_port, reload=True, log_level="debug")
