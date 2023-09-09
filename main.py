import logging
from logging.config import dictConfig
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from dependencies import get_settings
from models import CountryResponse, HeadersResponse, RootResponse
from utils import ip_to_country, request_to_ip

settings = get_settings()

# setup logging
dictConfig(settings.logger_config)
logger = logging.getLogger(settings.logger_name)

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
async def get_root(request: Request, settings: Annotated[Settings, Depends(get_settings)]) -> RootResponse:
    ip = request_to_ip(request)
    logger.debug(f"Responding to request on / for {ip=}")
    return RootResponse(
        app_name=settings.app_name,
        app_description=settings.app_description,
        app_version=settings.app_version,
    )


@app.get("/headers")
async def get_headers(request: Request) -> HeadersResponse:
    ip = request_to_ip(request)

    headers_dict = dict(**request.headers)
    headers_dict["ip"] = ip
    headers_dict.pop("x-forwarded-for", None)  # remove the proxy ip from the headers if it exists

    logger.debug(f"Getting headers for {ip=}")

    # set an appropriate host and protocol
    headers_dict["host"] = headers_dict.pop("x-forwarded-host", request.url.hostname or "")
    headers_dict["protocol"] = headers_dict.pop("x-forwarded-proto", request.url.scheme)

    # get the country code for the ip address
    headers_dict["country"] = await ip_to_country(headers_dict["ip"])

    # replace "-" with "_" in the header names
    headers_dict = {k.replace("-", "_"): v for k, v in headers_dict.items()}
    headers_response = HeadersResponse(**headers_dict)

    logger.debug(f"Responding to request on /headers for {ip=} headers={headers_response.model_dump()}")
    return headers_response


@app.get("/country")
async def get_country(request: Request) -> CountryResponse:
    ip = request_to_ip(request)
    country = await ip_to_country(ip)
    country_response = CountryResponse(ip=ip, country=country)
    logger.debug(f"Responding to request on /country for {ip=} country={country_response.model_dump()}")
    return country_response


if __name__ == "__main__":
    import uvicorn

    # run the http server at 0.0.0.0:8888 with reload and debug mode enabled
    uvicorn.run("main:app", host=settings.uvicorn_host, port=settings.uvicorn_port, reload=True, log_level="debug")
