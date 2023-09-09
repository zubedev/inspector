from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from dependencies import get_settings
from models import CountryResponse, HeadersResponse, RootResponse
from utils import ip_to_country

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
async def get_root(settings: Annotated[Settings, Depends(get_settings)]) -> RootResponse:
    return RootResponse(
        app_name=settings.app_name,
        app_description=settings.app_description,
        app_version=settings.app_version,
    )


@app.get("/headers")
async def get_headers(request: Request) -> HeadersResponse:
    headers_dict = dict(**request.headers)

    # get the ip address of the client. First check the proxy headers, then the client host
    client_ip = request.client.host if request.client else ""
    proxy_ip = headers_dict.pop("x-forwarded-for", "")
    headers_dict["ip"] = proxy_ip or client_ip

    # set an appropriate host and protocol
    headers_dict["host"] = headers_dict.pop("x-forwarded-host", request.url.hostname or "")
    headers_dict["protocol"] = headers_dict.pop("x-forwarded-proto", request.url.scheme)

    # get the country code for the ip address
    headers_dict["country"] = await ip_to_country(headers_dict["ip"])

    # replace "-" with "_" in the header names
    headers_dict = {k.replace("-", "_"): v for k, v in headers_dict.items()}

    return HeadersResponse(**headers_dict)


@app.get("/country")
async def get_country(request: Request) -> CountryResponse:
    # get the ip address of the client. First check the proxy headers, then the client host
    client_ip = request.client.host if request.client else ""
    proxy_ip = request.headers.get("x-forwarded-for", "")
    ip = proxy_ip or client_ip

    # get the country code for the ip address
    country = await ip_to_country(ip)

    return CountryResponse(ip=ip, country=country)


if __name__ == "__main__":
    import uvicorn

    # run the http server at 0.0.0.0:8888 with reload and debug mode enabled
    uvicorn.run("main:app", host=settings.uvicorn_host, port=settings.uvicorn_port, reload=True, log_level="debug")
