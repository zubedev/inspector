from enum import Enum

from pydantic import BaseModel, ConfigDict


class RootResponse(BaseModel):
    app_name: str
    app_description: str
    app_version: str


class HeadersResponse(BaseModel):
    # set from x-forwarded-*
    ip: str
    host: str
    protocol: str
    # set from request headers
    user_agent: str
    accept: str
    accept_encoding: str
    accept_language: str
    cookie: str
    # allow extra fields to be passed in
    model_config = ConfigDict(extra="allow")


class CountryResponse(BaseModel):
    ip: str
    country: str


class GeoIpApiRtypeEnum(str, Enum):
    json = "json"
    text = "text"


class GeoIpApi(BaseModel):
    url: str
    rtype: GeoIpApiRtypeEnum
    lookup: str
    delimiter: str = ""
